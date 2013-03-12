 $.noConflict();
   var isWikipage=false;
   var editWikipage=false;
   var objid;
   var twistid;
   var responseid;
   var isSection=false;
   var editSection=false;
   var isSubsection=false;
   var editSubsection=false;
   var isNode=false;
   var isObject=false;
   var isTwist=false;
   var isThread=false;
   var isResponse=false;
   var editTwist=false;
   var editThread=false;
   var editResponse=false;
   var editImage=false;
   var isImage=false;
   var isVideotitle=false;
   var isEditdoc = false;
   var isSubResponse=false;
   var checkeditor = 0;



function saveclick(objid){
    $("#add"+objid).show();
    var org_data = $("#gnoweditor").val();
    var encode_data = encodeURIComponent(org_data);
    var decode_data = decodeURIComponent(encode_data.replace(/\+/g, " "));       
    $("#text"+objid).val(decode_data);
    add_sub_response_ajax(objid)
    //$("#submit"+objid).trigger('click');
    $(".commenteditor").show();
    $(".editcontent").show();
    $(".orgitdown").hide();
}//closing saveclick                                                                                                             


jQuery(document).ready(function($) {
    $(document).on('click',".commenteditor",function(){
	if(checkeditor==0){
        $(this).after('<textarea id="gnoweditor" style="visibility:hidden;width:450px;height:60px;"></textarea>');
        isSubResponse=true;
        var a=$(this).attr("id");
	objid=a;
        $("#chart").hide();
	$("#content img").css({"max-width": "600px",})
        $("#content").css({"width": "600px",})
                document.getElementById('gnoweditor').style.visibility="visible";
        $("#gnoweditor").orgitdown(mySettings);
        $(".orgitdownContainer").css({"margin-top":"0px","margin-left":"10px"});
        $("#save"+a).show();
        $(".commenteditor").hide();
        $(".chkdel").hide();
        $(".submitdelete").hide();
        $(".rating").hide();
        $(".editor").hide();
	$(".topicchk").hide();
	$(".topicdelete").hide();
	$(".editcontent").hide();
	$(".commentsavecontent").hide();
	$('#gnoweditor').focus();
	window.scroll($(this).offset().left,($(this).offset().top-250));
	checkeditor = 1;
	}
	else{
	        $(this).after($('.orgitdown'));
    		$(".orgitdown").show();
                isSubResponse=true;
                var a=$(this).attr("id");
         	objid=a;
                $("#chart").hide();
                document.getElementById('gnoweditor').value="";	
                $("#save"+a).show();
                $(".commenteditor").hide();
	        $(".chkdel").hide();
	        $(".submitdelete").hide();
	        $(".rating").hide();
	        $(".editor").hide();
		$(".topicchk").hide();
		$(".topicdelete").hide();
		$(".editcontent").hide();
		$(".commentsavecontent").hide();
		$('#gnoweditor').focus();
		window.scroll($(this).offset().left,($(this).offset().top-250));
	
	}

    });

});
function topicsaveclick(objid){
    var org_data = $("#gnoweditor").val();
    var encode_data = encodeURIComponent(org_data);
    var decode_data = decodeURIComponent(encode_data.replace(/\+/g, " "));  
    $("#topictext"+objid).val(decode_data);
//    $("#topicsubmit"+objid).trigger('click');
    submtobj=objid;
//    activity="edited_twist"
//    not_obj=objid


    notifedtdel();
    $(".editor").show();
   // $(".editcontent").hide();
    $(".orgitdown").hide();
}//closing saveclick      
  jQuery(document).ready(function($) {
	$(document).on('click',".editor",function(){
       	//$(".editor").on("click",function() {
            $(this).after('<textarea id="gnoweditor" style="visibility:hidden;width:450px;height:60px;"></textarea>');
            isResponse=true;
            activity="added_response"
	    var a=$(this).attr("id");
	    not_obj=a
	    $("#chart").hide();
	    $("#content img").css({"max-width": "600px",})

	    $("#content").css({"width": "600px",})
	    document.getElementById('gnoweditor').style.visibility="visible";
	    $("#gnoweditor").orgitdown(mySettings);
	//    var screentop=$(document).scrollTop();
	  //  $(".orgitdownContainer").css({"margin-top":screentop,});
            $(".orgitdownContainer").css({"margin-top":"0px","margin-left":"10px"});
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
	    checkeditor = 1;
	});

});

 
jQuery(document).ready(function($) {
        $(".editcontent").one("click",function() {
            $(this).replaceWith('<textarea id="gnoweditor" style="visibility:hidden;width:450px"></textarea>');
	    editTwist=true;
	    activity="edited_twist"
	    var each_id = $(this).attr("id");
	    not_obj=each_id
	    $("#chart").hide();
            $("#content img").css({"max-width": "600px",})

	    $("#content").css({"width": "600px",})
	    document.getElementById('gnoweditor').style.visibility="visible";
	    $("#gnoweditor").orgitdown(mySettings);
	    var org_data=$("#commentdata"+each_id).val();
	    $("#edit"+each_id).val("edited");
	    $("#topictext"+each_id).val(org_data);
            var screentop=$(document).scrollTop();
	//    $(".orgitdownContainer").css({"margin-top":screentop,});
            $(".orgitdownContainer").css({"margin-top":"0px","margin-left":"10px"});
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
	  $(".orgitdownContainer").hide();
      });
	
	 $("#addthreadcontent").one("click",function() {
          $(this).replaceWith('<textarea id="gnoweditor" style="visibility:hidden;width:450px"></textarea>');
	  isThread=true;
	  $("#chart").hide();
	  $("#content img").css({"max-width": "600px",})

          $("#content").css({"width": "600px",})
          document.getElementById('gnoweditor').style.visibility="visible";
          $("#gnoweditor").orgitdown(mySettings);
          var screentop=$(document).scrollTop();
//          $(".orgitdownContainer").css({"margin-top":screentop,});
          $(".orgitdownContainer").css({"margin-top":"0px","margin-left":"10px"});
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
	  $(".orgitdownContainer").hide();
      });

  });
jQuery(document).ready(function($) {
        $("#threadedit").one("click",function() {
            $(this).replaceWith('<textarea id="gnoweditor" style="visibility:hidden;width:450px"></textarea>');
	    editThread=true;
	   
	    $("#chart").hide();
            $("#content img").css({"max-width": "600px",})

	    $("#content").css({"width": "600px",})
	    document.getElementById('gnoweditor').style.visibility="visible";
	    $("#gnoweditor").orgitdown(mySettings);
  

            var screentop=$(document).scrollTop();
    // $(".orgitdownContainer").css({"margin-top":screentop,});
      	    $(".orgitdownContainer").css({"margin-top":"0px","margin-left":"10px"});
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
            activity="edited_thread"
            not_obj=id
	   
            notifedtdel();
            $("#threadedit"+id).val("editthread");
            $(".commenteditor").hide();
            $(".editcontent").hide();
	    $(".orgitdownContainer").hide();

        });


});

