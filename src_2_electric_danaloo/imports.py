from enum import Enum


class TagType(Enum):
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

BLOCK_TAGS: set[str] = {
    "ol",
    "ul",
    "pre",
    "blockquote",
    f"h{int}",
    "p",
    "div",

}


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
    "code": TagType.CODE,
    "b": TagType.BOLD,
    # "b": TagType.BOLD,
    "strikethrough": TagType.STRIKE,
    "i": TagType.ITALIC,
    # "i": TagType.ITALIC,
    "img": TagType.IMAGE,
    "a": TagType.LINK,
}

