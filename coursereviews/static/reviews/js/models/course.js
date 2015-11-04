var middcourses = middcourses || {};

(function () {
  'use strict';

  middcourses.Course = Backbone.Model.extend({
    initialize: function () {
      this.set('type', 'course');
      this.set('active', false);
    },

    url: function () {
      return '/course/' + this.get('slug');
    },

    displayName: function () {
      return this.get('title');
    }
  });

})();
