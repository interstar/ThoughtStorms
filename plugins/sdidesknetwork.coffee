###

SdiDesk Network diagrams

###


window.plugins.sdidesknetwork =
    emit: (div, item) ->
        wiki.getScript '/js/d3/d3.js', ->
            div.append("<p>An SdiDesk Network Diagram</p>")
            
            inner = $("<div>")
                .attr("width", "400")
                .attr("height", "500")
                .attr("style", "border: 1px solid black")            
            
            svg=$("<svg>")
            svg.attr("xmlns","http://www.w3.org/2000/svg")            
            svg.attr("width", "380")
            svg.attr("height", "480")            
            svg.attr("style", "border: 1px solid black; width:380; height:480")
            #    .attr("version","1.1")

            #svg = document.createElement('SVG');
            #svg.setAttribute('style', 'border: 1px solid black');
            #svg.setAttribute('width', '380px');
            #svg.setAttribute('height', '480px');
            #svg.setAttribute('version', '1.1');
            #svg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');

            inner.append(svg)
            inner.append("hello teenage america")
            console.log(svg)
            div.append(inner)
                
 
            for k,v of item.net.nodes
                svg.append("<circle>")
                svg.find(":last-child")
                    .attr("cx",Math.floor(v.x/5))
                    .attr("cy",Math.floor(v.y/5))
                    .attr("r",10)
                    .attr("fill", "#6666ff")
                    .attr("stroke", "#0000ff")
                    .attr("stroke-width","1")
            
            div.append("hello")
    bind: (div, item) ->
        div.dblclick -> wiki.textEditor div, item    


