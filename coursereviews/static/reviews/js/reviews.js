$(document).ready(function () {
  // Initialize the create review page
  $("input#id_prof_course").select2({
    placeholder: "Select a course",
    data: JSON.parse($("script#prof_course_choices").html()),
    containerCss: "height: 34px;"
  });

  // $("input#id_grade").select2();

  $("select").select2({
    placeholder: "Select all that apply"
  });

  $("input#id_hours").slider({
    value: sliderInitVal,
    tooltip: false,
    min: 0,
    max: 12
  })
    .on('slide', function(ev) {
      var $hoursBox = $("div.hours-display");
      if (ev.value === 12) {
        $hoursBox.text("12+")
      }
      else {
        $hoursBox.text(ev.value);
      }
    });
  $("input#id_hours").removeClass("hide");

  $("label.active input").attr('checked', 'checked');

});