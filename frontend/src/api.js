import axios from "axios";

const API = "http://localhost:5000";

export const getPolls = () => axios.get(`${API}/polls`);

export const getResults = (pollId) => axios.get(`${API}/polls/${pollId}/results`);

export const vote = (pollId, optionId) => axios.post(`${API}/polls/${pollId}/vote`, {
  option_id: optionId, user_id: "user123" // replace with actual user ID if needed
});