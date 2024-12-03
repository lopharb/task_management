import { createRouter, createWebHistory } from "vue-router";
import TaskList from "../components/TaskList.vue"; // Adjust the path based on your component location
import UserProfile from "@/components/UserProfile.vue";

const routes = [
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
	// You can define additional routes here
];

const router = createRouter({
	history: createWebHistory(),
	routes,
});

export default router;
