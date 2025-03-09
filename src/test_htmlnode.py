import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        expected_result = 'href="https://www.google.com" target="_blank"'

        self.assertEqual(node.props_to_html(), expected_result)

    def test_to_html(self):
        node = HTMLNode("h", "value", "p", {"href": "https://www.google.com", "target": "_blank"})
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_correct_node_repr(self):
        node = HTMLNode("h", "value", "p", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(str(node), 'HTMLNode(tag= h, value= value, children= p, props= href="https://www.google.com" target="_blank")')
