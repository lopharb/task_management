<template>
	<div class="company-management">
		<h3 class="section-title">Companies</h3>
		<div class="table-wrapper">
			<table class="company-table">
				<thead>
					<tr>
						<th>ID</th>
						<th>Name</th>
						<th>Actions</th>
					</tr>
				</thead>
				<tbody>
					<tr v-for="company in companies" :key="company.id">
						<td>{{ company.id }}</td>
						<td>{{ company.company_name }}</td>
						<td>
							<div class="action-buttons">
								<button class="btn btn-edit" @click="editCompany(company)">
									<img
										src="@/assets/pencil.png"
										alt="Edit Task"
										class="pencil-icon"
									/>
								</button>
								<button
									class="btn btn-delete"
									@click="deleteCompany(company.id)"
								>
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
		<div class="action-wrapper">
			<button class="btn btn-create" @click="openCompanyForm()">
				Create New Company
			</button>
		</div>

		<!-- Company Form Modal -->
		<div v-if="showCompanyForm" class="modal-overlay">
			<div class="modal">
				<h3>{{ editMode ? "Edit Company" : "Create Company" }}</h3>
				<form @submit.prevent="submitCompanyForm" class="form">
					<input
						type="text"
						v-model="formData.company_name"
						placeholder="Company Name"
						required
						class="form-input"
					/>
					<div class="form-actions">
						<button type="submit" class="btn btn-save">Save</button>
						<button
							type="button"
							class="btn btn-cancel"
							@click="closeCompanyForm()"
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
	getAllCompanies,
	createCompany,
	deleteCompany,
	updateCompany,
} from "@/services/api";

export default {
	name: "CompanyManagement",
	data() {
		return {
			companies: [],
			showCompanyForm: false,
			editMode: false,
			formData: { id: null, company_name: "" },
		};
	},
	methods: {
		async fetchCompanies() {
			this.companies = await getAllCompanies();
		},
		editCompany(company) {
			this.openCompanyForm(company);
		},
		openCompanyForm(company = null) {
			this.editMode = !!company;
			this.formData = company ? { ...company } : { id: null, company_name: "" };
			this.showCompanyForm = true;
		},
		closeCompanyForm() {
			this.showCompanyForm = false;
		},
		async submitCompanyForm() {
			console.log(this.formData);
			if (this.editMode) {
				await updateCompany(this.formData.id, this.formData);
			} else {
				await createCompany(this.formData.company_name);
			}
			this.fetchCompanies();
			this.closeCompanyForm();
		},
		async deleteCompany(companyId) {
			if (confirm("Are you sure you want to delete this company?")) {
				await deleteCompany(companyId);
				this.fetchCompanies();
			}
		},
	},
	created() {
		this.fetchCompanies();
	},
};
</script>

<style scoped>
/* General Styling */
.company-management {
	padding: 20px;
	font-family: Arial, sans-serif;
	background-color: #f9f9f9;
	min-height: 100vh;
}

/* Section Title */
.section-title {
	font-size: 24px;
	margin-bottom: 15px;
	color: #333;
	text-align: center;
}

/* Table Styling */
.table-wrapper {
	overflow-x: auto;
	border-radius: 8px;
	box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
	background-color: white;
	margin: 20px 0;
}

.company-table {
	width: 100%;
	border-collapse: collapse;
}

.company-table th,
.company-table td {
	padding: 12px 15px;
	text-align: left;
}

.company-table th {
	background-color: #007bff;
	color: white;
}

.company-table tbody tr:nth-child(odd) {
	background-color: #f2f2f2;
}

.company-table tbody tr:hover {
	background-color: #e8f4ff;
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
	margin-right: 5px;
}

.btn-delete {
	background-color: #dc3545;
	color: white;
}

.btn-create {
	background-color: #007bff;
	color: white;
	margin-top: 15px;
}

.btn-edit:hover {
	background-color: #218838;
}

.btn-delete:hover {
	background-color: #c82333;
}

.btn-create:hover {
	background-color: #0056b3;
}

/* Modal Styling */
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

.form-input {
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

/* Button Wrapper */
.action-wrapper {
	text-align: center;
	margin: 20px 0;
}

.action-buttons {
	display: flex;
	gap: 5px;
}

.pencil-icon {
	width: 20px;
	height: 20px;
	transition: transform 0.3s ease;
}

.trashcan-icon {
	width: 20px;
	height: 20px;
	transition: transform 0.3s ease;
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
