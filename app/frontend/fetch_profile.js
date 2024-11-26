async function fetchProfile() {
	// Extract the userId from the URL query string
	const urlParams = new URLSearchParams(window.location.search);
	const userId = urlParams.get("userId");

	if (!userId) {
		document.getElementById("profile").innerHTML =
			"<p>No user ID found in the URL.</p>";
		return;
	}

	const profileContainer = document.getElementById("profile");
	profileContainer.innerHTML = '<p class="loading">Loading...</p>'; // Display loading message

	try {
		// send help
		const response = await fetch(`http://127.0.0.1:8000/api/profile/${userId}`); // Your FastAPI backend URL
		if (!response.ok) {
			throw new Error("Failed to fetch user profile");
		}
		const data = await response.json();

		// Clear the loading message
		profileContainer.innerHTML = "";

		// User Info Section
		const userSection = document.createElement("div");
		userSection.classList.add("section");
		userSection.innerHTML = `
            <h2>User Info</h2>
            <p><strong>Name:</strong> ${data.user.name}</p>
            <p><strong>Email:</strong> ${data.user.email}</p>
        `;

		// Tasks Section
		const tasksSection = document.createElement("div");
		tasksSection.classList.add("section");
		tasksSection.innerHTML = "<h2>Tasks</h2>";

		const taskList = document.createElement("ul");
		taskList.classList.add("task-list");
		data.tasks.forEach((task) => {
			const taskItem = document.createElement("li");
			taskItem.classList.add(task.status.toLowerCase().replace(" ", "-")); // Adds class for styling
			taskItem.innerHTML = `
                <strong>${task.code_name}</strong> - Status: ${task.status}
            `;
			taskList.appendChild(taskItem);
		});
		tasksSection.appendChild(taskList);

		// Company Section
		const companySection = document.createElement("div");
		companySection.classList.add("section");
		companySection.innerHTML = `
            <h2>Company</h2>
            <p><strong>Company Name:</strong> ${data.company.company_name}</p>
        `;

		// Role Section
		const roleSection = document.createElement("div");
		roleSection.classList.add("section");
		roleSection.innerHTML = `
            <h2>Role</h2>
            <p><strong>Role Name:</strong> ${data.role.role_name}</p>
        `;

		// Append all sections to the profile container
		profileContainer.appendChild(userSection);
		profileContainer.appendChild(tasksSection);
		profileContainer.appendChild(companySection);
		profileContainer.appendChild(roleSection);
	} catch (error) {
		profileContainer.innerHTML = `<p>Error: ${error.message}</p>`;
	}
}

window.onload = fetchProfile;
