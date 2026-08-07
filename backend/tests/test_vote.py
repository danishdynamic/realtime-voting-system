import pytest
import requests
import threading
import time
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000/api"


class TestVoteFlow:
    """Vote casting, deduplication, race conditions, and poll lifecycle."""

    @pytest.fixture
    def active_poll(self):
        """Create a poll that is currently active."""
        payload = {
            "question": "Vote Test: Pizza vs Burger",
            "options": ["Pizza", "Burger"],
            "created_by": "vote_test",
            "start_time": datetime.now().isoformat(),
            "end_time": (datetime.now() + timedelta(hours=1)).isoformat()
        }

        response = requests.post(f"{BASE_URL}/polls", json=payload, timeout=5)
        assert response.status_code == 200
        poll_id = response.json()["poll_id"]

        yield poll_id

    @pytest.fixture
    def ended_poll(self):
        """Create a poll that has already ended."""
        payload = {
            "question": "Ended Test: Summer vs Winter",
            "options": ["Summer", "Winter"],
            "created_by": "vote_test",
            "start_time": (datetime.now() - timedelta(hours=2)).isoformat(),
            "end_time": (datetime.now() - timedelta(hours=1)).isoformat()
        }

        response = requests.post(f"{BASE_URL}/polls", json=payload, timeout=5)
        assert response.status_code == 200
        poll_id = response.json()["poll_id"]

        yield poll_id

    def test_cast_vote_success(self, active_poll):
        """User should be able to cast a vote on an active poll."""
        payload = {
            "option_id": "Pizza",
            "option_text": "Pizza",
            "user_id": "user_001"
        }

        response = requests.post(
            f"{BASE_URL}/polls/{active_poll}/vote",
            json=payload,
            timeout=5
        )

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Vote cast successfully"

    def test_vote_reflects_in_results(self, active_poll):
        """After voting, results should show the vote count increased."""
        requests.post(
            f"{BASE_URL}/polls/{active_poll}/vote",
            json={"option_id": "Burger", "option_text": "Burger", "user_id": "user_002"},
            timeout=5
        )

        time.sleep(0.5)

        response = requests.get(f"{BASE_URL}/polls/{active_poll}/results", timeout=5)
        results = response.json()["results"]

        assert results["Burger"] >= 1

    def test_duplicate_vote_rejected(self, active_poll):
        """Same user voting twice should be rejected with 403."""
        user_id = "user_duplicate"

        resp1 = requests.post(
            f"{BASE_URL}/polls/{active_poll}/vote",
            json={"option_id": "Pizza", "option_text": "Pizza", "user_id": user_id},
            timeout=5
        )
        assert resp1.status_code == 200

        resp2 = requests.post(
            f"{BASE_URL}/polls/{active_poll}/vote",
            json={"option_id": "Burger", "option_text": "Burger", "user_id": user_id},
            timeout=5
        )

        assert resp2.status_code == 403
        assert "already voted" in resp2.json()["error"].lower()

    def test_vote_on_ended_poll_rejected(self, ended_poll):
        """Voting on an ended poll should return 403."""
        payload = {
            "option_id": "Summer",
            "option_text": "Summer",
            "user_id": "user_late"
        }

        response = requests.post(
            f"{BASE_URL}/polls/{ended_poll}/vote",
            json=payload,
            timeout=5
        )

        assert response.status_code == 403
        assert "not active" in response.json()["error"].lower()

    def test_race_condition_no_double_votes(self, active_poll):
        """Rapid simultaneous votes from same user should only count once."""
        user_id = "user_race"
        results = []

        def cast_vote():
            try:
                resp = requests.post(
                    f"{BASE_URL}/polls/{active_poll}/vote",
                    json={"option_id": "Pizza", "option_text": "Pizza", "user_id": user_id},
                    timeout=5
                )
                results.append(resp.status_code)
            except Exception:
                results.append("error")

        threads = [threading.Thread(target=cast_vote) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        success_count = results.count(200)
        reject_count = results.count(403)

        assert success_count == 1, f"Expected 1 success, got {success_count}"
        assert reject_count == 9, f"Expected 9 rejections, got {reject_count}"

    def test_concurrent_different_users(self, active_poll):
        """Multiple different users voting concurrently should all succeed."""
        user_count = 10

        def cast_vote(user_num):
            requests.post(
                f"{BASE_URL}/polls/{active_poll}/vote",
                json={
                    "option_id": "Pizza" if user_num % 2 == 0 else "Burger",
                    "option_text": "Pizza" if user_num % 2 == 0 else "Burger",
                    "user_id": f"user_concurrent_{user_num}"
                },
                timeout=5
            )

        threads = [threading.Thread(target=cast_vote, args=(i,)) for i in range(user_count)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        time.sleep(1)

        response = requests.get(f"{BASE_URL}/polls/{active_poll}/results", timeout=5)
        results = response.json()["results"]
        total = sum(results.values())

        assert total == user_count, f"Expected {user_count} votes, got {total}"

    def test_vote_without_user_id_rejected(self, active_poll):
        """Vote request missing user_id should return 400."""
        payload = {
            "option_id": "Pizza",
            "option_text": "Pizza"
        }

        response = requests.post(
            f"{BASE_URL}/polls/{active_poll}/vote",
            json=payload,
            timeout=5
        )

        assert response.status_code == 400

    def test_results_persist_after_vote(self, active_poll):
        """Results endpoint should consistently return data."""
        requests.post(
            f"{BASE_URL}/polls/{active_poll}/vote",
            json={"option_id": "Pizza", "option_text": "Pizza", "user_id": "user_persist"},
            timeout=5
        )

        time.sleep(0.5)

        for _ in range(5):
            response = requests.get(f"{BASE_URL}/polls/{active_poll}/results", timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert "results" in data
            assert isinstance(data["results"], dict)

    def test_poll_status_transitions(self):
        """Poll status should reflect time: upcoming -> active -> ended."""
        from datetime import datetime, timedelta

        future_start = datetime.now() + timedelta(minutes=1)
        future_end = datetime.now() + timedelta(hours=1)

        payload = {
            "question": "Status Test: Future Poll",
            "options": ["A", "B"],
            "created_by": "vote_test",
            "start_time": future_start.isoformat(),
            "end_time": future_end.isoformat()
        }

        create_resp = requests.post(f"{BASE_URL}/polls", json=payload, timeout=5)
        poll_id = create_resp.json()["poll_id"]

        detail_resp = requests.get(f"{BASE_URL}/polls/{poll_id}", timeout=5)
        assert detail_resp.json()["status"] == "upcoming"

        time.sleep(65)

        detail_resp = requests.get(f"{BASE_URL}/polls/{poll_id}", timeout=5)
        assert detail_resp.json()["status"] == "active"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
