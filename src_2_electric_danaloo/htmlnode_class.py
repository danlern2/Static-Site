from __future__ import annotations
# from delimiter_rules import bold_rule, italic_rule, link_rule, image_rule, strike_rule


# DELIM_TO_RULE: dict[str,] = {
#     "**": bold_rule,
#     "__": bold_rule,
#     "~~": strike_rule,
#     "*": italic_rule,
#     "_": italic_rule,
#     "[": link_rule,
#     "!": image_rule,
# }

## ============ HTMLNode Class =============##


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        text: str | None = None,
        # children: list[HTMLNode] | None = None,
        props: dict[str, str] | None = None,
    ):
        self.tag = tag
        self.text = text
        # self.children: list[HTMLNode] | None = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag}, '{self.text}', {self.props})"

    def print_details(self):
        print(f"Tags: {self.tag}")
        if self.text is None:
            print(f"Value: {self.text}")
        elif len(self.text) < 21:
            print(f"Value: {self.text[0:10]}")
        else:
            print(f"Value: {self.text[0:10]} ...{self.text[-20:len(self.text)]}")
        # print(f"Children: {self.children}")
        print(f"Props: {self.props}")

    def to_html(self) -> str | None:
        raise NotImplementedError

    def props_to_html(self):
        prop = ""
        if self.props is None:
            return prop
        for key in self.props:
            prop += f' {key}="{self.props[str(key)]}"'
        return prop


class LeafNode(HTMLNode):
    def __init__(self, text: str):
        super().__init__(None, text, None)

    def __repr__(self):
        return f"HTMLNode('{self.text}')"

    def to_html(self) -> str | None:
        if self.text is None:
            raise ValueError
        return self.text


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        # text: str | None,
        children: list[HTMLNode],
        props: dict[str, str] | None = None,
    ):
        super().__init__(tag, None, props)
        self.children: list[HTMLNode] = children
        for child in children:
            assert isinstance(child, HTMLNode)

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.children}, {self.props})"

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("Missing tag argument.")
        elif bool(self.children) is False:
            raise ValueError("Missing children argument.")
        html_string: str = ""
        html_string += f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html_string += child.to_html()  # type: ignore
        html_string += f"</{self.tag}>"  # type: ignore
        return html_string  # type: ignore


GrandparentNode = ParentNode

## ============ HTMLNode Class =============##
