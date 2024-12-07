<template>
	<div class="register-container">
		<h1>Register</h1>
		<form @submit.prevent="handleRegister">
			<div class="form-group">
				<label for="name">Name</label>
				<input type="text" id="name" v-model="name" required />
			</div>
			<div class="form-group">
				<label for="email">Email</label>
				<input type="email" id="email" v-model="email" required />
			</div>
			<div class="form-group">
				<label for="password">Password</label>
				<input type="password" id="password" v-model="password" required />
			</div>
			<div class="form-group">
				<label for="company">Company</label>
				<select id="company" v-model="selectedCompany" required>
					<option value="" disabled>Select your company</option>
					<option
						v-for="company in companies"
						:key="company.id"
						:value="company.id"
					>
						{{ company.company_name }}
					</option>
				</select>
			</div>
			<div class="form-group">
				<label for="role">Role</label>
				<input type="text" id="role" v-model="role" required />
			</div>
			<button type="submit">Register</button>
			<p class="redirect">
				Already have an account?
				<router-link to="/login">Login here</router-link>
			</p>
		</form>
	</div>
</template>

<script>
import { getAllCompanies } from "@/services/api";
import { register } from "@/services/api";

export default {
	name: "RegisterPage",
	data() {
		return {
			name: "",
			email: "",
			password: "",
			selectedCompany: "",
			role: "",
			companies: [],
		};
	},
	async created() {
		try {
			// Wait for the promise to resolve
			const comp_list = await getAllCompanies();
			this.companies = comp_list; // Assign the resolved value to companies
		} catch (error) {
			console.error("Error fetching companies:", error);
		}
	},
	methods: {
		handleRegister() {
			register(
				this.name,
				this.email,
				this.password,
				this.role,
				this.selectedCompany
			)
				.then((response) => {
					console.log("Registration successful:", response);
					this.$router.push("/login");
				})
				.catch((error) => {
					console.error("Registration failed:", error);
				});
		},
	},
};
</script>

<style scoped>
.register-container {
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

input,
select {
	width: 100%;
	padding: 10px;
	border: 1px solid #ccc;
	border-radius: 4px;
	transition: border-color 0.3s;
}

input:focus,
select:focus {
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
