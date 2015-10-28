var middcourses = middcourses || {};

(function () {
  'use strict';

  middcourses.Courses = Backbone.Collection.extend({
    model: middcourses.Course,

    url: '/api/courses'

  });
})();
