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
      margin = {top: 10, right: 10, bottom: 35, left: 10};

  var x = d3.scale.linear();

  var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom");

  var allStats = [];
  var sortedStats = [];
  d3.json(window.location.protocol + '//' + window.location.hostname
        + (window.location.port ? ':' + window.location.port: '')
        + '/api' + window.location.pathname + '/stats')
      .header('X-CSRFToken', getCookie('csrftoken'))
      .get(function(error, stats) {
        if (error) throw error;

        allStats = stats = JSON.parse(stats);
        for (var key in stats) {
          if (key !== 'comments' &&
              key !== 'date' &&
              key !== 'prof_course_id' &&
              key !== 'hours') {
            sortedStats.push({'key': key, 'stats': stats[key]});
          }
        }
        sortedStats.sort(function(a,b) {
          return questionLookup.keys().indexOf(a.key) -
                 questionLookup.keys().indexOf(b.key);
        });

        if (stats.hasOwnProperty('hours'))
          hoursChart(stats['hours']);

        makeCharts(sortedStats);
      });

  function hoursChart(hoursStats) {
    var margin = {top: 30, right: 10, bottom: 35, left: 30};
    var height = 300 - margin.top - margin.bottom;
    var width = $statsContainer.width() - 30;

    var data = d3.entries(d3.range(13)).map(function (h) {
      if (hoursStats.hasOwnProperty(h.key))
        return {key: +h.key, value: hoursStats[h.key]};

      return {key: +h.key, value: 0};
    });

    var x = d3.scale.linear()
        .domain(d3.extent(data, function (d) { return d.key; }))
        .range([width / data.length / 2, width - width / data.length / 2]);

    var y = d3.scale.linear()
        .domain([0, d3.max(data, function (d) { return d.value; })])
        .range([height, 0]);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient('bottom');

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient('left')
        .ticks(d3.max(data, function (d) { return d.value; }));

    $statsContainer.append('<div><h4>' + questionLookup.get('hours') +
                           '</h4><svg id="hours"></svg></div>');

    var chart = d3.select('#hours')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .attr('class', 'middcourses-chart')
      .append('g')
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    var xAxisEl = chart.append('g')
        .attr('class', 'x axis')
        .attr('transform', 'translate(0,' + height + ')')
        .call(xAxis);

    xAxisEl.append('text')
        .attr('dx', -5)
        .attr('dy', 30)
        .text('hours per week');

    chart.append('g')
        .attr('class', 'y axis')
        .call(yAxis);

    chart.append('g')
        .attr('class', 'y gridlines')
        .call(yAxis.tickFormat('').tickSize(-width, 0, 0))
        .style('stoke', 'grey');

    chart.selectAll('rect')
        .data(data)
      .enter().append('rect')
        .attr('class', 'bar')
        .attr('x', function (d) { return (x(d.key) - width / data.length / 2) + 1; })
        .attr('y', function (d) { return y(d.value)})
        .attr('width', (width / data.length) - 1)
        .attr('height', function (d) { return height - y(d.value)});

    var avgHours = d3.sum(d3.entries(hoursStats), function(d) {
      return +d.key * d.value;
    }) / d3.sum(d3.entries(hoursStats), function (d) { return d.value});

    var avg = chart.append('g')
        .datum(d3.round(avgHours, 1))
        .attr('class', 'avg')
        .attr('transform', function (d) {
          return 'translate(' + x(d) + ',0)';
        });
    avg
      .append('path')
        .attr('stroke-dasharray', '5,5')
        .attr('d', 'M0,-10L0,' + height);
    avg
      .append('text')
        .attr('dx', 3)
        .attr('dy', -5)
        .text(function (d) { return 'Average: ' + d + ' hours'; });
  }

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

  $(window).on('resize', function() {
    $statsContainer.empty();

    if (allStats.hasOwnProperty('hours'))
      hoursChart(allStats['hours']);

    makeCharts(sortedStats);
  });

  // Voting
  $('.upvote, .downvote').on('click', function() {
    var $this = $(this),
        id = $this.parent().data('comment-id'),
        voteType = $this.hasClass('upvote') ? 'up' : 'down';

    $.ajax({
      type: 'POST',
      url: '/api/' + id + '/vote',
      data: {'vote_type': voteType},
      dataType: 'json',
      beforeSend: function(xhr) {
        xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
      },
      success: function(res) {
        var $comment = $('[data-comment-id="' + res.id + '"]')
        if (res.vote_type === 'up') {
          $comment.find('.upvote').addClass('upvote-highlight');
          $comment.find('.downvote').removeClass('downvote-highlight');
        }
        else if (res.vote_type === 'down') {
          $comment.find('.upvote').removeClass('upvote-highlight');
          $comment.find('.downvote').addClass('downvote-highlight');
        }
      }
    });
  });

  var $flagModal = $('#flagModal'),
      $flagModalErrors = $flagModal.find('#errors');
  $('.flag').on('click', function() {
    var id = $(this).data('comment-id'),
        commentBody = $('.comment[data-comment-id="' + id + '"]')
                      .find('.comment-body').text();

    $flagModal.find('#modalCommentBody').text(commentBody);
    $flagModal.data('comment-id', id);
    $flagModal.modal('show');
  });

  $flagModal.on('hidden.bs.modal', function() {
    $('input').attr('checked', false);
    $flagModalErrors.text('').addClass('hide');
  });

  $('#submitFlag').on('click', function() {
    var id = $flagModal.data('comment-id');
    $.ajax({
      type: 'POST',
      url: '/api/' + id + '/flag',
      data: $flagModal.find('#flagForm').serialize(),
      dataType: 'json',
      beforeSend: function(xhr) {
        xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
      },
      success: function(res) {
        if (res.hasOwnProperty('errors')) {
          for (var err in res.errors.why_flag) {
            // Only need to check why_flag, as we only have one field
            $flagModalErrors.text(res.errors.why_flag[err]);
          }
          $flagModalErrors.removeClass('hide');
        }
        else if (res.flagged === true){
          $flagModal.modal('hide');
          $('.comment[data-comment-id="' + res.id + '"]')
            .fadeOut(function() { $(this).remove(); });
        }
      }
    });
  });
});
