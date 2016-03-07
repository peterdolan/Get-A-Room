/* Javascript */
$(document).ready(function () {
	getBuildings();
	calendar_refresh();
	// var date = new Date();
	// var d = date.getDate();
	// var m = date.getMonth();
	// var y = date.getFullYear();
	
	// var value = document.getElementById("calview_bldg");
	// var building = value.options[value.selectedIndex].value;
	// console.log(building);
	var h = window.innerHeight;
	// console.log("Height is " + h);
	var newh =  $('header').height();
	// console.log("height of obj is " + newh);


	// $('#calendar').fullCalendar({
	// 	header: {
	// 		left: 'prev,next today',
	// 		center: 'title',
	// 		right: 'agendaWeek,agendaDay'
	// 	},
	// 	start: '08:00',
	// 	end: '02:00',
	// 	allDaySlot: false,
	// 	height: 1200,
	// 	editable: true,
	// 	defaultView: 'agendaWeek',
	// 	eventColor: '#fed100',
	// 	eventTextColor: '#222222',
	//  	events: 'eventsfeed/'+building
	// });
});

var buildings_map;

function getBuildings() {
	jQuery.get("/booker/buildings",function(building_list) {
		buildings_map = JSON.parse(building_list);
		if(Object.keys(buildings_map).length > 0) {
			var select = document.getElementById("calview_bldg");
			var building = select.options[select.selectedIndex].value;
			$.each(buildings_map[building], function(key, value) {
		    	$('#calview_room')
		    		.append($("<option></option>")
		    		.attr("value",value)
		    		.text(value));
			});
			calendar_refresh();
		}
	});
}

function building_submit() {
    var select = document.getElementById("calview_bldg");
    var building = select.options[select.selectedIndex].value;
    // console.log(building);

    $('#calview_room')
    		.find('option')
    		.remove()
    		.end()

    $.each(buildings_map[building], function(key, value) {
    	$('#calview_room')
    		.append($("<option></option>")
    		.attr("value",value)
    		.text(value));
	});
	calendar_refresh();
}

function calendar_refresh() {
	var value = document.getElementById("calview_room");
	var room = value.options[value.selectedIndex].value;
	console.log(value);
	console.log(room);
	$('#calendar').remove()
	var new_div = document.createElement("div");
	new_div.id = 'calendar';
	$('.container')[0].appendChild(new_div);
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
	 	events: 'eventsfeed/'+room
	});
}

/*function notEmpty(){
	var value = document.getElementById("id_building");
    var building = value.options[value.selectedIndex].value;
	document.getElementById('aggregator_name').innerHTML = building;
}

notEmpty();        
document.getElementById("building_form").onsubmit = notEmpty;
*/
