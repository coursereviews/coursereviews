var middcourses = middcourses || {};

(function () {
  'use strict';

  var Courses = Backbone.Collection.extend({
    model: middcourses.Course,

    url: function () {
      return '/api/courses?' + $.param({department: middcourses.department});
    }

  });

  middcourses.courses = new Courses;
})();
