from txlib import MarkdownThoughtStorms, Environment

import unittest, re

def assertCollapseNL(test,a,b) :
    a = re.sub("\n+","\n",a)
    b = re.sub("\n+","\n",b)
    print(a)
    print(b)
    test.assertEqual(a,b)
    

class TestMarkdownThoughtStorms(unittest.TestCase) :

    def setUp(self) :
        self.chef = MarkdownThoughtStorms()
        self.env = Environment({},"/")


    def test1(self) :
        p = """
## Hello Teenage America

Goodbye *Cruel* **World**
"""
        self.assertEqual(self.chef.cook(p,self.env), 
"""<h2>Hello Teenage America</h2>
<p>Goodbye <em>Cruel</em> <strong>World</strong></p>""")

    def test2(self) :
        p = """
Before

[<YOUTUBE
id : kc_Jq42Og7Q
>]

During

[<YOUTUBE
id : kc_Jq42Og7Q
>]


After
"""
        self.assertEqual(self.chef.cook(p,self.env),
"""<p>Before</p>\n<p><div class="youtube-embedded"><iframe width="400" height="271" src="http://www.youtube.com/embed/kc_Jq42Og7Q" frameborder="0" allowfullscreen></iframe></div></p>\n<p>During</p>\n<p><div class="youtube-embedded"><iframe width="400" height="271" src="http://www.youtube.com/embed/kc_Jq42Og7Q" frameborder="0" allowfullscreen></iframe></div></p>\n<p>After</p>""")

    def test3(self) :
        p = """
## Some stuff
xxx
[<PRE

## This shouldn't be Markdowned

>]

Middle 

[<PRE
4




blank rows
>]

Aftermath"""
        r = """<h2>Some stuff</h2>
<p>xxx</p>

## This shouldn't be Markdowned

<p>Middle</p>

4




blank rows

<p>Aftermath</p>"""
        assertCollapseNL(self,self.chef.cook(p,self.env),r)

if __name__ == '__main__' :
    unittest.main()
