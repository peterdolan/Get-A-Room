/* Javascript */
$(document).ready(function () {
	var date = new Date();
	var d = date.getDate();
	var m = date.getMonth();
	var y = date.getFullYear();

	// var room_info = block.getElementsByTagName("SPAN");
	// var room_name = room_info[0].innerHTML;
	// var input = document.getElementById("room-input");
	// input.value = room_name;
	
	var value = document.getElementById("id_building");
	var building = value.options[value.selectedIndex].value;
	console.log(building);

	$('#calendar').fullCalendar({
		header: {
			left: 'prev,next today',
			center: 'title',
			right: 'agendaWeek,agendaDay'
		},
		editable: true,
		defaultView: 'agendaWeek',
		eventColor: 'blue',
		// eventSources: [
	 //        // your event source
	 //        {
	 //            events: [ // put the array in the `events` property
	 //                {
	 //                    title  : 'Hacking away at new features',
	 //                    start  : '2016-02-28T12:48:15+00:00',
	 //                    end	   : '2016-02-28T14:48:15+00:00',
	 //                    allDay : false
	 //                }
	 //            ]
	 //            // textColor: 'yellow' // an option!
	 //        }
	 //    ]
	 	events: 'eventsfeed/'+building
	});
});