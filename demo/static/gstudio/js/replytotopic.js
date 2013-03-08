 $.noConflict();
function saveclick(objid){
    $("#add"+objid).show();
    var org_data = $("#gnoweditor").val();
    var encode_data = encodeURIComponent(org_data);
    var decode_data = decodeURIComponent(encode_data.replace(/\+/g, " "));       
    $("#text"+objid).val(decode_data);
    $("#submit"+objid).trigger('click');
    $(".commenteditor").hide();
    $(".editcontent").hide();
}//closing saveclick                                                                                                             




jQuery(document).ready(function($) {
    $(".commenteditor").one("click",function() {
        var a=$(this).attr("id");
        $("#chart").hide();
        $("#content").css({"width": "300px",})
        document.getElementById('gnoweditor').style.visibility="visible";
        $("#gnoweditor").orgitdown(mySettings);
        var screentop=$(document).scrollTop();
        $(".orgitdownContainer").css({"margin-top":screentop,});
        $("#save"+a).show();
        $(".commenteditor").hide();
        $(".chkdel").hide();
        $(".submitdelete").hide();
        $(".rating").hide();
        $(".editor").hide();
	$(".topicchk").hide();
	$(".topicdelete").hide();
	$(".editcontent").hide();

    });

});
function topicsaveclick(objid){
    var org_data = $("#gnoweditor").val();
    var encode_data = encodeURIComponent(org_data);
    var decode_data = decodeURIComponent(encode_data.replace(/\+/g, " "));  
    $("#topictext"+objid).val(decode_data);
    $("#topicsubmit"+objid).trigger('click');
    $(".editor").hide();
    $(".editcontent").hide();
}//closing saveclick      
  jQuery(document).ready(function($) {
       	$(".editor").one("click",function() {
	    var a=$(this).attr("id");
	    $("#chart").hide();
	    $("#content").css({"width": "300px",})
	    document.getElementById('gnoweditor').style.visibility="visible";
	    $("#gnoweditor").orgitdown(mySettings);
	    var screentop=$(document).scrollTop();
	    $(".orgitdownContainer").css({"margin-top":screentop,});
	    $("#save"+a).show();
	    $(".editor").hide();
	    $(".topicchk").hide();
	    $(".topicdelete").hide();
	    $(".editcontent").hide();
	    $(".commenteditor").hide();
            $(".chkdel").hide();
            $(".submitdelete").hide();
            $(".rating").hide();
	});

});

 
jQuery(document).ready(function($) {
        $(".editcontent").one("click",function() {
	    var each_id = $(this).attr("id");
	    $("#chart").hide();
	    $("#content").css({"width": "300px",})
	document.getElementById('gnoweditor').style.visibility="visible";
	$("#gnoweditor").orgitdown(mySettings);
	    
	    var org_data=$("#commentdata"+each_id).val();
	    $("#edit"+each_id).val("edited");
	    $("#topictext"+each_id).val(org_data);
            var screentop=$(document).scrollTop();
	    $(".orgitdownContainer").css({"margin-top":screentop,});
	    $("#gnoweditor").val(org_data);
	    $("#save"+each_id).show();
	    $(".editcontent").hide();
	    $(".editor").hide();
	    $(".submitdelete").hide();
	    $(".commenteditor").hide();
	    $(".rating").hide();
	    $(".topicdelete").hide();
	    $(".chkdel").hide();
	    $(".topicchk").hide();			
	});


  });
