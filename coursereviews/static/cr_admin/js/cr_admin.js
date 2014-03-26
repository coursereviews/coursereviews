$(function() {
  $('tr.flagged-review-row').on('click', function() {
    var id = $(this).data('review-id');
    window.location.href = '/admin/review/' + id;
  });
});