
/*
Wikish 0.1
Phil Jones

Wikish is a wiki markup, derived from UseMod's and adapted for my earlier personal wiki software : SdiDesk.

This is the beginning of my adaptation of it for Smallest Federated Wiki, so that I can port my existing wikis to SFW

Summary
= h1 =
== h2 == 
etc.

''italic''
'''bold'''

* list item
** second level list item

CamelCase becomes link
*/

(function() {

  window.plugins.wikish = {
    emit: function(div, item) {
      var mp, p, text;
      mp = new MarkupProcessor('');
      text = mp.page(item.text);
      text = wiki.resolveLinks(text);
      p = $("<p/>").append(text);
      return div.append(p);
    },
    bind: function(div, item) {
      return div.dblclick(function() {
        return wiki.textEditor(div, item);
      });
    }
  };

  this.MarkupProcessor = (function() {

    function MarkupProcessor(root) {
      this.root = root;
      this.raw = "";
      this.cooked = "";
      this.blm = /^\s*$/;
      this.hr = /^----\s*$/;
      this.h6 = /^======(.*)?======\s*$/;
      this.h5 = /^=====(.*)?=====\s*$/;
      this.h4 = /^====(.*)?====\s*$/;
      this.h3 = /^===(.*)?===\s*$/;
      this.h2 = /^==(.*)?==\s*$/;
      this.h1 = /^=(.*)?=\s*$/;
      this.bold = /'''([^']*)?'''/g;
      this.italic = /''([^']*)?''/g;
      this.wikiword = /([A-Z][a-z]+([A-Z][a-z]+)+)/g;
      this.indent = 0;
    }

    MarkupProcessor.prototype.line = function(l) {
      var nl;
      nl = l;
      nl = nl.replace(this.blm, "<br/>\n");
      nl = nl.replace(this.hr, "<hr>");
      nl = nl.replace(this.bold, "<b>$1</b>");
      nl = nl.replace(this.italic, "<i>$1</i>");
      nl = nl.replace(this.h6, "<h6>$1</h6>");
      nl = nl.replace(this.h5, "<h5>$1</h5>");
      nl = nl.replace(this.h4, "<h4>$1</h4>");
      nl = nl.replace(this.h3, "<h3>$1</h3>");
      nl = nl.replace(this.h2, "<h2>$1</h2>");
      nl = nl.replace(this.h1, "<h1>$1</h1>");
      return nl;
    };

    MarkupProcessor.prototype.check = function(s) {
      if (s.charAt(s.length - 1) === '*') {
        s = s.substring(0, s.length - 1);
        s = "<strike>" + s + "</strike>";
      }
      return s;
    };

    MarkupProcessor.prototype.outlineFilter = function(l) {
      var count, meat, s;
      if (l[0] !== "*") {
        if (this.indent > 0) {
          s = Array(1 + this.indent).join("</ul>");
          this.indent = 0;
          l = s + "\n" + l;
        }
        return l;
      }
      count = 0;
      while (l[count] === "*") {
        count = count + 1;
      }
      meat = l.substring(count);
      if (count === this.indent) {
        return (Array(this.indent + 1).join(" ")) + "<li>" + this.check(meat) + "</li>";
      }
      if (count > this.indent) {
        this.indent = this.indent + 1;
        return "<ul>\n" + (Array(this.indent + 1).join(" ")) + "<li>" + this.check(meat) + "</li>";
      }
      s = (Array((1 + this.indent) - count).join("</ul>")) + "<li>" + this.check(meat) + "</li>\n";
      this.indent = count;
      return s;
    };

    MarkupProcessor.prototype.page = function(p) {
      var l, lines;
      this.raw = p;
      lines = (function() {
        var _i, _len, _ref, _results;
        _ref = p.split("\n");
        _results = [];
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          l = _ref[_i];
          _results.push(this.line(l));
        }
        return _results;
      }).call(this);
      lines = (function() {
        var _i, _len, _results;
        _results = [];
        for (_i = 0, _len = lines.length; _i < _len; _i++) {
          l = lines[_i];
          _results.push(this.outlineFilter(l));
        }
        return _results;
      }).call(this);
      this.cooked = lines.join('\n');
      return this.cooked;
    };

    return MarkupProcessor;

  })();

  /*
  To pull from other usemods
  */

  this.UseModGateway = (function() {

    function UseModGateway(base, urlPattern) {
      this.urlPattern = urlPattern;
      this.baseUrl = base + "?action=browse&raw=1&id=";
      this.chef = new MarkupProcessor(this.urlPattern);
    }

    UseModGateway.prototype.get = function(word, id, title) {
      var _this = this;
      return $.get(this.baseUrl + word, function(data) {
        $('#' + id).html(_this.chef.page(data));
        return $('#' + title).text(word);
      });
    };

    return UseModGateway;

  })();

  this.Transcluder = (function() {

    function Transcluder(url, dict) {
      $.ajax(url, {
        type: 'GET',
        dataType: 'html',
        error: function(jqXHR, textStatus, errorThrown) {
          console.log(textStatus);
          return console.log(errorThrown);
        },
        success: function(data, textStatus, jqXHR) {
          console.log(textStatus);
          console.log(text);
          return dict["cache"] = text;
        }
      });
    }

    return Transcluder;

  })();

}).call(this);
