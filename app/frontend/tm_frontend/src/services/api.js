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

export const fetchAllTasks = async () => {
	try {
		const response = await api.get("/tasks"); // Adjust the endpoint as needed
		return response.data;
	} catch (error) {
		console.error("Error fetching tasks:", error);
		throw error; // Rethrow to handle it in the component
	}
};

export const login = async (email, password) => {
	try {
		const response = await api.post("/login", { email, password });
		return response.data;
	} catch (error) {
		console.error("Error logging in:", error);
		throw error; // Rethrow to handle it in the component
	}
};

export const register = async (name, email, password, role, companyId) => {
	try {
		let contents = {
			name: name,
			password_hash: password, // Use 'pwd' for the password field
			email: email,
			role_id: role,
			company_id: companyId, // Use 'company_id' for the company ID
		};
		console.log(contents);
		const response = await api.post("/register/", contents);
		return response.data;
	} catch (error) {
		console.error("Error registering:", error);
		throw error; // Rethrow to handle it in the component
	}
};

export const getAllCompanies = async () => {
	try {
		const response = await api.get("/companies");
		return response.data;
	} catch (error) {
		console.error("Error fetching companies:", error);
		throw error;
	}
};

export const createTask = async (task) => {
	try {
		console.log(task);
		const response = await api.post("/tasks/", task);
		return response.data;
	} catch (error) {
		console.error("Error creating task:", error);
		throw error;
	}
};

export const getEmployees = async (company_id) => {
	try {
		const response = await api.get(`/users?company_id=${company_id}`);
		return response.data;
	} catch (error) {
		console.error("Error fetching employees:", error);
		throw error;
	}
};

export const updateTask = async (task_id, task) => {
	try {
		console.log(task);
		const response = await api.put(`/tasks/${task_id}`, task);
		return response.data;
	} catch (error) {
		console.error("Error updating task:", error);
		throw error;
	}
};
