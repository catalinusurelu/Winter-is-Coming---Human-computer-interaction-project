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
                    attendedEventsRequest(data[i].id);
                    createdEventsRequest(data[i].id);
                }
            }
        }
		});
}

function eventRequest() {
    var event_url = "http://128.199.38.110:5000/events";
    var user_url = "http://128.199.38.110:5000/users";
    var users;
    $.ajax({
        type: "GET",
	      dataType: "json",
	      url: user_url,
	      success: function(data1) {
          users = data1;
        }
		});

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
                var text = rating + name;
                if(getCookie("event=") == text) {
                    $('#event_name').text(name);
                    $('#Rating').text(rating);
                    $('#status').text(status);
                    $('#message').text(description);
                    for(var j=0; j < users.length; j++) {
                      if(data[i].creator_id == users[j].id) {
                        var usr = users[j].first_name;
                        usr += " ";
                        usr += users[j].last_name;
                        $('#initiator').text(usr);
                        var headername = usr + " " + rating;
                        $('#headername').text(headername);
                      }
                    }
                    var img = data[i].image_url;
                    if (img != null)
                        $('#image').attr("src", img);
                    peopleAttend(name);
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

function peopleAttend(eventName) {
    var user_url = "http://128.199.38.110:5000/users";
    $.ajax({
        type: "GET",
	      dataType: "json",
        contentType: "application/json",
	      url: user_url,
	      success: function(data1) {
          for(var i=0; i < data1.length; i++) {
            var id = data1[i].id;
            var event_url = "http://128.199.38.110:5000/users";
            event_url += "/" + id;
            event_url += "/events";
            console.log(event_url);
            var usr = data1[i];
            $.ajax({
              type: "GET",
              dataType: "json",
	            contentType: "application/json",
	            url: event_url,
	            success: function(data) {
                for(var j=0; j<data.length; j++) {
                  if(data[j].name == eventName) {
                    var name = usr.first_name;
                    name += " ";
                    name += usr.last_name;
                    var upvotes = usr.upvotes;
                    var pg = "<p><a href=\"user.html\" onclick=\"saveUser(this)\">";
                    pg += upvotes;
                    pg += "<span style=\"color:#F7BE81;\" class=\"glyphicon glyphicon-star\"></span>";
                    pg += name;
                    pg += "</a></p>";
                    $('#pattended').append( pg );
                  }
                }
              }
		        });
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
