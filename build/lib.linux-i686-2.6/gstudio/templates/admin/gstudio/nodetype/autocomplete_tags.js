{% load tagging_tags %}

$(document).ready(function() {
  {% tags_for_model gstudio.Objecttype as objecttype_tags %}
  var data = "{{ objecttype_tags|join:',' }}".split(",");
  $("#id_tags").autocomplete(data, {
                width: 150, max: 10, 
                multiple: true, multipleSeparator: ", ",
                scroll: true, scrollHeight: 300,
                matchContains: true, autoFill: true,});
});