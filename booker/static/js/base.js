$(document).ready(function() {
	jQuery.get("/booker/user/",function(user_obj) {
		user_picture = user_obj;
		console.log(user_obj);
		$('.profile-thumbnail').css('background-image','url(/static/'+user_picture+')');
	});
});

var user_picture;