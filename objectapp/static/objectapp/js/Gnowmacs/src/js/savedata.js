 $.noConflict();
  jQuery(document).ready(function($) {
    // Code that uses jQuery's $ can follow here.
	$("#editdata").click(function(){
	$("html").css({"margin":"0","padding": "0","overflow":"hidden","height": "100%"});
	$("#chart").hide();
	//$("#sidebar").hide();
	$("#gnoweditor").gnowmacs();
	

	    });
       
  });
