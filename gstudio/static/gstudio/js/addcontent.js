 $.noConflict();
    
  jQuery(document).ready(function($) {
       $("#addcontent").one("click",function(){
	       //var abc = document.getElementById('pageid1').value;
	       //window.location.replace('sectionadd1/'+abc);
		    $("#chart").hide();
		    // var orgdata = document.getElementById('orgcontent').value;
		    document.getElementById('gnoweditor').style.visibility="visible";
		    
		    $("#gnoweditor").orgitdown(mySettings);
		    
		    var orgtext = $("#gnoweditor").val();

		    //  });
		    //   });
	   });
	$("#save").one("click",function() {
		var org_data = $("#gnoweditor").val();
		document.getElementById("orgpage").value = org_data;
		var encode_data = encodeURIComponent(org_data);
		});

	$("#pagecontent1").one("click",function() {
	$("#chart").hide();
	document.getElementById('gnoweditor').style.visibility="visible";
	$("#gnoweditor").orgitdown(mySettings);
	    });
        $("#save").one("click",function() {
		var org_data = $("#gnoweditor").val();
	document.getElementById("orgpage1").value = org_data;
	var encode_data = encodeURIComponent(org_data);
	    });
	       $("#editseccontent").one("click",function(){
		    $("#chart").hide();
		    document.getElementById('gnoweditor').style.visibility="visible";
		    $("#gnoweditor").orgitdown(mySettings);
		    var a =  document.getElementById('sectionorg').value;
		    $("#gnoweditor").val(a);
		    var screenTop = $(document).scrollTop();
		    $(".orgitdownContainer").css({
			    "margin-top":screenTop,});
		  
	   });
       $("#saveseccontent").one("click",function(){
	         var org_data = $("#gnoweditor").val();
		 var id =  document.getElementById("sectionid").value
		 document.getElementById("sectionorg").value = org_data;
		 var encode_data = encodeURIComponent(org_data);
		                                                        
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
								 //alert("Data Saved");
								 location.reload();}
							 });
						 }      
					     });
				     }
				 }); 
			    
			 }
		     });





		
	   });
       $("#editsubsec").one("click",function(){
		    $("#chart").hide();
		    document.getElementById('gnoweditor').style.visibility="visible";
		    $("#gnoweditor").orgitdown(mySettings);
		    var a =  document.getElementById('subsecorg').value;
		    $("#gnoweditor").val(a);
		    var screenTop = $(document).scrollTop();
		    $(".orgitdownContainer").css({
			    "margin-top":screenTop,});
		  
	   });
       $("#savesubsec1").one("click",function(){
	         var org_data = $("#gnoweditor").val();
		 var id =  document.getElementById("subsecid").value
		 document.getElementById("subsecorg").value = org_data;
		 var encode_data = encodeURIComponent(org_data);
		                                                        
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
								 //alert("Data Saved");
								 location.reload();}
							 });
						 }      
					     });
				     }
				 }); 
			    
			 }
		     });





		
	   });
      
	$("#editpagecontent").one("click",function(){
	       //var abc = document.getElementById('pageid1').value;
	       //window.location.replace('sectionadd1/'+abc);
		    $("#chart").hide();
		    // var orgdata = document.getElementById('orgcontent').value;
		    document.getElementById('gnoweditor').style.visibility="visible";
		    
		    $("#gnoweditor").orgitdown(mySettings);
		    
		    // var org_data = $("#gnoweditor").val();
		  
		    var a =  document.getElementById('pageorg').value;
		    $("#gnoweditor").val(a);
		    var screenTop = $(document).scrollTop();
		    $(".orgitdownContainer").css({
			    "margin-top":screenTop,});
		  
		    
	    });
      $("#savepagecontent").one("click",function(){
	       // var org = $("#gnoweditor").val();
	       // $("#sectionorg").val(org);
	       // var test = $("#sectionorg").val();
	       // alert(test);
	         var org_data = $("#gnoweditor").val();
		 var id =  document.getElementById("pageid").value
		 document.getElementById("pageorg").value = org_data;
		 var encode_data = encodeURIComponent(org_data);
		 //$("#gnoweditor").val(org_data);
		                                                        
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
								 //alert("Data Saved");
								 location.reload();}
							 });
						 }      
					     });
				     }
				 }); 
			    
			 }
		     });


	  });


       $("#createsubsection").one("click",function(){
		    $("#chart").hide();
		    document.getElementById('gnoweditor').style.visibility="visible";
		    $("#gnoweditor").orgitdown(mySettings);
		    $("#gnoweditor").val('');
		    var screenTop = $(document).scrollTop();
		    $(".orgitdownContainer").css({
			    "margin-top":screenTop,});
	   });
       $("#savesubsec").one("click",function() {
		var org_data = $("#gnoweditor").val();
		document.getElementById("sectionreply").value = org_data;
		var encode_data = encodeURIComponent(org_data);
		alert(org_data);});

      $("#savecontent").one("click",function() {
	      var org_data = $("#gnoweditor").val();
	      var id =  document.getElementById("objectid").value
	       document.getElementById("orgcontent").value = org_data;
	      var encode_data = encodeURIComponent(org_data);
              
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

       
	    
