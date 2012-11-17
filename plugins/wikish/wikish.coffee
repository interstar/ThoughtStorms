###
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


###

window.plugins.wikish =
  emit: (div, item) ->
    mp = new MarkupProcessor('')
    text = mp.page(item.text)
    text = wiki.resolveLinks(text)
    p = $("<p/>").append(text)
    div.append p
  bind: (div, item) ->
    div.dblclick -> wiki.textEditor div, item

class @MarkupProcessor 

    constructor:(@root) ->
        @raw = ""
        @cooked = ""
        @blm = /^\s*$/
        @hr = /^----\s*$/
        @h6 = /^======(.*)?======\s*$/
        @h5 = /^=====(.*)?=====\s*$/
        @h4 = /^====(.*)?====\s*$/
        @h3 = /^===(.*)?===\s*$/
        @h2 = /^==(.*)?==\s*$/
        @h1 = /^=(.*)?=\s*$/
        @bold = /'''([^']*)?'''/g
        @italic = /''([^']*)?''/g
        @wikiword = /([A-Z][a-z]+([A-Z][a-z]+)+)/g
        
        @indent = 0
         
    line:(l) ->
        nl = l       
        nl = nl.replace(@blm,"<br/>\n")
        nl = nl.replace(@hr,"<hr>")
        nl = nl.replace(@bold,"<b>$1</b>")
        nl = nl.replace(@italic,"<i>$1</i>")

        nl = nl.replace(@h6,"<h6>$1</h6>")
        nl = nl.replace(@h5,"<h5>$1</h5>")
        nl = nl.replace(@h4,"<h4>$1</h4>")
        nl = nl.replace(@h3,"<h3>$1</h3>")
        nl = nl.replace(@h2,"<h2>$1</h2>")
        nl = nl.replace(@h1,"<h1>$1</h1>")

        #nl = nl.replace(@wikiword,"<a class='internal' href='/$1.html' data-page-name='$1' title='origin'>$1</a>")
        nl

    check:(s) ->
        if s.charAt(s.length-1)=='*'
            s = s.substring(0,s.length-1)
            s = "<strike>" + s + "</strike>"
        return s
        
    outlineFilter:(l) ->
        if l[0] != "*"
            if @indent > 0
                s = Array(1+@indent).join("</ul>")
                @indent = 0
                l = s + "\n" + l
            return l
        
        count = 0
        while l[count] == "*" 
            count=count+1
        meat = l.substring(count)

        if count == @indent
            return (Array(@indent+1).join(" ")) + "<li>" + @check(meat) + "</li>"
        if count > @indent 
            @indent = @indent + 1
            return "<ul>\n" + (Array(@indent+1).join(" ")) + "<li>" + @check(meat) + "</li>"
        s = (Array((1+@indent)-count).join("</ul>")) + "<li>" + @check(meat) + "</li>\n" 
        @indent = count
        return s

    page:(p) ->
        @raw = p
        lines = (@line(l) for l in p.split("\n"))
        lines = (@outlineFilter(l) for l in lines)
        @cooked = lines.join('\n')
        @cooked
         
                
###
To pull from other usemods
###

class @UseModGateway

    constructor:(base,@urlPattern) ->
        @baseUrl = base + "?action=browse&raw=1&id="
        @chef = new MarkupProcessor(@urlPattern)
    
    get:(word,id,title) ->
        $.get(@baseUrl+word, (data)=>        
            $('#'+id).html(@chef.page(data))
            $('#'+title).text(word)
        )
                
        
    
        
class @Transcluder
    constructor:(url,dict) ->
        $.ajax url,
            type: 'GET'
            dataType: 'html'
            error: (jqXHR, textStatus, errorThrown) ->
                #$('body').append "AJAX Error: #{textStatus}"
                console.log(textStatus)
                console.log(errorThrown)

            success: (data, textStatus, jqXHR) ->
                console.log(textStatus)
                console.log(text)
                dict["cache"]=text


