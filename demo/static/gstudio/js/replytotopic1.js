 $.noConflict();
  jQuery(document).ready(function($) {
   	$(".editor").one("click",function() {
	$("#chart").hide();
	    $("#content").css({"width": "300px",})
	document.getElementById('gnoweditor').style.visibility="visible";
	$("#gnoweditor").orgitdown(mySettings);
	    var screentop=$(document).scrollTop();
	    $(".orgitdownContainer").css({"margin-top":screentop,});
	    $(".editor").hide();
	    $(".savecontent").show();
	    $(".editcontent").hide();
	    $(".submitresponse").show();
	
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
	    $(".savecontent").hide();
	    $(".editcontent").show();

	});

	$(".editcontent").one("click",function() {
	
	    $("#chart").hide();
	    $("#content").css({"width": "300px",})
	document.getElementById('gnoweditor').style.visibility="visible";
	$("#gnoweditor").orgitdown(mySettings);
	  //  var org_data= document.getElementsByClassName(".commentdata");
            var org_data=this.name;
	    var elmts1 = document.getElementsByClassName("editval");
	    
            for (var i = 0; i < elmts1.length; i++) {
		
		elmts1[i].setAttribute("value","edited");
	    }
	   
//	    var a =  document.getElementById('reptext').value;

            $("#gnoweditor").val(org_data);
	    var elmts2 = document.getElementsByClassName ("reptext");
            for (var i = 0; i < elmts2.length; i++) {
		elmts2[i].setAttribute("value",org_data);
            }
	    var screentop=$(document).scrollTop();
	    $(".orgitdownContainer").css({"margin-top":screentop,});
	    $("#gnoweditor").val()	
	    $(".editcontent").hide();
	    $(".editor").hide();
	    $(".savecontent").show();
	    $(".submitresponse").show()
	});
     


  });
