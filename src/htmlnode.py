from textnode import TextNode
from enum import Enum
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
"link": "[",
"image": "!",
"heading": "#" }
delimiters2 = {
"**": "bold",
"*": "italic",
"```": "code_block",
"`": "code",
"[": "link",
"!": "image",
"#": "heading" }

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

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, None, children, props)
    
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

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'



def text_node_to_html_node(text_node):
    if text_node.text_type not in type_rules:
        raise Exception(f"Invalid text type: {text_node.text_type}")
    elif text_node.text_type == text_type_text:
        return LeafNode(value=text_node.text)
    elif text_node.text_type == text_type_bold:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == text_type_italic:
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == text_type_code:
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == text_type_link:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == text_type_image:
        return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
    
def test_eq2():
        node3 = TextNode("This is a text node", "italic", "http://localhost:8888/")
        node4 = TextNode("This is a text node but wrong", "italic")
        print(str(text_node_to_html_node(node4)))
        #print(dir(Type_Rules))
test_eq2()
