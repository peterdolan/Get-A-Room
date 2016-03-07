/* Javascript */
$(document).ready(function () {
	var csrftoken = Cookies.get('csrftoken');
	function csrfSafeMethod(method) {
		// these HTTP methods do not require CSRF protection
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
    		if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        		xhr.setRequestHeader("X-CSRFToken", csrftoken);
    		}
		}
	});


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
	// console.log(value);
	// console.log(room);
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
	var value = document.getElementById("calview_room");
	var room = value.options[value.selectedIndex].value;
	swal.withForm({
	    title: 'Make a reservation \non ' + grabDate(date) + '\n at '+ grabTime(date) + '\n in ' + room + '?',
	    text: 'Make reservations for your friends, teammates, etc.',
	    showCancelButton: true,
	    confirmButtonColor: '#FED100',
	    confirmButtonText: 'Make Reservation',
	    closeOnConfirm: false,   
		showLoaderOnConfirm: true,
	    formFields: [
			{ id: 'description', placeholder: 'Add a description for your booking' },
			{ id: 'length', placeholder: 'Duration of your booking' },
		]
		}, 
		function (isConfirm) {
			if (isConfirm) {
				// group_name = this.swalForm.name;
				$.ajax({
					url : "../post_reservation/",
					type: "POST",
					data : {room:room, date:getFormattedDate(date), time:getFormattedTime(date), duration:this.swalForm.length},
				});
				setTimeout(function(){ 
					swal({
						title: "Successfully created " + "res" + "!",
						type: "success",
					},
					function() {
						// location.replace("/booker/profile/?tab=reservation");
						location.replace("/booker/calendar/");
					});
    			}, 2000);
		    }
		}
	);
	calendar_refresh();
}

function grabTime(date) {
	var toReturn = "";
	var ampm = "";
	var hour = date.getHours()%12;
	if(hour == 0) {
		hour = 12;
	}
	if(date.getHours() < 12) {
		ampm = "AM";
	}
	else {
		ampm = "PM";
	}
	var halfhr = "";
	if(date.getMinutes() == 30){
		halfhr = "30";
	}
	else {
		halfhr = "00";
	}
	toReturn = hour + ":" + halfhr + " " + ampm;
	return toReturn;
}

//the following three helper functions were found on StackOverflow
function grabDate(date) {
	var monthNames = ["January", "February", "March", "April", "May", "June",
  		"July", "August", "September", "October", "November", "December"
	];
	return monthNames[date.getMonth()] + " " + ordinal_suffix_of(date.getDate());
}

function ordinal_suffix_of(i) {
    var j = i % 10,
        k = i % 100;
    if (j == 1 && k != 11) {
        return i + "st";
    }
    if (j == 2 && k != 12) {
        return i + "nd";
    }
    if (j == 3 && k != 13) {
        return i + "rd";
    }
    return i + "th";
}

function getFormattedDate(date) {
	var year = date.getFullYear();
	var month = (1 + date.getMonth()).toString();
	month = month.length > 1 ? month : '0' + month;
	var day = date.getDate().toString();
	day = day.length > 1 ? day : '0' + day;
	return month + '/' + day + '/' + year;
}

function getFormattedTime(date) {
	return (60*date.getHours() + date.getMinutes())/30;
}

function getCurrentRoom(){
	var value = document.getElementById("calview_room");
    var room = value.options[value.selectedIndex].value;
	document.getElementById('aggregator_name').innerHTML = room;
}
getCurrentRoom();

