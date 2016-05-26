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
});

function addClasses() {
    var password = document.getElementById("id_password");
    password.className = "form-control";

    var new1 = document.getElementById("id_new1");
    new1.className = "form-control";

    var new2 = document.getElementById("id_new2");
    new2.className = "form-control";

    var picture = document.getElementById("id_picture");
    picture.className = "form-control";
}

function changePassword() {
    var password = document.getElementById("id_password");
    var new1 = document.getElementById("id_new1");
    var new2 = document.getElementById("id_new2");
    var errorPassword = document.getElementById("errorPassword");

    if (password.value === "" || new1.value == "" || new2.value === "") {
        errorPassword.innerHTML = "- All fields must be filled out.";
    }else if (new1.value !== new2.value) {
        errorPassword.innerHTML = "- The new password and its confirmation are not equal";
    }else {
        $.ajax({
            url: "/booker/change_password/",
            type: "POST",
            data: {oldp: password.value, newp: new1.value},
            success: function(response) {
                errorPassword.innerHTML = "";
                password.value = "";
                new1.value = "";
                new2.value = "";
                setTimeout(function() {
                    swal({
                        title: "Successfully changed your password!",
                        type: "success",
                    }, function() {
                        location.replace("/booker/settings/");
                    });
                }, 2000);
            },
            error: function(response) {
                setTimeout(function() {
                    swal("Failed to change password. Specified old password was incorrect.");
                }, 2000);
            }
        });
    }
}

var org_names;

function getOrgList() {
    jQuery.get("/booker/organizations/",function(org_objs) {
        org_list = JSON.parse(org_objs);
        org_names = [];
        for (var i=0; i<org_list.length; i++) {
            org_names.push(org_list[i]["fields"]["name"]);
        }
    });
}

function createOrganization() {
    swal.withForm({
        title: 'Create an Organization!',
        text: 'Completion of this form will submit a request to create an organization.',
        showCancelButton: true,
        confirmButtonColor: '#FED100',
        confirmButtonText: 'Submit Request',
        closeOnConfirm: false,   
        showLoaderOnConfirm: true,
        formFields: [
            { id: 'name', placeholder: 'Name your organization' },
        ]
        }, 
        function (isConfirm) {
            if (isConfirm) {
                org_name = this.swalForm.name;
                if ($.inArray(org_name, org_names) === -1) {
                    $.ajax({
                        url : "/booker/create_organization/",
                        type: "POST",
                        data : {org_name:org_name},
                    });
                    setTimeout(function(){ 
                        swal({
                            title: "Successfully created organization " + org_name + "!",
                            type: "success",
                        },
                        function() {
                            location.replace("/booker/settings/?tab=create");
                        });   
                    }, 2000);
                } else {
                    setTimeout(function(){ 
                        swal("Whoops! An organization called " + org_name + " already exists! Please use another name.");   
                    }, 2000);
                }
            }
        }
    )
}

function uploadPhoto() {
    var picture = document.getElementById("id_picture");
    var errorPicture = document.getElementById("errorPicture")
    if (picture.value === "") {
        errorPicture.innerHTML = "- Must select a file to upload.";
    }else {
        document.forms['uform'].submit();
    }
}

// SWAL unnecessary (thanks, Jaaames.... /s)

// function changePassword() {
//     swal.withForm({
//         title: 'Change Your Password',
//         showCancelButton: true,
//         confirmButtonColor: '#FED100',
//         confirmButtonText: 'Submit',
//         closeOnConfirm: false,   
//         showLoaderOnConfirm: true,
//         formFields: [
//             {id: 'password', placeholder: 'Old password'},
//             {id: 'new1', placeholder: 'New password'},
//             {id: 'new2', placeholder: 'Confirm new password'},
//         ]
//     }, function (isConfirm) {
//         if (isConfirm) {
//             group_name = this.swalForm.name;
//             password = this.swalForm.password;
//             new1 = this.swalForm.new1;
//             new2 = this.swalForm.new2;

//             if (new1 === new2) {
//                 $.ajax({
//                     url: "/booker/change_password/",
//                     type: "POST",
//                     data: {oldp: password, newp: new1},
//                     success: function(response) {
//                         setTimeout(function() {
//                             swal({
//                                 title: "Successfully changed your password!",
//                                 type: "success",
//                             }, function() {
//                                 location.replace("/booker/settings/");
//                             });
//                         }, 2000);
//                     },
//                     error: function(response) {
//                         setTimeout(function() {
//                             swal("Failed to change password. Specified old password was incorrect.");
//                         }, 2000);
//                     }
//                 });
//             }else {
//                 setTimeout(function() {
//                     swal("The new password and its confirmation must match.");
//                 }, 2000);
//             }
//         }
//     });
// }