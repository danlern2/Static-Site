import unittest
from textnode import (TextNode, TextType)
from markdown_to_nodes import delimiter_loop_on_textnodes
class TestHTMLNode(unittest.TestCase):
    pass
    def test_delimiter_loop_on_textnodes2(self):
        # Arrange
        node = TextNode("hello, **This is your *captain* speaking**", TextType.TEXT)
        # Act
        actual_nodes = delimiter_loop_on_textnodes([node])
        print(actual_nodes)
        # Assert
        expected_nodes = [
            TextNode("hello, ", TextType.TEXT, None),
            TextNode("", TextType.BOLD, None),
            TextNode("This is your ", TextType.TEXT, None),
            TextNode("captain", TextType.ITALIC, None),
            TextNode(" speaking", TextType.TEXT, None),
            TextNode("", TextType.BOLD, None),
        ]
        self.assertListEqual(actual_nodes, expected_nodes)

if __name__ == "__main__":
    unittest.main()