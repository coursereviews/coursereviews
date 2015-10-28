var middcourses = middcourses || {};

(function () {
  'use strict';

  middcourses.Department = Backbone.Model.extend({
    initialize: function () {
      this.set('type', 'department');
      this.set('active', false);
    },

    displayName: function () {
      return this.get('display_name') === null
        ? this.get('name')
        : this.get('display_name');
    },

    url: function () {
      return '#/departments/' + this.get('slug')
    }
  });

})();
