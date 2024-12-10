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
		<ul class="worklog-list">
			<li v-for="worklog in worklogs" :key="worklog.id" class="worklog-item">
				<div class="worklog-content">
					{{
						`[${Math.floor(worklog.time_spent / 60)}:${
							worklog.time_spent % 60
						}] ${worklog.description} by ${worklog.assignee.name}`
					}}
				</div>
			</li>
		</ul>
	</div>
</template>

<script>
import { getWorklogs } from "@/services/api";

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
	list-style: none;
	padding: 0;
	max-width: 800px; /* Limit the width for better readability */
	margin: 0 auto; /* Center the list */
}

.worklog-item {
	background: white;
	border: 1px solid #e0e0e0; /* Light border for separation */
	border-radius: 8px;
	margin-bottom: 10px;
	padding: 15px;
	transition: box-shadow 0.3s ease; /* Smooth shadow effect */
}

.worklog-item:hover {
	box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1); /* Shadow on hover */
}

.worklog-content {
	color: #333; /* Dark text color for readability */
	font-size: 16px; /* Base font size */
	line-height: 1.5; /* Improved line height for readability */
}

/* Optional: Style for time spent */
.worklog-content::before {
	content: "[";
	font-weight: bold;
	color: #007bff; /* Primary color for time */
}

.worklog-content::after {
	content: "]";
	font-weight: bold;
	color: #007bff; /* Primary color for time */
}
</style>
