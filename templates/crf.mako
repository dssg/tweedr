<%inherit file="layout.mako" />

<div class="content">
  <div style="width: 600px;">
    <button style="float: right" class="random">Fill with random tweet</button>
    <h1>Tagger demonstration</h1>
  </div>

  <form style="width: 600px;">
    <textarea style="width: 100%; height: 150px; font-size: 1.5em;"></textarea>
    <button>Label tweet</button>
  </form>

  <div class="tweet"></div>
</div>

<script>
DEBUG = true;
// really naive localStorage shim
if (!window.localStorage) window.localStorage = {};

$('button.random').on('click', function() {
  $.getJSON('/tokenized_labels/sample', function(data) {
    var text = data.tweet;
    $('form textarea').val(text);
    tagAndDisplay(text);
  });
});

$('form').on('submit', function(ev) {
  ev.preventDefault();

  var text = $('form textarea').val();
  tagAndDisplay(text);
});


var SequencedText = Backbone.Model.extend({
  // usually has properties: text (a String), sequences (an array of arrays of strings)
  tag: function(callback) {
    // callback signature: function(err)
    var self = this;
    $.post('/tagger/tag', {text: this.get('text')}, function(result) {
      // result is the JSON representation of a row from labelized_token
      self.set('sequences', result.sequences)
      callback(null);
    });
  }
});

var SequencedTextView = TemplatedView.extend({
  template: 'gloss',
  events: {},
});

function tagAndDisplay(text) {
  // callback signature: function(err, tweet_view)
  var sequenced_text = new SequencedText({text: text});
  sequenced_text.tag(function(err) {
    new SequencedTextView({model: sequenced_text, el: $('.tweet')});
  });
}

$(function() {
  if (localStorage.text) {
    tagAndDisplay(localStorage.text);
  }
  else {
    $('button.random').trigger('click');
  }
});
</script>
