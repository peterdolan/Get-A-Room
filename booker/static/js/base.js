$(document).ready(function() {
	jQuery.get("/booker/user/",function(user_obj) {
		user_picture = user_obj;
		if (user_picture !== 'None') {
			$('.profile-thumbnail').css('background-image','url(/static/'+user_picture+')');
		} else {
			$('.profile-thumbnail').css('background-image','url(/static/images/mag_question.png');
			$('.profile-thumbnail').css('border','solid 1px black');
		}
		
	});
});

var user_picture;