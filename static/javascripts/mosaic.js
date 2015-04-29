$(document).ready(function () {
	var ref = new Firebase("https://facebook-mosaic.firebaseio.com");
	var progress = ref.child("progress").child(userID);
	$("#progressbar").progressbar({
		max: false,
		value: 0
	});
	progress.on("value", function (snapshot) {
		var status = snapshot.val();
		$("#message").html(status.message);
		$("#progressbar").progressbar("option", "max", status.max);
		$("#progressbar").progressbar("option", "value", status.val);
	});
});