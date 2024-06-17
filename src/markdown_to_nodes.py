from textnode import (TextNode, TextType, type_rules, delimiters, delimiters2, DELIMITER_TO_TYPE)
from typing import Optional, List
from enum import Enum
import re

#-----------------------------Inline Markdown------------------------------#
def split_node_delimiter(old_node: TextNode, delimiter: str) -> List[TextNode]:
    if old_node.text_type != TextType.TEXT:
        return [old_node]
    new_nodes = []
    split = old_node.text.split(delimiter)
    for i, item in enumerate(split):
        if item == "":
            continue
        if i % 2 == 0:
            new_nodes.append(TextNode(item, TextType.TEXT))
        else:
            new_nodes.append(TextNode(item, DELIMITER_TO_TYPE.get(delimiter)))
    return new_nodes

def split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str) -> List[TextNode]:
    new_nodes: List[TextNode] = []
    for node in old_nodes:
    #------unordered list exception-----#
        if delimiter == "*" and node.text[0:2] == "* ":
            unordered_list_text = node.text[2:]
            unordered_list_nodes = split_node_delimiter(TextNode(unordered_list_text, TextType.TEXT), delimiter)
            if unordered_list_nodes[0].text != None:
                unordered_list_nodes[0].text = "* " + unordered_list_nodes[0].text
                new_nodes.extend(unordered_list_nodes)
            else:
                unordered_list_nodes[1].text = "* " + unordered_list_nodes[1].text
                new_nodes.extend(unordered_list_nodes)
    #------unordered list exception-----#
        else:
            new_nodes.extend(split_node_delimiter(node, delimiter))
    return new_nodes

def nested_nodes_unpacker(old_nodes: List[TextNode]):
    unpacked_nodes: List[TextNode] = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            unpacked_nodes.append(node)
        else:
            unpacked_nodes.extend(nest_checker(node))
    return unpacked_nodes

def nest_checker(node: TextNode):
    new_nodes: List[TextNode] = []
    if split_nodes_by_delimiters([TextNode(node.text, TextType.TEXT)])[0].text_type != TextType.TEXT and split_nodes_by_delimiters([TextNode(node.text, TextType.TEXT)])[0].text_type != node.text_type:
        new_nodes.append(TextNode("", node.text_type))
        new_nodes.extend(split_nodes_by_delimiters([TextNode(node.text, TextType.TEXT)]))
        new_nodes.append(TextNode("", node.text_type))
    else:
        new_nodes.append(node)
    return new_nodes

def split_nodes_by_delimiters(nodes: List[TextNode]):
    for delimiter in DELIMITER_TO_TYPE:
        nodes = split_nodes_delimiter(nodes, delimiter)
    return nested_nodes_unpacker(nodes)

def extract_markdown_images(text) -> List[tuple]:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text) -> List[tuple]:
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes: List[TextNode]) -> List[TextNode]:
    new_nodes = []
    image_pattern = re.compile(r"!\[(.*?)\]\((.*?)\)")
    for node in old_nodes:
        if image_pattern.search(node.text) == None:
            if node.text_type == TextType.IMAGE:
                node.text_type = TextType.TEXT
            new_nodes.append(node)
        else:
            images = extract_markdown_images(node.text)
            split = node.text.split(f"![{images[0][0]}]({images[0][1]})", 1)
            if bool(split[0]) == True:
                new_nodes.append(TextNode(split[0], TextType.TEXT))
            new_nodes.append(TextNode(images[0][0], TextType.IMAGE, images[0][1]))
            if len(split) > 1 and bool(split[1]) == True:
                new_nodes.extend(split_nodes_image([TextNode(split[1], TextType.IMAGE)]))
    return new_nodes
            
def split_nodes_link(old_nodes: List[TextNode]) -> List[TextNode]:
    new_nodes = []
    link_pattern = re.compile(r"\[(.*?)\]\((.*?)\)")
    for node in old_nodes:
        if link_pattern.search(node.text) == None:
            if node.text_type == TextType.LINK:
                node.text_type = TextType.TEXT
            new_nodes.append(node)
        else:
            links = extract_markdown_links(node.text)
            split = node.text.split(f"[{links[0][0]}]({links[0][1]})", 1)
            if bool(split[0]) == True:
                new_nodes.append(TextNode(split[0], TextType.TEXT))
            new_nodes.append(TextNode(links[0][0], TextType.LINK, links[0][1]))
            if len(split) > 1 and bool(split[1]) == True:
                new_nodes.extend(split_nodes_link([TextNode(split[1], TextType.LINK)]))
    return new_nodes

def text_to_textnodes(text) -> List[TextNode]:
    node = TextNode(text, TextType.TEXT)
    delimited = split_nodes_by_delimiters([node])
    split_image = split_nodes_image(delimited)
    split_link = split_nodes_link(split_image)
    return split_link

def text_list_to_textnodes(text_list):
    textnodes = []
    for item in text_list:
        textnodes.extend(text_to_textnodes(item))
    return textnodes
  
#print(text_to_textnodes("This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"))

class MKBlockType(Enum):
    Paragraph = "paragraph"
    Heading = "heading"
    Code = "code"
    Quote = "quote"
    UnorderedList = "unordered_list"
    OrderedList = "ordered_list"

def markdown_to_blocks(markdown: str):
    blocks = markdown.split("\n\n")
    block_list = []
    for block in blocks:
        if block == "":
            continue
        block_list.append(block.strip())
    return block_list
# with open("/home/danlern2/bootdevworkspace/static_site/src/markdown_test") as file:
#     markdown_to_blocks(file.read())

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
    elif markdown_block[0:3] == "```" and markdown_block[-3:len(markdown_block)] == "```":
        return MKBlockType.Code
    elif markdown_block[0] == ">" and len(set([item[0] for item in markdown_block.split("\n")])) == 1:
        return MKBlockType.Quote
    elif (markdown_block[0] == "-" or markdown_block[0] == "*" or markdown_block[0] == "+" or markdown_block[0] == "-") and set([item[0:2] for item in markdown_block.split("\n")]) <= set(["- ", "* ", "+ ", "- "]):
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





#####---------- Potential inline nested markdown done properly -----------#######
# from textnode import TextNode

# text_type_text = "text"
# text_type_bold = "bold"
# text_type_italic = "italic"
# text_type_code = "code"
# text_type_link = "link"
# text_type_image = "image"

# def split_nodes_delimiter(
#     old_nodes: list[TextNode], delimiter: str, text_type: str
# ) -> list[TextNode]:
#     """
#     Splits TextNode objects in a list by a given delimiter and converts them
#     into multiple TextNodes of the specified type.

#     Args:
#         - old_nodes (list[TextNode]): List of TextNode objects to be processed.
#         - delimiter (str): The delimiter string used to split the text.
#         - text_type (str): The type of TextNode to create for the text between
#           delimiters.

#     Returns:
#         - list[TextNode]: A new list of TextNode objects, split based on the
#           given
#         delimiter.

#     Raises:
#         - ValueError: If a matching closing delimiter is not found in the text.

#     Example:
#         node = TextNode("This is text with a `code block` word", "text")
#         new_nodes = split_nodes_delimiter([node], "`", "code")
#         # new_nodes will be:
#         # [
#         #     TextNode("This is text with a ", "text"),
#         #     TextNode("code block", "code"),
#         #     TextNode(" word", "text"),
#         # ]
#     """
#     ret: list[TextNode] = []
#     for node in old_nodes:
#         if node.text_type != "text":
#             # Append the TextNode as-is if its type is not text.
#             ret.append(node)
#         else:
#             # Otherwise process the TextNode and extend the main TextNodes list
#             # with the processed TextNodes list.
#             ret.extend(splitter(node.text, delimiter, text_type))
#     return ret


# def splitter(text: str, delim: str, text_type: str) -> list[TextNode]:
#     """
#     Helper function to split a text string by a given delimiter and convert
#     segments into TextNode objects.

#     Args:
#         - text (str): The text to be split.
#         - delim (str): The delimiter string used to split the text.
#         - text_type (str): The type of TextNode to create for the text between
#           delimiters.

#     Returns:
#         - list[TextNode]: A list of TextNode objects created from the split
#           text.

#     Raises:
#         - ValueError: If a matching closing delimiter is not found in the text.

#     Example:
#         text = "This is text with a `code block` word"
#         nodes = splitter(text, "`", "code")
#         # nodes will be:
#         # [
#         #     TextNode("This is text with a ", "text"),
#         #     TextNode("code block", "code"),
#         #     TextNode(" word", "text"),
#         # ]
#     """
#     # All the TextNode segments are stored here for later return.
#     segments: list[TextNode] = []
#     # Used for identifying opening and ending of delimited text.
#     delim_start_found = False
#     # Used for accumulating normal text. This will be reset to empty string when
#     # an opening delimiter is found.
#     normal_segment = ""
#     # Used for accumulating delimited text, the text within `**` from `**bold**`
#     # for example. This will be reset to empty string after finding the closing
#     # delimiter.
#     delim_segment = ""
#     # Keep track of the index position in the target text string.
#     index = 0
#     while index < len(text):
#         # Check if the current position in the text is the start of a delimiter
#         # and that we are not already inside a delimited segment.
#         if text[index : index + len(delim)] == delim and not delim_start_found:
#             # Determine how many times the delimiter is consecutively repeated
#             # starting fom the current index position.
#             delim_repeat_count = get_delim_repeat_count(text, delim, index)
#             if delim_repeat_count > 1:
#                 # If the delimiter is repeated more than once, consider it as
#                 # part of the normal text. Add the repeated delimiter sequence
#                 # to the normal text segment.
#                 normal_segment += text[index : index + len(delim) * delim_repeat_count]
#                 # Advance the index by the length of the repeated delimiter
#                 # sequence.
#                 index += len(delim) * delim_repeat_count
#         # In this `while` block, the program will loop until `index` hits the
#         # length of the target text string.
#         if text[index : index + len(delim)] == delim:
#             # If the program enters this block of code, it means that it is
#             # currently at a certain position in the target text string where
#             # the delimiter exists.
#             if delim_start_found:
#                 # This block of code runs at a closing delimiter.If the program
#                 # hits this block of code, it means that a closing delimiter was
#                 # found. Therefore, we now set the delim_start_found back to
#                 # False.
#                 delim_start_found = False
#                 # And create and append the new TextNode containing the
#                 # delimited segment, for instance if we had the target
#                 # TextNode("This is text with a `code block` word", "text") and
#                 # we were delimiting the backtick, then this block of code would
#                 # append TextNode("code block", "code") to the segments array.
#                 if delim_segment:
#                     segments.append(TextNode(delim_segment, text_type))
#                 # Once we've created TextNode for the delimited text, we reset
#                 # the delim_segment string to get ready for any other delimited
#                 # text segments in the other parts of the target string.
#                 delim_segment = ""
#             else:
#                 # This block of code runs at an opening delimiter. Therefore, we
#                 # set delim_start_found to True.
#                 delim_start_found = True
#                 # If a normal text exists prior to a delimited text (e.g.
#                 # TextNode("This is a text with a `code block` word", "text"),
#                 # where "This is a text with a " is the normal text), we need to
#                 # create a separate normal text node for it.
#                 if normal_segment:
#                     # Ensure that `normal_segment` is not empty, emptied
#                     # normal_segment can happen if there is a delimited text at
#                     # the beginning of the target text for example:
#                     # TextNode("**bold** text is at the start", "text").
#                     segments.append(TextNode(normal_segment, "text"))
#                     # Once we've created TextNode for the normal text, we reset
#                     # the normal_segment string to get ready for any other
#                     # normal text segments in the other parts of the target
#                     # string.
#                     normal_segment = ""
#         else:
#             # The program enters this block of code if the current substring
#             # within the target text string is not the delimiter.
#             if delim_start_found:
#                 # Even if the current substring within the target text string is
#                 # not a delimiter, it can be a delimited string like "This is a
#                 # `**bold**` text", where we could current be at for instance
#                 # character `l` in the word "bold" which is part of a delimited
#                 # text. Therefore, we concatenate the substring to
#                 # `delim_segment`. But we only do this if we know that we've
#                 # previously found the opening delimiter.
#                 delim_segment += text[index]
#             else:
#                 # However, if the current substring that we're looking at is not
#                 # a part of the delimited string, then it is considered as a
#                 # normal string; therefore, we concatenate the current substring
#                 # to the `normal_segment`.
#                 normal_segment += text[index]
#         # Suppose that we reached the end of the target text string there was no
#         # more delimiter found, then if there's anything in `normal_segment` it
#         # means that the remaining text was a normal text, then create TextNode
#         # and append it to `segments`.
#         if index == len(text) - 1 and not delim_start_found and normal_segment:
#             segments.append(TextNode(normal_segment, "text"))
#         # This is where we increment the `index` value, but the size of the
#         # increment will vary by two different situations.
#         if text[index : index + len(delim)] == delim:
#             # One situation is when we find a delimiter, we need to advance the
#             # index by the length of the delimiter because in the next loop, we
#             # want to just see the delimited text string instead of another
#             # character of delimiter itself if the delimiter string is more than
#             # one cahracter long such as `**` for bold.
#             index += len(delim)
#         else:
#             # Otherwise, if the current substring is not a delimiter, just
#             # advanced index by one.
#             index += 1
#     # If `delim_start_found` is not False at this point, it means that we did
#     # not find any ending delimiter; therefore, the markdown syntax is invalid.
#     # For example, if the text "**bold string" is provided, we will have to
#     # raise the ValueError because `**` does not close.
#     if delim_start_found:
#         raise ValueError("Invalid markdown syntax.")
#     return segments


# def get_delim_repeat_count(text: str, delim: str, index: int) -> int:
    """
    Determine the number of consecutive repetitions of a delimiter starting from
    a given index in the text.

    Args:
        text (str): The text to be analyzed for repeated delimiters.
        delim (str): The delimiter string to count repetitions of.
        index (int): The starting index in the text to begin counting from.

    Returns:
        int: The count of consecutive delimiter repetitions.

    Example:
        count = get_delim_repeat_count("**bold** text", "*", 0)

        # count will be 2 because there are two consecutive instances of the
        delimiter "*" immediately following the index before breaking out of the
        loop.
    """
    repeated_count = 1
    while index < len(text):
        start_index = index + len(delim)
        end_index = index + 2 * len(delim)
        if text[start_index:end_index] == delim:
            repeated_count += 1
        else:
            break
        index = end_index
    return repeated_count