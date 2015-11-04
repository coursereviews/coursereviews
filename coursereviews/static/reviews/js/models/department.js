var middcourses = middcourses || {};

(function () {
  'use strict';

  middcourses.Department = Backbone.Model.extend({
    initialize: function () {
      this.set('type', 'department');
      this.set('active', +middcourses.department === this.get('id'));
    },

    displayName: function () {
      return this.get('display_name') === null
        ? this.get('name')
        : this.get('display_name');
    },

    url: function () {
      return this.get('url');
    }
  });

})();
