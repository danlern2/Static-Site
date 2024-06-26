from __future__ import annotations
from textnode import TextNode, TextType, DELIMITER_TO_TYPE
from typing import List
from enum import Enum
import re

# -----------------------------Inline Markdown------------------------------#
# def split_node_delimiter(old_node: TextNode, delimiter: str) -> List[TextNode]:
#     if old_node.text_type != TextType.TEXT:
#         return [old_node]
#     new_nodes = []
#     split = old_node.text.split(delimiter)
#     for i, item in enumerate(split):
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
#     #------unordered list exception-----#
#         if delimiter == "*" and node.text[0:2] == "* ":
#             unordered_list_text = node.text[2:]
#             unordered_list_nodes = split_node_delimiter(TextNode(unordered_list_text, TextType.TEXT), delimiter)
#             if unordered_list_nodes[0].text != None:
#                 unordered_list_nodes[0].text = "* " + unordered_list_nodes[0].text
#                 new_nodes.extend(unordered_list_nodes)
#             else:
#                 unordered_list_nodes[1].text = "* " + unordered_list_nodes[1].text
#                 new_nodes.extend(unordered_list_nodes)
#     #------unordered list exception-----#
#         else:
#             new_nodes.extend(split_node_delimiter(node, delimiter))
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

# def extract_markdown_images(text) -> List[tuple]:
#     return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

# def extract_markdown_links(text) -> List[tuple]:
#     return re.findall(r"\[(.*?)\]\((.*?)\)", text)

# def split_nodes_image(old_nodes: List[TextNode]) -> List[TextNode]:
#     new_nodes = []
#     image_pattern = re.compile(r"!\[(.*?)\]\((.*?)\)")
#     for node in old_nodes:
#         if image_pattern.search(node.text) == None:
#             if node.text_type == TextType.IMAGE:
#                 node.text_type = TextType.TEXT
#             new_nodes.append(node)
#         else:
#             images = extract_markdown_images(node.text)
#             split = node.text.split(f"![{images[0][0]}]({images[0][1]})", 1)
#             if bool(split[0]) == True:
#                 new_nodes.append(TextNode(split[0], TextType.TEXT))
#             new_nodes.append(TextNode(images[0][0], TextType.IMAGE, images[0][1]))
#             if len(split) > 1 and bool(split[1]) == True:
#                 new_nodes.extend(split_nodes_image([TextNode(split[1], TextType.IMAGE)]))
#     return new_nodes

# def split_nodes_link(old_nodes: List[TextNode]) -> List[TextNode]:
#     new_nodes = []
#     link_pattern = re.compile(r"\[(.*?)\]\((.*?)\)")
#     for node in old_nodes:
#         if link_pattern.search(node.text) == None:
#             if node.text_type == TextType.LINK:
#                 node.text_type = TextType.TEXT
#             new_nodes.append(node)
#         else:
#             links = extract_markdown_links(node.text)
#             split = node.text.split(f"[{links[0][0]}]({links[0][1]})", 1)
#             if bool(split[0]) == True:
#                 new_nodes.append(TextNode(split[0], TextType.TEXT))
#             new_nodes.append(TextNode(links[0][0], TextType.LINK, links[0][1]))
#             if len(split) > 1 and bool(split[1]) == True:
#                 new_nodes.extend(split_nodes_link([TextNode(split[1], TextType.LINK)]))
#     return new_nodes


def text_to_textnodes(text: str) -> List[TextNode]:
    node = TextNode(text, TextType.TEXT)
    delimited = delimiter_loop_on_textnodes([node])
    split_image = split_nodes_image(delimited)
    split_link = split_nodes_link(split_image)
    return split_link


def text_list_to_textnodes(text_list: list[str]):
    textnodes: list[TextNode] = []
    for item in text_list:
        textnodes.extend(text_to_textnodes(item))
    return textnodes


# print(
#     text_to_textnodes(
#         "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
#     )
# )


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


# print(block_to_block_type(">quote 1\n>quote 2\n>quote 3"))
# print(block_to_block_type("```this is a code block```"))
# print(block_to_block_type("- This is\n* an\n* unordered_list"))
# print(block_to_block_type("1. This is\n2. an\n3. ordered_list"))


# ------------New split node delimiter------------#
def delimiter_loop_on_textnodes(nodes: List[TextNode]) -> List[TextNode]:
    """
    For each delimiter, send the list of TextNodes to textnodes_loop_with_delimiter(nodes, delimiter)\n
    textnodes_loop_with_delimiter will return a new list of nodes separated by the given delimiter and return a new list\n
    This is will go until all the delimiters are accounted for.\n
    At the end, this will return a fully and properly delimited set of TextNodes including nested ones.
    """
    for delimiter in DELIMITER_TO_TYPE:
        nodes = textnodes_loop_with_delimiter(nodes, delimiter)
    # print(nodes)
    return nodes


def textnodes_loop_with_delimiter(
    nodes: List[TextNode], delimiter: str
) -> list[TextNode]:
    """
    Takes a list of TextNodes and a delimiter. Will send each node in the list and the given delimiter to the split_node_delimiter function and will extend that result to a new list of nodes.\n
    """
    new_nodes: list[TextNode] = []
    for node in nodes:
        # ------unordered list exception-----#
        if delimiter == "*" and node.text[0:2] == "* ":
            unordered_list_text: str = node.text[2:]
            unordered_list_nodes = split_node_delimiter(
                TextNode(unordered_list_text, TextType.TEXT), delimiter
            )
            if unordered_list_nodes[0].text is not None:  # type: ignore
                unordered_list_nodes[0].text = "* " + unordered_list_nodes[0].text
                new_nodes.extend(unordered_list_nodes)
            else:
                unordered_list_nodes[1].text = "* " + unordered_list_nodes[1].text
                new_nodes.extend(unordered_list_nodes)
        # ------unordered list exception-----#
        else:
            new_nodes.extend(split_node_delimiter(node, delimiter))
    return new_nodes


def split_node_delimiter(node: TextNode, delimiter: str) -> List[TextNode]:
    """
    Take a TextNode and a delimiter, check the text of the TextNode against the delimiter and if it contains it, split the text into multiple new textnodes\n
    ## Example:\n
        node = TextNode("This is text with a `code block` word", "text")
        ### new_nodes will be:
        #### [
        ####     TextNode("This is text with a ", "text"),
        ####     TextNode("code block", "code"),
        ####    TextNode(" word", "text"),
        #### ]
    """
    i = 0
    x = 0
    new_nodes: list[TextNode] = []
    text: str = node.text
    if node.text_type != TextType.TEXT:
        new_nodes.append(node)
    elif delimiter in text:
        # ---------------Italic Exception--------------#
        # if (delimiter == "*" or delimiter == "_") and delimiter in text:
        #     italicE = italic_exception(node, delimiter)
        #     new_nodes.extend(italicE[0])
        #     return textnodes_loop_with_delimiter(new_nodes, italicE[1])
        # ---------------Italic Exception--------------#

        # Set i to the first instance index of the delimiter
        i = text.index(delimiter)
        # If there is no match for the delimiter in the rest of the text then its not a true case of that delimiter
        # and append it as is
        if delimiter not in text[i + len(delimiter) :]:
            new_nodes.append(node)
        # Check if there is any delimiter in the first segment. If there is, recursively call on this function to check that delimiter first.
        # Otherwise make that slice from 0 - i of the text a new TextNode and append it to the list.
        if i != 0:
            if nest_checker(text[:i])[0] is False:
                new_nodes.append(TextNode(text[:i], TextType.TEXT))
            else:
                split_node_delimiter(node, nest_checker(text[:i])[1])
        # Set x to the value of the next index where you find the delimiter
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
                split_node_delimiter(TextNode(text[x:], TextType.TEXT), delimiter)
            )
    else:
        new_nodes.append(node)

    return new_nodes


# def italic_exception(node: TextNode, delimiter: str) -> tuple[list[TextNode], str]:
#     i = 0
#     x = 0
#     new_nodes: list[TextNode] = []
#     text: str = node.text

#     # Set i to the first instance index of the delimiter
#     i = text.index(delimiter)
#     # If there is no match for the delimiter in the rest of the text then its not a true case of that delimiter
#     # and append it as is
#     if delimiter not in text[i + 1 :]:
#         raise Exception("Not valid markdown")

#     # Set x to the value of the next index where you find the delimiter
#     x = text[i + 1 :].index(delimiter) + len(text[: i + 1])
#     x += 1
#     # Check if x is not the index of a pair of the delimiter (bold), and if it is, increment x to get outside.
#     if x != len(text) and text[x] == delimiter[0]:
#         x += 1
#     # Check the text again for the delimiter
#     if delimiter not in text[x + len(delimiter) :]:
#         new_nodes.append(node)
#     # If there is another delimiter in the text,

#     return new_nodes, delimiter


# print(italic_exception(TextNode("just *a **little test*** string", TextType.TEXT), "*"))


def splitter(text: str, delimiter: str) -> List[TextNode]:
    """
    Take a text string that has a delimiter in it (already determined by the caller) and split off the ends, creating a 3 part list.\n
    ### Example:
        ["**", "This is bolded text", "**"]\n
    Send the middle text portion of the split to the nest_checker to see if there are any more delimiters in it.\n
    If there's no nested delimiter, return a single item list containing a TextNode with the text and the TextType matching the delimiter.\n
    ### returns:
        [TextNode("This is bolded text", TextType.BOLD)]\n
    If there is a nested delimiter, return 3 textnodes, containing empty text delimiter-typed nodes wrapping a node with the rest of the text and TextType.TEXT.\n
    ### Example:
        ["**", "This is bolded and *italicized* text", "**"]
    ### returns:
        [
        #### TextNode(None, TextType.BOLD),
        #### TextNode("This is bolded and *italicized* text", TextType.TEXT),
        #### TextNode(None, TextType.BOLD)
        ]
    """
    new_nodes: list[TextNode] = []
    split_text: List[str] = []
    split_text.append(text.partition(delimiter)[1])
    split_text.append(text.partition(delimiter)[2].rpartition(delimiter)[0])
    split_text.append(text.partition(delimiter)[2].rpartition(delimiter)[1])
    if nest_checker(split_text[1]) is False:
        new_nodes.append(TextNode(split_text[1], DELIMITER_TO_TYPE.get(delimiter)))  # type: ignore
        return new_nodes
    else:
        new_nodes.append(TextNode("", DELIMITER_TO_TYPE.get(delimiter)))  # type: ignore
        new_nodes.append(TextNode(split_text[1], TextType.TEXT))
        new_nodes.append(TextNode("", DELIMITER_TO_TYPE.get(delimiter)))  # type: ignore
    return new_nodes


def nest_checker(text: str):
    for delim in DELIMITER_TO_TYPE:
        if delim in text:
            return True, delim
    return False, ""


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes: List[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    image_pattern = re.compile(r"!\[(.*?)\]\((.*?)\)")
    for node in old_nodes:
        if image_pattern.search(node.text) is None:
            if node.text_type == TextType.IMAGE:
                node.text_type = TextType.TEXT
            new_nodes.append(node)
        else:
            images = extract_markdown_images(node.text)
            split = node.text.split(f"![{images[0][0]}]({images[0][1]})", 1)
            if bool(split[0]) is True:
                new_nodes.append(TextNode(split[0], TextType.TEXT))
            new_nodes.append(TextNode(images[0][0], TextType.IMAGE, images[0][1]))
            if len(split) > 1 and bool(split[1]) is True:
                new_nodes.extend(
                    split_nodes_image([TextNode(split[1], TextType.IMAGE)])
                )
    return new_nodes


def split_nodes_link(old_nodes: List[TextNode]) -> List[TextNode]:
    new_nodes: list[TextNode] = []
    link_pattern = re.compile(r"\[(.*?)\]\((.*?)\)")
    for node in old_nodes:
        if link_pattern.search(node.text) is None:
            if node.text_type == TextType.LINK:
                node.text_type = TextType.TEXT
            new_nodes.append(node)
        else:
            links = extract_markdown_links(node.text)
            split = node.text.split(f"[{links[0][0]}]({links[0][1]})", 1)
            if bool(split[0]) is True:
                new_nodes.append(TextNode(split[0], TextType.TEXT))
            new_nodes.append(TextNode(links[0][0], TextType.LINK, links[0][1]))
            if len(split) > 1 and bool(split[1]) is True:
                new_nodes.extend(split_nodes_link([TextNode(split[1], TextType.LINK)]))
    return new_nodes
