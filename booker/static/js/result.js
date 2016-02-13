function updateActiveRoom(nname) {
	var old_rooms = document.getElementsByClassName("list-group-item active");
	var room = document.getElementById(nname);
	var button = document.getElementById("book-button");

	if (room === old_rooms[0]) {
		room.className = "list-group-item";
		button.className = "btn disabled";
	}else {
		if (old_rooms.length !== 0) {
			old_rooms[0].className = "list-group-item";
		}
		room.className = "list-group-item active";
		button.className = "btn btn-success";
	}
}

function checkIfListsEmpty() {
	var lists = document.getElementsByTagName("UL");
	for (var i = 0; i < lists.length; i++) {
		var lis = lists[i].getElementsByTagName("LI");
		if (lis.length === 0) {
			var new_li = document.createElement("LI");
			new_li.className = "empty";
			var textNode = document.createTextNode("None");
			new_li.appendChild(textNode);
			lists[i].appendChild(new_li);
		}
	}
}

function bookRoom(date, time, duration) {
	var block = document.getElementsByClassName("list-group-item active")[0];
	var room_info = block.getElementsByTagName("SPAN");
	var room_name = room_info[0].innerHTML;
	var input = document.getElementById("room-input");
	input.value = room_name;
    document.forms['param_form'].submit();
}
