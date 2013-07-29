<%inherit file="layout.mako" />

<div class="content">
  <div>
    <table class="valign">
      <tr>
        <td>
          <h1>Tagger demonstration</h1>
        </td>
        <td style="text-align: right">
          <button data-action="random">Fill with random tweet</button>
        </td>
      </tr>
    </table>
    <textarea style="width: 600px; height: 150px; font-size: 1.6em;"></textarea>
    <button data-action="label">Label tweet</button>
    <p class="result">

    </p>
  </div>
</div>


<script>

$('button[data-action="random"]').on('click', function() {
  $.getJSON('/tokenized_labels/sample', function(data) {
    $('textarea').val(data.tweet);
  });
});

$('button[data-action="label"]').on('click', function() {
  var text = $('textarea').val();
  console.log('text-->', text);
  $.post('/tagger/tag', {text: text}, function(result, textStatus, jqXHR) {
    console.log('/tagger/tag result:', result);
    $('p.result').html(result);
  });
});

</script>
