import React, { useEffect, useState } from "react";
import socket from "../socket";
import { getResults, vote } from "../api";
import LiveChart from "../components/LiveChart";

function PollDetails({ pollId }) {
  const [results, setResults] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // initial load from flask api
    getResults(pollId).then(data => {
      setResults(data.results || data || {});
      setLoading(false);
    })

    .catch(err => {
      console.error("Error fetching results:", err);
      setLoading(false);
    });

    // Listen for Kafka -> Socket.io real-time updates
    socket.on("vote_update", (data) => {
      if (data.poll_id === pollId) {
        setResults(data.results);
      }
    });

    return () => socket.off("vote_update");
  }, [pollId]);

  const handleVote = (optionId) => {
    vote(pollId, optionId).catch(err => {
      console.error("Error voting:", err);
    });
  };

  return (
    <div style={{ padding: "20px" , textAlign: "center"}}>
      <h2>Poll: {pollId}</h2>

     <div style={{ marginBottom: "20px" }}>
        {/* ✅ DYNAMIC BUTTONS: Loop through the keys in your results object */}
        {Object.keys(results).length > 0 ? (
          Object.keys(results).map((optionName) => (
            <button
              key={optionName}
              onClick={() => handleVote(optionName)}
              style={{ margin: "10px", padding: "10px 20px", cursor: "pointer" }}
            >
              Vote {optionName}
            </button>
          ))
        ) : (
          <p>No options found for this poll.</p>
        )}
      </div>

      <LiveChart results={results} />
    </div>
  );
}

export default PollDetails;