from __future__ import annotations
import re
from htmlnode_class import (
    HTMLNode,
    LeafNode,
    ParentNode,
)
from imports import DELIMITER_TO_TYPE



# //!𝗦𝗘𝗖𝗧𝗜𝗢𝗡 - 𝗥𝘂𝗹𝗲𝘀​


def delimiter_nester_in_node(node: ParentNode, text: str):
    children: list[HTMLNode] = node.children
    result: tuple[list[HTMLNode], str] = base_rule(text)
    children.extend(result[0])
    return node


def base_rule(text: str) -> tuple[list[HTMLNode], str]:
    children: list[HTMLNode] = []
    plain_text: str = ""

    for i in range(len(text)):
        for delim in DELIMITER_TO_TYPE:
            if text[i:].startswith(delim):
                if (delim == "!" or delim == "[") and link_and_image_checker(
                    text[i:], delim
                ) is False:
                    continue
                # # * Check for the ending delimiter. If its a fake delimiter, continue.
                # if delim != "!" and delim != "[" and end_delimiter_checker(text[i+len(delim):], delim) is False:
                #     continue
                plain_text = text[:i]
                # * Since a delimiter rule was called, there is no more plain text. take what you have and append it as a leafnode
                children.append(LeafNode(plain_text))
                # * Reset plain text so it returns blank.
                plain_text = ""
                # * Make a new parentnode with the tag type of the delimiter
                delim_parent = ParentNode(DELIMITER_TO_TYPE[delim], children=[])
                # * Call the delimiter specific rule on all the remaining text except the delimiter itself
                rule_result: tuple[list[HTMLNode], str] = DELIM_TO_RULE[delim](
                    text[i + len(delim) :], delim
                )  # type: ignore
                # * Check if the result has a prop, and if it does add it into the ParentNode
                if len(rule_result) == 3:
                    delim_parent.props = rule_result[2]
                # * Add whatever nested children were made in the rule to the delimiter parent's children list
                delim_parent.children.extend(rule_result[0])
                # * Recursive call on the remaining text returned from the rule
                rest_of_text_result: tuple[list[HTMLNode], str] = base_rule(
                    rule_result[1]
                )
                plain_text += rest_of_text_result[1]
                children.append(delim_parent)
                children.extend(rest_of_text_result[0])
                return children, plain_text

    children.append(LeafNode(text))
    # * return children, plain_text
    return children, text


def delimited_rule(
    text: str, end_delim: str
) -> tuple[list[HTMLNode], str]:
    children: list[HTMLNode] = []
    plain_text: str = ""
    if len(text) <= len(end_delim):
        return children, plain_text
    for i in range(len(text)):
        for delim in DELIMITER_TO_TYPE:
            if text[i:].startswith(delim):
                if (delim == "!" or delim == "[") and link_and_image_checker(
                    text[i:], delim
                ) is False:
                    continue
            # # # * Check for the ending delimiter. If its a fake delimiter, continue.
            # if text[i:].startswith(delim) and delim != "!" and delim != "[" and delim != end_delim and end_delimiter_checker(text[i+len(delim):], delim) is False:
            #     continue
                
            # * If you find the same delimiter the rule is currently checking for, you have found the end of the rule.
            # * return whatever text is found as a leafnode, and any remaining text
            if text[i:].startswith(delim) and (delim == end_delim):
                plain_text = text[:i]
                children.append(LeafNode(plain_text))
                return children, text[i + len(delim) :]

            elif text[i:].startswith(delim):
                plain_text = text[:i]
                # * Since a delimiter rule was called, there is no more plain text. take what you have and append it as a leafnode
                children.append(LeafNode(plain_text))
                # * Reset plain text so it returns blank.
                plain_text = ""
                # * Make a new parentnode with the tag type of the delimiter
                delim_parent = ParentNode(DELIMITER_TO_TYPE[delim], children=[])
                # * Call the delimiter specific rule on all the remaining text except the delimiter itself
                rule_result: tuple[list[HTMLNode], str] = DELIM_TO_RULE[delim](
                    text[i + len(delim) :], delim
                )  # type: ignore
                # * Check if the result has a prop, and if it does add it into the ParentNode
                if len(rule_result) == 3:
                    delim_parent.props = rule_result[2]
                # * Add whatever nested children were made in the rule to the delimiter parent's children list
                delim_parent.children.extend(rule_result[0])
                children.append(delim_parent)

                if len(rule_result[1]) > len(delim):
                    # * Recursive call on the remaining text returned from the rule
                    rest_of_delimited: tuple[list[HTMLNode], str] = delimited_rule(
                        rule_result[1], end_delim
                    )
                    children.extend(rest_of_delimited[0])
                    return children, rest_of_delimited[1]
                else:
                    return children, plain_text
    children.append(LeafNode(text))
    return children, plain_text


def code_rule(text: str, delim: str) -> tuple[list[HTMLNode], str]:
    children: list[HTMLNode] = []
    plain_text: str = ""
    # * Inline code can not contain nested markdown. Find all the text within the delimiters, and return the rest.
    for i in range(len(text)):
        if text[i:].startswith(delim):
                plain_text = text[:i]
                children.append(LeafNode(plain_text))
                return children, text[i + len(delim) :]

    return children, text


def link_rule(text: str, delim: str) -> tuple[list[HTMLNode], str, dict[str, str]]:
    text = "[" + text
    children: list[HTMLNode] = []
    plain_text: str = ""
    prop: dict[str, str] = {}
    # * Check the delimiter, and depending on which it is set a regex pattern for it and make a match.
    pattern = re.compile(r"\[(.*?)\]\((.*?)\)")
    match: re.Match[str] | None = re.match(pattern, string=text)
    # * Find the groupings the pattern has made (returned as a list), and assign the appropriate list indexes to the alt_text and url.
    found = re.findall(pattern, text)
    alt_text: str  = found[0][0]
    url: str  = found[0][1]
    # * Assign the plain_text to all of the text after a found match's ending span.
    plain_text = text[match.span()[1]:]  # type: ignore ⁡⁢⁢⁣text[match.span()[1] + 1:]⁡
    prop["href"] = url
    # prop["alt"] = alt_text
    children.append(LeafNode(alt_text))
    return children, plain_text, prop


def image_rule(text: str, delim: str) -> tuple[list[HTMLNode], str, dict[str, str]]:
    text = "!" + text
    children: list[HTMLNode] = []
    plain_text: str = ""
    prop: dict[str, str] = {}
    pattern = re.compile(r"!\[(.*?)\]\((.*?)\)")
    match: re.Match[str] | None = re.match(pattern, string=text)
    # * Find the groupings the pattern has made (returned as a list), and assign the appropriate list indexes to the alt_text and url.
    found = re.findall(pattern, text)
    alt_text: str  = found[0][0]
    url: str = found[0][1]
    # * Assign the plain_text to all of the text after a found match's ending span.
    plain_text = text[match.span()[1] + 1 :]  # type: ignore
    prop["src"] = url
    prop["alt"] = alt_text
    children.append(LeafNode("")) #//!Look into if this is a problem later 
    ## Example node: image_node: HTMLNode = ParentNode("img", children=list[HTMLNode], props={"src": "", "alt": ""}) # props={"src": /url/, "alt": /the alt text/}
    return children, plain_text, prop


def link_and_image_checker(text: str, delim: str) -> bool:
    # if delim == "!" and re.match(r"!\[(.*?)\]\((.*?)\)", string=text).span[0] is not None:
    if delim == "!":
        pattern = re.compile(r"!\[(.*?)\]\((.*?)\)")
        imatch: re.Match[str] | None = re.match(pattern, string=text)
        if imatch is not None and imatch.span()[0] == 0:
            return True
    elif delim == "[":
        pattern = re.compile(r"\[(.*?)\]\((.*?)\)")
        lmatch: re.Match[str] | None = re.match(pattern, string=text)
        if lmatch is not None and lmatch.span()[0] == 0:
            return True
    return False

# def end_delimiter_checker(text: str, delim: str) -> bool:
#     for i in range(len(text)):
#         if text[i:].startswith(delim) and text[i-len(delim):i] == delim and text[i+1:i+len(delim)+1] == delim:
#             continue
#         if text[i:].startswith(delim) and text[i-1:i].isspace() and (not text[i+len(delim):].startswith("**") or not text[i+len(delim):].startswith("__")):
#             return False

#         # * If the leading character is a space, youre at the start of a delimiter, not the end.
#         if text[i:].startswith(delim) and text[i-1:i].isspace():
#             continue
#         if text[i:].startswith(delim) and (delim == "**" or delim == "__"):
#             return True
#         if text[i:].startswith(delim) and text[i:i+1] == text[i+1:i+2]:
#             continue
#         if text[i:].startswith(delim) and (i == (len(text)-1) or (text[i+1:i+1+len(delim)].isspace() or not text[i+1:i+1+len(delim)].isalpha())):
#             return True
#     return False



DELIM_TO_RULE = {
    "`": code_rule,
    "**": delimited_rule,
    "__": delimited_rule,
    "~~": delimited_rule,
    "*": delimited_rule,
    "_": delimited_rule,
    "!": image_rule,
    "[": link_rule,
}


def test():
    text = "blep *Text **like this** b*"
    delimited = base_rule(text)
    print(delimited)
    return

test()

