<template>
	<div class="time-tracker">
		<h3>Time Tracker</h3>
		<form @submit.prevent="submitTimeTracking">
			<div class="form-group">
				<label for="timeSpent">Time Spent (in hours)</label>
				<input
					type="number"
					id="timeSpent"
					v-model="timeSpent"
					required
					min="0"
					step="0.1"
				/>
			</div>
			<div class="form-group">
				<label for="worklogDescription">Worklog Description (optional)</label>
				<textarea
					id="worklogDescription"
					v-model="worklogDescription"
					placeholder="Enter description (optional)"
				></textarea>
			</div>
			<button type="submit">Submit</button>
		</form>
	</div>
</template>

<script>
export default {
	name: "TimeTracker",
	data() {
		return {
			timeSpent: null,
			worklogDescription: "",
		};
	},
	methods: {
		submitTimeTracking() {
			if (this.timeSpent) {
				// Logic to handle time tracking submission
				const timeEntry = {
					timeSpent: this.timeSpent,
					worklogDescription: this.worklogDescription,
				};
				console.log("Time Entry Submitted:", timeEntry);

				// Reset the fields after submission
				this.timeSpent = null;
				this.worklogDescription = "";
			}
		},
	},
};
</script>

<style scoped>
.time-tracker {
	border: 1px solid #ddd;
	border-radius: 4px;
	padding: 15px;
	background-color: #f9f9f9;
	width: 35%;
}

.form-group {
	margin-bottom: 15px;
}

label {
	display: block;
	margin-bottom: 5px;
}

input[type="number"],
textarea {
	width: 95%;
	padding: 8px;
	border: 1px solid #ccc;
	border-radius: 4px;
}

button {
	background-color: #007bff;
	color: white;
	border: none;
	padding: 10px 15px;
	border-radius: 4px;
	cursor: pointer;
}

button:hover {
	background-color: #0056b3;
}
</style>
