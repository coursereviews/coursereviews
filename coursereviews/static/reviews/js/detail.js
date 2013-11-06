  $(function() {
  var keys = {
    value: {
      N: 'Not much',
      A: 'Average',
      V: 'Valuable'
    },
    find: {
      B: 'Boring',
      A: 'Average',
      F: 'Fascinating'
    },
    atmosphere: {
      F: 'Friendly',
      A: 'Average',
      C: 'Competitive'
    },
    deserving: {
      L: 'Lower',
      A: 'Accurate',
      H: 'Higher'
    },
    help: {
      Y: 'Yes',
      N: 'No'
    },
    another: {
      Y: 'Yes',
      N: 'No'
    },
    recommend: {
      Y: 'Yes',
      N: 'No'
    }
  }

  var pluck = function(stooges, value) {
    return $.map(stooges, function(o) { return o.fields[value]; });
  };

  var tally = function(array, field, fieldNames) {
    var vals = pluck(array, field);
    var counts = {};
    for (var i = 0; i < vals.length; i++) {
      if (fieldNames[vals[i]] in counts) {
        counts[fieldNames[vals[i]]]++;
      } else {
        counts[fieldNames[vals[i]]] = 1;
      }
    }
    return counts;
  };

  var Comment = Backbone.Model.extend({});
  var Comments = Backbone.Collection.extend({
    model: Comment
  });
  var CommentView = Backbone.View.extend({
    tagName: "li",
    className: "comment",
    initialize: function() {
      this.listenTo(this.model, "change", this.render);
    },
    render: function() {
      console.log("render world!");
    }
  });

  var value = tally(reviews, 'value', keys.value);
  var find = tally(reviews, 'find', keys.find);
  var atmosphere = tally(reviews, 'atmosphere', keys.atmosphere);
  var deserving = tally(reviews, 'deserving', keys.deserving);
  var help = tally(reviews, 'help', keys.help);
  var another = tally(reviews, 'another', keys.another);
  var recommend = tally(reviews, 'recommend', keys.recommend);
  var commentsArray = _.map(pluck(reviews, 'comment') function(o) { return new Comment(o); });
  var comments = new Comments(commentsArray);

  });
});

// var width = 300,
//     height = 200,
//     radius = Math.min(width, height) / 2;

// var color = d3.scale.category20();

// var pie = d3.layout.pie()
//     // .value(function(d) { return d; })
//     .sort(null);

// var arc = d3.svg.arc()
//     // .innerRadius(radius - 100)
//     .outerRadius(radius - 20);

// var svg = d3.select("#review-body").append("svg")
//     .attr("width", width)
//     .attr("height", height)
//   .append("g")
//     .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

// var data = tally(reviews, 'atmosphere');
// console.log(data);
// var path = svg.datum(data).selectAll("path")
//     .data(pie)
//   .enter().append("path")
//     .attr("fill", function(d, i) { return color(i); })
//     .attr("d", arc)
//     .each(function(d) { this._current = d; }); // store the initial angles

// d3.selectAll("input")
// .on("change", change);

// var timeout = setTimeout(function() {
//   d3.select("input[value=\"oranges\"]").property("checked", true).each(change);
// }, 2000);

// function change() {
//   var value = this.value;
//   clearTimeout(timeout);
//   pie.value(function(d) { return d[value]; }); // change the value function
//   path = path.data(pie); // compute the new angles
//   path.transition().duration(750).attrTween("d", arcTween); // redraw the arcs
// }

// function type(d) {
//   d.apples = +d.apples;
//   d.oranges = +d.oranges;
//   return d;
// }

// Store the displayed angles in _current.
// Then, interpolate from _current to the new angles.
// During the transition, _current is updated in-place by d3.interpolate.
// function arcTween(a) {
//   var i = d3.interpolate(this._current, a);
//   this._current = i(0);
//   return function(t) {
//     return arc(i(t));
//   };
// }