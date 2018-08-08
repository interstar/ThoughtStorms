from txlib import MarkdownThoughtStorms, Environment

import unittest 

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

if __name__ == '__main__' :
    unittest.main()
