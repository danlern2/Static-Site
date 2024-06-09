from enum import Enum
import sys
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
"link": "[",
"image": "!",
"heading": "#",
"strikethrough": "~~" }
delimiters2 = {
"**": "bold",
"*": "italic",
"```": "code_block",
"`": "code",
"[": "link",
"!": "image",
"#": "heading",
"~~": "strikethrough" }

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

def mk_to_textnode(text):
    nodes = []
    if bool(text) is False or text is None:
            sys.exit
    for delim in delimiters2.keys():
            if delim not in text:
                continue
            else:
                text.find(delim)
                new_string = text[:text.find(delim)]
                if bool(new_string) == True:
                    nodes.append((TextNode(new_string, "text")))
                delim_string = text[text.find(delim)+1:text.rfind(delim)]
                nodes.append((TextNode(delim_string.strip(delim), delimiters2.get(delim))))
                mk_to_textnode(delim_string)
                after_delim_string = text[text.rfind(delim)+1:]
                mk_to_textnode(after_delim_string[after_delim_string.rfind(delim)+1:])
                if bool(after_delim_string) == True:
                    nodes.extend(mk_to_textnode(after_delim_string.lstrip(delim)))
                return nodes
    nodes.append(TextNode(text, "text"))
    return nodes

###Needs work 
def text_nodes_delimiter(old_nodes, text_type, *delimiter):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode):
            if text_type is not text_type_text:
                print(f"this is the print: {node.text}")
                split = node.text.split(delimiters.get(text_type))
                if bool(split[0]) == True:
                    new_nodes.append(TextNode(split[0], text_type_text))
                new_nodes.append(TextNode(split[1], text_type))
                if bool(split[2]) == True:
                    new_nodes.append(TextNode(split[2], text_type_text))
            else:
                new_nodes.append(node)
    return new_nodes
###


def test():
    mkstring = "This is text with a ***bolded and not italicized*** sentence"
    another_string = "`this is a code string`"
    another_string2 = "this is a ~~wrong~~ correct string"
    another_string3 = "`this is a ~~wrong~~ correct string in code`"
    nodelist = [TextNode("This is text with a **bolded and not italicized** sentence", "bold")]
    #TextNode("`this is a code string`", "code"),]
    #TextNode("this is a ~~wrong~~ correct statement: Yoni sucks", "strikethrough")]
    # print(mk_to_textnode(mkstring))
    # print(mk_to_textnode(another_string))
    # print(mk_to_textnode(another_string2))
    # print(mk_to_textnode(another_string3))
    print(text_nodes_delimiter(nodelist, text_type_bold))
test()




        

    