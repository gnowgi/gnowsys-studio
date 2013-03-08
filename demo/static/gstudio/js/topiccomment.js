 $.noConflict();
  jQuery(document).ready(function($) {
      $("#topicaddcontent").one("click",function() {
          $("#chart").hide();
          $("#content").css({"width": "300px",})
          document.getElementById('gnoweditor').style.visibility="visible";
          $("#gnoweditor").orgitdown(mySettings);
          var screentop=$(document).scrollTop();
          $(".orgitdownContainer").css({"margin-top":screentop,});
          $("#topicaddsave").show();
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
	  $("#chart").hide();
          $("#content").css({"width": "300px",})
          document.getElementById('gnoweditor').style.visibility="visible";
          $("#gnoweditor").orgitdown(mySettings);
          var screentop=$(document).scrollTop();
          $(".orgitdownContainer").css({"margin-top":screentop,});
	  $("#addthreadcontent").hide();
	  $("#threadsave").show();
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
