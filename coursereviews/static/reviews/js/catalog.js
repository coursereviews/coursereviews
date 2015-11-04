var middcourses = middcourses || {};

$(function () {
  'use strict';

  middcourses.router = new middcourses.CatalogRouter;
  Backbone.history.start();
});
