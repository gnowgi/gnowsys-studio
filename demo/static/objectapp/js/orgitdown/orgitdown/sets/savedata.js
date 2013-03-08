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
       $("#savecontent").one("click",function() {
	      var org_data = $("#gnoweditor").val();
	      var id =  document.getElementById("objectid").value
	       document.getElementById("orgcontent").value = org_data;
	      var encode_data = encodeURIComponent(org_data);
          $("#savecontent").hide();
		         $.ajax({
			       url: '/nodetypes/ajax/contentorgadd/?id=' + id + '&contentorg=' + encode_data,
			       success: function(data) {
			         $.ajax({
				    url: '/nodetypes/ajax/ajaxcreatefile/?id=' +id+ '&content_org=' +encode_data,
				    success: function(data) {
				    	$.ajax({
				    		url: '/nodetypes/ajax/ajaxcreatehtml/',
				    		success: function(data) {
				    		    $.ajax({
				    			    url: '/nodetypes/ajax/contentadd/?id=' +id,
                                                            success: function(data) {
								// alert("Data Saved");
                                                              location.reload();}
				    			});
				    		}      
				     	    });
				     }
				}); 
			    
			       }
			 });
		    
      });
  });

