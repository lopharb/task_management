<template>
	<header>
		<HeaderComponent />
	</header>
	<div class="analytics-container">
		<div class="content">
			<h1>Task Time Analytics</h1>

			<!-- Filters Section -->
			<div class="filters">
				<label>
					<span>Select Company:</span>
					<select v-model="selectedCompany" @change="updateCompanyData">
						<option value="">All Companies</option>
						<option
							v-for="company in companies"
							:key="company.id"
							:value="company.id"
						>
							{{ company.company_name }}
						</option>
					</select>
				</label>
				<label v-if="selectedCompany">
					<span>Select Employee:</span>
					<select v-model="selectedEmployee" @change="updateEmployeeData">
						<option value="">Company-wide</option>
						<option
							v-for="employee in employees"
							:key="employee.id"
							:value="employee.id"
						>
							{{ employee.name }}
						</option>
					</select>
				</label>
			</div>

			<!-- Charts Section -->
			<div class="chart-container">
				<h2 v-if="selectedEmployee">Employee Task Time Histogram</h2>
				<h2 v-else-if="selectedCompany">Company Task Time Histogram</h2>
				<h2 v-else>All Companies Task Time Histogram</h2>
				<canvas id="taskTimeChart" width="400" height="200"></canvas>
			</div>
		</div>
	</div>
	<footer>
		<FooterComponent />
	</footer>
</template>

<script>
import Chart from "chart.js/auto";
import { getAllCompanies, getEmployees, fetchAllTasks } from "@/services/api";
import HeaderComponent from "./HeaderComponent.vue";
import FooterComponent from "./FooterComponent.vue";

export default {
	name: "TaskAnalytics",
	components: {
		HeaderComponent,
		FooterComponent,
	},
	data() {
		return {
			companies: [], // List of companies
			employees: [], // List of employees
			taskTimeData: [], // Task time tracking data
			selectedCompany: "", // Selected company ID
			selectedEmployee: "", // Selected employee ID
			taskTimeChart: null, // Chart.js instance
		};
	},
	computed: {
		filteredTaskTimeData() {
			// Filter task time data based on company and employee
			return this.taskTimeData.filter(
				(task) =>
					!this.selectedEmployee || task.assignee_id === this.selectedEmployee
			);
		},
	},
	methods: {
		async updateCompanyData() {
			await this.fetchTaskTimeData(this.selectedCompany);
			this.fetchEmployees(this.selectedCompany);
			if (this.selectedCompany) {
				this.plotChart(this.taskTimeData, "Company Tasks");
			}
		},
		async updateEmployeeData() {
			if (this.selectedEmployee) {
				await this.fetchTaskTimeData(this.selectedCompany);
				this.plotChart(this.filteredTaskTimeData, "Employee Tasks");
			} else {
				this.updateCompanyData(); // Fallback to company-wide if no employee selected
			}
		},
		timeStringToMinutes(timeString) {
			const [hours, minutes] = timeString.split(":").map(Number);
			return hours * 60 + minutes;
		},
		plotChart(data, chartTitle) {
			const taskNames = data.map((task) => task.code_name);
			const times = data.map((task) =>
				this.timeStringToMinutes(task.tracked_time)
			);

			if (this.taskTimeChart) {
				this.taskTimeChart.destroy(); // Destroy old chart instance if it exists
			}

			this.taskTimeChart = new Chart(document.getElementById("taskTimeChart"), {
				type: "bar",
				data: {
					labels: taskNames,
					datasets: [
						{
							label: chartTitle,
							data: times,
							backgroundColor: "rgba(75, 192, 192, 0.2)",
							borderColor: "rgba(75, 192, 192, 1)",
							borderWidth: 1,
						},
					],
				},
				options: {
					indexAxis: "y",
					responsive: true,
					scales: {
						y: {
							beginAtZero: true,
							title: {
								display: true,
								text: "Tasks",
								color: "#f0f0f0",
							},
							ticks: {
								color: "#f0f0f0",
							},
						},
						x: {
							title: {
								display: true,
								text: "Time Tracked (minutes)",
								color: "#f0f0f0",
							},
							ticks: {
								color: "#f0f0f0",
							},
						},
					},
				},
			});
		},
		async fetchCompanies() {
			this.companies = await getAllCompanies();
		},
		async fetchEmployees(company_id) {
			this.employees = await getEmployees(company_id);
		},
		async fetchTaskTimeData(company_id) {
			this.taskTimeData = await fetchAllTasks(company_id);
		},
	},
	async created() {
		await this.fetchCompanies();
	},
};
</script>

<style scoped>
.analytics-container {
	max-width: 1000px;
	margin: 0 auto;
	padding: 20px;
}

.filters {
	display: flex;
	gap: 20px;
	margin-bottom: 20px;
}

.filters label {
	display: flex;
	flex-direction: column;
	font-size: 14px;
}

select {
	padding: 8px 12px;
	border-radius: 4px;
	border: 1px solid #ddd;
}

.chart-container {
	margin-top: 30px;
}
</style>
