import unittest
from htmlnode import HTMLNode 
from htmlnode import LeafNode
from htmlnode import ParentNode
from textnode import TextNode
from htmlnode import text_node_to_html_node
class TestHTMLNode(unittest.TestCase):
      pass
    # def testRepr(self):
    #     new_node = HTMLNode(value=["diiick"], props={"href": "https://www.google.com", "target": "_blank"})
    #     #new_node.__repr__()
    # def testRepr2(self):
    #     new_node2 = HTMLNode(tag="h1", value="dongle", props={"href": "https://www.google.com", "target": "_blank"})
    #     #new_node2.__repr__()
    # def testPropToHtml(self):
    #     new_node2 = HTMLNode(tag="h1", props={"href": "https://www.google.com", "target": "_blank", "biggus": "dickus"})
    #     print(new_node2.props_to_html())

    # def testLeafNode(self):
    #     leaf = LeafNode(tag="h1", value="dongle", props={"href": "https://www.google.com", "target": "_blank"})
    #     print(leaf.to_html())
    # def testLeafNode2(self):
    #     leaf2 = LeafNode(value="dongle", props={"href": "https://www.google.com"})
    #     print(leaf2.to_html())
    # def testLeafNode3(self):
    #     leaf3 = LeafNode(None, "my value", props={"href": "https://www.google.com"})
    #     print(leaf3.to_html())

    # def testParentNode(self):
    #     parent = ParentNode(
    # "1st",
    # [
    #     LeafNode("b", "Bold text"),
    #     LeafNode(None, "Normal text"),
    #     ParentNode(
    # "nest",
    # [
    #     LeafNode("b", "Bold"),
    #     LeafNode(None, "Normal"),
    #     LeafNode("i", "italic"),
    #     LeafNode(None, "blah", props={"href": "www.dick.com", "named": "yoni"}),
    #     LeafNode("s", "Normal text yet slightly off kilter", props={"href": "www.dick.com", "named": "yoni"}),
    #     LeafNode("k", "dongle", props={"href": "www.google.com"})
    # ]
    # ),
    #     #ParentNode(None,[LeafNode("i", "italic text")]),
    #     #ParentNode("p", []),
    #     ParentNode("p",[LeafNode("i", "italic text")], props={"href": "www.dan.com", "named": "the_man"}),
    #     LeafNode("i", "italic text"),
    #     LeafNode(None, "blahblah blah", props={"href": "https://www.dick.com", "named": "yoni"}),
    #     LeafNode("s", "Normal text yet slightly off kilter", props={"href": "https://www.dick.com", "named": "yoni"}),
    #     LeafNode("k", "dongle", props={"href": "https://www.google.com", "target": "_blank"})
    # ]
    # )
    #     print(parent.to_html())
    
    # def test_eq2(self):
    #     node3 = TextNode("This is a text node", "italic", "http://localhost:8888/")
    #     node4 = TextNode("This is a text node but wrong", "italic")
    #     print(str(text_node_to_html_node(node3)))


# if __name__ == "__main__":
#     unittest.main()


def markdown_to_blocks(markdown: str):
    blocks = markdown.split("\n\n")
    block_list = []
    for block in blocks:
        if block == "":
            continue
        block_list.append(block.strip())
    return block_list

def test(list):
    new_list = []
    for item in list:
        new_list.extend(item.split("\n"))
    return new_list


with open("/home/danlern2/bootdevworkspace/static_site/src/markdown_test") as file:
    print(test(markdown_to_blocks(file.read())))
