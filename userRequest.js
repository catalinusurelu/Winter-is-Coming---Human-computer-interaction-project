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
                    var img = data[i].image_url.replace('5000:',''); // workaround :)
                    if (img != null)
                        $('#image').attr("src", img);
                    attendedEventsRequest(data[i].id);
                    createdEventsRequest(data[i].id);
                }
            }
        }
		});
}


function createdEventsRequest(creator_id) {
    var event_url = "http://128.199.38.110:5000/events";

    $.ajax({
        type: "GET",
	      dataType: "json",
	      url: event_url,
	      success: function(data) {
            for (var i=0; i < data.length; i++) {
                var name = data[i].name;
                var upvotes = data[i].upvotes;
                if(creator_id == data[i].creator_id) {
                    var pg = "<p><a href=\"event.html\" onclick=\"saveEvent(this)\">";
                    pg += upvotes;
                    pg += "<span style=\"color:#F7BE81;\" class=\"glyphicon glyphicon-star\"></span>";
                    pg += name;
                    pg += "</a></p>";
                    $('#ecreated').append( pg );
                }
            }
        }
		});
}

function attendedEventsRequest(id) {
    var event_url = "http://128.199.38.110:5000/users";
    event_url += "/" + id;
    event_url += "/events";

    console.log(event_url);

    $.ajax({
        type: "GET",
        dataType: "json",
	      contentType: "application/json",
	      url: event_url,
	      success: function(data) {
            for (var i=0; i < data.length; i++) {
                var name = data[i].name;
                var upvotes = data[i].upvotes;
                var pg = "<p><a href=\"event.html\" onclick=\"saveEvent(this)\">";
                pg += upvotes;
                pg += "<span style=\"color:#F7BE81;\" class=\"glyphicon glyphicon-star\"></span>";
                pg += name;
                pg += "</a></p>";
                $('#eattended').append( pg );
                console.log(name);               
            }
        }
		});
}

function peopleAttend(user_event) {
    $.ajax({
        url: "http://128.199.38.110:5000/events/" + user_event.id + "/users",
        type: "GET",
        conection: "keep-alive",
        contentType: "application/json",
        cache: false,
        processData: false,
        success: function(data) {
            participants = $.parseJSON(data);
            for(var i = 0; i < participants.length; i++) {
                var name = participants[i].first_name;
                name += " ";
                name += participants[i].last_name;
                var upvotes = participants[i].upvotes;
                var pg = "<p><a href=\"user.html\" onclick=\"saveUser(this)\">";
                pg += upvotes;
                pg += "<span style=\"color:#F7BE81;\" class=\"glyphicon glyphicon-star\"></span>";
                pg += name;
                pg += "</a></p>";
                $('#pattended').append( pg );
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
