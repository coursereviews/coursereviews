$(document).ready(function () {
  $("input#id_prof_course").select2({
    placeholder: "Select a course",
    data: JSON.parse($("script#prof_course_choices").html()),
    containerCss: "height: 34px;"
  });
});