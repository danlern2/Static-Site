from __future__ import annotations
from enum import Enum
import re

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"
type_rules = ["text", "bold", "italic", "code", "link", "image"]
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


class TextNode:
    def __init__(self, text: str, text_type: str, url: str | None = None):
        self.text: str = text
        self.text_type: str = text_type
        self.url: str | None = url

    def __eq__(self: TextNode, other: TextNode) -> bool:  # type: ignore
        if (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        ):
            return True
        return False

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


class TextType(Enum):
    TEXT: str = "text"
    BOLD: str = "bold"
    ITALIC: str = "italic"
    CODE: str = "code"
    LINK: str = "link"
    IMAGE: str = "image"


DELIMITER_TO_TYPE = {
    "**": TextType.BOLD,
    # '__': TextType.BOLD,
    "*": TextType.ITALIC,
    # '_': TextType.ITALIC,
    "`": TextType.CODE,
}
REGEX_TO_TYPE = {
    re.compile(r"(\*\*\b)|(\b\*\*)"): TextType.BOLD,
    re.compile(r"(__\b)|(\b__)"): TextType.BOLD,
    re.compile(r"(\*\b)|(\b\*)"): TextType.ITALIC,
    re.compile(r"(_\b)|(\b_)"): TextType.ITALIC,
}
