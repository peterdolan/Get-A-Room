$(document).ready(function () {
	$(window).bind("beforeunload", function(e) {
		deleted_reservations = document.getElementsByClassName("deleted-reservation");
		
		console.log("Deleted reservations:",deleted_reservations);
	});
});

var delete_called = false;

function updateActiveGroup(nname) {
	console.log("updateActiveGroup being called");
	var old_group = document.getElementsByClassName("list-group-item active");
	var group = document.getElementById(nname);
	var old_button = document.getElementsByClassName("remove-group-button active");
	var button = document.getElementById("remove-group-button "+nname);

	if (group === old_group[0]) {
		group.className = "list-group-item";
		button.className = "remove-reservation-button";
	} else {
		if (old_group.length !== 0) {
			old_group[0].className = "list-group-item";
			old_button[0].className = "remove-group-button"
		}
		group.className = "list-group-item active";
		button.className = "remove-group-button active";
	}
}

function updateActiveReservation(nname) {
	console.log("delete_called is: ", delete_called)
	if(delete_called) {
		delete_called = false;
		return;
	}
	var old_reservation = document.getElementsByClassName("list-group-item active");
	var reservation = document.getElementById(nname);
	var old_button = document.getElementsByClassName("remove-reservation-button active");
	var button = document.getElementById("remove-reservation-button "+nname);

	if (reservation === old_reservation[0]) {
		reservation.className = "list-group-item";
		button.className = "remove-reservation-button";
	} else {
		if (old_reservation.length !== 0) {
			old_reservation[0].className = "list-group-item";
			old_button[0].className = "remove-reservation-button"
		}
		reservation.className = "list-group-item active";
		button.className = "remove-reservation-button active";
	}
}

function removeReservation(nname) {
	delete_called = true;
	nname = "#" + nname;
	// var reservation = document.getElementById(nname);
	$(nname).addClass('deleted-reservation');
	// $('#'+nname)[0].addClass('deleted-reservation');
	// reservation.className += "deleted-reservation";
	$(nname).css("display","none");
	// console.log($(nname)[0]);
	// document.getElementById(nname)
}

function makeContentInactive() {
	console.log("makeContentInactive being called");
	var active_items = document.getElementsByClassName("list-group-item active");
	// console.log(active_items);
	for (var i = 0; i < active_items.length; i++) {
		active_items[i].className = "list-group-item";
	}
	// console.log(active_items);
	var active_buttons = document.getElementsByClassName("remove-reservation-button active");
	for (i = 0; i < active_buttons.length; i++) {
		active_buttons[i].className = "remove-reservation-button";
	}
	active_buttons = document.getElementsByClassName("remove-group-button active");
	for (i = 0; i < active_buttons.length; i++) {
		active_buttons[i].className = "remove-group-button";
	}
	active_buttons = document.getElementsByClassName("remove-org-button active");
	for (i = 0; i < active_buttons.length; i++) {
		active_buttons[i].className = "remove-org-button";
	}
}