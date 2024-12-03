<template>
	<div>
		<div v-if="task">
			<TaskDetail :task="task" />
		</div>
		<div v-else>
			<p>Loading task...</p>
		</div>
	</div>
</template>

<script>
import { fetchTask } from "../services/api"; // Import the fetch function
import TaskDetail from "./TaskDetail.vue"; // Import the TaskDetail component

export default {
	components: {
		TaskDetail,
	},
	data() {
		return {
			task: null,
		};
	},
	async created() {
		try {
			const taskId = this.$route.query.task_id;
			if (!taskId) {
				throw new Error("No task ID provided");
			}
			this.task = await fetchTask(taskId);
		} catch (error) {
			console.error("Failed to fetch task:", error);
		}
	},
};
</script>

<style scoped>
/* Add any styles specific to TaskList here */
</style>
