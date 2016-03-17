$(document).ready(function () {
	activePane = 'time';
	rightArrowSrc = $('#rightarrowlink img').attr('src');
	$("#leftarrow").hide();
	$('#id_date').val(getToday());
	var date = document.getElementById("id_date");
	verifyDate();

	addClasses();
    checkTimeValues();
    checkDurationValues();
});

var rightArrowSrc;
var activePane;
var paneKey = {"time":0,"amenities":1,"location":2};
var paneKeyReverse = {0:"time",1:"amenities",2:"location"};

function addClasses() {
	var group = document.getElementById("id_group");
	if (group !== null) {
		group.className = "form-control";
	}

	var date = document.getElementById("id_date");
	date.className = "form-control";

	var time = document.getElementById("id_time");
	time.className = "form-control";

	var duration = document.getElementById("id_duration");
	duration.className = "form-control";

	var capacity = document.getElementById("id_capacity");
	capacity.className = "form-control";

	var weekly = document.getElementById("id_weekly");
	if (weekly !== null) {
		weekly.className = "form-control";
		weekly.onchange = function() {
			if (nmeetings.style.display === "none") {
				nmeetings.style.display = "block";
			}else {
				nmeetings.style.display = "none";
			}
		};
	}

	var nmeetings = document.getElementById("id_nmeetings");
	if (nmeetings !== null) {
		nmeetings.className = "form-control";
		nmeetings.max = nmeetings.value;
		if (!weekly.checked) {
			nmeetings.style.display = "none";
		}
	}

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

function verifyDate(){
	var date = document.getElementById("id_date");
	var options = document.getElementsByTagName("option");
	var today = getToday();	
	if(today === date.value){
		var startToday = new Date();
		var year = startToday.getFullYear();
		var month = startToday.getMonth();
		var day = startToday.getDate();
		var finalNewDate = new Date(year, month, day, 0, 0, 0, 0);
		var curDayStart = finalNewDate.valueOf()/1000;
		var cur = Date.now();
		var available = true;
		for(var i = 0; i < 37; i++){
			if((curDayStart + (options[i].value * 1800)) < cur/1000){
				options[i].style.display = 'none';
			} else {
				if(available){
					if(i < 5){
						$('#id_time').val(i);
					} else {
						$('#id_time').val(i + 11);
					}
					available = false;
				}
			}
		}
	} else {
		for(var i = 0; i < 37; i++){	
			options[i].style.display = 'inline';
		}
	}
}

function checkTimeValues() {
	var date = document.getElementById("id_date");
	date.onchange = function() {
		verifyDate()
	}
}

function convertTimeToMinutes(hour){
	return hour * 60;
}

function checkDurationValues() {
	var cutOffTime = convertTimeToMinutes(2); // Put 2 for 2am, 1.5 for 1:30 etc
	var restartTime = convertTimeToMinutes(8);
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

function paneShift(oldPane,dirOut,newPane,dirIn,arrowClick) {
	var animationEnd = 'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend';
	console.log($('#'+oldPane+'-pill'));
	console.log($('#'+newPane+'-pill'));
	var nextRightPaneId = paneKey[newPane] + 1;
	var nextLeftPaneId = paneKey[newPane] - 1;
	if (nextLeftPaneId < 0) {
			$("#leftarrow").hide();
	}
	if (arrowClick) {
		$('#'+oldPane+'-pill').removeClass('active');
		$('#'+newPane+'-pill').addClass('active');
	}
	$("#"+newPane).addClass('animated fadeIn'+dirIn).one(animationEnd, function() {
		$("#"+newPane).removeClass('animated fadeIn'+dirIn);
		if (nextRightPaneId >= Object.keys(paneKey).length) {
			$("#rightarrowlink").replaceWith($('<label for="submit-form" id="rightarrowlink"><img alt="Right" /></label>'));
			$("#rightarrowlink img").attr('src',rightArrowSrc);
		} else {
			var nextRightPane = paneKeyReverse[paneKey[newPane]+1];
			$("#rightarrowlink").replaceWith($('<a id="rightarrowlink" data-toggle="pill" onclick="transitionPane(1)"><img alt="Right" /></a>'));
			$("#rightarrowlink").attr("href","#"+nextRightPane);
			$("#rightarrowlink img").attr('src',rightArrowSrc);
		}

		if (nextLeftPaneId < 0) {
			$("#leftarrow").hide();
		} else {
			var nextLeftPane = paneKeyReverse[paneKey[newPane]-1];
			$("#leftarrowlink").attr("href","#"+nextLeftPane);
			$("#leftarrow").show();
			console.log($("#leftarrow"));
		}	
	});
}

function transitionPane(newPane) {
	console.log("New Pane", newPane);
	if (newPane !== activePane) {
		var oldPaneId = paneKey[activePane];
		var newPaneId;
		var arrowClick = false;
		if (Number.isInteger(newPane)) {
			newPaneId = oldPaneId + newPane;
			arrowClick = true;
		} else {
			newPaneId = paneKey[newPane];
		}
		console.log(oldPaneId);
		console.log(newPaneId);
		activePane = paneKeyReverse[oldPaneId];
		newPane = paneKeyReverse[newPaneId];
		console.log(activePane);
		console.log(newPane);
		if (oldPaneId < newPaneId) {
			paneShift(activePane,"Left",newPane,"Right",arrowClick);
		} else {
			paneShift(activePane,"Right",newPane,"Left",arrowClick);
		}
		activePane = newPane;
	}
}
