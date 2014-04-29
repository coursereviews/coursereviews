$(document).ready(function () {
  // Initialize the create review page

  var $coursesLoading = $("#coursesLoading");
  var showLoading = window.setTimeout(function() {
    $coursesLoading.removeClass("hide-fade");
  }, 1000);

  $.getJSON("/api/review/options", function(courses) {
    window.clearTimeout(showLoading);
    $coursesLoading.addClass("hide");
    $("input#id_prof_course").select2({
      placeholder: "Select a course",
      data: courses,
      containerCss: "height: 34px;"
    });
  });
  
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