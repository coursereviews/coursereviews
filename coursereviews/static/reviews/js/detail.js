$(function() {

  var questionLookup = d3.map({
    'hours': 'How many hours per week did you spend preparing for this course?',
    'again': 'Would you take this course again?',
    'another': 'Would you take another course with this professor?',
    'grasp': 'How was your grade in relation to your grasp of the material?',
    'prof_lecturing': 'Lecturing',
    'prof_leading': 'Leading discussion',
    'prof_help': 'Providing help',
    'prof_feedback': 'Providing feedback',
    'components': 'What were the primary components of this course?',
    'value': 'Why was this course valuable?',
    'why_take': 'Why did you take this course?'
  });

  // D3.js, display the stats
  var $statsContainer = $("#stats-container"),
      barHeight = 30,
      margin = {top: 10, right: 10, bottom: 20, left: 10},
      // Subtract 10 from width because of right border on body
      width = $statsContainer.width() - 10;

  var x = d3.scale.linear()
      .range([0, width]);

  var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom");

  var sortedStats = [];
  for (var key in stats) {
    if (key !== 'comments' &&
        key !== 'date' &&
        key !== 'prof_course_id') {
      sortedStats.push({'key': key, 'stats': stats[key]});
    }
  }
  sortedStats.sort(function(a,b) { return questionLookup.keys().indexOf(a.key) - questionLookup.keys().indexOf(b.key); });

  sortedStats.forEach(function(d) {
      var data = [];
      for (var k in d.stats) {
        data.push({'key': k, 'value': d.stats[k]});
      }

      if (d.key === 'prof_lecturing') {
        $statsContainer.append('<div><h4>Evaluate the professor in the following areas:</h4></div>');
      }

      if (d.key === 'prof_lecturing' ||
          d.key === 'prof_leading' ||
          d.key === 'prof_help' ||
          d.key === 'prof_feedback') {
        $statsContainer.append('<div><h5>' + questionLookup.get(d.key) + '</h5>'
                             + '<svg id="' + d.key + '"></svg></div>');
      } else {
        $statsContainer.append('<div><h4>' + questionLookup.get(d.key) + '</h4>'
                             + '<svg id="' + d.key + '"></svg></div>');
      }

      var height = barHeight * data.length;

      var chart = d3.select('#' + d.key)
          .data(data)
          .attr('width', width + margin.left + margin.right)
          .attr('height', height + margin.top + margin.bottom)
          .attr('class', 'middcourses-chart')
        .append('g')
          .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

      x.domain([0, d3.max(data, function(d) { return d.value })]);

      xAxis.ticks(d3.max(data, function(d) { return d.value}));

      var bar = chart.selectAll('g')
          .data(data)
        .enter().append('g')
          .attr('class', 'bar')
          .attr('transform', function(d, i) { return 'translate(0,' + i * barHeight + ')'; });

      bar.append('rect')
          .attr('width', function(d) { return x(d.value) })
          .attr('height', barHeight - 1);

      bar.append('text')
          .attr('x', function(d) { return x(d.value) - 10 })
          .attr('y', barHeight / 2 - 1)
          .attr('dy', '.35em')
          .attr('text-anchor', 'end')
          .text(function(d) { return "" + d.key });

      chart.append('g')
          .attr('class', 'x axis')
          .attr('transform', 'translate(0,' + height + ')')
          .call(xAxis)
        .append('text')
          .attr('transform', 'translate(8,18)')
          .text('votes');
  });

  var charts = d3.selectAll('.middcourses-chart');
  d3.select(window).on('resize', function() {
    var newWidth = $statsContainer.width() - 10;

    charts.attr('width', newWidth + margin.left + margin.right);

    x.range([0, newWidth]);

    charts.select('rect').attr('width', function(d) { return x(d.value); });
    charts.select('text').attr('x', function(d) { return x(d.value) - 10; });

    charts.select('g.x.axis').remove();
    charts.append('g')
        .attr('class', 'x axis')
        .attr('transform', function(d) { 
          var rects = $(this.parentNode).find('rect');
          return 'translate(10,' + (rects.length * barHeight + 10) + ')'; 
        })
        .call(xAxis)
      .append('text')
        .attr('transform', 'translate(8,18)')
        .text('votes');
  });
});
