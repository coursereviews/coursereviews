$(document).ready(function () {
  $("input#search-bar").typeahead([
  {
    name: 'professors',
    prefetch: "/api/typeahead/professors",
    header: "<h3 class='typeahead-suggestion-header'>Professors</h3>",
    template: "<p>{{name}}</p>",
    engine: Hogan
  },
  {
    name: 'courses',
    prefetch: "/api/typeahead/courses",
    header: "<h3 class='typeahead-suggestion-header'>Courses</h3>",
    template: "<p>{{name}}</p>",
    engine: Hogan
  }
  ]).on("keydown", function(e) {
    if (e.which == 13) {
        $("form.big-search").submit();
    }
  });
});