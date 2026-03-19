import React, { useEffect, useState } from "react";
import socket from "../socket";
import { getResults, vote } from "../api";
import LiveChart from "../components/LiveChart";

function PollDetails({ pollId }) {
  const [results, setResults] = useState({});

  useEffect(() => {
    // initial load
    getResults(pollId).then(res => setResults(res.data.results));

    // live updates
    socket.on("vote_update", (data) => {
      if (data.poll_id === pollId) {
        setResults(data.results);
      }
    });

    return () => socket.off("vote_update");
  }, [pollId]);

  const handleVote = (optionId) => {
    vote(pollId, optionId);
  };

  return (
    <div>
      <h2>Poll: {pollId}</h2>

      {/* Replace with real options later */}
      <button onClick={() => handleVote("A")}>Vote A</button>
      <button onClick={() => handleVote("B")}>Vote B</button>

      <LiveChart results={results} />
    </div>
  );
}

export default PollDetails;