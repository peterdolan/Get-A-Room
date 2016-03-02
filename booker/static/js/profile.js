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

	getGroupList();
	getOrgList();

	$(window).bind("beforeunload", function(e) {
		deleted_reservations = document.getElementsByClassName("deleted-reservation");
		deleted_reservation_ids = [];
		for (var i=0; i<deleted_reservations.length; i++) {
			stripped_id = deleted_reservations[i].id.substring("reservation".length);
			deleted_reservation_ids.push(stripped_id);
		}
		unjoined_groups = document.getElementsByClassName("deleted-group");
		unjoined_groups_ids = [];
		for (i=0; i<unjoined_groups.length; i++) {
			stripped_id = unjoined_groups[i].id.substring("group".length);
			unjoined_groups_ids.push(stripped_id);
		}
		unjoined_orgs = document.getElementsByClassName("deleted-org");
		unjoined_orgs_ids = [];
		for (i=0; i<unjoined_orgs.length; i++) {
			stripped_id = unjoined_orgs[i].id.substring("org".length);
			unjoined_orgs_ids.push(stripped_id);
		}

		$.ajax({
			url : "/booker/delete_profile_info/",
			type: "POST",
			data : {reservation_ids:JSON.stringify(deleted_reservation_ids),
					group_ids:JSON.stringify(unjoined_groups_ids),
					org_ids:JSON.stringify(unjoined_orgs_ids),
				}
		});
	});
});

function getGroupList() {
	jQuery.get("/booker/get_group_list/",function(group_names) {
		group_list = JSON.parse(group_names)
	});
}

function getOrgList() {
	jQuery.get("/booker/get_org_list/",function(org_names) {
		org_list = JSON.parse(org_names)
	});
}

var group_list;
var org_list;
var delete_called = false;

function updateActiveOrg(nname) {
	if(delete_called) {
		delete_called = false;
		return;
	}
	var old_org = document.getElementsByClassName("list-group-item active");
	var org = document.getElementById(nname);
	var old_button = document.getElementsByClassName("remove-org-button active");
	var button = document.getElementById("remove-org-button "+nname);

	if (org === old_org[0]) {
		org.className = "list-group-item";
		button.className = "remove-org-button";
	} else {
		if (old_org.length !== 0) {
			old_org[0].className = "list-group-item";
			old_org[0].className = "remove-org-button"
		}
		org.className = "list-group-item active";
		button.className = "remove-org-button active";
	}
}

function updateActiveGroup(nname) {
	if(delete_called) {
		delete_called = false;
		return;
	}
	var old_group = document.getElementsByClassName("list-group-item active");
	var group = document.getElementById(nname);
	var old_button = document.getElementsByClassName("remove-group-button active");
	var button = document.getElementById("remove-group-button "+nname);

	if (group === old_group[0]) {
		group.className = "list-group-item";
		button.className = "remove-group-button";
	} else {
		if (old_group.length !== 0) {
			old_group[0].className = "list-group-item";
			old_button[0].className = "remove-group-button"
		}
		group.className = "list-group-item active";
		button.className = "remove-group-button active";
	}
}

function updateActiveReservation(nname) {
	if(delete_called) {
		delete_called = false;
		return;
	}
	var old_reservation = document.getElementsByClassName("list-group-item active");
	var reservation = document.getElementById(nname);
	var old_button = document.getElementsByClassName("remove-reservation-button active");
	var button = document.getElementById("remove-reservation-button "+nname);

	if (reservation === old_reservation[0]) {
		reservation.className = "list-group-item";
		button.className = "remove-reservation-button";
	} else {
		if (old_reservation.length !== 0) {
			old_reservation[0].className = "list-group-item";
			old_button[0].className = "remove-reservation-button"
		}
		reservation.className = "list-group-item active";
		button.className = "remove-reservation-button active";
	}
}

function removeReservation(nname) {
	delete_called = true;
	nname = "#" + nname;
	$(nname).removeClass('active');
	$(nname).addClass('deleted-reservation');
	$(nname).css("display","none");
}

function removeGroup(nname) {
	delete_called = true;
	nname = "#" + nname;
	$(nname).removeClass('active');
	$(nname).addClass('deleted-group');
	$(nname).css("display","none");
}

function removeOrg(nname) {
	delete_called = true;
	nname = "#" + nname;
	$(nname).removeClass('active');
	$(nname).addClass('deleted-org');
	$(nname).css("display","none");
}

function makeContentInactive() {
	console.log("makeContentInactive being called");
	var active_items = document.getElementsByClassName("list-group-item active");
	// console.log(active_items);
	for (var i = 0; i < active_items.length; i++) {
		active_items[i].className = "list-group-item";
	}
	// console.log(active_items);
	var active_buttons = document.getElementsByClassName("remove-reservation-button active");
	for (i = 0; i < active_buttons.length; i++) {
		active_buttons[i].className = "remove-reservation-button";
	}
	active_buttons = document.getElementsByClassName("remove-group-button active");
	for (i = 0; i < active_buttons.length; i++) {
		active_buttons[i].className = "remove-group-button";
	}
	active_buttons = document.getElementsByClassName("remove-org-button active");
	for (i = 0; i < active_buttons.length; i++) {
		active_buttons[i].className = "remove-org-button";
	}
}

function joinGroupPopup() {
	swal.withForm({   
		title: "Join a Group!", 
		text: 'Search existing groups:',
		showCancelButton: true,   
		closeOnConfirm: false,   
		showLoaderOnConfirm: true, 
		html: true,
		formFields: [
			{ id: 'name', placeholder: 'Start typing group name' },
		]
	}, 
	function(isConfirm) {
		if (isConfirm) {
			group_name = this.swalForm.name;
			if ($.inArray(group_name, group_list) !== -1) {
				$.ajax({
					url : "/booker/join_group/",
					type: "POST",
					data : {group_name:group_name},
				});
				setTimeout(function(){ 
					swal({
						title: "Successfully joined " + group_name + "!",
						type: "success",
					},
					function() {
						location.reload();
					});   
	    		}, 2000);
			} else {
				setTimeout(function(){ 
					swal("Uh oh! There is no group called " + group_name + "!");   
	    		}, 2000);
			}
	    }
	});
	jQuery(function($) {
		var data = group_list;
		$("#name").autocomplete({
			source: data
		});
	});
}

function joinOrgPopup() {
	swal.withForm({   
		title: "Join an Organization!", 
		text: 'Search existing organizations:',
		showCancelButton: true,   
		closeOnConfirm: false,   
		showLoaderOnConfirm: true, 
		html: true,
		formFields: [
			{ id: 'name', placeholder: 'Start typing organization name' },
		]
	}, 
	function(isConfirm) {
		if (isConfirm) {
			org_name = this.swalForm.name;
			if ($.inArray(org_name, org_list) !== -1) {
				$.ajax({
					url : "/booker/join_org/",
					type: "POST",
					data : {org_name:org_name},
				});
				setTimeout(function(){ 
					swal({
						title: "Successfully joined " + org_name + "!",
						type: "success",
					},
					function() {
						location.reload();
					});   
	    		}, 2000);
			} else {
				setTimeout(function(){ 
					swal("Uh oh! There is no organization called " + org_name + "!");   
	    		}, 2000);
			}
	    }
	});
	jQuery(function($) {
		var data = org_list;
		$("#name").autocomplete({
			source: data
		});
	});
}

function createGroupPopup() {
	swal.withForm({
	    title: 'Create a Group!',
	    text: 'Make reservations for your friends, teammates, etc.',
	    showCancelButton: true,
	    confirmButtonColor: '#FED100',
	    confirmButtonText: 'Create Group',
	    closeOnConfirm: false,   
		showLoaderOnConfirm: true,
	    formFields: [
			{ id: 'name', placeholder: 'Name your group' },
			// { id: 'description', placeholder: 'Add a description for your group' },
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
							location.reload();
						});   
	    			}, 2000);
				} else {
					setTimeout(function(){ 
						swal("Whoops! A group called " + group_name + " already exists! Please use another name.");   
		    		}, 2000);
				}
		    }
		}
	)
}



