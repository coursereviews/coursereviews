var middcourses = middcourses || {};

(function () {
  'use strict';

  middcourses.Professor = Backbone.Model.extend({
    initialize: function () {
      this.set('type', 'professor');
      this.set('active', false);
    },

    url: function () {
      return '/professor/' + this.get('slug');
    },

    displayName: function () {
      return this.get('name');
    }
  });

})();
