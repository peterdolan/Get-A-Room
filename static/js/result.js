function updateActiveRoom(name) {
	var old_rooms = document.getElementsByClassName("list-group-item active");
	var room = document.getElementById(name);

	if (room === old_rooms[0]) {
		room.className = "list-group-item";
	}else {
		if (old_rooms.length !== 0) {
			old_rooms[0].className = "list-group-item";
		}
		room.className = "list-group-item active";
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
