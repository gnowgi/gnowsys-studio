$.noConflict();

function saveclick(objid){
	$("#add"+objid).show();
	var org_data = $("#gnoweditor").val();
	$("#text"+objid).val(org_data);
	$("#submit"+objid).show();
	$(".commenteditor").hide();
	$(".editcontent").hide();
}

jQuery(document).ready(function($) {
    $(".commenteditor").one("click",function() {
	var a = $(this).attr("id");
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
    });
  });
