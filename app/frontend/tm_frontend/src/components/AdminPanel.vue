<template>
	<header>
		<HeaderComponent />
	</header>
	<div class="admin-panel">
		<header>
			<h1>Administration Panel</h1>
		</header>
		<nav class="admin-tabs">
			<button
				v-for="tab in tabs"
				:key="tab"
				@click="currentTab = tab"
				:class="{ active: currentTab === tab }"
			>
				{{ tab }}
			</button>
		</nav>
		<div class="admin-content">
			<template v-if="currentTab === 'Users'">
				<h2>Manage Users</h2>
				<UserManagement />
			</template>
			<template v-else-if="currentTab === 'Companies'">
				<h2>Manage Companies</h2>
				<CompanyManagement />
			</template>
		</div>
	</div>
</template>

<script>
import UserManagement from "./UserManagement.vue";
import CompanyManagement from "./CompanyManagement.vue";
import HeaderComponent from "./HeaderComponent.vue";
export default {
	name: "AdminPanel",
	data() {
		return {
			tabs: ["Users", "Companies"],
			currentTab: "Users",
		};
	},
	components: {
		UserManagement,
		CompanyManagement,
		HeaderComponent,
	},
};
</script>

<style scoped>
.admin-panel {
	padding: 20px;
}

header {
	text-align: center;
	margin-bottom: 20px;
}

.admin-tabs {
	display: flex;
	justify-content: center;
	margin-bottom: 20px;
}

.admin-tabs button {
	background: #f7f7f7;
	border: 1px solid #ddd;
	padding: 10px 20px;
	cursor: pointer;
}

.admin-tabs button.active {
	background: #007bff;
	color: white;
	border-color: #0056b3;
}

.admin-content {
	padding: 20px;
	background: #ffffff;
	border: 1px solid #ddd;
	border-radius: 4px;
}
</style>
