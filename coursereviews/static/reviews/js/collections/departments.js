var middcourses = middcourses || {};

(function () {
  'use strict';

  var Departments = Backbone.Collection.extend({
    model: middcourses.Department,

    url: '/api/departments',

    comparator: function (a, b) {
      return a.displayName().localeCompare(b.displayName());
    },

    withCourses: function () {
      return this.where({has_courses: true});
    },

    withProfessors: function () {
      return this.where({has_professors: true});
    }
  });

  middcourses.departments = new Departments();
})();
