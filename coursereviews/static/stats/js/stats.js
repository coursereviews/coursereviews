function timeseriesChart() {
  var margin = {top: 20, right: 20, bottom: 50, left: 30},
      width = 945,
      height = 155,
      xScale = d3.time.scale(),
      yScale = d3.scale.linear(),
      xAxis = d3.svg.axis().scale(xScale).orient('bottom').tickFormat(d3.time.format('%m/%d')),
      yAxis = d3.svg.axis().scale(yScale).orient('left').ticks(5),
      yGridLines = d3.svg.axis()
          .scale(yScale)
          .orient('left')
          .ticks(5)
          .tickFormat(""),
      line = d3.svg.line().x(X).y(Y);

  function chart(selection) {
    selection.each(function () {

      var data = JSON.parse(d3.select(this).select('svg').attr('data-timeseries'));

      var parse = d3.time.format('%Y-%m-%d').parse;

      data = data.map(function (d) {
        return [parse(d[0]), d[1]];
      });

      xScale
          .domain(d3.extent(data, function (d) { return d[0]; }))
          .range([0, width - margin.left - margin.right]);

      yScale
          .domain([0, d3.max(data, function (d) { return d[1]; })])
          .range([height - margin.top - margin.bottom, 0]);

      yGridLines.tickSize(-width + margin.left + margin.right)

      var svg = d3.select(this).select('svg').data([data])
          .attr('width', width)
          .attr('height', height)
        .append('g')
          .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

      svg.append('g')
          .attr('class', 'y gridlines')
          .call(yGridLines);

      svg.append('g')
          .attr('class', 'y axis')
          .call(yAxis);

      svg.append('g')
          .attr('class', 'x axis')
          .attr('transform', 'translate(0,' + (height - margin.top - margin.bottom) + ')')
          .call(xAxis);

      svg.append('path')
          .attr('d', line);
    });
  }

  function X(d) {
    return xScale(d[0]);
  }

  function Y(d) {
    return yScale(d[1]);
  }

  chart.width = function (value) {
    if (!arguments.length) return width;
    width = value;
    return chart;
  };

  chart.height = function (value) {
    if (!arguments.length) return height;
    height = value;
    return chart;
  };

  return chart;
}

var timeseries = timeseriesChart()
    .height($('#reviews .timeseries').height())
    .width($('#reviews .timeseries').width());

d3.selectAll('#reviews .timeseries, #users .timeseries').call(timeseries);