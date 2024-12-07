<template>
	<div class="user-profile">
		<h1>User Profile</h1>
		<div class="profile-info">
			<h2>{{ user.name }}</h2>
			<p><strong>Email:</strong> {{ user.email }}</p>
			<p><strong>Company:</strong> {{ company }}</p>
			<p><strong>Role:</strong> {{ role }}</p>
		</div>

		<h3>Assigned Tasks</h3>
		<ul class="task-list">
			<li v-for="task in tasks" :key="task.id" class="task-item">
				<div class="task-code-name">
					<a :href="`/tasks?task_id=${task.id}`">{{ task.code_name }}</a>
				</div>
				<div class="task-status">{{ task.status }}</div>
			</li>
		</ul>
	</div>
</template>

<script>
import { fetchProfile } from "../services/api"; // Import the function to fetch user profile

export default {
	name: "UserProfile",
	data() {
		return {
			user: {
				name: "",
				email: "",
			},
			company: "",
			role: "",
			tasks: [],
		};
	},
	async created() {
		try {
			const userId = parseInt(this.$route.query.user_id, 10);
			if (isNaN(userId)) {
				throw new Error("No user ID provided");
			}
			const profileData = await fetchProfile(userId);
			this.user = profileData.user;
			this.company = profileData.company.company_name;
			this.role = profileData.role.role_name;
			this.tasks = profileData.tasks;
		} catch (error) {
			console.error("Failed to fetch profile:", error);
		}
	},
};
</script>

<style scoped>
.user-profile {
	max-width: 600px;
	margin: 0 auto;
	padding: 20px;
	background-color: #f9f9f9;
	border-radius: 8px;
	box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h1 {
	font-size: 2rem;
	margin-bottom: 20px;
}

.profile-info {
	margin-bottom: 30px;
}

h2 {
	font-size: 1.5rem;
	margin: 0 0 10px;
}

p {
	margin: 5px 0;
	color: #555;
}

h3 {
	margin-top: 20px;
	font-size: 1.2rem;
}

.task-list {
	list-style-type: none;
	padding: 0;
}

.task-item {
	padding: 10px 15px;
	margin: 5px 0;
	background-color: #fff;
	border-radius: 4px;
	box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
	display: flex;
	justify-content: space-between;
}

.task-code-name {
	font-weight: bold;
}

.task-status {
	color: #888;
}
</style>
