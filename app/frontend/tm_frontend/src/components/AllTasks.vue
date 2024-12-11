<template>
	<header>
		<HeaderComponent />
	</header>
	<div class="task-list">
		<h1 style="text-align: left">Task List</h1>
		<!-- Search Bar -->
		<div class="search-container">
			<input
				type="text"
				v-model="searchQuery"
				placeholder="Search tasks..."
				class="search-bar"
			/>
			<!-- Toggle Button for User Filter -->
			<label class="user-filter">
				<input type="checkbox" v-model="filterByCurrentUser" class="checkbox" />
				<span>My Tasks Only</span>
			</label>
			<!-- Toggle Button for Epic Tasks Filter -->
			<label class="user-filter">
				<input type="checkbox" v-model="filterEpics" class="checkbox" />
				<span>Epics Only</span>
			</label>
			<!-- Toggle button for TaskCreate -->
			<button @click="toggleTaskCreate" class="btn-toggle">
				{{ showTaskCreate ? "Hide Creation" : "New Task" }}
			</button>
		</div>
		<div v-for="task in filteredTasks" :key="task.code_name" class="task-item">
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
				<button class="btn-edit" @click.stop="openTaskEditor(task)">
					<img src="@/assets/pencil.png" alt="Edit Task" class="pencil-icon" />
				</button>
			</div>
			<div v-if="isCollapsed(task.code_name)" class="task-details">
				<p style="text-align: left">{{ task.description }}</p>

				<h3 style="text-align: left">Child Tasks</h3>

				<ul class="task-list">
					<li
						v-for="child in task.child_tasks"
						:key="child.id"
						class="task-item"
					>
						<div class="child-code-name">
							<a :href="`/tasks?task_id=${child.id}`">{{ child.code_name }}</a>
						</div>
						<div class="task-status" :style="getStatusStyle(child.status)">
							{{ child.status }}
						</div>
					</li>
				</ul>

				<button class="btn-add-child" @click="openChildTaskCreator(task)">
					Add Child Task
				</button>
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

		<!-- TaskCreate Component as an Overlay -->
		<TaskCreate
			v-if="showTaskCreate"
			:task="currentTask"
			:mode="taskMode"
			@close="closeTaskCreate"
			@task-created="fetchTasks"
		/>
	</div>
	<footer>
		<FooterComponent />
	</footer>
</template>

<script>
import {
	fetchAllTasks,
	updateTask,
	deleteTask,
	fetchProfile,
} from "@/services/api";
import TaskCreate from "./TaskCreate.vue";
import TimeTracker from "./TimeTracker.vue";
import HeaderComponent from "./HeaderComponent.vue";
import FooterComponent from "./FooterComponent.vue";
import Cookies from "js-cookie";

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
			searchQuery: "",
			filterByCurrentUser: false,
			filterEpics: false,
		};
	},
	components: {
		HeaderComponent,
		TaskCreate,
		TimeTracker,
		FooterComponent,
	},
	computed: {
		filteredTasks() {
			const query = this.searchQuery.toLowerCase();
			return this.tasks.filter((task) => {
				const matchesSearch =
					task.code_name.toLowerCase().includes(query) ||
					task.description.toLowerCase().includes(query);
				const matchesUser =
					!this.filterByCurrentUser ||
					task.assignee_id == Cookies.get("user_id");
				const matchesEpic = !this.filterEpics || task.parent_tasks.length === 0;

				return matchesSearch && matchesUser && matchesEpic;
			});
		},
	},

	methods: {
		openChildTaskCreator(task) {
			this.currentTask = task; // Устанавливаем текущую задачу как родительскую
			this.taskMode = "create"; // Режим создания
			this.showTaskCreate = true; // Показываем компонент создания задачи
		},
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
		openTaskEditor(task) {
			this.currentTask = task;
			this.taskMode = "edit";
			this.showTaskCreate = true;
		},
		toggleTaskCreate() {
			this.currentTask = null;
			this.taskMode = "create";
			this.showTaskCreate = !this.showTaskCreate;
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
			const user = await fetchProfile(Cookies.get("user_id"));
			let company_id = user.company.id;
			this.tasks = await fetchAllTasks(company_id);
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
				this.fetchTasks();
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
		editTask(task) {
			this.taskToEdit = task;
			this.showTaskCreate = true;
		},

		closeTaskCreate() {
			this.showTaskCreate = false;
			this.showTimeTrackerOverlay = this.showTimeTracker;
			this.taskToEdit = null; // Reset the edit mode
		},
		async deleteTask(task) {
			if (
				confirm(`Are you sure you want to delete the task "${task.code_name}"?`)
			) {
				try {
					await deleteTask(task.id);
					this.fetchTasks();
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
	max-width: 1000px;
	margin: 0 auto;
}

.task-item {
	border: 1px solid #ddd;
	border-radius: 4px;
	margin-bottom: 10px;
	overflow: hidden;
	text-align: left;
	transition: transform 0.2s ease;
}
.task-item:hover {
	transform: scale(1.02);
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
	padding: 5px 10px;
	border-radius: 20px;
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

.search-bar {
	width: 60%;
	padding: 10px;
	/* margin-bottom: 15px; */
	border: 1px solid #ddd;
	border-radius: 4px;
	font-size: 16px;
}
.search-container {
	display: flex;
	align-items: center;
	margin-bottom: 15px;
	justify-content: space-between;
}

.user-filter {
	margin-left: 15px;
	display: flex;
	align-items: center;
}

.checkbox {
	margin-right: 5px;
	transform: scale(1.2);
	cursor: pointer;
}

.user-filter span {
	font-size: 14px;
	color: #aaa;
}

.btn-edit {
	margin-left: 10px;
	padding: 5px;
	background-color: #007bff;
	border: none;
	border-radius: 4px;
	cursor: pointer;
	display: flex;
	align-items: center;
	justify-content: center;
	transition: transform 0.3s ease;
}

.pencil-icon {
	width: 20px;
	height: 20px;
	transition: transform 0.3s ease;
}

.btn-edit:hover {
	background-color: #0056b3;
}

.btn-edit:hover .pencil-icon {
	transform: scale(1.2);
}

.btn-add-child {
	margin-top: 10px;
	padding: 10px;
	background-color: #17a2b8;
	color: white;
	border: none;
	border-radius: 4px;
	cursor: pointer;
	transition: background-color 0.3s ease;
}

.btn-add-child:hover {
	background-color: #138496;
}
</style>
