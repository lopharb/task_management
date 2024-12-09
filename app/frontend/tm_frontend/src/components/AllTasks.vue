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
				<button class="btn-time-track" @click.stop="openTimeTracker(task)">
					<img
						src="@/assets/hourglass.png"
						alt="Track Time"
						class="hourglass-icon"
					/>
				</button>
				<button class="btn-delete" @click.stop="deleteTask(task)">
					<img
						src="@/assets/trashcan.png"
						alt="Delete Task"
						class="trashcan-icon"
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

		<!-- Overlay for dimming effect -->
		<div
			v-if="showTimeTrackerOverlay || showTaskCreate"
			class="overlay"
			@click="closeAll"
		></div>

		<!-- Time Tracker Component -->
		<TimeTracker
			v-if="showTimeTracker"
			:task="currentTask"
			@close="closeTimeTracker"
		/>

		<!-- Toggle button for TaskCreate -->
		<button @click="toggleTaskCreate" class="btn-toggle">
			{{ showTaskCreate ? "Hide Task Creation" : "Create New Task" }}
		</button>

		<!-- TaskCreate Component as an Overlay -->
		<TaskCreate
			v-if="showTaskCreate"
			@close="closeTaskCreate"
			class="task-create"
		/>
	</div>
</template>

<script>
import { fetchAllTasks, updateTask, deleteTask } from "@/services/api";
import CurrentUserFlair from "./CurrentUserFlair.vue";
import TaskCreate from "./TaskCreate.vue";
import TimeTracker from "./TimeTracker.vue";

export default {
	name: "TaskList",
	data() {
		return {
			tasks: [],
			collapsedTasks: {},
			showTaskCreate: false,
			showTimeTracker: false,
			showTimeTrackerOverlay: false,
			currentTask: null,
		};
	},
	components: {
		CurrentUserFlair,
		TaskCreate,
		TimeTracker,
	},
	methods: {
		openTimeTracker(task) {
			this.currentTask = task;
			this.showTimeTracker = true;
			this.showTimeTrackerOverlay = true;
		},
		closeTimeTracker() {
			this.showTimeTracker = false;
			this.showTimeTrackerOverlay = false;
			this.currentTask = null;
		},
		toggleTaskCreate() {
			this.showTaskCreate = !this.showTaskCreate;
			this.showTimeTrackerOverlay = this.showTaskCreate || this.showTimeTracker;
		},
		closeTaskCreate() {
			this.showTaskCreate = false;
			this.showTimeTrackerOverlay = this.showTimeTracker;
		},
		closeAll() {
			this.closeTimeTracker();
			this.closeTaskCreate();
		},
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
		toggleStatusDropdown(task) {
			this.tasks.forEach((t) => {
				if (t !== task) t.showStatusDropdown = false;
			});
			task.showStatusDropdown = !task.showStatusDropdown;
		},
		async updateStatus(task, newStatus) {
			try {
				const task_updated = {
					assignee_id: task.assignee_id,
					code_name: task.code_name,
					creator_id: task.creator_id,
					description: task.description,
					status: newStatus,
				};
				await updateTask(task.id, task_updated);
				task.status = newStatus;
				task.showStatusDropdown = false;
			} catch (error) {
				console.error("Failed to update status:", error);
			}
		},
		getStatusStyle(status) {
			switch (status) {
				case "TO DO":
					return {
						color: "#6c757d",
						backgroundColor: "rgba(108, 117, 125, 0.2)",
					};
				case "IN PROGRESS":
					return {
						color: "#007bff",
						backgroundColor: "rgba(0, 123, 255, 0.2)",
					};
				case "DONE":
					return {
						color: "#28a745",
						backgroundColor: "rgba(40, 167, 69, 0.2)",
					};
				default:
					return {};
			}
		},
		async deleteTask(task) {
			if (
				confirm(`Are you sure you want to delete the task "${task.code_name}"?`)
			) {
				try {
					await deleteTask(task.id);
					this.tasks = this.tasks.filter((t) => t.id !== task.id);
					alert("Task deleted successfully!");
				} catch (error) {
					console.error("Failed to delete the task:", error);
					alert("Failed to delete the task. Please try again.");
				}
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
	flex-grow: 1;
	text-align: left;
}

.task-header h2 {
	margin: 0;
	font-size: 1.5rem;
}

.status {
	font-weight: bold;
	cursor: pointer;
	position: relative;
	padding: 5px;
	border-radius: 4px;
}

.btn-time-track {
	margin-left: 10px;
	padding: 5px;
	background-color: #28a745;
	border: none;
	border-radius: 4px;
	cursor: pointer;
	display: flex;
	align-items: center;
	justify-content: center;
	transition: transform 0.3s ease;
}

.hourglass-icon {
	width: 20px;
	height: 20px;
	transition: transform 0.3s ease;
}

.btn-time-track:hover .hourglass-icon {
	transform: rotateZ(180deg);
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
	border-left: 5px solid #333;
	border-right: 5px solid transparent;
	border-bottom: 5px solid transparent;
	border-top: 5px solid transparent;
	transition: transform 0.3s;
}

.triangle.collapsed {
	transform: rotate(90deg);
}

.btn-toggle {
	margin: 20px 0;
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
	z-index: 10;
	margin-top: 5px;
	width: 150px;
	border-radius: 4px;
	transition: all 0.2s ease;
}

.status-dropdown ul {
	list-style: none;
	padding: 0;
	margin: 0;
}

.status-dropdown li {
	padding: 8px 10px;
	cursor: pointer;
	transition: background-color 0.2s;
}

.status-dropdown li:hover {
	background-color: #f0f0f0;
}

.status-dropdown li:active {
	background-color: #e0e0e0;
}

a {
	color: #777;
	text-decoration: none;
}

.overlay {
	position: fixed;
	top: 0;
	left: 0;
	right: 0;
	bottom: 0;
	background-color: rgba(0, 0, 0, 0.5);
	z-index: 9;
}

.task-create {
	position: fixed;
	top: 50%;
	left: 50%;
	transform: translate(-50%, -50%);
	background-color: white;
	border-radius: 8px;
	box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
	padding: 20px;
	z-index: 10;
	max-width: 90%;
}
.time-tracker {
	position: fixed;
	top: 50%;
	left: 50%;
	transform: translate(-50%, -50%);
	background-color: white;
	border-radius: 8px;
	box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
	z-index: 10; /* Ensure it appears above the overlay */
}

.btn-delete {
	margin-left: 10px;
	width: 30px;
	height: 30px;
	padding: 0;
	background-color: #dc3545;
	border: none;
	border-radius: 4px;
	cursor: pointer;
	display: flex;
	align-items: center;
	justify-content: center;
	transition: transform 0.3s ease;
}

.trashcan-icon {
	width: 20px;
	height: 20px;
	transition: transform 0.3s ease;
}

.btn-delete:hover {
	background-color: #c82333;
}

.btn-delete:hover .trashcan-icon {
	transform: rotateY(180deg);
}
</style>
