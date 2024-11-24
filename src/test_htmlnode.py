import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("h1", "Hello", None, {"class": "title"})
        self.assertEqual(node.props_to_html(), ' class="title"')

    def test_repr(self):
        text = HTMLNode("p", "Hello")
        node = HTMLNode("div", None, [text], {"id": "main"})
        self.assertEqual(
            repr(node),
            "HTMLNode(div, None, [HTMLNode(p, Hello, None, None)], {'id': 'main'})",
        )

    def test_to_html(self):
        text = HTMLNode("p", "Hello")
        node = HTMLNode("div", None, [text], {"id": "main"})
        self.assertRaises(NotImplementedError, node.to_html)


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "This is a paragraph of text.")

    def test_to_html_no_value(self):
        node = LeafNode("p", None)
        self.assertRaises(ValueError, node.to_html)


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "Italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>Italic text</i>Normal text</p>",
        )

    def test_to_html_no_tag(self):
        node = ParentNode(None, [LeafNode("p", "This is a paragraph of text.")])
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_no_children(self):
        node = ParentNode("div", None)
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_nested(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "Italic text"),
                        LeafNode(None, "Normal text"),
                    ],
                )
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><p><b>Bold text</b>Normal text<i>Italic text</i>Normal text</p></div>",
        )

    def test_to_html_nested_multiple(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "Italic text"),
                        LeafNode(None, "Normal text"),
                    ],
                ),
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "Italic text"),
                        LeafNode(None, "Normal text"),
                    ],
                ),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><p><b>Bold text</b>Normal text<i>Italic text</i>Normal text</p>"
            "<p><b>Bold text</b>Normal text<i>Italic text</i>Normal text</p></div>",
        )

    def test_to_html_nested_no_children(self):
        node = ParentNode("div", [ParentNode("p", None)])
        self.assertRaises(ValueError, node.to_html)


if __name__ == "__main__":
    unittest.main()
