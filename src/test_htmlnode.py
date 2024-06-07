import unittest

from htmlnode import HTMLNode 
from htmlnode import LeafNode
class TestHTMLNode(unittest.TestCase):
    
    
    # def testRepr(self):
    #     new_node = HTMLNode(value=["diiick"], props={"href": "https://www.google.com", "target": "_blank"})
    #     #new_node.__repr__()
    # def testRepr2(self):
    #     new_node2 = HTMLNode(tag="h1", value="dongle", props={"href": "https://www.google.com", "target": "_blank"})
    #     #new_node2.__repr__()
    # def testPropToHtml(self):
    #     new_node2 = HTMLNode(tag="h1", props={"href": "https://www.google.com", "target": "_blank", "biggus": "dickus"})
    #     print(new_node2.props_to_html())

    def testLeafNode(self):
        leaf = LeafNode(tag="h1", value="dongle", props={"href": "https://www.google.com", "target": "_blank"})
        print(leaf.to_html())
    def testLeafNode2(self):
        leaf2 = LeafNode(value="dongle", props={"href": "https://www.google.com"})
        print(leaf2.to_html())
    def testLeafNode3(self):
        leaf3 = LeafNode("p", "dongle", props={"href": "https://www.google.com", "target": "_blank"})
        print(leaf3.to_html())


if __name__ == "__main__":
    unittest.main()
     