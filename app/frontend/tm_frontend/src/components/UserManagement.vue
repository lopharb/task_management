<template>
	<div class="user-management">
		<h3 class="section-title">Users</h3>
		<div class="table-wrapper">
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
							<div class="action-buttons">
								<button class="btn btn-edit" @click="editUser(user)">
									<img
										src="@/assets/pencil.png"
										alt="Edit Task"
										class="pencil-icon"
									/>
								</button>
								<button class="btn btn-delete" @click="deleteUser(user.id)">
									<img
										src="@/assets/trashcan.png"
										alt="Delete Task"
										class="trashcan-icon"
									/>
								</button>
							</div>
						</td>
					</tr>
				</tbody>
			</table>
		</div>

		<!-- User Form Modal -->
		<div v-if="showUserForm" class="modal-overlay">
			<div class="modal">
				<h3>{{ editMode ? "Edit User" : "Create User" }}</h3>
				<form @submit.prevent="submitUserForm" class="form">
					<input
						type="text"
						v-model="formData.name"
						placeholder="Name"
						required
						class="form-input"
					/>
					<input
						type="email"
						v-model="formData.email"
						placeholder="Email"
						required
						class="form-input"
					/>

					<!-- Company Select -->
					<select v-model="formData.companyId" required class="form-select">
						<option value="" disabled>Select Company</option>
						<option
							v-for="company in companies"
							:key="company.id"
							:value="company.id"
						>
							{{ company.company_name }}
						</option>
					</select>

					<!-- Role Select -->
					<select v-model="formData.roleId" required class="form-select">
						<option value="" disabled>Select Role</option>
						<option v-for="role in roles" :key="role.id" :value="role.id">
							{{ role.company_name }}
						</option>
					</select>

					<div class="form-actions">
						<button type="submit" class="btn btn-save">Save</button>
						<button
							:type="button"
							class="btn btn-cancel"
							@click="closeUserForm()"
						>
							Cancel
						</button>
					</div>
				</form>
			</div>
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
			companies: [],
			roles: [],
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
			this.companies = await getAllCompanies();
		},
		async fetchRoles() {
			this.roles = await getAllRoles();
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
		this.fetchCompanies();
		this.fetchRoles();
	},
};
</script>

<style scoped>
.user-management {
	padding: 20px;
	font-family: Arial, sans-serif;
	background-color: #f9f9f9;
	min-height: 100vh;
}

.section-title {
	font-size: 24px;
	margin-bottom: 15px;
	color: #333;
	text-align: center;
}

.table-wrapper {
	overflow-x: auto;
	border-radius: 8px;
	box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
	background-color: white;
	margin: 20px 0;
}

.user-table {
	width: 100%;
	border-collapse: collapse;
}

.user-table th,
.user-table td {
	padding: 12px 15px;
	text-align: left;
}

.user-table th {
	background-color: #007bff;
	color: white;
}

.user-table tbody tr:nth-child(odd) {
	background-color: #f2f2f2;
}

.user-table tbody tr:hover {
	background-color: #e8f4ff;
}

.action-buttons {
	display: flex;
	gap: 5px;
}

.btn {
	padding: 8px 12px;
	border: none;
	border-radius: 4px;
	cursor: pointer;
	font-size: 14px;
}

.btn-edit {
	background-color: #28a745;
	color: white;
}

.btn-edit:hover {
	background-color: #218838;
}

.modal-overlay {
	position: fixed;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
	background: rgba(0, 0, 0, 0.5);
	display: flex;
	justify-content: center;
	align-items: center;
}

.modal {
	background: white;
	padding: 30px;
	border-radius: 8px;
	box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
	max-width: 400px;
	width: 100%;
}

.form {
	display: flex;
	flex-direction: column;
}

.form-input,
.form-select {
	padding: 10px;
	margin-bottom: 15px;
	border: 1px solid #ccc;
	border-radius: 4px;
	font-size: 14px;
}

.form-actions {
	display: flex;
	justify-content: flex-end;
	gap: 10px;
}

.btn-save {
	background-color: #007bff;
	color: white;
}

.btn-cancel {
	background-color: #6c757d;
	color: white;
}

.btn-save:hover {
	background-color: #0056b3;
}

.btn-cancel:hover {
	background-color: #5a6268;
}

.pencil-icon {
	width: 20px;
	height: 20px;
	transition: transform 0.3s ease;
}
.btn-edit {
	margin-left: 10px;
	padding: 5px;
	background-color: #007bff;
	border: none;
	border-radius: 4px;
	cursor: pointer;
	display: flex;
	align-items: center;
	justify-content: center;
	transition: transform 0.3s ease;
}

.pencil-icon {
	width: 20px;
	height: 20px;
	transition: transform 0.3s ease;
}

.btn-edit:hover {
	background-color: #0056b3;
}
.btn-edit:hover .pencil-icon {
	transform: scale(1.2);
}
.btn-delete {
	margin-left: 10px;
	width: 30px;
	height: 30px;
	padding: 0;
	background-color: #dc3545;
	border: none;
	border-radius: 4px;
	cursor: pointer;
	display: flex;
	align-items: center;
	justify-content: center;
	transition: transform 0.3s ease;
}

.trashcan-icon {
	width: 20px;
	height: 20px;
	transition: transform 0.3s ease;
}

.btn-delete:hover {
	background-color: #c82333;
}

.btn-delete:hover .trashcan-icon {
	transform: rotateY(180deg);
}
</style>
