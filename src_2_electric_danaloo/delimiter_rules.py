from __future__ import annotations
from htmlnode_class import (
    HTMLNode,
    GrandparentNode,
    LeafNode,
    ParentNode,
)
from markdown_direct_to_html import (
    DELIMITER_TO_TYPE,
    # DELIM_TO_RULE,
)


# def get_rule(delim):
#     from markdown_direct_to_html import DELIM_TO_RULE
#     return DELIM_TO_RULE[delim]


def delimiter_nester_in_node(grandparent_node: GrandparentNode, text: str):
    children: list[HTMLNode] = grandparent_node.children
    result = base_rule(text)
    children.extend(result[0])
    # children.append(LeafNode(result[1]))
    return grandparent_node


def base_rule(text: str) -> tuple[list[HTMLNode], str]:
    children: list[HTMLNode] = []
    plain_text: str = ""

    if len(text) == 0:
        return children, plain_text

    for i in range(len(text)):
        for delim in DELIMITER_TO_TYPE:
            if text[i:].startswith(delim):
                plain_text = text[:i]
                # Since a delimiter rule was called, there is no more plain text. take what you have and append it as a leafnode
                children.append(LeafNode(plain_text))
                # Reset plain text so it returns blank.
                plain_text = ""
                # Make a new parentnode with the tag type of the delimiter
                delim_parent = ParentNode(DELIMITER_TO_TYPE[delim], children=[])
                # Call the delimiter specific rule on all the remaining text except the delimiter itself
                rule_result = DELIM_TO_RULE[delim](text[i + len(delim) :], delim)
                # Add whatever nested children were made in the rule to the delimiter parent's children list
                delim_parent.children.extend(rule_result[0])
                # Recursive call on the remaining text returned from the rule
                rest_of_text_result = base_rule(rule_result[1])
                plain_text += rest_of_text_result[1]
                children.append(delim_parent)
                children.extend(rest_of_text_result[0])
                return children, plain_text

    children.append(LeafNode(text))
    print(f"From base: {children}")
    # return children, plain_text
    return children, text


def delimited_rule(
    text: str, end_delim: str | None = None
) -> tuple[list[HTMLNode], str]:
    children: list[HTMLNode] = []
    plain_text: str = ""
    print(f"top delimited rule = {text}")
    if len(text) == 0:
        return children, plain_text

    for i in range(len(text)):
        for delim in DELIMITER_TO_TYPE:
            if text[i:].startswith(delim) and (delim == end_delim):
                plain_text = text[:i]
                children.append(LeafNode(plain_text))
                return children, text[i + len(delim) :]

            elif text[i:].startswith(delim):
                plain_text = text[:i]
                # Since a delimiter rule was called, there is no more plain text. take what you have and append it as a leafnode
                children.append(LeafNode(plain_text))
                # Reset plain text so it returns blank.
                plain_text = ""
                # Make a new parentnode with the tag type of the delimiter
                delim_parent = ParentNode(DELIMITER_TO_TYPE[delim], children=[])
                # Call the delimiter specific rule on all the remaining text except the delimiter itself
                rule_result: tuple[list[HTMLNode], str] = DELIM_TO_RULE[delim](
                    text[i + len(delim) :], delim
                )
                # Add whatever nested children were made in the rule to the delimiter parent's children list
                delim_parent.children.extend(rule_result[0])
                children.append(delim_parent)
                # Recursive call on the remaining text returned from the rule
                rest_of_delimited = delimited_rule(rule_result[1], end_delim)
                children.extend(rest_of_delimited[0])
                print(f"from delimited 2{children}")
                return children, rest_of_delimited[1]
    children.append(LeafNode(text))
    print(f"From delimited: {children}")
    return children, plain_text


def code_rule(text: str, end_delim: str | None = None) -> tuple[list[HTMLNode], str]:
    children: list[HTMLNode] = []
    plain_text: str = ""
    return children, plain_text


def image_rule(text: str, end_delim: str | None = None) -> tuple[list[HTMLNode], str]:
    # image_node: HTMLNode = ParentNode("img", children=list[HTMLNode], props={"src": "", "alt": ""}) # props={"src": /url/, "alt": /the plain text/}
    children: list[HTMLNode] = []
    plain_text: str = ""
    url: LeafNode = LeafNode("")
    return children, plain_text


def link_rule(text: str, end_delim: str | None = None) -> tuple[list[HTMLNode], str]:
    # link_node: HTMLNode = ParentNode("a", children=list[HTMLNode], props={"href": }) # props={"href": /url/}
    children: list[HTMLNode] = []
    plain_text: str = ""
    url: LeafNode = LeafNode("")
    return children, plain_text


DELIM_TO_RULE = {
    "`": code_rule,
    "**": delimited_rule,
    "__": delimited_rule,
    "~~": delimited_rule,
    "*": delimited_rule,
    "_": delimited_rule,
    "[": link_rule,
    "!": image_rule,
}
# return delimiter_nester_in_node()


node = GrandparentNode("pre", children=[])
text = "This is an *italic-~~__containing__~~ sentence, **and also has** bold*"

print(delimiter_nester_in_node(node, text))
