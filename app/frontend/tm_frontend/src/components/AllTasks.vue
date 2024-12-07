<template>
	<div class="task-list">
		<h1 style="text-align: left">Task List</h1>
		<div v-for="task in tasks" :key="task.code_name" class="task-item">
			<div class="task-header" @click="toggleCollapse(task.code_name)">
				<span
					:class="{ triangle: true, collapsed: isCollapsed(task.code_name) }"
				></span>
				<a :href="`/tasks?task_id=${task.id}`">
					<h2 style="text-align: left">{{ task.code_name }}</h2>
				</a>
				<span class="status" style="text-align: left">{{ task.status }}</span>
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
		</div>
	</div>
</template>

<script>
import { fetchAllTasks } from "@/services/api";
export default {
	name: "TaskList",
	data() {
		return {
			tasks: [],
			collapsedTasks: {},
		};
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
	font-size: 1.5rem;
}

.status {
	font-weight: bold;
	color: #007bff;
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
</style>
