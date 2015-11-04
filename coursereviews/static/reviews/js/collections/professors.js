var middcourses = middcourses || {};

(function () {
  'use strict';

  var Professors = Backbone.Collection.extend({
    model: middcourses.Professor,

    url: function () {
      return '/api/professors?' + $.param({department: middcourses.department});
    }

  });

  middcourses.professors = new Professors;
})();
