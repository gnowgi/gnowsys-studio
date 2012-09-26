 $.noConflict();
var isThread=false;
var editThread=false;
var isTwist=false;
var editTwist=false;
var isResponse=false;
var objid;
var twistid;
var responseid;
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
	$("#content img").css({"max-width": "600px",})
        $("#content").css({"width": "600px",})
        
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
            isResponse=true;
	    var a=$(this).attr("id");
	    $("#chart").hide();
	    $("#content img").css({"max-width": "600px",})

	    $("#content").css({"width": "600px",})
	    document.getElementById('gnoweditor').style.visibility="visible";
	    $("#gnoweditor").orgitdown(mySettings);
	    var screentop=$(document).scrollTop();
	    $(".orgitdownContainer").css({"margin-top":screentop,});
	    responseid=a;
	    //$("#save"+a).show();
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
	    editTwist=true;
	    var each_id = $(this).attr("id");
	    $("#chart").hide();
            $("#content img").css({"max-width": "600px",})

	    $("#content").css({"width": "600px",})
	    document.getElementById('gnoweditor').style.visibility="visible";
	    $("#gnoweditor").orgitdown(mySettings);
	    var org_data=$("#commentdata"+each_id).val();
	    $("#edit"+each_id).val("edited");
	    $("#topictext"+each_id).val(org_data);
            var screentop=$(document).scrollTop();
	    $(".orgitdownContainer").css({"margin-top":screentop,});
	    $("#gnoweditor").val(org_data);
	    twistid=each_id;
	    //$("#save"+each_id).show();
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

 $.noConflict();
  jQuery(document).ready(function($) {
      $("#topicaddcontent").one("click",function() {
	  isTwist=true;
          $("#chart").hide();
	  $("#content img").css({"max-width": "600px",})

          $("#content").css({"width": "600px",})
          document.getElementById('gnoweditor').style.visibility="visible";
          $("#gnoweditor").orgitdown(mySettings);
          var screentop=$(document).scrollTop();
          $(".orgitdownContainer").css({"margin-top":screentop,});
  //        $("#topicaddsave").show();
      });
      
      $("#topicaddsave").one("click",function(){
	  var org_data = $("#gnoweditor").val();
	  var encode_data = encodeURIComponent(org_data);
          var decode_data = decodeURIComponent(encode_data.replace(/\+/g, " "));       
	  $("#contenttext").val(decode_data);
 	  $('#topicsubmit').trigger('click');
          $("#topicaddsave").hide();
      });
	
	 $("#addthreadcontent").one("click",function() {
	  isThread=true;
	  $("#chart").hide();
	  $("#content img").css({"max-width": "600px",})

          $("#content").css({"width": "600px",})
          document.getElementById('gnoweditor').style.visibility="visible";
          $("#gnoweditor").orgitdown(mySettings);
          var screentop=$(document).scrollTop();
          $(".orgitdownContainer").css({"margin-top":screentop,});
	  $("#addthreadcontent").hide();
	 // $("#threadsave").show();
      });

      $("#threadsave").one("click",function(){
          var org_data = $("#gnoweditor").val();
	  var encode_data = encodeURIComponent(org_data);
          var decode_data = decodeURIComponent(encode_data.replace(/\+/g, " "));       
          $("#threadcontent").val(decode_data);
          $('.orgitdownContainer').hide();
          $("#threadsave").hide();
	  $("#addthreadcontent").show();
      });

  });
jQuery(document).ready(function($) {
        $("#threadedit").one("click",function() {
	    editThread=true;
	    $("#chart").hide();
            $("#content img").css({"max-width": "600px",})

	    $("#content").css({"width": "600px",})
	    document.getElementById('gnoweditor').style.visibility="visible";
	    $("#gnoweditor").orgitdown(mySettings);
  

            var screentop=$(document).scrollTop();
	    $(".orgitdownContainer").css({"margin-top":screentop,});
	    var id=document.getElementById("threadid").value;
	    var org_data=document.getElementById("threadcontent"+id).value;
	    $("#gnoweditor").val(org_data);
	    $("#threadedit").hide();
            $(".editor").hide();
            $(".editcontent").hide();
	    $("#addthreadcontent").hide();
	    $("#twistaddbtn").hide();
	    $("#Release *").hide();
	    //$("#editthreadsave").show();	
	});

	 $("#editthreadsave").one("click",function() {
            var id=document.getElementById("threadid").value;
	    var org_data=$("#gnoweditor").val();
	    $("#threadcontent"+id).val(org_data);
	    $('.orgitdownContainer').hide();
	    $("#threadsave").hide();
	    $("#threadedit"+id).val("editthread");
	    $(".commenteditor").hide();
	    $(".editcontent").hide();
	    $("#subeditresp").trigger('click');
	});
});

