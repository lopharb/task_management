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
				<a :href="`/tasks?task_id=${task.id}`">
					<h2 style="text-align: left">{{ task.code_name }}</h2>
				</a>
				<span class="status" @click.stop="toggleStatusDropdown(task)">
					{{ task.status }} <i class="dropdown-icon">▼</i>
				</span>
				<button class="btn-time-track" @click.stop="trackTime(task)">
					Track Time
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
import { fetchAllTasks, updateTask } from "@/services/api"; // Import the updateTaskStatus function
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
				console.log(task);
				const task_update = {
					code_name: task.code_name,
					status: newStatus,
					assignee_id: task.assignee_id,
					creator_id: task.creator_id,
					description: task.description,
				};
				await updateTask(task.id, task_update); // Make API call to update status
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

.task-header h2 {
	margin: 0;
	text-align: left;
	font-size: 1.5rem;
}

.status {
	font-weight: bold;
	color: #007bff;
	cursor: pointer; /* Change cursor to pointer */
	position: relative; /* For dropdown positioning */
}

.btn-time-track {
	margin-left: 10px; /* Space between status and button */
	padding: 5px 10px;
	background-color: #28a745; /* Green color for tracking */
	color: white;
	border: none;
	border-radius: 4px;
	cursor: pointer;
}

.btn-time-track:hover {
	background-color: #218838;
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

.status-dropdown {
	position: absolute;
	background-color: white;
	border: 1px solid #ddd;
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
	z-index: 10; /* Ensure dropdown is on top */
	margin-top: 5px; /* Space from status */
}

.status-dropdown ul {
	list-style: none;
	padding: 0;
	margin: 0;
}

.status-dropdown li {
	padding: 8px 10px;
	cursor: pointer;
}

.status-dropdown li:hover {
	background-color: #f0f0f0; /* Highlight on hover */
}
</style>
