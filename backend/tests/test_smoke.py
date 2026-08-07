import pytest
import requests
import time

BASE_URL = "http://localhost:5000/api"
KAFKA_BROKER = "localhost:9092"
REDIS_HOST = "localhost"
REDIS_PORT = 6379


class TestSmoke:
    """Basic connectivity and infrastructure health checks."""

    def test_health_endpoint(self):
        """Flask API should respond with status ok."""
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"

    def test_polls_list_endpoint(self):
        """GET /polls should return a list (empty or populated)."""
        response = requests.get(f"{BASE_URL}/polls", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_create_poll_endpoint(self):
        """POST /polls should create a new poll and return poll_id."""
        from datetime import datetime, timedelta

        payload = {
            "question": "Smoke Test: Coffee vs Tea",
            "options": ["Coffee", "Tea"],
            "created_by": "smoke_test",
            "start_time": datetime.now().isoformat(),
            "end_time": (datetime.now() + timedelta(hours=1)).isoformat()
        }

        response = requests.post(f"{BASE_URL}/polls", json=payload, timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert "poll_id" in data
        assert data["question"] == payload["question"]
        assert len(data["options"]) == 2

        # Store for cleanup
        self.created_poll_id = data["poll_id"]

    def test_get_poll_detail(self):
        """GET /polls/:id should return poll with status and timer info."""
        from datetime import datetime, timedelta

        payload = {
            "question": "Detail Test: Apple vs Orange",
            "options": ["Apple", "Orange"],
            "created_by": "smoke_test",
            "start_time": datetime.now().isoformat(),
            "end_time": (datetime.now() + timedelta(minutes=30)).isoformat()
        }

        create_resp = requests.post(f"{BASE_URL}/polls", json=payload, timeout=5)
        poll_id = create_resp.json()["poll_id"]

        # Get detail
        response = requests.get(f"{BASE_URL}/polls/{poll_id}", timeout=5)
        assert response.status_code == 200
        data = response.json()

        assert data["poll_id"] == poll_id
        assert "status" in data
        assert data["status"] in ["upcoming", "active", "ended"]
        assert "time_remaining" in data or data["status"] == "ended"
        assert "options" in data
        assert len(data["options"]) == 2

    def test_poll_results_endpoint(self):
        """GET /polls/:id/results should return results dict."""
        from datetime import datetime, timedelta

        payload = {
            "question": "Results Test: Cat vs Dog",
            "options": ["Cat", "Dog"],
            "created_by": "smoke_test",
            "start_time": datetime.now().isoformat(),
            "end_time": (datetime.now() + timedelta(hours=1)).isoformat()
        }

        create_resp = requests.post(f"{BASE_URL}/polls", json=payload, timeout=5)
        poll_id = create_resp.json()["poll_id"]

        response = requests.get(f"{BASE_URL}/polls/{poll_id}/results", timeout=5)
        assert response.status_code == 200
        data = response.json()

        assert "poll_id" in data
        assert "results" in data
        assert data["results"]["Cat"] == 0
        assert data["results"]["Dog"] == 0

    def test_404_for_nonexistent_poll(self):
        """GET /polls/nonexistent should return 404."""
        response = requests.get(f"{BASE_URL}/polls/this-does-not-exist", timeout=5)
        assert response.status_code == 404

    def test_redis_connection(self):
        """Redis should be reachable."""
        import redis
        try:
            r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, socket_connect_timeout=2)
            assert r.ping() is True
        except redis.ConnectionError:
            pytest.fail("Redis is not reachable")

    def test_kafka_connection(self):
        """Kafka should be reachable."""
        from kafka import KafkaProducer
        try:
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_BROKER,
                api_version=(2, 5, 0),
                request_timeout_ms=3000
            )
            assert producer.bootstrap_connected() is True
            producer.close()
        except Exception as e:
            pytest.fail(f"Kafka is not reachable: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
