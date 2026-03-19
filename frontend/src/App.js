import React, { useEffect, useState } from "react";
import axios from "axios";
import socket from "./socket";

function App() {
  const [results, setResults] = useState({});
  const pollId = "YOUR_POLL_ID"; // replace this

  useEffect(() => {
    // Fetch initial results
    axios.get(`http://localhost:5000/polls/${pollId}/results`)
      .then(res => setResults(res.data.results));

    // Listen for live updates
    socket.on("vote_update", (data) => {
      if (data.poll_id === pollId) {
        setResults(data.results);
      }
    });

    return () => socket.off("vote_update");
  }, []);

  const vote = async (optionId) => {
    await axios.post(`http://localhost:5000/polls/${pollId}/vote`, {
      option_id: optionId
    });
  };

  return (
    <div>
      <h1>Live Voting</h1>

      <button onClick={() => vote("A")}>Option A</button>
      <button onClick={() => vote("B")}>Option B</button>

      <h2>Results:</h2>
      {Object.entries(results).map(([opt, count]) => (
        <p key={opt}>{opt}: {count}</p>
      ))}
    </div>
  );
}

export default App;