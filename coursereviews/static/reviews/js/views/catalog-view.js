var middcourses = middcourses || {};

(function () {
  'use strict';

  middcourses.CatalogView = Backbone.View.extend({
    el: '.catalog',

    itemTemplate: _.template($('#catalog-item-template').html()),

    initialize: function () {
      this.$departments = this.$('.departments');
      this.$courses = this.$('.courses');
      this.$coursesCol1 = this.$('.courses-col-1', this.$courses);
      this.$coursesCol2 = this.$('.courses-col-2', this.$courses);
      this.$professorsCol1 = this.$('.professors-col-1', this.$professors);
      this.$professorsCol2 = this.$('.professors-col-2', this.$professors);

      this.listenTo(middcourses.departments, 'reset', this.addAllDepartments);

      middcourses.departments.fetch({reset: true});
    },

    render: function () {

    },

    addAllDepartments: function () {
      this.$departments.html('');
      middcourses.departments.withCourses().forEach(_.bind(function (department) {
        var view = new middcourses.CatalogItemView({model: department});
        this.$departments.append(view.render().el);
      }, this));
    }
  });
})();
