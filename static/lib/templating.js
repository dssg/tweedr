// Copyright 2013, Christopher Brown <io@henrian.com>, MIT Licensed
// https://github.com/chbrown/misc-js :: templating.js
"use strict"; /*jslint indent: 2 */ /*globals _, $, Backbone, Handlebars */

// Templates debug / caching. E.g.:
// new TemplateManager({
//   cache: window.DEBUG ? Handlebars.templates : {},
//   url: '/templates/',
//   extension: '.bars',
//   compile: Handlebars.compile
// });
function TemplateManager(opts) {
  this.cache = opts.cache || {}; // optional, defaults to {}
  this.url = opts.url || '/'; // where to look for templates
  this.extension = opts.extension || ''; // append to given template names
  this.querystring = opts.querystring || '?t=' + (new Date()).getTime(); // aka., url.search
  this.compile = opts.compile || null; // what to use for cache misses
}
TemplateManager.prototype.render = function(template_name, context) {
  // synchronous; returns html.
  var self = this;
  var cached_template = this.cache[template_name];
  // only cache once per page load
  if (!cached_template) {
    $.ajax({
      url: this.url + template_name + this.extension + this.querystring,
      async: false,
      success: function(template_src) {
        cached_template = self.compile(template_src);
      }
    });
    // yes, the above *will* execute synchronously!
    this.cache[template_name] = cached_template;
  }
  return cached_template(context);
};

// handlebars_manager is a global this file offers. requires `Handlebars` to be loaded.
var HandlebarsTemplates = new TemplateManager({
  cache: window.DEBUG ? Handlebars.templates : {},
  url: '/templates/',
  extension: '.bars',
  compile: Handlebars.compile
});
var Templates = HandlebarsTemplates;

// requires Backbone and handlebars_manager
var TemplatedView = Backbone.View.extend({
  // TemplatedView has hooks called (pre|post)(Initialize|Render), each of which take a context
  //   that context is just the model and whatever options the view is initialized with.
  // preInitialize, postInitialize, preRender, postRender
  initialize: function(opts) {
    // prePreRender
    var ctx = _.extend(this.model ? this.model.toJSON() : {}, opts);
    if (this.preInitialize) this.preInitialize(ctx);
    this.render(ctx);
    if (this.postInitialize) this.postInitialize(ctx);
  },
  render: function(ctx) {
    if (this.preRender) this.preRender(ctx);
    this.el.innerHTML = Templates.render(this.template, ctx);
    if (this.postRender) this.postRender(ctx);
    if (ctx.replace) {
      // if .replace is given, it's the parent node that this new view should
      // attach to, replacing the old contents.
      ctx.replace.replaceWith(this.$el);
    }
    return this;
  }
});

var TemplatedCollection = Backbone.Collection.extend({
  renderTo: function($el, View) {
    var fragment = document.createDocumentFragment();
    this.each(function(model) {
      var ctx = model.toJSON();
      ctx.model = model;
      var view = new View(ctx);
      fragment.appendChild(view.el);
    });
    $el.append(fragment);
  }
});
