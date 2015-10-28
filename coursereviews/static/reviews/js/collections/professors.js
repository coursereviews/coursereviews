var middcourses = middcourses || {};

(function () {
  'use strict';

  var Professors = Backbone.Collection.extend({
    model: middcourses.Professor,

    url: '/api/professors'

  });
})();
