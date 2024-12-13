import { createRouter, createWebHistory } from "vue-router";
import TaskList from "../components/TaskList.vue";
import UserProfile from "@/components/UserProfile.vue";
import AllTasks from "@/components/AllTasks.vue";
import LoginPage from "@/components/LoginPage.vue";
import RegisterPage from "@/components/RegisterPage.vue";
import Landing from "@/components/Landing.vue";
import AdminPanel from "@/components/AdminPanel.vue";
import TaskAnalytics from "@/components/TaskAnalytics.vue";
const routes = [
	{
		path: "/",
		name: "Landing",
		component: Landing,
	},
	{
		path: "/tasks",
		name: "TaskList",
		component: TaskList,
	},
	{
		path: "/users",
		name: "UserProfile",
		component: UserProfile,
	},
	{
		path: "/tasks/browse",
		name: "AllTasks",
		component: AllTasks,
	},
	{
		path: "/login",
		name: "LoginPage",
		component: LoginPage,
	},
	{
		path: "/register",
		name: "RegisterPage",
		component: RegisterPage,
	},
	{
		path: "/administrate",
		name: "AdminPanel",
		component: AdminPanel,
	},
	{
		path: "/analytics",
		name: "TaskAnalytics",
		component: TaskAnalytics,
	},
];

const router = createRouter({
	history: createWebHistory(),
	routes,
});

export default router;
