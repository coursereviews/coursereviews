$(document).ready(function () {
  // Initialize typeahead on the homepage
  $("input#search-bar").typeahead([
  {
    name: 'search',
    local: ["Murray Dry", "Pieter Broucke"]
  }
  ]).on("keydown", function(e) {
    if (e.which == 13) {
        $("form").submit();
    }
  });
});