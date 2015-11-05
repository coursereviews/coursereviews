var middcourses = middcourses || {};

(function () {
  'use strict';

  middcourses.CatalogView = Backbone.View.extend({
    el: '.catalog',

    itemTemplate: _.template($('#catalog-item-template').html()),

    events: {
      'click .department': 'hideDepartments'
    },

    initialize: function (options) {
      this.activePanel = options.activePanel || 'departments';

      this.$departments = this.$('.departments-list');
      this.$coursesCol1 = this.$('.courses-col-1', this.$courses);
      this.$coursesCol2 = this.$('.courses-col-2', this.$courses);
      this.$professorsCol1 = this.$('.professors-col-1', this.$professors);
      this.$professorsCol2 = this.$('.professors-col-2', this.$professors);

      this.listenTo(middcourses.departments, 'reset', this.addAllDepartments);
      this.listenTo(middcourses.courses, 'reset', this.addAllCourses);
      this.listenTo(middcourses.professors, 'reset', this.addAllProfessors);
      $(window).on('resize', this.render);

      // outside the scope of the view
      $('.departments-back-btn').on('click', this.showDepartments)

      middcourses.departments.fetch({reset: true});
      this.render();
    },

    render: function () {
      // mobile
      if ($(window).width() < 992) {
        this.$('.departments-list, .courses-professors').removeAttr('style');

        // hide the inactive panel on resize

        this.$('.departments').toggleClass('hidden', this.activePanel === 'courses-professors');
        this.$('.courses-professors').toggleClass('hidden', this.activePanel === 'departments');

        // outside the scope of the view
        $('.departments-back').toggleClass('hidden', this.activePanel === 'departments');
        return;
      }

      // desktop

      // make sure both are in view
      this.$('.departments, .courses-professors').removeClass('hidden');

      // make sure departments back button is hidden
      $('.departments-back').addClass('hidden');

      var windowHeight = $(window).height();
      var headerHeight = $('.container:first').height();
      var searchBarHeight = $('.row:first').height();

      this.$('.departments-list, .courses-professors')
        .height(windowHeight - headerHeight - searchBarHeight - 10 /* border */);

      // go back to departments on resize to mobile view
      this.activePanel = 'departments';
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
    },

    showDepartments: function () {
      $('.departments').removeClass('hidden');
      $('.courses-professors').addClass('hidden');
      $('.departments-back').addClass('hidden');

      this.activePanel = 'departments';
    },

    hideDepartments: function () {
      // this is called whenever a department it clicked, so don't do anything
      // if we're not in mobile
      if ($(window).width() >= 992) {
        return;
      }

      $('.departments').addClass('hidden');
      $('.courses-professors').removeClass('hidden');
      $('.departments-back').removeClass('hidden');

      this.activePanel = 'courses-professors';
    }
  });
})();
