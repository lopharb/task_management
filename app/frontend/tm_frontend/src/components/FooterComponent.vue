<template>
	<footer class="site-footer">
		<div>
			<p>
				&copy; {{ new Date().getFullYear() }} Task Management. All rights
				reserved.
			</p>
		</div>
		<div class="footer-links">
			<a href="/privacy-policy" class="footer-item">Privacy Policy</a>
			<a href="/terms-of-service" class="footer-item">Terms of Service</a>
			<a href="/contact-us" class="footer-item">Contact Us</a>
		</div>
	</footer>
</template>

<script>
export default {
	name: "FooterComponent",
};
</script>

<style scoped>
.site-footer {
	position: relative;
	bottom: 0;
	max-width: 100%;
	padding: 15px 30px;
	background: #333;
	color: white;
	text-align: center;
	background: #53718f;
}

.footer-links {
	margin-top: 10px;
	display: flex;
	justify-content: center;
	gap: 20px;
}

.footer-item {
	text-decoration: none;
	color: #bbb;
	font-size: 0.9em;
}

.footer-item:hover {
	color: white;
	text-decoration: underline;
}
</style>
