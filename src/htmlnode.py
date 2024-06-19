from textnode import *
from enum import Enum
from markdown_to_nodes import *
from typing import Optional, List

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"
type_rules = [
"text",
"bold",
"italic",
"code",
"link",
 "image"]    
delimiters = {
"bold": "**",
"italic": "*",
"code_block": "```",
"code": "`",
"strikethrough": "~~",
# "link": "[",
# "image": "!",
# "heading": "#"
}
delimiters2 = {
"**": "bold",
"*": "italic",
"```": "code_block",
"`": "code",
"~~": "strikethrough",
# "[": "link",
# "!": "image",
# "#": "heading" 
}
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'

    def print_details(self):
        print(f"Tags: {self.tag}")
        if self.value == None:
            print(f"Value: {self.value}")
        elif len(self.value) < 21:
            print(f"Value: {self.value[0:10]}")
        else:
            print(f"Value: {self.value[0:10]} ...{self.value[-20:len(self.value)]}")
        print(f"Children: {self.children}")
        print(f"Props: {self.props}")
            
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        prop = ""
        if self.props is None:
            return prop
        for key in self.props:
            prop += f' {key}="{self.props[str(key)]}"'
        return prop

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        # if children:
        for child in children:
            assert isinstance(child, HTMLNode)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("Missing tag argument.")
        elif self.children is None or bool(self.children) == False:
            raise ValueError("Missing children argument.")
        html_string = ""
        html_string += f'<{self.tag}{self.props_to_html()}>'
        for child in self.children:
            html_string += child.to_html()
        html_string += f'</{self.tag}>'
        return html_string

def text_node_to_html_node(text_node: TextNode):
    if text_node.text_type not in TextType:
        raise Exception(f"Invalid text type: {text_node.text_type}")
    elif text_node.text_type == TextType.TEXT:
        return LeafNode(tag=None, value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
    
#------------------------------mk doc to html nodes----------------------#
def mk_block_child_unpacker(block):
    children = []
    # textnodes = block_to_textnodes(block)
    # print(f"{textnodes}")
    # htmlnodes = textnodes_to_html(textnodes)
    # print(f"{htmlnodes}")
    children.extend(textnodes_to_html(block_to_textnodes(block)))
    # print(f"{children}")
    return children

def block_to_textnodes(block):
    textnodes = []
    # split = block.splitlines(keepends=True)
    split = block.split("\n\n")
    for line in split:
        textnodes.extend(text_to_textnodes(line))
    return textnodes

def textnodes_to_html(textnodes):
    htmlnodes = []
    if isinstance(textnodes, TextNode) == True:
        htmlnodes.append(text_node_to_html_node(textnodes))
    else:
        for textnode in textnodes:
            htmlnodes.extend(textnodes_to_html(textnode))
    return htmlnodes
        
def mk_doc_to_html_node(markdown_doc):
    markdown_blocks = markdown_to_blocks(markdown_doc)
    block_dict = {}
    for block in markdown_blocks:
        block_dict[block] = block_to_block_type(block)
    block_html_nodes = [] 
    block_tuples = zip(block_dict.keys(), block_dict.values())   
    for block, type in block_tuples:
        if type == MKBlockType.Heading:
            block_html_nodes.append(heading_block_to_html_node(block))
        if type == MKBlockType.Code:
            block_html_nodes.append(code_block_to_html_node(block))
        if type == MKBlockType.Quote:
            block_html_nodes.append(quote_block_to_html_node(block))
        if type == MKBlockType.UnorderedList:
            block_html_nodes.append(unordered_list_to_html_node(block))
        if type == MKBlockType.OrderedList:
            block_html_nodes.append(ordered_list_block_to_html_node(block))
        if type == MKBlockType.Paragraph:
            block_html_nodes.append(paragraph_block_to_html_node(block))
    return ParentNode(tag="div", children=block_html_nodes)

def heading_block_to_html_node(heading_block):
    children = []
    stripped = heading_block[heading_block[0:6].count("#")+1:]
    children.extend(mk_block_child_unpacker(stripped))
    return ParentNode(tag=f"h{heading_block[0:6].count("#")}", children=children)

def code_block_to_html_node(code_block):
    children = []
    stripped = code_block.strip("```")
    stripped2 = stripped.lstrip("\n\r\x1d\x1e\u2028\u2029")
    children.append(LeafNode("code", value=stripped2))
    if bool(children) is False:
                assert("inline children is empty")
    return ParentNode(tag="pre", children=children)

def quote_block_to_html_node(quote_block):
    children = []
    stripped = quote_block.replace(">", "\n")
    children.extend(mk_block_child_unpacker(stripped))
    return ParentNode(tag="blockquote", children=children)

def unordered_list_to_html_node(unordered_list_block):
    children = []
    inline_children = []
    for line in unordered_list_block.split("\n"):
        if (line[0] == "-" or line[0] == "*" or line[0] == "+" or line[0] == "-") and set([item[0:2] for item in unordered_list_block.split("\n")]) <= set(["- ", "* ", "+ ", "- "]):
            inline_children.extend(textnodes_to_html(text_to_textnodes(line[2:])))
            children.append(ParentNode("li", children=inline_children))
            if bool(inline_children) == False:
                assert("inline children is empty")
            inline_children = []
    return ParentNode(tag="ul", children=children)

def ordered_list_block_to_html_node(ordered_list_block):
    children = []
    inline_children = []
    for line in ordered_list_block.split("\n"):
        inline_children.extend(textnodes_to_html(text_to_textnodes(line[3:])))
        children.append(ParentNode("li", children=inline_children))
        if bool(inline_children) == False:
            assert("inline children is empty")
        inline_children = []
    return ParentNode(tag="ol", children=children)

def paragraph_block_to_html_node(paragraph_block):
    children = []
    children.extend(mk_block_child_unpacker(paragraph_block))
    return ParentNode("p", children=children)

# markdown = (
# """
# 1. An elaborate pantheon of deities (the `Valar` and `Maiar`)
# 2. The tragic saga of the Noldor Elves
# 3. The rise and fall of great kingdoms such as Gondolin and Númenor
# """)
# print(mk_doc_to_html_node(markdown))
# print(text_to_textnodes("An elaborate pantheon of deities (the `Valar` and `Maiar`)"))
# def test(markdown):
#     html_nodes = mk_doc_to_html_node(markdown)
#     print(html_nodes)
#     # textnodes = block_to_textnodes(markdown)
#     # print(f"{textnodes}")
#     # htmlnodes = textnodes_to_html(textnodes)
#     # print(f"{htmlnodes}")
#     return html_nodes


# with open("./static_site/src/markdown_test") as file:
    # print(f"\n\n{[mk_doc_to_html_node(file.read())]}\n")


# print(f"\n{textnodes_to_html(block_to_textnodes("Markdown uses email-style `>` characters for blockquoting. If you're\nfamiliar with quoting passages of text in an email message, then you\nknow how to create a blockquote in Markdown. It looks best if you hard\nwrap the text and put a `>` before every line:"))}")

# test("### Markdown\n\nuses email-style `>` characters for blockquoting. If you're\nfamiliar with quoting passages of text in an email message, then you\nknow how to create a blockquote in Markdown. It looks best if you hard\nwrap the text and put a `>` before every line:")