<template>
	<header>
		<HeaderComponent />
	</header>
	<div class="user-profile">
		<div class="profile-card">
			<h2 class="user-name">{{ user.name }}</h2>
			<p><strong>Email:</strong> {{ user.email }}</p>
			<p><strong>Company:</strong> {{ company }}</p>
			<p><strong>Role:</strong> {{ role }}</p>
		</div>

		<div class="tasks-section">
			<h3 class="section-title">Assigned Tasks</h3>
			<ul class="task-list">
				<li v-for="task in tasks" :key="task.id" class="task-item">
					<div class="task-details">
						<a :href="`/tasks?task_id=${task.id}`" class="task-link">
							{{ task.code_name }}
						</a>
					</div>
					<div class="task-status" :style="getStatusStyle(task.status)">
						{{ task.status }}
					</div>
				</li>
			</ul>
		</div>
	</div>
	<footer>
		<FooterComponent />
	</footer>
</template>

<script>
import { fetchProfile } from "../services/api";
import HeaderComponent from "./HeaderComponent.vue";
import FooterComponent from "./FooterComponent.vue";

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
	methods: {
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
	components: {
		HeaderComponent,
		FooterComponent,
	},
};
</script>

<style scoped>
/* General layout */
.user-profile {
	max-width: 960px;
	margin: 20px auto;
	padding: 20px;
	background-color: #f8f9fa;
	border-radius: 12px;
	box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.title {
	font-size: 2.5rem;
	font-weight: bold;
	text-align: center;
	margin-bottom: 20px;
	color: #343a40;
}

.profile-card {
	padding: 20px;
	background-color: #ffffff;
	border-radius: 12px;
	box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
	margin-bottom: 30px;
}

.user-name {
	font-size: 1.8rem;
	margin-bottom: 10px;
	color: #007bff;
}

p {
	margin: 8px 0;
	color: #495057;
	font-size: 1rem;
}

/* Tasks section */
.tasks-section {
	margin-top: 20px;
}

.section-title {
	font-size: 1.5rem;
	font-weight: bold;
	margin-bottom: 15px;
	color: #343a40;
}

.task-list {
	list-style: none;
	padding: 0;
	margin: 0;
}

.task-item {
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

.task-item:hover {
	transform: scale(1.02);
}

.task-details {
	font-size: 1.1rem;
	font-weight: 500;
	color: #007bff;
}

.task-link {
	text-decoration: none;
	color: #007bff;
}

.task-link:hover {
	text-decoration: underline;
}

/* Status styles */
.task-status {
	font-size: 0.9rem;
	font-weight: bold;
	text-align: center;
	min-width: 80px;
	text-transform: uppercase;
}

/* Responsive design */
@media screen and (max-width: 768px) {
	.user-profile {
		padding: 15px;
	}
	.title {
		font-size: 2rem;
	}
	.profile-card {
		padding: 15px;
	}
	.task-item {
		flex-direction: column;
		align-items: flex-start;
	}
	.task-status {
		margin-top: 8px;
	}
}
</style>
