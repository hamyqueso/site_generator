import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        expected_result = ' href="https://www.google.com" target="_blank"'

        self.assertEqual(node.props_to_html(), expected_result)

    def test_to_html(self):
        node = HTMLNode("h", "value", "p", {"href": "https://www.google.com", "target": "_blank"})
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_correct_node_repr(self):
        node = HTMLNode("h", "value", "p", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(str(node), 'HTMLNode(tag= h, value= value, children= p, props=  href="https://www.google.com" target="_blank")')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello world")
        self.assertEqual(node.to_html(), "<p>Hello world</p>")

    def test_leaf_to_html_h(self):
        node = LeafNode("h1", "Hello world")
        self.assertEqual(node.to_html(), "<h1>Hello world</h1>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_no_tag(self):
        node = LeafNode(None, "Hello world!")
        self.assertEqual(node.tag, None)
        self.assertEqual(node.to_html(), "Hello world!")