<template>
	<div class="login-container">
		<h1>Login</h1>
		<form @submit.prevent="handleLogin">
			<div class="form-group">
				<label for="email">Email</label>
				<input type="email" id="email" v-model="email" required />
			</div>
			<div class="form-group">
				<label for="password">Password</label>
				<input type="password" id="password" v-model="password" required />
			</div>
			<button type="submit">Login</button>
			<p class="redirect">
				Don't have an account?
				<router-link to="/register">Register here</router-link>
			</p>
		</form>
	</div>
</template>

<script>
export default {
	name: "LoginPage",
	data() {
		return {
			email: "",
			password: "",
		};
	},
	methods: {
		handleLogin() {
			// Add your login logic here
			console.log("Logging in with", this.email, this.password);
		},
	},
};
</script>

<style scoped>
.login-container {
	max-width: 400px;
	margin: 0 auto;
	padding: 20px;
	border: 1px solid #ddd;
	border-radius: 8px;
	background-color: #f9f9f9;
	box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h1 {
	text-align: center;
	margin-bottom: 20px;
}

.form-group {
	margin-bottom: 15px;
}

label {
	display: block;
	margin-bottom: 5px;
	font-weight: bold;
}

input {
	width: 100%;
	padding: 10px;
	border: 1px solid #ccc;
	border-radius: 4px;
	transition: border-color 0.3s;
}

input:focus {
	border-color: #007bff;
}

button {
	width: 100%;
	padding: 10px;
	background-color: #007bff;
	color: white;
	border: none;
	border-radius: 4px;
	cursor: pointer;
	transition: background-color 0.3s;
}

button:hover {
	background-color: #0056b3;
}

.redirect {
	text-align: center;
	margin-top: 15px;
}
</style>
