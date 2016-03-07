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
	//     dayClick: function(date, jsEvent, view) {

	//         alert('Clicked on: ' + date.format());

	//         alert('Coordinates: ' + jsEvent.pageX + ',' + jsEvent.pageY);

	//         alert('Current view: ' + view.name);

	//         // change the day's background color just for fun
	//         $(this).css('background-color', 'red');

	//         make_reservation(date);
	//     }
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
	getCurrentRoom();
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
	 	events: 'eventsfeed/'+room,
	 	dayClick: make_reservation
	});
	getCurrentRoom();
}

function make_reservation(date) {
	console.log("Date is: " + date);
	swal.withForm({
	    title: 'Make a reservation!',
	    text: 'Make reservations for your friends, teammates, etc.',
	    showCancelButton: true,
	    confirmButtonColor: '#FED100',
	    confirmButtonText: 'Make Reservation',
	    closeOnConfirm: false,   
		showLoaderOnConfirm: true,
	    formFields: [
			{ id: 'name', placeholder: 'Name your group' },
			{ id: 'description', placeholder: 'Add a description for your group' },
			{ id: 'duration', placeholder: 'Duration of your booking' },
		]
		}, 
		function (isConfirm) {
			if (isConfirm) {
				group_name = this.swalForm.name;
				if ($.inArray(group_name, group_list) === -1) {
					$.ajax({
						url : "/booker/create_group/",
						type: "POST",
						data : {group_name:group_name},
					});
					setTimeout(function(){ 
						swal({
							title: "Successfully created " + group_name + "!",
							type: "success",
						},
						function() {
							location.replace("/booker/profile/?tab=group");
						});   
	    			}, 2000);
				} else {
					setTimeout(function(){ 
						swal("Whoops! A group called " + group_name + " already exists! Please use another name.");   
		    		}, 2000);
				}
		    }
		}
	);
}

function getCurrentRoom(){
	var value = document.getElementById("calview_room");
    var room = value.options[value.selectedIndex].value;
	document.getElementById('aggregator_name').innerHTML = room;
}
getCurrentRoom();

