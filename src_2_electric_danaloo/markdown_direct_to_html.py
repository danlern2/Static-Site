from __future__ import annotations
# from delimiter_rules import bold_rule, italic_rule, link_rule, image_rule, strike_rule

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


class DelimiterType(Enum):
    # TEXT: None = None
    CODE: str = "code"
    BOLD: str = "b"
    STRIKE: str = "strikethrough"
    ITALIC: str = "i"
    LINK: str = "a"
    IMAGE: str = "img"


# text = "You can find the [wiki here](https://lotr.fandom.com/wiki/Main_Page)."
# print(str(DelimiterType.LINK) in text)


class TextType(Enum):
    TEXT: str = "text"
    CODE: str = "code"
    BOLD: str = "bold"
    STRIKE: str = "strike"
    ITALIC: str = "italic"
    LINK: str = "link"
    IMAGE: str = "image"


DELIMITER_TO_TYPE = {
    "`": DelimiterType.CODE,
    "**": DelimiterType.BOLD,
    # '__': DelimiterType.BOLD,
    "~~": DelimiterType.STRIKE,
    "*": DelimiterType.ITALIC,
    # '_': DelimiterType.ITALIC,
    "[": DelimiterType.LINK,
    "!": DelimiterType.IMAGE,
}
REGEX_TO_TYPE = {
    re.compile(r"(\*\*\b)|(\b\*\*)"): TextType.BOLD,
    re.compile(r"(__\b)|(\b__)"): TextType.BOLD,
    re.compile(r"(\*\b)|(\b\*)"): TextType.ITALIC,
    re.compile(r"(_\b)|(\b_)"): TextType.ITALIC,
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


def delimiter_checker_loop(text: str):
    for i in range(len(text)):
        for delim in DELIMITER_TO_TYPE:
            if text[i:].startswith(delim):
                return delim
    return
    # x: int = 0
    # i: float = float("inf")
    # delimiters_found: dict[int, str] = {}
    # try:
    #     for delim in DELIMITER_TO_TYPE:
    #         x = text.find(delim)
    #         if x == i:
    #             return delimiters_found[i]
    #         if x != -1:
    #             if x < i:
    #                 i = x
    #                 delimiters_found[x] = delim
    #                 if x == 0:
    #                     print("hi")
    #                     break
    #     return delimiters_found[i]
    # except Exception as e:
    #     pass


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
#     if text_node.text_type not in DelimiterType:
#         raise Exception(f"Invalid text type: {text_node.text_type}")
#     DelimiterType.TEXT:
#         return ParentNode(tag=None, text=text_node.text)  # type: ignore
#     DelimiterType.BOLD:
#         return ParentNode(tag="b", text=text_node.text)
#     DelimiterType.ITALIC:
#         return ParentNode(tag="i", text=text_node.text)
#     DelimiterType.CODE:
#         return ParentNode(tag="code", text=text_node.text)
#     DelimiterType.LINK:
#         return ParentNode(tag="a", text=text_node.text, props={"href": text_node.url})
#     DelimiterType.IMAGE:
#         return ParentNode(
#             tag="img",
#             text="",
#             props={"src": text_node.url, "alt": text_node.text},
#         )


# -------------------------------mk doc to html nodes----------------------#
# --------------Markdown blocks-------------#
class MKBlockType(Enum):
    Paragraph = "paragraph"
    Heading = "heading"
    Code = "code"
    Quote = "quote"
    UnorderedList = "unordered_list"
    OrderedList = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    block_list: list[str] = []
    for block in blocks:
        if block == "":
            continue
        block_list.append(block.strip())
    return block_list


def block_to_block_type(markdown_block: str) -> MKBlockType:
    if (
        markdown_block.startswith("# ")
        or markdown_block.startswith("## ")
        or markdown_block.startswith("### ")
        or markdown_block.startswith("#### ")
        or markdown_block.startswith("##### ")
        or markdown_block.startswith("###### ")
    ):
        return MKBlockType.Heading
    elif (
        markdown_block[0:3] == "```"
        and markdown_block[-3 : len(markdown_block)] == "```"
    ):
        return MKBlockType.Code
    elif (
        markdown_block[0] == ">"
        and len(set([item[0] for item in markdown_block.split("\n")])) == 1
    ):
        return MKBlockType.Quote
    elif (
        markdown_block[0] == "-"
        or markdown_block[0] == "*"
        or markdown_block[0] == "+"
        or markdown_block[0] == "-"
    ) and set([item[0:2] for item in markdown_block.split("\n")]) <= set(
        ["- ", "* ", "+ ", "- "]
    ):
        return MKBlockType.UnorderedList
    elif markdown_block.startswith("1. "):
        i = 1
        for line in markdown_block.split("\n"):
            if not line.startswith(f"{i}. "):
                return MKBlockType.Paragraph
            i += 1
        return MKBlockType.OrderedList
    return MKBlockType.Paragraph


def mk_block_child_unpacker(block: str) -> list[HTMLNode]:
    children: list[HTMLNode] = []
    #
    #
    return children


def block_to_htmlnodes(block: str) -> list[HTMLNode]:
    htmlnodes: list[HTMLNode] = []
    # split = block.splitlines(keepends=True)
    split: list[str] = block.split("\n\n")
    for line in split:
        htmlnodes.extend(text_to_htmlnode(line))
    return htmlnodes


def text_to_htmlnode(text: str) -> list[HTMLNode]:
    html_nodes: list[HTMLNode] = []
    html_nodes.extend(delimiter_loop_on_textnodes(text))
    return html_nodes


# def parent_to_leaf(nodes: list[HTMLNode]) -> list[HTMLNode]:
#     for node in nodes:
#         if node.children is None or node.children is []:


def mk_doc_to_html_node(markdown_doc: str) -> HTMLNode:
    markdown_blocks = markdown_to_blocks(markdown_doc)
    block_dict: dict[str, MKBlockType] = {}
    for block in markdown_blocks:
        block_dict[block] = block_to_block_type(block)
    block_html_nodes: list[HTMLNode] = []
    block_tuples: zip[tuple[str, MKBlockType]] = zip(
        block_dict.keys(), block_dict.values()
    )
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
    return GrandparentNode(tag="div", children=block_html_nodes)


def heading_block_to_html_node(heading_block: str) -> HTMLNode:
    children: list[HTMLNode] = []
    stripped: str = heading_block[heading_block[0:6].count("#") + 1 :]
    children.extend(mk_block_child_unpacker(stripped))
    return ParentNode(tag=f"h{heading_block[0:6].count("#")}", children=children)


def code_block_to_html_node(code_block: str) -> HTMLNode:
    children: list[HTMLNode] = []
    stripped: str = code_block.strip("```")
    stripped2 = stripped.lstrip("\n\r\x1d\x1e\u2028\u2029")
    children.append(LeafNode(text=stripped2))
    if bool(children) is False:
        assert "inline children is empty"
    return GrandparentNode(tag="pre", children=children)


def quote_block_to_html_node(quote_block: str) -> HTMLNode:
    children: list[HTMLNode] = []
    stripped: str = quote_block.replace(">", "\n")
    return ParentNode(tag="blockquote", text=stripped, children=children)


def unordered_list_to_html_node(unordered_list_block: str) -> HTMLNode:
    children: list[HTMLNode] = []
    inline_children: list[HTMLNode] = []
    for line in unordered_list_block.split("\n"):
        if (
            line[0] == "-" or line[0] == "*" or line[0] == "+" or line[0] == "-"
        ) and set([item[0:2] for item in unordered_list_block.split("\n")]) <= set(
            ["- ", "* ", "+ ", "- "]
        ):
            inline_children.extend(textnodes_to_html(text_to_textnodes(line[2:])))
            children.append(ParentNode("li", children=inline_children))
            if bool(inline_children) is False:
                assert "inline children is empty"
            inline_children = []
    return GrandparentNode(tag="ul", children=children)


def ordered_list_block_to_html_node(ordered_list_block: str) -> HTMLNode:
    children: list[HTMLNode] = []
    inline_children: list[HTMLNode] = []
    for line in ordered_list_block.split("\n"):
        inline_children.extend(textnodes_to_html(text_to_textnodes(line[3:])))
        children.append(ParentNode("li", children=inline_children))
        if bool(inline_children) is False:
            assert "inline children is empty"
        inline_children = []
    return ParentNode(tag="ol", children=children)


def paragraph_block_to_html_node(paragraph_block: str) -> HTMLNode:
    children: list[HTMLNode] = []
    children.extend(mk_block_child_unpacker(paragraph_block))
    return ParentNode("p", children=children)


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)
