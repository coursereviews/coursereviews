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
      margin = {top: 10, right: 10, bottom: 20, left: 10};

  var x = d3.scale.linear();

  var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom");

  var sortedStats = [];
  d3.json(window.location.protocol + '//' + window.location.hostname
        + (window.location.port ? ':' + window.location.port: '')
        + '/api' + window.location.pathname + '/stats')
      .header('X-CSRFToken', getCookie('csrftoken'))
      .get(function(error, stats) {
        if (error) throw error;

        stats = JSON.parse(stats);
        for (var key in stats) {
          if (key !== 'comments' &&
              key !== 'date' &&
              key !== 'prof_course_id') {
            sortedStats.push({'key': key, 'stats': stats[key]});
          }
        }
        sortedStats.sort(function(a,b) {
          return questionLookup.keys().indexOf(a.key) - 
                 questionLookup.keys().indexOf(b.key);
        });

        makeCharts(sortedStats);
      });

  function makeCharts(stats) {
    // Subtract 10 from width because of right border on body
    width = $statsContainer.width() - 10;

    x.range([0, width]);

    stats.forEach(function(d) {
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
          .text(function(d) { return '' + d.key });

      chart.append('g')
          .attr('class', 'x axis')
          .attr('transform', 'translate(0,' + height + ')')
          .call(xAxis)
        .append('text')
          .attr('transform', 'translate(8,18)')
          .text('votes');
    });
  }

  $(window).on("resize", function() {
    $statsContainer.empty();
    makeCharts(sortedStats);
  });
});
