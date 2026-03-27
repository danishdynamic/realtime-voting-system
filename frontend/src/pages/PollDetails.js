import React, { useEffect, useState } from "react";
import socket from "../socket";
import { getResults, vote } from "../api";
import LiveChart from "../components/LiveChart";

function PollDetails({ pollId }) {
  const [results, setResults] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // initial load from flask api
    console.log("PollDetails mounted with ID:" , pollId)
    
    if (!pollId){
      console.error("No PollID provided to PollDetails")
      return;
    }


    getResults(pollId).then(data => {
      console.log("Fetched esults Data", data);

      const finalResults = data.results || data || {};

      setResults(finalResults);
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

  // 🛑 Safety check: If still loading, stop here and show message
  if (loading) return <p>Loading poll results for {pollId}...</p>;

  // 1. The function only needs the Name
  const handleVote = (optionName) => {
  // We pass optionName twice: once as the 'id' and once as the 'text'
  // Your backend is now smart enough to use the text to find the right Redis key!
      vote(pollId, optionName, optionName)
      .then(() => {
        console.log(`✅ Vote cast for: ${optionName}`);
      })
      .catch(err => {
        console.error("❌ Error voting:", err);
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