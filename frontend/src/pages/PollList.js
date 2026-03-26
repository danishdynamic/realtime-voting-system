import React, { useEffect, useState } from "react";
import { getPolls } from "../api";

function PollList({ onSelect }) {
    const [polls, setPolls] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        getPolls()
            .then((data) => {
                // Ensure res.polls exists before setting state
                console.log("API Response:", data);

                const pollsData = data.polls || data || [];
                setPolls(pollsData);
                setLoading(false);
            })
            .catch(err => {
                console.error("Failed to fetch polls:", err);
                setLoading(false);
            });
    }, []); // Empty array ensures this only runs once on mount

    if (loading) return <p>Loading polls...</p>;

    return (
        <div className="poll-container">
            <h2>Available Polls</h2>
            {polls.length === 0 ? (
                <p>No active polls found.</p>
            ) : (
                 polls.map((p) => (
                    <div key={p.public_id || p.id} className="poll-item">
                        <h3>{p.question}</h3>
                        <button onClick={() => onSelect(p.public_id || p.id)}>
                            Open Poll
                        </button>
                    </div>
                ))
            )}
        </div>
    );
}

export default PollList;