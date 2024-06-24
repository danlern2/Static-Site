from __future__ import annotations
from delimiter_rules import delimiter_nester_in_node

from htmlnode_class import HTMLNode, LeafNode, ParentNode, GrandparentNode
from enum import Enum
import re

# LINK: str = r"\[(.*?)\]\((.*?)\)"
# IMAGE: str = r"!\[(.*?)\]\((.*?)\)"

# DELIM_TO_RULE: dict[str,] = {
#     "**": bold_rule,
#     "__": bold_rule,
#     "~~": strike_rule,
#     "*": italic_rule,
#     "_": italic_rule,
#     "[": link_rule,
#     "!": image_rule,
# }


class TagType(Enum):
    # TEXT: None = None
    CODE: str = "code"
    BOLD: str = "b"
    STRIKE: str = "strikethrough"
    ITALIC: str = "i"
    LINK: str = "a"
    IMAGE: str = "img"
    LIST: str = "li"
    OLIST: str = "ol"
    UNOLIST: str = "ul"
    CODEBLOCK: str = "pre"
    QUOTE: str = "blockquote"
    HEADING: str = "h"
    PARAGRAPH: str = "p"
    DOC: str = "div"


class MKBlockType(Enum):
    Paragraph = "paragraph"
    Heading = "heading"
    Code = "code"
    Quote = "quote"
    UnorderedList = "unordered_list"
    OrderedList = "ordered_list"
    Document = "div"

DELIMITER_TO_TYPE = {
    "`": TagType.CODE,
    "**": TagType.BOLD,
    # '__': TagType.BOLD,
    "~~": TagType.STRIKE,
    "*": TagType.ITALIC,
    # '_': TagType.ITALIC,
    "!": TagType.IMAGE,
    "[": TagType.LINK,
}
TAG_TYPE_TO_TAG = {
    "p": TagType.PARAGRAPH,
    "h": TagType.HEADING,
    "pre": TagType.CODEBLOCK,
    "blockquote": TagType.QUOTE,
    "ul": TagType.UNOLIST,
    "ol": TagType.OLIST,
    "div": TagType.DOC,
    "`": TagType.CODE,
    "**": TagType.BOLD,
    # '__': TagType.BOLD,
    "~~": TagType.STRIKE,
    "*": TagType.ITALIC,
    # '_': TagType.ITALIC,
    "!": TagType.IMAGE,
    "[": TagType.LINK,
}

## ============ HTMLNode Class =============##


def blep():
    pass
    # class HTMLNode:
    #     def __init__(
    #         self,
    #         tag: str | None = None,
    #         text: str | None = None,
    #         children: list[HTMLNode] | None = None,
    #         props: dict[str | None, str | None] | None = None,
    #     ):
    #         self.tag = tag
    #         self.text = text
    #         self.children: list[HTMLNode] | None = children
    #         self.props = props

    #     def __repr__(self):
    #         return f"HTMLNode({self.tag}, {self.text}, {self.children}, {self.props})"

    #     def print_details(self):
    #         print(f"Tags: {self.tag}")
    #         if self.text is None:
    #             print(f"Value: {self.text}")
    #         elif len(self.text) < 21:
    #             print(f"Value: {self.text[0:10]}")
    #         else:
    #             print(f"Value: {self.text[0:10]} ...{self.text[-20:len(self.text)]}")
    #         print(f"Children: {self.children}")
    #         print(f"Props: {self.props}")

    #     def to_html(self) -> str | None:
    #         raise NotImplementedError

    #     def props_to_html(self):
    #         prop = ""
    #         if self.props is None:
    #             return prop
    #         for key in self.props:
    #             prop += f' {key}="{self.props[str(key)]}"'
    #         return prop

    # class LeafNode(HTMLNode):
    #     def __init__(self, text: str):
    #         super().__init__(None, text, None, None)

    #     def to_html(self) -> str | None:
    #         if self.text is None:
    #             raise ValueError
    #         return self.text

    # class ParentNode(HTMLNode):
    #     def __init__(
    #         self,
    #         tag: str,
    #         # text: str | None,
    #         children: list[HTMLNode],
    #         props: dict[str | None, str | None] | None = None,
    #     ):
    #         super().__init__(tag, None, children, props)
    #         # if children:
    #         for child in children:
    #             assert isinstance(child, HTMLNode)

    #     def to_html(self) -> str:
    #         if self.tag is None:
    #             raise ValueError("Missing tag argument.")
    #         elif self.children is None or bool(self.children) is False:
    #             raise ValueError("Missing children argument.")
    #         html_string: str = ""
    #         html_string += f"<{self.tag}{self.props_to_html()}>"
    #         for child in self.children:
    #             html_string += child.to_html()  # type: ignore
    #         html_string += f"</{self.tag}>"  # type: ignore
    #         return html_string  # type: ignore

    # class GrandparentNode(HTMLNode):
    #     def __init__(
    #         self,
    #         tag: str,
    #         children: list[HTMLNode],
    #         props: dict[str | None, str | None] | None = None,
    #     ):
    #         super().__init__(tag, None, children, props)
    #         # if children:
    #         for child in children:
    #             assert isinstance(child, HTMLNode)

    #     def to_html(self) -> str:
    #         if self.tag is None:
    #             raise ValueError("Missing tag argument.")
    #         elif self.children is None or bool(self.children) is False:
    #             raise ValueError("Missing children argument.")
    #         html_string: str = ""
    #         html_string += f"<{self.tag}{self.props_to_html()}>"
    #         for child in self.children:
    #             html_string += child.to_html()  # type: ignore
    #         html_string += f"</{self.tag}>"  # type: ignore
    #         return html_string  # type: ignore


## ============ HTMLNode Class =============##

## ============ Inline Markdown to HTMLNode =============##


# def delimiter_loop_on_htmlnodes(nodes: list[HTMLNode]) -> list[HTMLNode]:
#     """
#     For each delimiter, send the list of TextNodes to textnodes_loop_with_delimiter(nodes, delimiter)\n
#     textnodes_loop_with_delimiter will return a new list of nodes separated by the given delimiter and return a new list\n
#     This is will go until all the delimiters are accounted for.\n
#     At the end, this will return a fully and properly delimited set of TextNodes including nested ones.
#     """
#     for delimiter in DELIMITER_TO_TYPE:
#         nodes = htmlnodes_loop_with_delimiter(nodes, delimiter)
#     # print(nodes)
#     return nodes


# def delimiter_checker_loop(text: str):
#     for i in range(len(text)):
#         for delim in DELIMITER_TO_TYPE:
#             if text[i:].startswith(delim):
#                 return delim
#     return
#     # x: int = 0
#     # i: float = float("inf")
#     # delimiters_found: dict[int, str] = {}
#     # try:
#     #     for delim in DELIMITER_TO_TYPE:
#     #         x = text.find(delim)
#     #         if x == i:
#     #             return delimiters_found[i]
#     #         if x != -1:
#     #             if x < i:
#     #                 i = x
#     #                 delimiters_found[x] = delim
#     #                 if x == 0:
#     #                     print("hi")
#     #                     break
#     #     return delimiters_found[i]
#     # except Exception as e:
#     #     pass


# print(delimiter_checker_loop("string"))
# print(delimiter_checker_loop("t**`***this* s~~tring"))


def htmlnodes_loop_with_delimiter(
    nodes: list[HTMLNode], delimiter: str
) -> list[HTMLNode]:
    """
    Takes a list of TextNodes and a delimiter. Will send each node in the list and the given delimiter to the split_node_delimiter function and will extend that result to a new list of nodes.\n
    """
    new_nodes: list[HTMLNode] = []
    for node in nodes:
        # ------unordered list exception-----#
        if delimiter == "*" and node.text[0:2] == "* ":
            unordered_list_text: str = node.text[2:]
            unordered_list_nodes = split_node_delimiter(
                HTMLNode("li", unordered_list_text), delimiter
            )
            # if unordered_list_nodes[0].text is not None:  # type: ignore
            #     unordered_list_nodes[0].text = "* " + unordered_list_nodes[0].text
            #     new_nodes.extend(unordered_list_nodes)
            # else:
            #     unordered_list_nodes[1].text = "* " + unordered_list_nodes[1].text
            #     new_nodes.extend(unordered_list_nodes)
            ul_node_text = unordered_list_nodes.index(LeafNode).text
            ul_node_text = "* " + ul_node_text
            new_nodes.extend(unordered_list_nodes)
        # ------unordered list exception-----#
        else:
            new_nodes.extend(split_node_delimiter(node, delimiter))
    return new_nodes


def split_node_delimiter(node: HTMLNode, delimiter: str) -> list[HTMLNode]:
    text: str = node.text
    children: list[HTMLNode] = node.children
    nest_bool = nest_checker(text)
    if isinstance(node, LeafNode):
        return
    if nest_bool[0] is False:
        children.append(LeafNode(text))
        node.text = None
        return node

    i = 0
    x = 0
    # Set i to the first instance index of the delimiter
    i = text.index(delimiter)
    # If there is no match for the delimiter in the rest of the text then its not a true case of that delimiter
    # and it should be a leafnode. Add it to the children and clear the parent text.
    if delimiter not in text[i + len(delimiter) :]:
        children.append(LeafNode(text))
        node.text = None
        return children
    x = text[i + len(delimiter) :].index(delimiter) + len(text[: i + len(delimiter)])
    x += len(delimiter)
    # Check if x is the outside delimiter, and if its not, make it.
    if x != len(text) and text[x] == delimiter[0]:
        x += 1
    # Send the delimited text to the splitter, and extend the results into new_nodes
    children.extend(splitter(text[i:x], delimiter))
    # If its not the end of the node's text, send the remainder back through this function.
    if x != len(text):
        node.text = text[x:]
        children.extend(split_node_delimiter(node, delimiter))


def split_node_delimiter(node: HTMLNode, delimiter: str) -> list[HTMLNode]:
    """
    Take a HTMLNode and a delimiter, check the text of the HTMLNode against the delimiter and if it contains it, split the text into multiple new textnodes\n
    ## Example:\n
        node = HTMLNode("This is text with a `code block` word", "text")
        ### new_nodes will be:
        #### [
        ####     HTMLNode("This is text with a ", "text"),
        ####     HTMLNode("code block", "code"),
        ####    HTMLNode(" word", "text"),
        #### ]
    """
    i = 0
    x = 0
    children = node.children
    new_nodes: list[HTMLNode] = []
    text: str = node.text
    if node.text_type != TextType.TEXT:
        new_nodes.append(node)
    elif delimiter in text:
        # # ---------------Italic Exception--------------#
        # if (delimiter == "*" or delimiter == "_") and delimiter in text:
        #     italicE = italic_exception(node, delimiter)
        #     new_nodes.extend(italicE[0])
        #     return htmlnodes_loop_with_delimiter(new_nodes, italicE[1])
        # # ---------------Italic Exception--------------#

        # Set i to the first instance index of the delimiter
        i = text.index(delimiter)
        # If there is no match for the delimiter in the rest of the text then its not a true case of that delimiter
        # and append it as is
        if delimiter not in text[i + len(delimiter) :]:
            new_nodes.append(node)
        # Check if there is any delimiter in the first segment. If there is, recursively call on this function to check that delimiter first.
        # Otherwise make that slice from 0 - i of the text a new HTMLNode and append it to the list.
        if i != 0:
            if nest_checker(text[:i])[0] is False:
                new_nodes.append(HTMLNode(text[:i], TextType.TEXT))
            else:
                split_node_delimiter(node, nest_checker(text[:i])[1])
        # Set x to the text of the next index where you find the delimiter
        x = text[i + len(delimiter) :].index(delimiter) + len(
            text[: i + len(delimiter)]
        )
        x += len(delimiter)
        # Check if x is the outside delimiter, and if its not, make it.
        if x != len(text) and text[x] == delimiter[0]:
            x += 1
        # Send the delimited text to the splitter, and extend the results into new_nodes
        new_nodes.extend(splitter(text[i:x], delimiter))
        # If its not the end of the node's text, send the remainder back through this function.
        if x != len(text):
            new_nodes.extend(
                split_node_delimiter(HTMLNode(text[x:], TextType.TEXT), delimiter)
            )
    else:
        new_nodes.append(node)

    return new_nodes


def italic_exception(node: HTMLNode, delimiter: str) -> tuple[list[HTMLNode], str]:
    i = 0
    x = 0
    new_nodes: list[HTMLNode] = []
    text: str = node.text

    # Set i to the first instance index of the delimiter
    i = text.index(delimiter)
    # If there is no match for the delimiter in the rest of the text then its not a true case of that delimiter
    # and append it as is
    if delimiter not in text[i + 1 :]:
        raise Exception("Not valid markdown")

    # Set x to the text of the next index where you find the delimiter
    x = text[i + 1 :].index(delimiter) + len(text[: i + 1])
    x += 1
    # Check if x is not the index of a pair of the delimiter (bold), and if it is, increment x to get outside.
    if x != len(text) and text[x] == delimiter[0]:
        x += 1
    # Check the text again for the delimiter
    if delimiter not in text[x + len(delimiter) :]:
        new_nodes.append(node)
    # If there is another delimiter in the text,

    return new_nodes, delimiter


# print(italic_exception(HTMLNode("just *a **little test*** string", TextType.TEXT), "*"))


def splitter(text: str, delimiter: str) -> list[HTMLNode]:
    new_nodes: list[HTMLNode] = []
    split_text: list[str] = []
    split_text.append(text.partition(delimiter)[1])
    split_text.append(text.partition(delimiter)[2].rpartition(delimiter)[0])
    split_text.append(text.partition(delimiter)[2].rpartition(delimiter)[1])
    # if nest_checker(split_text[1])[0] is False:
    #     new_nodes.append(HTMLNode(split_text[1], DELIMITER_TO_TYPE.get(delimiter)))  # type: ignore
    #     return new_nodes
    # else:
    #     new_nodes.append(HTMLNode("", DELIMITER_TO_TYPE.get(delimiter)))  # type: ignore
    #     new_nodes.append(HTMLNode(split_text[1], TextType.TEXT))
    #     new_nodes.append(HTMLNode("", DELIMITER_TO_TYPE.get(delimiter)))  # type: ignore
    new_nodes.append(ParentNode(DELIMITER_TO_TYPE.get(delimiter), split_text[1]))
    return new_nodes


def nest_checker(text: str):
    for delim in DELIMITER_TO_TYPE:
        if delim in text:
            return True, delim
    return False, ""


## ============ Inline Markdown to HTMLNode =============##


# def text_node_to_html_node(text_node: HTMLNode) -> HTMLNode | None:
#     if text_node.text_type not in TagType:
#         raise Exception(f"Invalid text type: {text_node.text_type}")
#     TagType.TEXT:
#         return ParentNode(tag=None, text=text_node.text)  # type: ignore
#     TagType.BOLD:
#         return ParentNode(tag="b", text=text_node.text)
#     TagType.ITALIC:
#         return ParentNode(tag="i", text=text_node.text)
#     TagType.CODE:
#         return ParentNode(tag="code", text=text_node.text)
#     TagType.LINK:
#         return ParentNode(tag="a", text=text_node.text, props={"href": text_node.url})
#     TagType.IMAGE:
#         return ParentNode(
#             tag="img",
#             text="",
#             props={"src": text_node.url, "alt": text_node.text},
#         )


# -------------------------------mk doc to html nodes----------------------#
# --------------Markdown blocks-------------#


# def markdown_to_blocks(markdown: str) -> list[str]:
#     blocks = markdown.split("\n\n")
#     block_list: list[str] = []
#     for block in blocks:
#         if block == "":
#             continue
#         block_list.append(block.strip())
#     return block_list


# def block_to_block_type(markdown_block: str):
#     if (
#         markdown_block.startswith("# ")
#         or markdown_block.startswith("## ")
#         or markdown_block.startswith("### ")
#         or markdown_block.startswith("#### ")
#         or markdown_block.startswith("##### ")
#         or markdown_block.startswith("###### ")
#     ):
#         return TagType.HEADING
#     elif (
#         markdown_block[0:3] == "```"
#         and markdown_block[-3 : len(markdown_block)] == "```"
#     ):
#         return TagType.CODEBLOCK
#     elif (
#         markdown_block[0] == ">"
#         and len(set([item[0] for item in markdown_block.split("\n")])) == 1
#     ):
#         return TagType.QUOTE
#     elif (
#         markdown_block[0] == "-"
#         or markdown_block[0] == "*"
#         or markdown_block[0] == "+"
#         or markdown_block[0] == "-"
#     ) and set([item[0:2] for item in markdown_block.split("\n")]) <= set(
#         ["- ", "* ", "+ ", "- "]
#     ):
#         return TagType.UNOLIST
#     elif markdown_block.startswith("1. "):
#         i = 1
#         for line in markdown_block.split("\n"):
#             if not line.startswith(f"{i}. "):
#                 return TagType.PARAGRAPH
#             i += 1
#         return TagType.OLIST
#     return TagType.PARAGRAPH


# # def mk_block_child_unpacker(block: str) -> list[HTMLNode]:
# #     children: list[HTMLNode] = []
# #     #
# #     #
# #     return children


# # def block_to_htmlnodes(block: str) -> list[HTMLNode]:
# #     htmlnodes: list[HTMLNode] = []
# #     # split = block.splitlines(keepends=True)
# #     split: list[str] = block.split("\n\n")
# #     for line in split:
# #         htmlnodes.extend(text_to_htmlnode(line))
# #     return htmlnodes


# def mk_doc_to_html_node(markdown_doc: str) -> HTMLNode:
#     markdown_blocks = markdown_to_blocks(markdown_doc)
#     block_dict: dict[str, str] = {}
#     for block in markdown_blocks:
#         block_dict[block] = block_to_block_type(block)
#     block_html_nodes: list[HTMLNode] = []
#     block_tuples: zip[tuple[str, str]] = zip(
#         block_dict.keys(), block_dict.values()
#     )
#     for block, type in block_tuples:
#         if type == TagType.HEADING:
#             block_html_nodes.append(heading_block_to_html_node(block))
#         if type == TagType.CODEBLOCK:
#             block_html_nodes.append(code_block_to_html_node(block))
#         if type == TagType.QUOTE:
#             block_html_nodes.append(quote_block_to_html_node(block))
#         if type == TagType.UNOLIST:
#             block_html_nodes.append(unordered_list_to_html_node(block))
#         if type == TagType.OLIST:
#             block_html_nodes.append(ordered_list_block_to_html_node(block))
#         if type == TagType.PARAGRAPH:
#             block_html_nodes.append(paragraph_block_to_html_node(block))
#     return GrandparentNode(tag=TagType.DOC, children=block_html_nodes)

# # //? Maybe done
# def heading_block_to_html_node(heading_block: str) -> HTMLNode:
#     stripped: str = heading_block[heading_block[0:6].count("#") + 1 :]
#     new_node = GrandparentNode(tag=f"h{heading_block[0:6].count("#")}", children=[])
#     delimiter_nester_in_node(new_node, stripped)

#     return new_node

# # //? Maybe done
# def code_block_to_html_node(code_block: str) -> HTMLNode:
#     children: list[HTMLNode] = []
#     stripped: str = code_block.strip("```")
#     stripped2 = stripped.lstrip("\n\r\x1d\x1e\u2028\u2029")
#     children.append(LeafNode(text=stripped2))
#     if bool(children) is False:
#         assert "inline children is empty"
#     return GrandparentNode(TagType.CODEBLOCK, children=children)

# # //? Maybe done
# def quote_block_to_html_node(quote_block: str) -> HTMLNode:
#     children: list[HTMLNode] = []
#     stripped: str = quote_block.replace(">", "\n")
#     children.append(LeafNode(stripped))
#     return GrandparentNode(tag=TagType.QUOTE, children=children)

# # //? Maybe done
# def unordered_list_to_html_node(unordered_list_block: str) -> HTMLNode:
#     inline_children: list[HTMLNode] = []
#     for line in unordered_list_block.split("\n"):
#         if (
#             line[0] == "-" or line[0] == "*" or line[0] == "+" or line[0] == "-"
#         ) and set([item[0:2] for item in unordered_list_block.split("\n")]) <= set(
#             ["- ", "* ", "+ ", "- "]
#         ):
#             new_node = ParentNode(TagType.LIST, children=[])
#             inline_children.append(delimiter_nester_in_node(new_node, line[2:]))
#             if bool(inline_children) is False:
#                 assert "inline children is empty"
#     return GrandparentNode(tag=TagType.UNOLIST, children=inline_children)

# # //? Maybe done
# def ordered_list_block_to_html_node(ordered_list_block: str) -> HTMLNode:
#     inline_children: list[HTMLNode] = []
#     for line in ordered_list_block.split("\n"):
#         new_node = ParentNode(TagType.LIST, children=[])
#         inline_children.append(delimiter_nester_in_node(new_node, line[2:]))
#         if bool(inline_children) is False:
#             assert "inline children is empty"
#     return ParentNode(tag=TagType.OLIST, children=inline_children)

# # //? Maybe done
# def paragraph_block_to_html_node(paragraph_block: str) -> HTMLNode:
#     children: list[HTMLNode] = []
#     new_node = ParentNode("p", children=children)
#     delimiter_nester_in_node(new_node, paragraph_block)
#     return new_node

