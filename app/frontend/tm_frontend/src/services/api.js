import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api"; // Adjust if your backend runs on a different address

export const api = axios.create({
	baseURL: API_URL,
	timeout: 1000,
});

// Fetch task by ID
export const fetchTask = async (taskId) => {
	try {
		const response = await api.get(`/tasks/${taskId}`); // Adjust the endpoint as needed
		return response.data;
	} catch (error) {
		console.error("Error fetching task:", error);
		throw error; // Rethrow to handle it in the component
	}
};

export const fetchProfile = async (user_id) => {
	try {
		const response = await api.get(`/users/${user_id}`); // Adjust the endpoint as needed
		return response.data;
	} catch (error) {
		console.error("Error fetching profile:", error);
		throw error; // Rethrow to handle it in the component
	}
};

// Other API functions can be added here
