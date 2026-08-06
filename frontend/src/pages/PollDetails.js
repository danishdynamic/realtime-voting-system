import React, { useEffect, useState } from "react";
import socket from "../socket";
import { getResults, vote, getPoll } from "../api";
import LiveChart from "../components/LiveChart";

function PollDetails({ pollId }) {
  const [poll, setPoll] = useState(null);
  const [results, setResults] = useState({});
  const [loading, setLoading] = useState(true);
  const [hasVoted, setHasVoted] = useState(false);
  const [userChoice, setUserChoice] = useState(null);
  const [timeLeft, setTimeLeft] = useState(null);
  const [isExpired, setIsExpired] = useState(false);
  const [error, setError] = useState(null);

  // Fetch poll details + results on mount
  useEffect(() => {
    if (!pollId) {
      console.error("No PollID provided to PollDetails");
      setLoading(false);
      return;
    }

    // Fetch poll metadata (question, options, start_time, end_time)
    getPoll(pollId)
      .then((pollData) => {
        setPoll(pollData);
        // Check if already expired on load
        const now = new Date();
        const end = new Date(pollData.end_time);
        if (now >= end) {
          setIsExpired(true);
        }
      })
      .catch((err) => {
        console.error("Error fetching poll:", err);
        setError("Failed to load poll");
      });

    // Fetch current results
    getResults(pollId)
      .then((data) => {
        const finalResults = data.results || {};
        setResults(finalResults);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching results:", err);
        setLoading(false);
      });

    // Listen for real-time updates
    socket.on("vote_update", (data) => {
      if (data.poll_id === pollId) {
        setResults(data.results);
      }
    });

    return () => socket.off("vote_update");
  }, [pollId]);

  // Countdown timer
  useEffect(() => {
    if (!poll?.end_time) return;

    const interval = setInterval(() => {
      const now = new Date();
      const end = new Date(poll.end_time);
      const diff = end - now;

      if (diff <= 0) {
        setIsExpired(true);
        setTimeLeft({ hours: 0, minutes: 0, seconds: 0, expired: true });
        clearInterval(interval);
        return;
      }

      const hours = Math.floor(diff / (1000 * 60 * 60));
      const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
      const seconds = Math.floor((diff % (1000 * 60)) / 1000);

      setTimeLeft({ hours, minutes, seconds, expired: false });
    }, 1000);

    return () => clearInterval(interval);
  }, [poll?.end_time]);

  const handleVote = (optionName) => {
    if (hasVoted || isExpired) return;

    vote(pollId, optionName, optionName)
      .then(() => {
        console.log(`✅ Vote cast for: ${optionName}`);
        setHasVoted(true);
        setUserChoice(optionName);
      })
      .catch((err) => {
        console.error("❌ Error voting:", err);
        // If backend says already voted, sync frontend state
        if (err.response?.data?.error?.includes("already voted")) {
          setHasVoted(true);
        }
      });
  };

  // Determine winner
  const getWinner = () => {
    if (!results || Object.keys(results).length === 0) return null;
    const entries = Object.entries(results);
    const maxVotes = Math.max(...entries.map(([, v]) => v));
    const winners = entries.filter(([, v]) => v === maxVotes);
    // Tie = multiple winners
    return { names: winners.map(([k]) => k), votes: maxVotes };
  };

  const winner = isExpired ? getWinner() : null;

  // Loading state
  if (loading) return <p>Loading poll...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;
  if (!poll) return <p>Poll not found.</p>;

  const options = poll.options || Object.keys(results);

  return (
    <div style={{ padding: "20px", textAlign: "center", maxWidth: "800px", margin: "0 auto" }}>
      {/* Poll Header */}
      <h2>{poll.question || `Poll: ${pollId}`}</h2>

      {/* Timer */}
      <div style={{ 
        margin: "20px 0", 
        padding: "16px", 
        background: isExpired ? "#fee2e2" : "#ecfdf5",
        borderRadius: "12px",
        border: `2px solid ${isExpired ? "#ef4444" : "#10b981"}`
      }}>
        {isExpired ? (
          <p style={{ color: "#ef4444", fontWeight: "bold", fontSize: "18px", margin: 0 }}>
            ⏹ Voting Closed
          </p>
        ) : timeLeft ? (
          <div>
            <p style={{ margin: "0 0 8px 0", color: "#059669", fontWeight: "600" }}>
              ⏱ Vote ends in:
            </p>
            <p style={{ 
              margin: 0, 
              fontSize: "32px", 
              fontWeight: "800", 
              fontFamily: "monospace",
              color: timeLeft.minutes < 5 ? "#dc2626" : "#059669"
            }}>
              {String(timeLeft.hours).padStart(2, "0")}:
              {String(timeLeft.minutes).padStart(2, "0")}:
              {String(timeLeft.seconds).padStart(2, "0")}
            </p>
          </div>
        ) : (
          <p>Calculating time...</p>
        )}
      </div>

      {/* Winner Banner (shown when expired) */}
      {isExpired && winner && (
        <div style={{
          margin: "20px 0",
          padding: "24px",
          background: "linear-gradient(135deg, #fbbf24, #f59e0b)",
          borderRadius: "16px",
          color: "white",
        }}>
          <p style={{ margin: "0 0 8px 0", fontSize: "14px", fontWeight: "600", opacity: 0.9 }}>
            🏆 WINNER
          </p>
          <p style={{ margin: 0, fontSize: "28px", fontWeight: "800" }}>
            {winner.names.length > 1 
              ? `It's a tie! ${winner.names.join(" & ")}` 
              : winner.names[0]}
          </p>
          <p style={{ margin: "8px 0 0 0", fontSize: "16px", opacity: 0.9 }}>
            {winner.votes.toLocaleString()} votes
          </p>
        </div>
      )}

      {/* Vote Buttons */}
      <div style={{ marginBottom: "20px" }}>
        {options.length > 0 ? (
          options.map((option) => {
            const isSelected = userChoice === option.text;
            const isDisabled = hasVoted || isExpired;

            return (
              <button
                key={option.id || option}
                onClick={() => handleVote(option.text || option)}
                disabled={isDisabled}
                style={{
                  margin: "10px",
                  padding: "14px 28px",
                  fontSize: "16px",
                  fontWeight: "600",
                  borderRadius: "12px",
                  border: isSelected ? "2px solid #10b981" : "2px solid #e5e7eb",
                  background: isSelected 
                    ? "#ecfdf5" 
                    : isDisabled 
                      ? "#f3f4f6" 
                      : "#ffffff",
                  color: isSelected 
                    ? "#059669" 
                    : isDisabled 
                      ? "#9ca3af" 
                      : "#374151",
                  cursor: isDisabled ? "not-allowed" : "pointer",
                  boxShadow: isSelected 
                    ? "0 0 0 3px rgba(16, 185, 129, 0.2)" 
                    : "0 1px 3px rgba(0,0,0,0.1)",
                  transition: "all 0.2s",
                }}
              >
                {isSelected ? `✓ Voted ${option.text || option}` : `Vote ${option.text || option}`}
              </button>
            );
          })
        ) : (
          <p>No options found for this poll.</p>
        )}
      </div>

      {/* Already voted message */}
      {hasVoted && !isExpired && (
        <p style={{ color: "#059669", fontWeight: "600", marginBottom: "20px" }}>
          ✅ You voted for {userChoice}
        </p>
      )}

      {/* Final Results Chart */}
      <LiveChart results={results} />
      
      {/* Total votes footer */}
      <p style={{ color: "#6b7280", fontSize: "14px", marginTop: "16px" }}>
        Total votes: {Object.values(results).reduce((a, b) => a + b, 0).toLocaleString()}
      </p>
    </div>
  );
}

export default PollDetails;