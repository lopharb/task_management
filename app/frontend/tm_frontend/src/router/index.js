import { createRouter, createWebHistory } from "vue-router";
import TaskList from "../components/TaskList.vue";
import UserProfile from "@/components/UserProfile.vue";
import AllTasks from "@/components/AllTasks.vue";
import LoginPage from "@/components/LoginPage.vue";
import RegisterPage from "@/components/RegisterPage.vue";
import Landing from "@/components/Landing.vue";

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
];

const router = createRouter({
	history: createWebHistory(),
	routes,
});

export default router;
