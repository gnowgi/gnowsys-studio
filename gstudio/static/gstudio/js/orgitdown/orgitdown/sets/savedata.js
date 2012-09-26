 $.noConflict();
  jQuery(document).ready(function($) {
   	$("#editdata").one("click",function() {
	$("#chart").hide();
	var orgdata = document.getElementById('orgcontent').value;
	document.getElementById('gnoweditor').style.visibility="visible";
	$("#gnoweditor").orgitdown(mySettings);
	$("#gnoweditor").val(orgdata);
	$("#editdata").hide();
	$("#savecontent").show();


	      });
       

  });

