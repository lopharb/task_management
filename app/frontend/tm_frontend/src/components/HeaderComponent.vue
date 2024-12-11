<template>
	<header class="site-header">
		<div class="logo">
			<h1>Task Management</h1>
		</div>
		<nav class="navigation">
			<router-link to="/tasks/browse" class="nav-item">Home</router-link>
			<router-link to="/administrate" class="nav-item">Admin Panel</router-link>
			<router-link :to="`/users?user_id=${userId}`" class="nav-item"
				>Profile</router-link
			>
			<button @click="handleLogout" class="btn btn-logout">Logout</button>
		</nav>
	</header>
</template>

<script>
import Cookies from "js-cookie";
export default {
	name: "HeaderComponent",
	data() {
		return {
			userId: Cookies.get("user_id"),
		};
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
.site-header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 15px 30px;
	margin-top: 0;
	background: #53718f;
	color: white;
}

.logo {
	display: flex;
	align-items: center;
}

.logo img {
	height: 40px;
	margin-right: 10px;
}

.navigation {
	display: flex;
	gap: 15px;
}

.nav-item {
	text-decoration: none;
	color: white;
	font-weight: bold;
}

.nav-item:hover {
	text-decoration: underline;
}
.btn-logout {
	background-color: #aaa;
	border-radius: 5px;
}

.btn-logout:hover {
	background-color: #ddd;
}
</style>
