 $.noConflict();
  jQuery(document).ready(function($) {
      $("#topicaddcontent").one("click",function() {
          $("#chart").hide();
          $("#content").css({"width": "300px",})
          document.getElementById('gnoweditor').style.visibility="visible";
          $("#gnoweditor").orgitdown(mySettings);
          var screentop=$(document).scrollTop();
          $(".orgitdownContainer").css({"margin-top":screentop,});
      });
      
      $("#topicaddsave").one("click",function(){
	  var org_data = $("#gnoweditor").val();
	  $("#contenttext").val(org_data);
 	  $('#topicsubmit').trigger('click');
      });
  });
