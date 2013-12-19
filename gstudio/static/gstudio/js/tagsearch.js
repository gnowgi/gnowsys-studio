jQuery(document).ready(function($) {

    $(window).load(function() {
        $("button[rel]").overlay({mask: '#000', effect: 'apple'});
    });

    $(document).on('click',"#tagsearch",function() {
        $("button[rel]").overlay({mask: '#000', effect: 'apple'});

        var a= document.getElementById("opt");
        var b=a.options[a.selectedIndex].value;

        if (b=='AND')
        {
   oprtn="AND"
        }
  else
        {

    oprtn="OR"
        }
    ajurl="/gstudio/resources/addreln/puttagsearch/"
        first_d=$("#search_first").val();
        second_d=$("#search_secnd").val();
        $.ajax({
            url: ajurl,
            data: {first:first_d,second:second_d,operation:oprtn},
            success: function(data)
            {
                $(".overlay").append(data);
                $("button[rel]").overlay({mask: '#000', effect: 'apple'});
            }
        });

    });
    $(document).on('click',".overlay",function()
                      { 
  ajurl="/gstudio/resources/addreln/refreshtag/"
                          $.ajax({
                              url: ajurl,
                              success: function(data)
                              {
                               $("#search_first").val("");
                               $("#search_secnd").val("");
                               $(".overlay h2").html("");
                               $(".overlay p").html("");//.html("<a class='close'></a>");//.empty();                                         
                                 // $("#tagdiv").html(data);                                                                                 
                        
                              }
                          });
                      });
});
