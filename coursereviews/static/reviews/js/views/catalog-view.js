var middcourses = middcourses || {};

(function () {
  'use strict';

  middcourses.CatalogView = Backbone.View.extend({
    el: '.catalog',

    itemTemplate: _.template($('#catalog-item-template').html()),

    initialize: function () {
      this.$departments = this.$('.departments');
      this.$coursesCol1 = this.$('.courses-col-1', this.$courses);
      this.$coursesCol2 = this.$('.courses-col-2', this.$courses);
      this.$professorsCol1 = this.$('.professors-col-1', this.$professors);
      this.$professorsCol2 = this.$('.professors-col-2', this.$professors);

      this.listenTo(middcourses.departments, 'reset', this.addAllDepartments);
      this.listenTo(middcourses.courses, 'reset', this.addAllCourses);
      this.listenTo(middcourses.professors, 'reset', this.addAllProfessors);
      $(window).on('resize', this.render);

      middcourses.departments.fetch({reset: true});
      this.render();
    },

    render: function () {
      var windowHeight = $(window).height();
      var headerHeight = $('.container:first').height();
      var searchBarHeight = $('.row:first').height();

      this.$('.departments, .courses-professors')
        .height(windowHeight - headerHeight - searchBarHeight - 10 /* border */);
    },

    addAllDepartments: function () {
      this.$departments.html('');
      middcourses.departments.withCourses().forEach(_.bind(function (department) {
        var view = new middcourses.CatalogItemView({model: department});
        this.$departments.append(view.render().el);
      }, this));
    },

    addAllCourses: function () {
      this.$coursesCol1.html('');
      this.$coursesCol2.html('');

      var limitCol1 = Math.ceil(middcourses.courses.length / 2);
      middcourses.courses.each(_.bind(function (course, i) {
        var view = new middcourses.CatalogItemView({model: course});

        if (i < limitCol1) {
          this.$coursesCol1.append(view.render().el);
        } else {
          this.$coursesCol2.append(view.render().el);
        }
      }, this));
    },

    addAllProfessors: function () {
      this.$professorsCol1.html('');
      this.$professorsCol2.html('');

      var limitCol1 = Math.ceil(middcourses.professors.length / 2);
      middcourses.professors.each(_.bind(function (professor, i) {
        var view = new middcourses.CatalogItemView({model: professor});

        if (i < limitCol1) {
          this.$professorsCol1.append(view.render().el);
        } else {
          this.$professorsCol2.append(view.render().el);
        }
      }, this));
    }
  });
})();
