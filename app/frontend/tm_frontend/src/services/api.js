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

export const fetchAllTasks = async (company_id = null) => {
	try {
		if (!company_id) {
			const response = await api.get("/tasks"); // Adjust the endpoint as needed
			return response.data;
		}
		const response = await api.get(`/tasks?company_id=${company_id}`); // Adjust the endpoint as needed
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

export const deleteTask = async (task_id) => {
	try {
		const response = await api.delete(`/tasks/${task_id}`);
		return response.data;
	} catch (error) {
		console.error("Error deleting task:", error);
		throw error;
	}
};

export const trackTime = async (worklog) => {
	try {
		const response = await api.post(`/worklogs/`, worklog);
		return response.data;
	} catch (error) {
		console.error("Error tracking time:", error);
		throw error;
	}
};

export const getWorklogs = async (task_id) => {
	try {
		const response = await api.get(`/worklogs?task_id=${task_id}`);
		return response.data;
	} catch (error) {
		console.error("Error fetching worklogs:", error);
		throw error;
	}
};

export const deleteWorklog = async (worklog_id) => {
	try {
		const response = await api.delete(`/worklogs/${worklog_id}`);
		return response.data;
	} catch (error) {
		console.error("Error deleting worklog:", error);
		throw error;
	}
};

export const createDependency = async (task_id, parent_id) => {
	try {
		const response = await api.post(
			`/tasks/${task_id}/dependencies/${parent_id}`
		);
		return response.data;
	} catch (error) {
		console.error("Error creating dependency:", error);
		throw error;
	}
};

export const getAllUsers = async () => {
	try {
		const response = await api.get("/users");
		return response.data;
	} catch (error) {
		console.error("Error fetching users:", error);
		throw error;
	}
};

export const updateUser = async (user_id, user) => {
	try {
		const response = await api.put(`/users/${user_id}`, user);
		return response.data;
	} catch (error) {
		console.error("Error updating user:", error);
		throw error;
	}
};

export const deleteUser = async (user_id) => {
	try {
		const response = await api.delete(`/users/${user_id}`);
		return response.data;
	} catch (error) {
		console.error("Error deleting user:", error);
		throw error;
	}
};

export const getAllRoles = async () => {
	try {
		const response = await api.get("/roles");
		return response.data;
	} catch (error) {
		console.error("Error fetching roles:", error);
		throw error;
	}
};

export const createCompany = async (company_name) => {
	try {
		const response = await api.post("/companies", {
			company_name: company_name,
		});
		return response.data;
	} catch (error) {
		console.error("Error creating company:", error);
		throw error;
	}
};

export const deleteCompany = async (company_id) => {
	try {
		const response = await api.delete(`/companies/${company_id}`);
		return response.data;
	} catch (error) {
		console.error("Error deleting company:", error);
		throw error;
	}
};

export const updateCompany = async (company_id, company) => {
	try {
		const response = await api.put(`/companies/${company_id}`, company);
		return response.data;
	} catch (error) {
		console.error("Error updating company:", error);
		throw error;
	}
};
