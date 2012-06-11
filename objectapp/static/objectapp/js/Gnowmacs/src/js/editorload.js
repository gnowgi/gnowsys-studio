 $.noConflict();
  jQuery(document).ready(function($) {
    // Code that uses jQuery's $ can follow here.
	$("#editdata").click(function(){
	alert("test");
	$("#sidebar").hide();
	$("#gnoweditor").gnowmacs();

	//	var org_data = encodeURIComponent($("#bufferdata").val());
	//	alert("encode" +org_data);

	//	alert("supriya");
	//	var content = $("#bufferdata").val();
	//	var iden = $("#objectid").val();
	//	alert ("data" + content);
	//alert ("id" +iden);
	// url = "/nodetypes/ajax/contentorgadd/?id=" + iden + "&contentorg=" +content;
	// alert(url);
	//  $.get(url,
	//    		function(data){
	// 	     alert("qqq" + data);
	//              })			     

	});
	
  });
  // Code that uses other library's $ can follow here.

