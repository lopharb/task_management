<template>
	<div>
		<h3>Users</h3>
		<table class="user-table">
			<thead>
				<tr>
					<th>ID</th>
					<th>Name</th>
					<th>Email</th>
					<th>Actions</th>
				</tr>
			</thead>
			<tbody>
				<tr v-for="user in users" :key="user.id">
					<td>{{ user.id }}</td>
					<td>{{ user.name }}</td>
					<td>{{ user.email }}</td>
					<td>
						<button @click="editUser(user)">Edit</button>
						<button @click="deleteUser(user.id)">Delete</button>
					</td>
				</tr>
			</tbody>
		</table>

		<!-- User Form Modal -->
		<div v-if="showUserForm" class="modal">
			<h3>{{ editMode ? "Edit User" : "Create User" }}</h3>
			<form @submit.prevent="submitUserForm">
				<input
					type="text"
					v-model="formData.name"
					placeholder="Name"
					required
				/>
				<input
					type="email"
					v-model="formData.email"
					placeholder="Email"
					required
				/>

				<!-- Company Select -->
				<select v-model="formData.companyId" required>
					<option value="" disabled>Select Company</option>
					<option
						v-for="company in companies"
						:key="company.id"
						:value="company.id"
					>
						{{ company.name }}
					</option>
				</select>

				<!-- Role Select -->
				<select v-model="formData.roleId" required>
					<option value="" disabled>Select Role</option>
					<option v-for="role in roles" :key="role.id" :value="role.id">
						{{ role.name }}
					</option>
				</select>

				<button type="submit">Save</button>
				<button type="button" @click="closeUserForm()">Cancel</button>
			</form>
		</div>
	</div>
</template>

<script>
import {
	getAllUsers,
	getAllCompanies,
	getAllRoles,
	updateUser,
	deleteUser,
} from "../services/api";

export default {
	name: "UserManagement",
	data() {
		return {
			users: [],
			companies: [], // Store companies here
			roles: [], // Store roles here
			showUserForm: false,
			editMode: false,
			formData: {
				id: null,
				name: "",
				email: "",
				companyId: null,
				roleId: null,
			},
		};
	},
	methods: {
		async fetchUsers() {
			this.users = await getAllUsers();
		},
		async fetchCompanies() {
			this.companies = await getAllCompanies(); // Fetch companies
		},
		async fetchRoles() {
			this.roles = await getAllRoles(); // Fetch roles
		},
		openUserForm(user = null) {
			this.editMode = !!user;
			this.formData = user
				? { ...user }
				: { id: null, name: "", email: "", companyId: null, roleId: null };
			this.showUserForm = true;
		},
		editUser(user) {
			this.openUserForm(user);
		},
		closeUserForm() {
			this.showUserForm = false;
		},
		async submitUserForm() {
			await updateUser(this.formData.id, this.formData);
			this.fetchUsers();
			this.closeUserForm();
		},
		async deleteUser(userId) {
			if (confirm("Are you sure you want to delete this user?")) {
				await deleteUser(userId);
				this.fetchUsers();
			}
		},
	},
	created() {
		this.fetchUsers();
		this.fetchCompanies(); // Fetch companies on created
		this.fetchRoles(); // Fetch roles on created
	},
};
</script>

<style scoped>
.user-table {
	width: 100%;
	border-collapse: collapse;
	margin-bottom: 20px;
}

.user-table th,
.user-table td {
	border: 1px solid #ddd;
	padding: 10px;
	text-align: left;
}

.modal {
	background: white;
	border-radius: 4px;
	border: 1px solid #ddd;
	left: 50%;
	margin-top: 10px;
	padding: 20px;
	position: fixed;
	top: 50%;
	transform: translate(-50%, -50%);
	width: 100%;
}
</style>
