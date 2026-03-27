import React, { useState } from "react";
import PollList from "./pages/PollList";
import PollDetails from "./pages/PollDetails";
import "./App.css"; 

function App() {
  const [selectedPollId, setSelectedPollId] = useState(null);

  const handlePollSelect = (publicId) => {
    console.log("DEBUG: Poll Selected ->", publicId);
    setSelectedPollId(publicId);
  };

  const handleBackToList = () => {
    setSelectedPollId(null);
  };

  return (
    <div className="App" style={{ padding: "20px" }}>
      <header style={{ textAlign: "center", marginBottom: "30px" }}>
        <h1>Real-Time Voting System</h1>
      </header>

     
      <main style={{ maxWidth: "800px", margin: "0 auto" }}>
      {selectedPollId === null ? (
        <PollList onSelect={(id) => handlePollSelect(id)} />
      ) : (
        <div>
          <button onClick={handleBackToList} style={{ marginBottom: "20px" }}>
            Back to List
          </button>
          <PollDetails pollId={selectedPollId} />
        </div>
      )}
      </main>
    </div>
  );
}

export default App;