$(function() {

  var questionLookup = {
    'components': 'What were the primary components of this course?',
    'again': 'Would you take this course again?',
    'hours': 'How many hours per week did you spend preparing for this course?',
    'another': 'Would you take another course with this professor?',
    'grasp': 'How was your grade in relation to your grasp of the material?',
    'prof_lecturing': 'Lecturing',
    'prof_leading': 'Leading discussion',
    'prof_help': 'Providing help',
    'prof_feedback': 'Providing feedback',
    'value': 'Why was this course valuable?',
    'why_take': 'Why did you take this course?'
  }

  // D3.js, display the stats
  var $statsContainer = $("#stats-container")
    , barHeight = 30;

  var makeChart = function(key, data) {
    // Format the data
    var dataArray = [];
    for (k in data) {
      dataArray.push({'key': k, 'value': data[k]});
    }

    var margin = {top: 10, right: 10, bottom: 20, left: 10}
      // Subtract 10 from width because of right border on body
      , width = $statsContainer.width() - 10
      , height = barHeight * dataArray.length
      , el = $statsContainer.append('<div><h4>' + questionLookup[key] + '</h4>'
                                    + '<svg id="' + key + '"></svg></div>');

    var chart = d3.select('#' + key)
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
      .append('g')
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    var x = d3.scale.linear()
        .domain([0, d3.max(dataArray, function(d) { return d.value })])
        .range([0, width]);

    var xAxis = d3.svg.axis()
        .scale(x)
        .ticks(d3.max(dataArray, function(d) { return d.value}))
        .orient('bottom');

    var bar = chart.selectAll('g')
        .data(dataArray)
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
        .text(function(d) { return "" + d.key })

    chart.append('g')
        .attr('class', 'x axis')
        .attr('transform', 'translate(0,' + height + ')')
        .call(xAxis);

  }

  var makeAllCharts = function() {
    $statsContainer.html('');

    for (key in stats) {
      if (key !== 'comments' && key !== 'date' && key !== 'prof_course_id') {
        makeChart(key, stats[key]);
      }
    }
  }

  d3.select(window).on('resize', makeAllCharts);
  
  makeAllCharts();
});
