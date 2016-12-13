<?php

    $oldsite=$_POST["old"];
    $newsite=$_POST["new"];
    $page=$_POST["page"];

//    echo $oldsite . " -- " . $newsite . " -- " . $page;

    $old = file_get_contents($oldsite . "/" . $page . ".json");
    $new = file_get_contents($newsite . "/" . $page . ".json");

//    echo $old . "<br/>" . $new;
    
?>

<html>
<head>
    <title>JSON Diff</title>
    <link rel="stylesheet" href="master.css" type="text/css" media="screen" title="no title" charset="utf-8">
    <script type="text/javascript" charset="utf-8">
        // THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
        // WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
        // COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
        // OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        var jsonBoxA, jsonBoxB;

        var HashStore = {
            load : function(callback) {
                if (window.location.hash) {
                    try {
                        var hashObject = JSON.parse(decodeURIComponent(window.location.hash.slice(1)));
                        callback && callback(hashObject.d);
                        return;
                    } catch (e) {
                        console.log()
                    }
                }
                callback && callback(null);
            },
            sync : function(object) {
                var hashObject = { d : object };
                window.location.hash = "#" + encodeURIComponent(JSON.stringify(hashObject));
            }
        };

        function init() {
            document.addEventListener("click", clickHandler, false);

            jsonBoxA = document.getElementById("jsonA");
            jsonBoxB = document.getElementById("jsonB");

            HashStore.load(function(data) {
                if (data) {
                    jsonBoxA.value = data.a;
                    jsonBoxB.value = data.b;
                }
            });

            startCompare();
        }

        function swapBoxes() {
            var tmp = jsonBoxA.value;
            jsonBoxA.value = jsonBoxB.value;
            jsonBoxB.value = tmp;
        }

        function clearBoxes() {
            jsonBoxA.value = "";
            jsonBoxB.value = "";
        }

        function startCompare() {
            var aValue = jsonBoxA.value;
            var bValue = jsonBoxB.value;

            var objA, objB;
            try {
                objA = JSON.parse(aValue);
                jsonBoxA.style.backgroundColor = "";
            } catch(e) {
                jsonBoxA.style.backgroundColor = "rgba(255,0,0,0.5)";
            }
            try {
                objB = JSON.parse(bValue);
                jsonBoxB.style.backgroundColor = "";
            } catch(e) {
                jsonBoxB.style.backgroundColor = "rgba(255,0,0,0.5)";
            }

            HashStore.sync({
                a : aValue,
                b : bValue
            });

            results = document.getElementById("results");
            removeAllChildren(results);

            compareTree(objA, objB, "root", results);
        }

        function compareTree(a, b, name, results) {
            var typeA = typeofReal(a);
            var typeB = typeofReal(b);

            var typeSpanA = document.createElement("span");
            typeSpanA.appendChild(document.createTextNode("("+typeA+")"))
            typeSpanA.setAttribute("class", "typeName");

            var typeSpanB = document.createElement("span");
            typeSpanB.appendChild(document.createTextNode("("+typeB+")"))
            typeSpanB.setAttribute("class", "typeName");

            var aString = (typeA === "object" || typeA === "array") ? "" : String(a) + " ";
            var bString = (typeB === "object" || typeB === "array") ? "" : String(b) + " ";

            var leafNode = document.createElement("span");
            leafNode.appendChild(document.createTextNode(name));
            if (a === undefined) {
                leafNode.setAttribute("class", "added");
                leafNode.appendChild(document.createTextNode(": " + bString));
                leafNode.appendChild(typeSpanB);
            }
            else if (b === undefined) {
                leafNode.setAttribute("class", "removed");
                leafNode.appendChild(document.createTextNode(": " + aString));
                leafNode.appendChild(typeSpanA);
            }
            else if (typeA !== typeB || (typeA !== "object" && typeA !== "array" && a !== b)) {
                leafNode.setAttribute("class", "changed");
                leafNode.appendChild(document.createTextNode(": " + aString));
                leafNode.appendChild(typeSpanA);
                leafNode.appendChild(document.createTextNode(" => "+ bString));
                leafNode.appendChild(typeSpanB);
            }
            else {
                leafNode.appendChild(document.createTextNode(": " + aString));
                leafNode.appendChild(typeSpanA);
            }

            if (typeA === "object" || typeA === "array" || typeB === "object" || typeB === "array") {
                var keys = [];
                for (var i in a) {
                    if (a.hasOwnProperty(i)) {
                        keys.push(i);
                    }
                }
                for (var i in b) {
                    if (b.hasOwnProperty(i)) {
                        keys.push(i);
                    }
                }
                keys.sort();

                var listNode = document.createElement("ul");
                listNode.appendChild(leafNode);

                for (var i = 0; i < keys.length; i++) {
                    if (keys[i] === keys[i-1]) {
                        continue;
                    }
                    var li = document.createElement("li");
                    listNode.appendChild(li);

                    compareTree(a && a[keys[i]], b && b[keys[i]], keys[i], li);
                }
                results.appendChild(listNode);
            }
            else {
                results.appendChild(leafNode);
            }
        }

        function removeAllChildren(node) {
            var child;
            while (child = node.lastChild) {
                node.removeChild(child);
            }
        }

        function isArray(value) {
            return value && typeof value === "object" && value.constructor === Array;
        }
        function typeofReal(value) {
            return isArray(value) ? "array" : typeof value;
        }

        function clickHandler(e) {
            var e = e || window.event;
            if (e.target.nodeName.toUpperCase() === "UL") {
                if (e.target.getAttribute("closed") === "yes")
                    e.target.setAttribute("closed", "no");
                else
                    e.target.setAttribute("closed", "yes");
            }
        }
    </script>
</head>
<body onload="init();">
    <h2>JSON Diff</h2>
    <div class="contentbox" id="instructions">
        <ul>
            <li>Paste some JSON in each of the text fields. Click "Compare" to see the diff.</li>
            <li>Changed portions are displayed in <span class="changed">yellow</span>. Additions are displayed in <span class="added">green</span>. Deletions are displayed in <span class="removed">red</span>.</li>
              <li>It also works as a JSON viewer. Click the disclosure triangles to display/hide portions of the JSON.</li>
            <li>Invalid JSON is indicated by the text fields turning red.</li>
            <li>Swap the contents of the text areas by clicking "Swap". Clear them by clicking "Clear".</li>
        </ul>
    </div>
    <div class="contentbox" id="inputs">
        <!--
        <?php echo $old; ?> 
        =====================================================================================
        <?php echo $new; ?>
         -->
        
        <textarea id="jsonA"><?php echo $old; ?></textarea>
        <textarea id="jsonB"><?php echo $new; ?></textarea>
            <input type="button" value="Compare" id="compare" onclick="startCompare();" />
            <input type="button" value="Swap" id="swap" onclick="swapBoxes();"/>
            <input type="button" value="Clear" id="clear" onclick="clearBoxes();"/>
    </div>
    <div class="contentbox" id="results">
    </div>
        <div class="contentbox" id="issues">
            <h3>About</h3>
            <p>JSON Diff is a simple way to visualize and compare <a href="http://json.org">JSON</a>.</p>
            <h3>Known Issues</h3>
            <ul>
                <li>Diff algorithm not very intelligent when dealing with arrays</li>
                <li>Probably doesn't work in IE</li>
            </ul>
        </div>

    <h3><a name="comment">comment</a> <a href="#top">^</a></h3>

<div id="disqus_thread"></div>
<script type="text/javascript" charset="utf-8">
    var disqus_developer = true;
</script>
<script type="text/javascript" src="http://disqus.com/forums/tlrobinson/embed.js"></script>
<noscript><p><a href="http://tlrobinson.disqus.com/?url=ref">View the forum thread.</a></p></noscript>
<div id="footer">
    <p>
        
<a href="http://news.ycombinator.com/" onclick="window.location='http://news.ycombinator.com/submitlink?u='+encodeURIComponent(document.location)+'&amp;t='+encodeURIComponent(document.title); return false">
    <img alt="Submit to Reddit" src="/images/badge-hn.png" height="15" width="80">
</a>

<a href="http://www.reddit.com/submit" onclick="window.location='http://www.reddit.com/submit?url='+encodeURIComponent(document.location)+'&amp;title='+encodeURIComponent(document.title); return false">
    <img alt="Submit to Hacker News" src="/images/badge-reddit.png" height="15" width="80">
</a>

<a href="http://ycombinator.com/">
    <img alt="Y Combinator" src="/images/badge-yc.png" height="15" width="80">
</a>

<a href="http://catb.org/~esr/faqs/hacker-howto.html#what_is">
    <img alt="How To Become A Hacker" src="http://catb.org/hacker-emblem/hacker.png" height="15" width="80">
</a>

<!-- <a href="http://www.dreamhost.com/green.cgi">
    <img alt="Green Web Hosting! This site hosted by DreamHost." src="https://secure.newdream.net/green3.gif" height="15" width="80">
</a> -->

<a rel="license" href="http://creativecommons.org/licenses/by-nc/3.0/us/">
    <img alt="Creative Commons License" src="/images/badge-cc-by-nc.png" height="15" width="80">
</a>

<a href="http://validator.w3.org/check?uri=referer">
    <img alt="Valid HTML 4.01 Strict" src="/images/badge-w3c.png" height="15" width="80">
</a>


<!-- <script type="text/javascript" src="http://www.cornify.com/js/cornify.js"></script>
<a href="#" onclick="cornify_add();return false;"><img src="http://www.cornify.com/assets/cornify.gif" width="61" height="16" border="0" alt="Cornify"></a> -->

<br />
<br />

<iframe
    src="http://www.facebook.com/plugins/like.php?href=http%3A%2F%2Ftlrobinson.net%2Fprojects%2Fjavascript-fun%2Fjsondiff%2F&amp;layout=standard&amp;show_faces=true&amp;width=450&amp;action=like&amp;font=verdana&amp;colorscheme=light"
    scrolling="no" frameborder="0" allowTransparency="true"
    style="border:1px; overflow:hidden; width:450px; height:px;">
</iframe>    </p>
    <p>
        &copy; 2006-2010 Thomas Robinson.&nbsp;<a rel="license" href="http://creativecommons.org/licenses/by-nc/3.0/us/">Some rights reserved</a>.    </p>
</div>
<script type="text/javascript">
    var _gaq = _gaq || [];
    _gaq.push(['_setAccount', 'UA-1520701-1']);
    _gaq.push(['_trackPageview']);

    (function() {
        var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
        ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
        (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(ga);
    })();
</script>

<script type='text/javascript'> var mp_protocol = (('https:' == document.location.protocol) ? 'https://' : 'http://'); document.write(unescape('%3Cscript src="' + mp_protocol + 'api.mixpanel.com/site_media/js/api/mixpanel.js" type="text/javascript"%3E%3C/script%3E')); </script> <script type='text/javascript'> try {  var mpmetrics = new MixpanelLib('3889b1fe2f191cc24ce4c542efeffd2e'); } catch(err) { null_fn = function () {}; var mpmetrics = {  track: null_fn,  track_funnel: null_fn,  register: null_fn,  register_once: null_fn, register_funnel: null_fn }; } </script>

</body>
</html>
