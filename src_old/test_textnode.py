import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq1(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2, "is not equal")
    def test_eq2(self):
        node3 = TextNode("This is a text node", "italic", "http://localhost:8888/")
        node4 = TextNode("This is a text node but wrong", "italic", "http://localhost:8888/")
        self.assertEqual(node3, node4, "is not equal")
    def test_eq3(self):
        node5 = TextNode("This is a text node", "italic", "http://localhost:8888/")
        node6 = TextNode("This is a text node", "bold", "http://localhost:8888/")
        self.assertEqual(node5, node6, "is not equal")
    def test_eq4(self):
        node7 = TextNode("This is a text node", "bold")
        node8 = TextNode("This is a text node", "bold", None)
        self.assertEqual(node7, node8, "is not equal")
    def test_eq5(self):
        node7 = TextNode("This is a text node", "bold")
        node8 = TextNode("This is a text node", "bold", "https://www.boot.dev/lessons/0abc7ce4-3855-4624-9f2d-7e566690fee1")
        self.assertEqual(node7, node8, "is not equal")



if __name__ == "__main__":
    unittest.main()
