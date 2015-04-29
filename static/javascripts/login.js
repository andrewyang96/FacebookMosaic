function statusChangeCallback(response) {
	console.log('statusChangeCallback');
	console.log(response);
	// The response object is returned with a status field that lets the
	// app know the current login status of the person.
	// Full docs on the response object can be found in the documentation
	// for FB.getLoginStatus().
	if (response.status === 'connected') {
		// Logged into your app and Facebook.
		console.log("Logged in!");
	} else if (response.status === 'not_authorized') {
		// The person is logged into Facebook, but not your app.
		console.log("Please login.");
	} else {
		// The person is not logged into Facebook, so we're not sure if
		// they are logged into this app or not.
		console.log("Please login.");
	}
}

function checkLoginState() {
	FB.getLoginStatus(function(response) {
		statusChangeCallback(response);
	});
}