 $.noConflict();
  jQuery(document).ready(function($) {
   	$(".editor").one("click",function() {
	$("#chart").hide();
	    $("#content").css({"width": "300px",})
	document.getElementById('gnoweditor').style.visibility="visible";
	$("#gnoweditor").orgitdown(mySettings);
	    var screentop=$(document).scrollTop();
	    $(".orgitdownContainer").css({"margin-top":screentop,});
	
	 });


        $(".savecontent").one("click",function() {
	    alert("Please click on Submit");
	 	var org_data = $("#gnoweditor").val();

	// 	alert(org_data);
	//	document.getElementsByClassName("reptext").value = org_data;
	        
 	    var elmts = document.getElementsByClassName ("reptext");
            for (var i = 0; i < elmts.length; i++) {
		elmts[i].setAttribute("value",org_data);
            }

	});
     


  });
