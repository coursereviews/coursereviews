$(document).ready(function () {
  $("input#id_prof_course").select2({
    placeholder: "Select a course",
    data: JSON.parse($("script#prof_course_choices").html()),
    containerCss: "height: 34px;"
  });

  $("input#id_hours").slider({
    value: sliderInitVal,
    tooltip: false
  })
    .on('slide', function(ev) {
      $("div.hours-display").text(ev.value);
    });
  $("input#id_hours").removeClass("hide");

  $("label.active input").attr('checked', 'checked');

});