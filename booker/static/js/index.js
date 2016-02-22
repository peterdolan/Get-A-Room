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

function getToday(){
	var today = new Date();
	var dd = today.getDate();
	var mm = today.getMonth()+1; //January is 0!
	var yyyy = today.getFullYear();
	if(dd<10) {
	    dd='0'+dd
	} 
	if(mm<10) {
	    mm='0'+mm
	} 
	today = mm+'/'+dd+'/'+yyyy;
	return today;
}

function checkTimeValues() {
	var date = document.getElementById("id_date");
	date.onchange = function() {
		var options = document.getElementsByTagName("option");
		var today = getToday();		
		if(today === date.value){
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

function convertTimeToMinutes(hour){
	return hour * 60;
}

function checkDurationValues() {
	var cutOffTime = convertTimeToMinutes(2); // Put 150 for 2:30 am, 18.5* 60 for 6:30 pm etc
	var restartTime = convertTimeToMinutes(8);
	console.log(cutOffTime);
	var time = document.getElementById("id_time");
	time.onchange = function() {
		var curTime = document.getElementById("id_time");
		var options = document.getElementsByTagName("option");
		for(var i = 37; i < 43;i++){
			var until = (+(curTime.value * 30) + +options[i].value)%1440;
			if(until > cutOffTime && until < restartTime){
				options[i].style.display = 'none';
			} else {
				options[i].style.display = 'inline';
			}
		}
	}
}
