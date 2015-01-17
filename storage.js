var storage = undefined;
	
function init_storage() {

	// Load session.
	// Strangely if I assign user = null, user is seen as string ?
	if((!sessionStorage.user || sessionStorage.user == "null") && (!localStorage.user || localStorage.user == "null")) {
    		window.location.href = "login.html";
    }

	if(sessionStorage.user) {
		storage = sessionStorage;
	}
	else
	{
		storage = localStorage;
	}
}



function ajaxFailed(message, appendToId) {

    $("#" + appendToId).
    append($("<div/>", {
        class: "row",
        id: "removeFailedMessage",
        style: "margin-top:10px;margin-bottom:10px;text-align:center"
    }).append($("<div/>", {
        class: "alert alert-danger",
        role: "alert",
        style: "margin-bottom:0px"
    }).append("<strong>" + message)))

    window.setTimeout(function() {
        $("#removeFailedMessage").fadeTo(2000, 0).slideUp(2000, function() {
            $(this).remove();
        });
    }, 3000);
}