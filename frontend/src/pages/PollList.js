import React, { useEffect, useState } from "react";
import { getPolls } from "../api";

function PollList({ onSelect }) {
    const [polls, setPolls] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        getPolls()
            .then((data) => {
                // Debug: See exactly what the API returns
                console.log("API Response:", data);

                // Handle both { polls: [] } or raw []
                const pollsData = data.polls || data || [];
                setPolls(pollsData);
                setLoading(false);
            })
            .catch(err => {
                console.error("Failed to fetch polls:", err);
                setLoading(false);
            });
    }, []);

    if (loading) return <p style={{ textAlign: "center" }}>Loading available polls...</p>;

    return (
        <div className="poll-container" style={{ textAlign: "center" }}>
            <h2>Available Polls</h2>
            {polls.length === 0 ? (
                <p>No active polls found. Check if your database is seeded.</p>
            ) : (
                <div style={{ display: "flex", flexDirection: "column", gap: "15px", alignItems: "center" }}>
                    {polls.map((p, index) => {
                        // 🔍 DEBUG: This helps us find the right ID name in the F12 console
                        console.log(`Poll ${index} structure:`, p);

                        // Fallback logic: Try every common ID name
                        const pollId = p.public_id || p.id || p.poll_id || p._id;

                        return (
                            <div key={pollId || index} className="poll-item" style={{
                                border: "1px solid #ccc",
                                padding: "15px",
                                borderRadius: "8px",
                                width: "300px"
                            }}>
                                <h3>{p.question}</h3>
                                <button 
                                    onClick={() => {
                                        console.log("Button clicked for ID:", pollId);
                                        onSelect(pollId);
                                    }}
                                    style={{ padding: "8px 16px", cursor: "pointer" }}
                                >
                                    Open Poll
                                </button>
                            </div>
                        );
                    })}
                </div>
            )}
        </div>
    );
}

export default PollList;