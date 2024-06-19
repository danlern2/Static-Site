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
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
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
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


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
