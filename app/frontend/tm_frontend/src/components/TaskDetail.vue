<template>
	<div class="task-detail">
		<h2>{{ task.code_name }}</h2>
		<p><strong>Description:</strong> {{ task.description }}</p>
		<p><strong>Status:</strong> {{ task.status }}</p>
		<p><strong>Tracked Time:</strong> {{ task.tracked_time }}</p>
		<p>
			<strong>Assignee:</strong>
			<a :href="`/users?user_id=${task.assignee_id}`">
				{{ task.assignee }}
			</a>
		</p>
		<p><strong>Creator:</strong> {{ task.creator }}</p>

		<ul>
			<h3>Parent Tasks</h3>
			<li v-for="parent in task.parent_tasks" :key="parent.id">
				<a :href="`/tasks?task_id=${parent.id}`">
					{{ parent.code_name }}
				</a>
				<span>(Status: {{ parent.status }})</span>
			</li>
		</ul>

		<ul>
			<h3>Child Tasks</h3>
			<li v-for="child in task.child_tasks" :key="child.id">
				<a :href="`/tasks?task_id=${child.id}`">
					{{ child.code_name }}
				</a>
				<span>(Status: {{ child.status }})</span>
			</li>
		</ul>

		<h3 class="worklog-title">Logged Work</h3>
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
					<a :href="`/users?user_id=${worklog.assignee_id}`">
						{{ worklog.assignee.name }}
					</a>
				</p>
				<button class="btn-delete" @click.stop="deleteWorklogL(worklog)">
					<img
						src="@/assets/trashcan.png"
						alt="Delete Task"
						class="trashcan-icon"
					/>
				</button>
			</div>
		</div>
	</div>
</template>

<script>
import { getWorklogs, deleteWorklog } from "@/services/api";

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
		goToTask(task) {
			this.$router.push(`/tasks?task_id=${task.id}`);
		},
		async fetchWorklogs() {
			this.worklogs = await getWorklogs(this.task.id);
		},

		async deleteWorklogL(worklog) {
			if (confirm(`Are you sure you want to delete the worklog?`)) {
				try {
					await deleteWorklog(worklog.id);
					this.worklogs = this.worklgetStatusStyleogs.filter(
						(t) => t.id !== worklog.id
					);
				} catch (error) {
					console.error("Failed to delete the task:", error);
					alert("Failed to delete the task. Please try again.");
				}
			}
		},
	},
	async created() {
		await this.fetchWorklogs();
	},
};
</script>

<style>
.task-detail {
	width: 80%;
	max-width: 600px;
	border: 1px solid #ddd;
	padding: 16px;
	border-radius: 8px;
	margin: 16px auto;
	background-color: #f9f9f9;
	box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
	transition: transform 0.2s;
}
.task-detail:hover {
	transform: scale(1.01);
}
.task-detail h2,
.task-detail p {
	color: #333;
	font-weight: bold;
	margin: 0 0 8px;
}
.task-detail h3 {
	color: #555;
	margin: 16px 0 8px;
}
.task-detail ul {
	list-style-type: none;
	padding-left: 0;
}
.task-detail li {
	padding: 8px 0;
	border-bottom: 1px solid #eee;
}
.task-detail li:last-child {
	border-bottom: none;
}
.task-detail li:nth-child(odd) {
	background-color: #fcfcfc;
}
.worklog-title {
	font-size: 24px;
	margin-bottom: 20px;
	color: #333;
}

.worklog-list {
	display: flex;
	flex-direction: column;
}

.worklog-item {
	margin-bottom: 10px;
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
	border-radius: 8px;
	background-color: white;
	padding: 10px;
	display: flex;
}

.worklog-time {
	font-size: 18px;
	margin-right: 10px;
	flex: 0 0 50px;
}

.worklog-description {
	flex-grow: 1;
	text-align: left;
}

.worklog-author {
	margin-top: 200px;
	color: #555;
	font-size: 14px;
	display: block;
	text-align: right;
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
