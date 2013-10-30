$(document).ready(function () {
  // Initialize typeahead on the homepage
  $("input#search-bar").typeahead([
  {
    name: 'professors',
    prefetch: STATIC_URL + "reviews/professors.json",
    header: "<h3 class='typeahead-suggestion-header'>Professors</h3>",
    template: "<p>{{name}}</p>",
    engine: Hogan
  },
  {
    name: 'courses',
    prefetch: STATIC_URL + "reviews/courses.json",
    header: "<h3 class='typeahead-suggestion-header'>Courses</h3>",
    template: "<p>{{name}}</p>",
    engine: Hogan
  }
  ]).on("keydown", function(e) {
    if (e.which == 13) {
        $("form").submit();
    }
  });
});