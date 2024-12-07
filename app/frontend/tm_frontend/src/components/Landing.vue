<template>
	<div class="landing-page">
		<div class="content">
			<h1>Welcome to Task Tracker</h1>
			<p>
				Your ultimate solution for tracking tasks and managing projects
				efficiently, just like Jira and Trello.
			</p>
			<div class="buttons">
				<router-link to="/login" class="btn">Login</router-link>
				<router-link to="/register" class="btn btn-secondary"
					>Register</router-link
				>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	name: "LandingPage",
};
</script>

<style scoped>
.landing-page {
	display: flex;
	justify-content: center;
	align-items: center;
	height: 100vh;
	background-color: #f0f4f8; /* Light background for contrast */
	text-align: center;
}

.content {
	max-width: 600px;
	padding: 20px;
	background-color: white;
	border-radius: 8px;
	box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

h1 {
	font-size: 2.5rem;
	margin-bottom: 20px;
}

p {
	font-size: 1.2rem;
	margin-bottom: 30px;
}

.buttons {
	display: flex;
	justify-content: space-around;
}

.btn {
	padding: 10px 20px;
	background-color: #007bff;
	color: white;
	text-decoration: none;
	border-radius: 4px;
	transition: background-color 0.3s;
}

.btn:hover {
	background-color: #0056b3;
}

.btn-secondary {
	background-color: #28a745; /* Green for register */
}

.btn-secondary:hover {
	background-color: #218838;
}
</style>
