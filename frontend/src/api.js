import axios from "axios";

const API = "http://localhost:5000";

export const getPolls = () => axios.get(`${API}/polls`).then(res => res.data);

export const getResults = (pollId) => axios.get(`${API}/polls/${pollId}/results`).then(res => res.data);

export const vote = (pollId, optionId, optionText) => axios.post(`${API}/polls/${pollId}/vote`, {
  option_id: optionId, option_text: optionText, user_id: "user123" // replace with actual user ID if needed
});