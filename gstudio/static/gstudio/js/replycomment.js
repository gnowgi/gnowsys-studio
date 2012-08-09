$.noConflict();
jQuery(document).ready(function($) {
    $(".commenteditor").one("click",function() {
        $("#chart").hide();
        $("#content").css({"width": "300px",})
        document.getElementById('gnoweditor').style.visibility="visible";
        $("#gnoweditor").orgitdown(mySettings);
        var screentop=$(document).scrollTop();
        $(".orgitdownContainer").css({"margin-top":screentop,});
    });
  
    $(".commentsavecontent").one("click",function(){
	var org_data = $("#gnoweditor").val();


//	document.getElementByClass("commentreptext").setAttribute("value",org_data);
	var elmts = document.getElementsByClassName ("commentreptext");
	for (var i = 0; i < elmts.length; i++) {
            elmts[i].setAttribute("value",org_data);
	      }
	alert(org_data);
       
    });
    $(".deleteresponse").one("click",function() {
	var elmts=document.getElementsByClassName("deleteresponse");
	alert("hai");
	alert(elmts.length);

	 

    });
});
