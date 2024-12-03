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
	</div>
</template>

<script>
export default {
	name: "TaskDetail",
	props: {
		task: {
			type: Object,
			required: true,
		},
	},
	methods: {
		goToTask(task) {
			this.$router.push(`/tasks?task_id=${task.id}`);
		},
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
</style>
