 $.noConflict();
    
  jQuery(document).ready(function($) {
       $("#addcontent").one("click",function(){
	       //var abc = document.getElementById('pageid1').value;
	       //window.location.replace('sectionadd1/'+abc);
	       $("#save").show();
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
		$('#submitsec').trigger('click');
		
		});

	$("#pagecontent1").one("click",function() {
	$("#chart").hide();
	document.getElementById('gnoweditor').style.visibility="visible";
	$("#gnoweditor").orgitdown(mySettings);
	$("#save1").show();
	    });
        $("#save1").one("click",function() {
	var org_data = $("#gnoweditor").val();
	document.getElementById("orgpage1").value = org_data;
	var encode_data = encodeURIComponent(org_data);
	$('#submitpage').trigger('click');	

	});
	       $(".editseccontent").one("click",function(){
		   $(".submitresponse").show();
		     $(".saveseccontent").show();
		   $(".editseccontent").hide();
   
		    $("#chart").hide();
		    document.getElementById('gnoweditor').style.visibility="visible";
		    $("#gnoweditor").orgitdown(mySettings);
		    var a = this.name;
		    $("#gnoweditor").val(a);
		   var elmts = document.getElementsByClassName("editval");
	           for (var i = 0; i < elmts.length; i++){
		       elmts[i].setAttribute("value","edited");}
		   var screenTop = $(document).scrollTop();
		   $(".orgitdownContainer").css({
		       "margin-top":screenTop,});
	       });
       $(".saveseccontent").one("click",function(){
	   var org_data = $("#gnoweditor").val();
	   var elmts = document.getElementsByClassName("reptext");
	   for (var i = 0; i < elmts.length; i++){
	       elmts[i].setAttribute("value",org_data);}
		
       });
       $(".editsubsec").one("click",function(){
	         $(".savesubsec1").show();
	         $(".submitsubsec1").show();
	         $(".editsubsec").hide();
		    $("#chart").hide();
		    document.getElementById('gnoweditor').style.visibility="visible";
		    $("#gnoweditor").orgitdown(mySettings);
		    var a = this.name;
		    $("#gnoweditor").val(a);
		   var elmts = document.getElementsByClassName("editval");
	           for (var i = 0; i < elmts.length; i++){
		       elmts[i].setAttribute("value","edited");}
	   
		    var screenTop = $(document).scrollTop();
		    $(".orgitdownContainer").css({
			    "margin-top":screenTop,});
		    
       });
       $(".savesubsec1").one("click",function(){
	   var org_data = $("#gnoweditor").val();
	   var elmts = document.getElementsByClassName("reptext");
	   for (var i = 0; i < elmts.length; i++){
	       elmts[i].setAttribute("value",org_data);}
       });
       $(".editpagecontent").one("click",function(){
      	    $("#chart").hide();
	    $(".editpagecontent").hide();
      	    $(".savepagecontent").show();
	   $(".pagedit").show();
      	    document.getElementById('gnoweditor').style.visibility="visible";
	    $("#gnoweditor").orgitdown(mySettings);
            var a = this.name;
	    $("#gnoweditor").val(a);
	    var elmts = document.getElementsByClassName("editval");
	    for (var i = 0; i < elmts.length; i++){
		elmts[i].setAttribute("value","edited");}
	   var screenTop = $(document).scrollTop();
      	    $(".orgitdownContainer").css({
      		"margin-top":screenTop,});
		    
       });
       $(".savepagecontent").one("click",function(){
	   var org_data = $("#gnoweditor").val();
	   var elmts = document.getElementsByClassName("reptext");
	   for (var i = 0; i < elmts.length; i++){
	       elmts[i].setAttribute("value",org_data);}
       });


       $(".createsubsection").one("click",function(){
	           $(".savesubsec").show();
	           $(".submitsubsec").show();
	          $(".createsubsection").hide();
   
		    $("#chart").hide();
		    document.getElementById('gnoweditor').style.visibility="visible";
		    $("#gnoweditor").orgitdown(mySettings);
		    $("#gnoweditor").val('');
		    var screenTop = $(document).scrollTop();
		    $(".orgitdownContainer").css({
			    "margin-top":screenTop,});
		  
	   });
       $(".savesubsec").one("click",function() {
	   var org_data = $("#gnoweditor").val();
	   var elmts = document.getElementsByClassName("reptext");
	   for (var i = 0; i < elmts.length; i++){
	       elmts[i].setAttribute("value",org_data);}
       });

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
       
    
