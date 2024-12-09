<template>
	<div class="task-create">
		<h2>{{ mode === "edit" ? "Edit Task" : "Create a New Task" }}</h2>
		<form @submit.prevent="submitTask">
			<div class="form-group">
				<label for="code_name">Code Name:</label>
				<input
					type="text"
					id="code_name"
					v-model="taskData.code_name"
					required
				/>
			</div>
			<div class="form-group">
				<label for="assignee_id">Assignee:</label>
				<select id="assignee_id" v-model="taskData.assignee_id" required>
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
			<div class="form-group">
				<label for="description">Description:</label>
				<textarea
					id="description"
					v-model="taskData.description"
					required
				></textarea>
			</div>
			<div class="form-group">
				<label for="status">Status:</label>
				<select id="status" v-model="taskData.status" required>
					<option value="TO DO">TO DO</option>
					<option value="IN PROGRESS">IN PROGRESS</option>
					<option value="DONE">DONE</option>
				</select>
			</div>
			<button type="submit" class="btn">
				{{ mode === "edit" ? "Update Task" : "Create Task" }}
			</button>
		</form>
		<div v-if="error" class="error">{{ error }}</div>
		<div v-if="success" class="success">{{ success }}</div>
	</div>
</template>

<script>
import {
	createTask,
	updateTask,
	getEmployees,
	fetchProfile,
} from "@/services/api";
import Cookies from "js-cookie";

export default {
	name: "TaskCreate",
	props: {
		task: {
			type: Object,
			default: () => null,
		},
		mode: {
			type: String,
			default: "create", // "create" or "edit"
		},
	},
	data() {
		return {
			userId: Cookies.get("user_id"),
			employees: [],
			taskData: {
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
		// Pre-fill form if editing an existing task
		if (this.task && this.mode === "edit") {
			this.taskData = { ...this.task };
		}

		// Fetch employees
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
				if (this.mode === "edit") {
					// Update existing task
					await updateTask(this.taskData.id, this.taskData);
					this.success = "Task updated successfully!";
				} else {
					// Create new task
					await createTask(this.taskData);
					this.success = "Task created successfully!";
				}
				this.error = ""; // Clear error message
				await this.$emit("task-created"); // Notify parent to refresh tasks
			} catch (err) {
				this.error =
					"Failed to " +
					(this.mode === "edit" ? "update" : "create") +
					" task: " +
					(err.response?.data?.detail || err.message);
				this.success = ""; // Clear success message
			}
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
