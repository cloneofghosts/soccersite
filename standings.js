$(document).ready(function() {
	$('#standings').DataTable({
		searching: false,
		order: [[5, "desc"], [1, "desc"], [8, "desc"]],
		pageLength: 25,
		lengthChange: false,
	});
});
