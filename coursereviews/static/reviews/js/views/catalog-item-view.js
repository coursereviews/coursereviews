var middcourses = middcourses || {};

(function () {
  'use strict';

  middcourses.CatalogItemView = Backbone.View.extend({
    tagName: 'a',

    className: 'list-group-item',

    template: _.template($('#catalog-item-template').html()),

    initialize: function (options) {
      this.listenTo(this.model, 'destroy', this.remove);
      this.listenTo(this.model, 'change', this.render);
    },

    render: function () {
      var context = {
        reviews_count_text: this.reviewCountText(),
        name: this.model.displayName()
      };

      this.$el.html(this.template(context));
      this.$el.addClass(this.model.get('type'));
      this.$el.attr('href', this.model.url());

      this.$el.toggleClass('active', this.model.get('active'));

      return this;
    },

    reviewCountText: function () {
      var count = this.model.get('reviews_count');

      if (count === 1) {
        return count + ' review';
      } else {
        return count + ' reviews';
      }
    }
  });
})();
