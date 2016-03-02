/* Javascript */
$(document).ready(function () {
	var date = new Date();
	var d = date.getDate();
	var m = date.getMonth();
	var y = date.getFullYear();
	
	var value = document.getElementById("id_building");
	var building = value.options[value.selectedIndex].value;
	console.log(building);
	var h = window.innerHeight;
	console.log("Height is " + h);
	var newh =  $('header').height();
	console.log("height of obj is " + newh);


	$('#calendar').fullCalendar({
		header: {
			left: 'prev,next today',
			center: 'title',
			right: 'agendaWeek,agendaDay'
		},
		start: '08:00',
		end: '02:00',
		allDaySlot: false,
		height: 1200,
		editable: true,
		defaultView: 'agendaWeek',
		eventColor: '#fed100',
		eventTextColor: '#222222',
	 	events: 'eventsfeed/'+building
	});
});

/*function notEmpty(){
	var value = document.getElementById("id_building");
    var building = value.options[value.selectedIndex].value;
	document.getElementById('aggregator_name').innerHTML = building;
}

notEmpty();        
document.getElementById("building_form").onsubmit = notEmpty;
*/
