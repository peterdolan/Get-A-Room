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
	
	var h = window.innerHeight;
	var newh =  $('header').height();
});

var buildings_map;
var reservations_list;

// function mycomparator(a,b) {
// 	return 
// }

function getBuildings() {
	jQuery.get("/booker/buildings",function(building_list) {
		buildings_map = JSON.parse(building_list);
		if(Object.keys(buildings_map).length > 0) {
			var select = document.getElementById("calview_bldg");
			var building = select.options[select.selectedIndex].value;
			var rooms = buildings_map[building];
			$.each(rooms.sort(), function(key, value) {
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
    var rooms = buildings_map[building];
    $.each(rooms.sort(), function(key, value) {
    	$('#calview_room')
    		.append($("<option></option>")
    		.attr("value",value)
    		.text(value));
	});
	calendar_refresh();
	getCurrentRoom();
}

function getHeight() {
	var clientHeight;
	if( typeof( window.innerWidth ) == 'number' ) {
	//Non-IE
	clientHeight = window.innerHeight;
	} else if( document.documentElement && ( document.documentElement.clientWidth || document.documentElement.clientHeight ) ) {
	//IE 6+ in 'standards compliant mode'
	clientHeight = document.documentElement.clientWidth;
	return document.documentElement.clientHeight;
	} else if( document.body && ( document.body.clientWidth || document.body.clientHeight ) ) {
	//IE 4 compatible
	clientHeight = document.body.clientHeight;
	}
	clientHeight -= $('.header').outerHeight(true);
	clientHeight -= $('.CalendarTitle').outerHeight(true);
	clientHeight -= ($('.cal_container').outerHeight(true) - $('.cal_container').height());
	return clientHeight-20;
}

function calendar_refresh() {
	var value = document.getElementById("calview_room");
	var room = value.options[value.selectedIndex].value;
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
		views:
        {
        	agendaWeek: {
     //        	businessHours: {
     //    			start: '02:00',
					// end: '08:00',
					// dow: [1,2,3,4,5,6,7]
     //    		},
        	}
        },
		allDaySlot: false,
		height: getHeight(),
		editable: false,
		defaultView: 'agendaWeek',
		eventColor: '#fed100',
		eventTextColor: '#222222',
	 	events: 'eventsfeed/'+room,
	 	dayClick: make_reservation
	});
	getCurrentRoom();
}

function make_reservation(date) {
	var today = new Date();
	if(date > today) {
		var value = document.getElementById("calview_room");
		var room = value.options[value.selectedIndex].value;
		$.ajax({
			url : "get_closest_reservation/",
			type: "POST",
			data : {room:room, date:date},
			success : function(reservation_time) {
				res_info = JSON.parse(reservation_time);
				var d = new Date(res_info['year'],res_info['month']-1,res_info['day'],res_info['hour'],res_info['minute'],res_info['second']);
				var options = [
						{value: '30', text: '30 minutes'},
						{value: '60', text: '1 hour'},
						{value: '90', text: '1 hour and a half'},
						{value: '120', text: '2 hours'},
						{value: '150', text: '2 and a half hours'},
						{value: '180', text: '3 hours'}
					];
				var diff = getFormattedTime(d) - getFormattedTime(date);
				if(getFormattedDate(d) == getFormattedDate(date) && ((getFormattedTime(d) - getFormattedTime(date)) < 6)) {
					options = options.slice(0,diff);
				}
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
						{ id: 'length', type: 'select', options: options }
					]
					}, 
					function (isConfirm) {
						if (isConfirm) {
							var desc;
							if (this.swalForm.description == '') {
								desc = "MyEvent!";
							}
							else {
								desc = this.swalForm.description;
							}
							$.ajax({
								url : "../post_reservation/",
								type: "POST",
								data : {room:room, date:getFormattedDate(date), time:getFormattedTime(date), nmeetings:1, duration:this.swalForm.length, description:desc},
							});
							setTimeout(function(){ 
								swal({
									title: "Successfully created reservation!",
									type: "success",
								},
								function() {
									location.replace("/booker/calendar/");
								});
			    			}, 2000);
					    }
					}
				);
				calendar_refresh();
			}
		});	
	}
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
}
getCurrentRoom();

