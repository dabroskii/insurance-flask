import axios from "axios";

const axiosInstance = axios.create({
  baseURL: "http://127.0.0.1:5000/api",
  withCredentials: true, // This ensures cookies are sent with requests
});

export default axiosInstance;
