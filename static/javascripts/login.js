function statusChangeCallback(response) {
	// console.log(response);
	userID = response.authResponse.userID;
	// The response object is returned with a status field that lets the
	// app know the current login status of the person.
	// Full docs on the response object can be found in the documentation
	// for FB.getLoginStatus().
	if (response.status === 'connected') {
		// Logged into your app and Facebook.
		$("#fb-root").html("<h3>Great! Your mosaic is being created.</h3><script src='/static/javascripts/mosaic.js'></script>");
	}
}

function checkLoginState() {
	FB.getLoginStatus(function(response) {
		statusChangeCallback(response);
	});
}