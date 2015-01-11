function userRequest() {
    var user_url = "http://128.199.38.110:5000/users";

    console.log(user_url);

    $.ajax({
        type: "GET",
	      dataType: "json",
	      url: user_url,
	      success: function(data) {
            for (var i=0; i < data.length; i++) {
                var name = data[i].first_name;
                name += " " + data[i].last_name;
                var rating = data[i].upvotes;
                var text = rating + name;
                var headername = name + " " + rating;
                if(getCookie("user=") == text) {
                    $('#user_name').text(name);
                    $('#Rating').text(rating);
                    $('#headername').text(headername);
                    var img = data[i].image_url;
                    if (img != null)
                        $('#image').attr("src", img);
                }
            }
        }
		});
}

function eventRequest() {
    var event_url = "http://128.199.38.110:5000/events";

    console.log(event_url);

    $.ajax({
        type: "GET",
	      dataType: "json",
	      url: event_url,
	      success: function(data) {
            for (var i=0; i < data.length; i++) {
                var description = data[i].message;
                var name = data[i].name;
                var rating = data[i].upvotes;
                var status = data[i].event_status;
                var text = rating + " " + name;
                if(getCookie("event=") == text) {
                    $('#event_name').text(name);
                    $('#Rating').text(rating);
                    $('#status').text(status);
                    $('#message').text(description);
                    var img = data[i].image_url;
                    if (img != null)
                        $('#image').attr("src", img);
                }
            }
        }
		});
}

function saveUser(val) {
    console.log(val.text);
    document.cookie = "user=" + val.text + ";";
}

function saveHeadUser(txt) {
    console.log(txt);
    document.cookie = "user=" + txt + ";";
}

function saveEvent(val) {
    document.cookie = "event=" + val.text + ";";
    console.log(val.text);
}

function getCookie(cname) {
    var name = cname;
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1);
        if (c.indexOf(name) == 0) return c.substring(name.length, c.length);
    }
    return "";
}
