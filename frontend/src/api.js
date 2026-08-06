const API_URL = process.env.REACT_APP_API_URL || "http://localhost:5000";

export const getResults = (pollId) =>
  fetch(`${API_URL}/polls/${pollId}/results`).then((res) => res.json());

export const getPoll = (pollId) =>
  fetch(`${API_URL}/polls/${pollId}`).then((res) => res.json());

export const vote = (pollId, optionId, optionText) =>
  fetch(`${API_URL}/polls/${pollId}/vote`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ option_id: optionId, option_text: optionText, user_id: "user123" }),
  }).then((res) => {
    if (!res.ok) throw res;
    return res.json();
  });