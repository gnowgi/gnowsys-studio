$ = django.jQuery
 

 $(document).ready(function() {
	   
	   $("#id_atrributetype").ajaxSend(function(e,xhr,opt){
		   

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = $.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }

	       }
	       );


	   $("#id_attributetype").change(function() {
		   test = $("#id_attributetype").val()
		   url = "/nodetypes/ajax/ajaxattribute/?id=" + test

		   $.get(url,
		   	 function(data){			     

		   	             $("#id_subject").empty()
			     
		   	             for (var key in data) {
		   			$('#id_subject').append(
		   						$('<option></option>').val(key).html(data[key])
		   						);
		   		     }


			     


		   	 });

	   
	       });
	$(function() {
		$( "#id_creation_date_0" ).datepicker();
	});

	$(function() {
		$( "#id_creation_date_1" ).timepicker();
	});

	$(function() {
		$( "#id_last_update_0" ).datepicker();
	});

	$(function() {
		$( "#id_last_update_1" ).timepicker();
	});



 });
