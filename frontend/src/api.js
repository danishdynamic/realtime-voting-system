import axios from "axios";

const API = "http://127.0.0.1:5000";

export const getPolls = () => axios.get(`${API}/polls`).then(res => res.data);

export const getResults = (pollId) => axios.get(`${API}/polls/${pollId}/results`).then(res => res.data);

export const vote = (pollId, optionId) => axios.post(`${API}/polls/${pollId}/vote`, {
  option_id: optionId, user_id: "user123" // replace with actual user ID if needed
});