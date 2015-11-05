var professors = new Bloodhound({
  datumTokenizer: Bloodhound.tokenizers.whitespace,
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  remote: {
    url: '/api/search?type=professor&q=%QUERY',
    wildcard: '%QUERY'
  }
});

var courses = new Bloodhound({
  datumTokenizer: Bloodhound.tokenizers.whitespace,
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  remote: {
    url: '/api/search?type=course&q=%QUERY',
    wildcard: '%QUERY'
  }
});

$(document).ready(function () {
  $("input#search-bar").typeahead(null,
    {
      name: 'courses',
      source: courses,
      templates: {
        header: "<h3 class='typeahead-suggestion-header'>Courses</h3>",
        suggestion: _.template('<a href="<%- url %>"><p><%- code %>: <%- title %></span></p></a>'),
      },
      display: _.template('<%- code %>: <%- title %>'),
      minLength: 3,
      limit: 10
    },
    {
      name: 'professors',
      source: professors,
      templates: {
        header: "<h3 class='typeahead-suggestion-header'>Professors</h3>",
        suggestion: _.template('<a href="<%- url %>"><p><%- name %></span></p></a>'),
      },
      display: _.template('<%- name %>'),
      minLength: 3,
      limit: 10
    }
  )
  .on('typeahead:select', function (event, obj) {
    window.location = obj.url;
  });
});
