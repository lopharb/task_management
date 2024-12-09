<template>
	<div class="task-list">
		<header>
			<CurrentUserFlair />
		</header>
		<h1 style="text-align: left">Task List</h1>

		<div v-for="task in tasks" :key="task.code_name" class="task-item">
			<div class="task-header" @click="toggleCollapse(task.code_name)">
				<span
					:class="{ triangle: true, collapsed: isCollapsed(task.code_name) }"
				></span>
				<a :href="`/tasks?task_id=${task.id}`" class="task-name">
					<h2>{{ task.code_name }}</h2>
				</a>
				<span
					class="status"
					:style="getStatusStyle(task.status)"
					@click.stop="toggleStatusDropdown(task)"
				>
					{{ task.status }} <i class="dropdown-icon">▼</i>
				</span>
				<!-- Updated Track Time Button -->
				<button class="btn-time-track" @click.stop="trackTime(task)">
					<img
						src="@/assets/hourglass.png"
						alt="Track Time"
						class="hourglass-icon"
					/>
				</button>
			</div>
			<div v-if="isCollapsed(task.code_name)" class="task-details">
				<p style="text-align: left">{{ task.description }}</p>

				<h3 style="text-align: left">Child Tasks</h3>
				<ul style="text-align: left">
					<li v-for="child in task.child_tasks" :key="child.id">
						{{ child.code_name }} (Status: {{ child.status }})
					</li>
				</ul>
			</div>
			<div v-if="task.showStatusDropdown" class="status-dropdown">
				<ul>
					<li @click="updateStatus(task, 'TO DO')">TO DO</li>
					<li @click="updateStatus(task, 'IN PROGRESS')">IN PROGRESS</li>
					<li @click="updateStatus(task, 'DONE')">DONE</li>
				</ul>
			</div>
		</div>

		<!-- Toggle button for TaskCreate -->
		<button @click="toggleTaskCreate" class="btn-toggle">
			{{ showTaskCreate ? "Hide Task Creation" : "Create New Task" }}
		</button>

		<!-- Conditionally render TaskCreate -->
		<div v-if="showTaskCreate">
			<TaskCreate />
		</div>
	</div>
</template>

<script>
import { fetchAllTasks, updateTask } from "@/services/api"; // Import the updateTask function
import CurrentUserFlair from "./CurrentUserFlair.vue";
import TaskCreate from "./TaskCreate.vue";

export default {
	name: "TaskList",
	data() {
		return {
			tasks: [],
			collapsedTasks: {},
			showTaskCreate: false, // State for toggling TaskCreate visibility
		};
	},
	components: {
		CurrentUserFlair,
		TaskCreate,
	},
	methods: {
		toggleCollapse(taskCodeName) {
			this.collapsedTasks[taskCodeName] = !this.isCollapsed(taskCodeName);
		},
		isCollapsed(taskCodeName) {
			return !!this.collapsedTasks[taskCodeName];
		},
		async fetchTasks() {
			this.tasks = await fetchAllTasks();
			console.log(this.tasks);
		},
		toggleTaskCreate() {
			this.showTaskCreate = !this.showTaskCreate; // Toggle visibility
		},
		toggleStatusDropdown(task) {
			// Toggle the dropdown for the specific task
			this.tasks.forEach((t) => {
				if (t !== task) t.showStatusDropdown = false; // Close others
			});
			task.showStatusDropdown = !task.showStatusDropdown;
		},
		async updateStatus(task, newStatus) {
			try {
				// Update the task status
				const task_updated = {
					assignee_id: task.assignee_id,
					code_name: task.code_name,
					creator_id: task.creator_id,
					description: task.description,
					status: newStatus,
				};
				await updateTask(task.id, task_updated); // Make API call to update status
				task.status = newStatus; // Update the status in the local state
				task.showStatusDropdown = false; // Close the dropdown after selection
			} catch (error) {
				console.error("Failed to update status:", error);
			}
		},
		trackTime(task) {
			// Logic to track time for the task (to be implemented)
			console.log(`Tracking time for task: ${task.code_name}`);
		},
		getStatusStyle(status) {
			switch (status) {
				case "TO DO":
					return {
						color: "#6c757d", // Grey text
						backgroundColor: "rgba(108, 117, 125, 0.2)", // Light grey background
					};
				case "IN PROGRESS":
					return {
						color: "#007bff", // Blue text
						backgroundColor: "rgba(0, 123, 255, 0.2)", // Light blue background
					};
				case "DONE":
					return {
						color: "#28a745", // Green text
						backgroundColor: "rgba(40, 167, 69, 0.2)", // Light green background
					};
				default:
					return {};
			}
		},
	},
	async created() {
		await this.fetchTasks();
	},
};
</script>

<style scoped>
.task-list {
	max-width: 800px;
	margin: 0 auto;
}

.task-item {
	border: 1px solid #ddd;
	border-radius: 4px;
	margin-bottom: 10px;
	overflow: hidden;
	text-align: left;
}

.task-header {
	background-color: #f7f7f7;
	padding: 15px;
	cursor: pointer;
	display: flex;
	justify-content: space-between;
	align-items: center;
}

.task-name {
	flex-grow: 1; /* Allow name to take available space */
	text-align: left; /* Align task name to the left */
}

.task-header h2 {
	margin: 0;
	font-size: 1.5rem;
}

.status {
	font-weight: bold;
	cursor: pointer; /* Change cursor to pointer */
	position: relative; /* For dropdown positioning */
	padding: 5px; /* Add some padding for better appearance */
	border-radius: 4px; /* Rounded corners for status */
}

.btn-time-track {
	margin-left: 10px; /* Space between status and button */
	padding: 5px; /* Adjust for icon */
	background-color: #28a745; /* Green color for tracking */
	border: none;
	border-radius: 4px;
	cursor: pointer;
	display: flex;
	align-items: center;
	justify-content: center;
	transition: transform 0.3s ease; /* Smooth transition for hover effect */
}

.hourglass-icon {
	width: 20px; /* Adjust size as needed */
	height: 20px; /* Keep aspect ratio */
	transition: transform 0.3s ease; /* Smooth transition for the icon */
}

.btn-time-track:hover .hourglass-icon {
	transform: rotateZ(180deg); /* Flip the hourglass icon */
}

.task-details {
	padding: 15px;
	background-color: #fff;
}

.task-details h3 {
	margin-top: 15px;
}

.triangle {
	display: inline-block;
	width: 0;
	height: 0;
	margin-right: 10px;
	vertical-align: middle;
	border-left: 5px solid transparent;
	border-right: 5px solid transparent;
	border-top: 5px solid #333;
	transition: transform 0.3s;
}

.triangle.collapsed {
	transform: rotate(180deg);
}

.btn-toggle {
	margin: 20px 0; /* Spacing around the button */
	padding: 10px 15px;
	background-color: #007bff;
	color: white;
	border: none;
	border-radius: 4px;
	cursor: pointer;
}

.btn-toggle:hover {
	background-color: #0056b3;
}

.status {
	font-weight: bold;
	cursor: pointer; /* Change cursor to pointer */
	position: relative; /* For dropdown positioning */
	padding: 5px; /* Add some padding for better appearance */
	border-radius: 4px; /* Rounded corners for status */
}

.status-dropdown {
	position: absolute; /* Position it absolutely */
	background-color: white;
	border: 1px solid #ddd;
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
	z-index: 10; /* Ensure dropdown is on top */
	margin-top: 5px; /* Space from status */
	width: 150px; /* Set a fixed width */
	border-radius: 4px; /* Rounded corners for dropdown */
	transition: all 0.2s ease; /* Smooth transition */
}

.status-dropdown ul {
	list-style: none;
	padding: 0;
	margin: 0;
}

.status-dropdown li {
	padding: 8px 10px;
	cursor: pointer;
	transition: background-color 0.2s; /* Smooth background transition */
}

.status-dropdown li:hover {
	background-color: #f0f0f0; /* Highlight on hover */
}

.status-dropdown li:active {
	background-color: #e0e0e0; /* Slightly darker on click */
}
a {
	color: #777;
	text-decoration: none;
}
</style>
