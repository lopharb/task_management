<template>
	<div class="user-profile">
		<h2>
			Welcome,
			<router-link :to="`/users?user_id=${userId}`" class="user-name">{{
				userName
			}}</router-link>
		</h2>
		<button @click="handleLogout" class="btn btn-logout">Logout</button>
	</div>
</template>

<script>
import { fetchProfile } from "@/services/api";
import Cookies from "js-cookie"; // Import js-cookie for cookie management

export default {
	name: "CurrentUserFlair",
	data() {
		return {
			userId: Cookies.get("user_id"), // Get user_id from cookie
			userName: "", // Initialize userName
		};
	},
	async created() {
		if (this.userId) {
			try {
				const user = await fetchProfile(this.userId); // Fetch user data by ID
				this.userName = user.user.name; // Assume the API returns a user object with a name property
			} catch (error) {
				console.error("Error fetching user data:", error);
			}
		}
	},
	methods: {
		handleLogout() {
			Cookies.remove("user_id"); // Remove user_id cookie
			this.$router.push("/login"); // Redirect to login page
		},
	},
};
</script>

<style scoped>
.user-profile {
	text-align: right; /* Align text to the right */
	padding: 10px; /* Reduce padding for a more minimal look */
	background-color: #f9f9f9;
	border-radius: 8px;
	position: absolute; /* Position it in the top right */
	top: 5px;
	right: 10px; /* Adjust based on your layout */
}

.user-name {
	color: #007bff; /* Link color */
	text-decoration: none; /* Remove underline from link */
	font-weight: bold; /* Make the username bold */
}

.user-name:hover {
	text-decoration: underline; /* Underline on hover */
}

.btn-logout {
	background-color: #dc3545; /* Red for logout */
	border-radius: 5px;
	margin-top: 10px; /* Spacing above logout button */
}

.btn-logout:hover {
	background-color: #c82333;
}
</style>
