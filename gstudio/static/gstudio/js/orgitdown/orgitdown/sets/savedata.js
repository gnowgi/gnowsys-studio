 $.noConflict();
  jQuery(document).ready(function($) {
    // Code that uses jQuery's $ can follow here.
	$("#editdata").click(function(){
		//	$("html").css({"margin":"0","padding": "0","overflow":"hidden","height": "100%"});
	$("#chart").hide();
	document.getElementById('gnoweditor').style.visibility="visible";
	//$("#gnoweditor").show();
       	$("#gnoweditor").orgitdown(mySettings);
	//	alert($("#gnoweditor").val());

	    });
       
  });

