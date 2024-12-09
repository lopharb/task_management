<template>
	<div class="task-create">
		<h2>Create a New Task</h2>
		<form @submit.prevent="submitTask">
			<div class="form-group">
				<label for="code_name">Code Name:</label>
				<input type="text" id="code_name" v-model="task.code_name" required />
			</div>
			<div class="form-group">
				<label for="assignee_id">Assignee:</label>
				<select id="assignee_id" v-model="task.assignee_id" required>
					<option value="" disabled>Select Assignee</option>
					<option
						v-for="employee in employees"
						:key="employee.id"
						:value="employee.id"
					>
						{{ employee.name }}
					</option>
				</select>
			</div>
			<div class="form-group"></div>
			<div class="form-group">
				<label for="description">Description:</label>
				<textarea
					id="description"
					v-model="task.description"
					required
				></textarea>
			</div>
			<button type="submit" class="btn">Create Task</button>
		</form>
		<div v-if="error" class="error">{{ error }}</div>
		<div v-if="success" class="success">{{ success }}</div>
	</div>
</template>

<script>
import { createTask } from "@/services/api"; // Adjust the import based on your API structure
import { getEmployees, fetchProfile } from "@/services/api";
import Cookies from "js-cookie";
export default {
	name: "TaskCreate",
	data() {
		return {
			userId: Cookies.get("user_id"),
			employees: [],
			task: {
				code_name: "",
				creator_id: Cookies.get("user_id"),
				assignee_id: null,
				status: "TO DO",
				description: "",
			},
			success: "",
			error: "",
		};
	},
	async created() {
		let company_id = null;
		try {
			const user = await fetchProfile(this.userId);
			company_id = user.company.id;
			this.employees = await getEmployees(company_id);
		} catch (error) {
			console.error("Error fetching user data:", error);
		}
	},
	methods: {
		async submitTask() {
			try {
				await createTask(this.task);
				this.success = "Task created successfully!";
				this.error = ""; // Clear error message
				this.resetForm(); // Optionally reset the form after successful creation
			} catch (err) {
				this.error =
					"Failed to create task: " +
					(err.response?.data?.detail || err.message);
				this.success = ""; // Clear success message
			}
		},
		resetForm() {
			this.task = {
				code_name: "",
				creator_id: null,
				assignee_id: null,
				status: "",
				description: "",
			};
		},
	},
};
</script>

<style scoped>
.task-create {
	width: 35%;
	margin: 0 auto;
	padding: 20px;
	border-radius: 8px;
	box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
	background-color: #f9f9f9;
}

.form-group {
	margin-bottom: 15px;
}

label {
	display: block;
	margin-bottom: 5px;
}

input,
select,
textarea {
	width: 95%;
	padding: 8px;
	border: 1px solid #ccc;
	border-radius: 4px;
}

.btn {
	padding: 10px 15px;
	background-color: #007bff;
	color: white;
	border: none;
	border-radius: 4px;
	cursor: pointer;
}

.btn:hover {
	background-color: #0056b3;
}

.error {
	color: #dc3545;
}

.success {
	color: #28a745;
}
</style>
