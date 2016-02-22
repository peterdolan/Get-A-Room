function addClasses() {
	var date = document.getElementById("id_date");
	date.className = "form-control";

	var time = document.getElementById("id_time");
	time.className = "form-control";

	var duration = document.getElementById("id_duration");
	duration.className = "form-control";

	var capacity = document.getElementById("id_capacity");
	capacity.className = "form-control";

	var projector = document.getElementById("id_projector");
	projector.className = "form-control";

	var whiteboard = document.getElementById("id_whiteboard");
	whiteboard.className = "form-control";

	var windows = document.getElementById("id_windows");
	windows.className = "form-control";

	var area = document.getElementById("id_area");
	area.className = "form-control";

	var windows = document.getElementById("id_windows");
	windows.className = "form-control";

	var flexible = document.getElementById("id_flexible");
	flexible.className = "form-control";
}

function checkTimeValues() {
	var date = document.getElementById("id_date");
	console.log("We back");
	date.onchange = function() {
		var options = document.getElementsByTagName("option");
		var today = getToday();		
		if(today === date.value){
			console.log("We back");
			var startToday = new Date();
			var year = startToday.getUTCFullYear();
 			var month = startToday.getUTCMonth();
 			var day = startToday.getUTCDate();
 			var finalNewDate = new Date(year, month, day, 0, 0, 0, 0);
 			var curDayStart = finalNewDate.valueOf()/1000;

			var cur = Date.now();
			for(var i = 0; i < 37; i++){
				if((curDayStart + (options[i].value * 1800)) < cur/1000){
					options[i].style.display = 'none';
				}
			}
		} else {
			for(var i = 0; i < 37; i++){	
				options[i].style.display = 'inline';
			}
		}
	}
}
