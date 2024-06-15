from enum import Enum
from typing import Optional, List
from dataclasses import dataclass
#from htmlnode import Type_Rules
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

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

class TextType(Enum):
    TEXT = "TEXT"
    BOLD = "BOLD"
    ITALIC = "ITALIC"
    CODE = "CODE"
    LINK = "LINK"
    IMAGE = "IMAGE"

DELIMITER_TO_TYPE = {
    '**': TextType.BOLD,
    '*': TextType.ITALIC,
    '_': TextType.ITALIC,
    '`': TextType.CODE,
}

# @dataclass()
# class TextNode:
#     text: str
#     text_type: TextType
#     url: Optional[str] = None

#---------in markdown.py---------#
# def split_node_delimiter(old_node: TextNode, delimiter: str) -> List[TextNode]:
#     if old_node.text_type != TextType.TEXT:
#         return [old_node]
#     new_nodes = []
#     split = old_node.text.split(delimiter)
#     for i, item in enumerate(split):
#         if len(split) > 1 and "*" in split[i] and "*" in split[i+1]:
#             item += "*"
#             split[i+1] = split[i+1][1:]
#         if item == "":
#             continue
#         if i % 2 == 0:
#             new_nodes.append(TextNode(item, TextType.TEXT))
#         else:
#             new_nodes.append(TextNode(item, DELIMITER_TO_TYPE.get(delimiter)))
#     return new_nodes
# def split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str) -> List[TextNode]:
#     new_nodes: List[TextNode] = []
#     for node in old_nodes:
#         new_nodes.extend(split_node_delimiter(node, delimiter))
#     return new_nodes
# def nested_nodes_unpacker(old_nodes: List[TextNode]):
#     unpacked_nodes: List[TextNode] = []
#     for node in old_nodes:
#         if node.text_type == TextType.TEXT:
#             unpacked_nodes.append(node)
#         else:
#             unpacked_nodes.extend(nest_checker(node))
#     return unpacked_nodes
# def nest_checker(node: TextNode):
#     new_nodes: List[TextNode] = []
#     if split_nodes_by_delimiters([TextNode(node.text, TextType.TEXT)])[0].text_type != TextType.TEXT and split_nodes_by_delimiters([TextNode(node.text, TextType.TEXT)])[0].text_type != node.text_type:
#         new_nodes.append(TextNode("", node.text_type))
#         new_nodes.extend(split_nodes_by_delimiters([TextNode(node.text, TextType.TEXT)]))
#         new_nodes.append(TextNode("", node.text_type))
#     else:
#         new_nodes.append(node)
#     return new_nodes
# def split_nodes_by_delimiters(nodes: List[TextNode]):
#     for delimiter in DELIMITER_TO_TYPE:
#         nodes = split_nodes_delimiter(nodes, delimiter)
#     return nested_nodes_unpacker(nodes)
      