<template>
	<header>
		<HeaderComponent />
	</header>
	<div class="task-detail">
		<h2 class="task-title">{{ task.code_name }}</h2>
		<p class="task-description">
			<strong>Description:</strong> {{ task.description }}
		</p>
		<p>
			<strong>Status:</strong>
			<span :class="`status ${task.status.toLowerCase().replace(' ', '-')}`">{{
				task.status
			}}</span>
		</p>
		<p><strong>Tracked Time:</strong> {{ task.tracked_time }}</p>
		<p>
			<strong>Assignee:</strong>
			<a :href="`/users?user_id=${task.assignee_id}`" class="link">
				{{ task.assignee }}
			</a>
		</p>
		<p><strong>Creator:</strong> {{ task.creator }}</p>

		<section class="task-relations">
			<h3>Parent Tasks</h3>
			<ul class="child-list">
				<li
					v-for="child in task.parent_tasks"
					:key="child.id"
					class="child-item"
				>
					<div class="child-details">
						<a :href="`/tasks?task_id=${child.id}`" class="child-link">
							{{ child.code_name }}
						</a>
					</div>
					<div class="child-status" :style="getStatusStyle(child.status)">
						{{ child.status }}
					</div>
				</li>
			</ul>

			<h3>Child Tasks</h3>
			<ul class="child-list">
				<li
					v-for="child in task.child_tasks"
					:key="child.id"
					class="child-item"
				>
					<div class="child-details">
						<a :href="`/tasks?task_id=${child.id}`" class="child-link">
							{{ child.code_name }}
						</a>
					</div>
					<div class="child-status" :style="getStatusStyle(child.status)">
						{{ child.status }}
					</div>
				</li>
			</ul>
		</section>

		<section class="worklog-section">
			<h3>Logged Work</h3>
			<div class="worklog-list">
				<div v-for="worklog in worklogs" :key="worklog.id" class="worklog-item">
					<div class="worklog-time">
						{{
							`[${Math.floor(worklog.time_spent / 60)
								.toString()
								.padStart(2, "0")}:${(worklog.time_spent % 60)
								.toString()
								.padStart(2, "0")}]`
						}}
					</div>
					<div class="worklog-description">
						<p>{{ worklog.description }}</p>
					</div>
					<p class="worklog-author">
						by
						<a :href="`/users?user_id=${worklog.assignee_id}`" class="link">
							{{ worklog.assignee.name }}
						</a>
					</p>
					<button class="btn-delete" @click.stop="deleteWorklogL(worklog)">
						<img
							src="@/assets/trashcan.png"
							alt="Delete Worklog"
							class="trashcan-icon"
						/>
					</button>
				</div>
			</div>
		</section>
	</div>
	<footer>
		<FooterComponent />
	</footer>
</template>

<script>
import { getWorklogs, deleteWorklog } from "@/services/api";
import HeaderComponent from "./HeaderComponent.vue";
import FooterComponent from "./FooterComponent.vue";

export default {
	name: "TaskDetail",
	props: {
		task: {
			type: Object,
			required: true,
		},
	},
	data() {
		return {
			worklogs: [],
		};
	},
	methods: {
		async fetchWorklogs() {
			this.worklogs = await getWorklogs(this.task.id);
		},
		async deleteWorklogL(worklog) {
			if (confirm(`Are you sure you want to delete this worklog?`)) {
				try {
					await deleteWorklog(worklog.id);
					this.worklogs = this.worklogs.filter((w) => w.id !== worklog.id);
				} catch (error) {
					alert("Failed to delete the worklog. Please try again.");
				}
			}
		},
		getStatusStyle(status) {
			switch (status) {
				case "TO DO":
					return {
						color: "#6c757d",
						backgroundColor: "#f2f2f2",
						borderRadius: "20px",
						padding: "5px 10px",
					};
				case "IN PROGRESS":
					return {
						color: "#007bff",
						backgroundColor: "rgba(0, 123, 255, 0.1)",
						borderRadius: "20px",
						padding: "5px 10px",
					};
				case "DONE":
					return {
						color: "#28a745",
						backgroundColor: "rgba(40, 167, 69, 0.1)",
						borderRadius: "20px",
						padding: "5px 10px",
					};
				default:
					return {};
			}
		},
	},
	async created() {
		await this.fetchWorklogs();
	},
	components: {
		HeaderComponent,
		FooterComponent,
	},
};
</script>

<style scoped>
.task-detail {
	width: 85%;
	max-width: 800px;
	margin: 20px auto;
	padding: 20px;
	background-color: #ffffff;
	border-radius: 10px;
	box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.task-title {
	font-size: 2rem;
	font-weight: bold;
	color: #2c3e50;
	margin-bottom: 15px;
}

.task-description {
	font-size: 1rem;
	color: #34495e;
	margin-bottom: 15px;
}

.status {
	padding: 5px 10px;
	border-radius: 12px;
	font-size: 0.9rem;
	color: #fff;
	display: inline-block;
}

.status.to-do {
	background-color: #6c757d;
}

.status.in-progress {
	background-color: #007bff;
}

.status.done {
	background-color: #28a745;
}

.link {
	color: #007bff;
	text-decoration: none;
	font-weight: bold;
}

.link:hover {
	text-decoration: underline;
}

.task-relations h3 {
	font-size: 1.25rem;
	color: #2c3e50;
	margin-top: 20px;
	margin-bottom: 10px;
}

.task-relations ul {
	padding: 0;
	list-style: none;
}

.task-relations li {
	margin-bottom: 8px;
	color: #34495e;
}

.worklog-section h3 {
	font-size: 1.5rem;
	margin: 20px 0 15px;
	color: #2c3e50;
}

.worklog-list {
	display: flex;
	flex-direction: column;
}

.worklog-item {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 10px;
	margin-bottom: 10px;
	border-radius: 8px;
	background-color: #f8f9fa;
	box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.worklog-time {
	font-size: 1rem;
	color: #555;
	margin-right: 15px;
}

.worklog-description {
	flex-grow: 1;
	font-size: 0.95rem;
	color: #2c3e50;
}

.worklog-author {
	font-size: 0.85rem;
	color: #777;
	text-align: right;
	margin-left: 10px;
}

.btn-delete {
	background: #e74c3c;
	border: none;
	color: white;
	border-radius: 4px;
	padding: 6px;
	cursor: pointer;
	display: flex;
	align-items: center;
}

.btn-delete:hover {
	background: #c0392b;
}

.trashcan-icon {
	width: 16px;
	height: 16px;
}

p {
	margin: 8px 0;
	color: #495057;
	font-size: 1rem;
}

/* Tasks section */
.child-section {
	margin-top: 20px;
}

.section-title {
	font-size: 1.5rem;
	font-weight: bold;
	margin-bottom: 15px;
	color: #343a40;
}

.child-list {
	list-style: none;
	padding: 0;
	margin: 0;
}

.child-item {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 15px;
	margin-bottom: 10px;
	background-color: #ffffff;
	border-radius: 8px;
	box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
	transition: transform 0.2s ease;
}

.child-item:hover {
	transform: scale(1.02);
}

.child-details {
	font-size: 1.1rem;
	font-weight: 500;
	color: #007bff;
}

.child-link {
	text-decoration: none;
	color: #007bff;
}

.child-link:hover {
	text-decoration: underline;
}

/* Status styles */
.child-status {
	font-size: 0.9rem;
	font-weight: bold;
	text-align: center;
	min-width: 80px;
	text-transform: uppercase;
}
</style>
