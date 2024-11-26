async function login() {
	const email = document.getElementById("email").value;
	const password = document.getElementById("password").value;
	const errorElement = document.getElementById("error");

	// Reset previous error message
	errorElement.innerHTML = "";

	if (!email || !password) {
		errorElement.innerHTML = "Please fill in both fields.";
		return;
	}

	// Prepare the data to send in the request
	const credentials = { email, password };
	console.log(JSON.stringify(credentials));
	try {
		// Send POST request to the API endpoint
		const response = await fetch("http://127.0.0.1:8000/api/login/", {
			// Replace with your actual API endpoint
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify(credentials),
		});

		const data = await response.json();

		if (!response.ok) {
			// Display error message if login failed
			errorElement.innerHTML =
				data.error || "Login failed. Please check your credentials.";
		} else {
			// If login successful, redirect to profile page with user ID in URL
			const userId = data.user_id; // Assuming the response contains user_id
			window.location.href = `profile.html?userId=${userId}`;
		}
	} catch (error) {
		// Handle any other errors (e.g., network issues)
		errorElement.innerHTML = "An error occurred. Please try again later.";
		console.error(error);
	}
}
