import unittest

from textnode import *
from htmlnode import *
from main import *
from inline_markdown_functions import *

class TestMainModule(unittest.TestCase):
    
    # text_node_to_html_node tests

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, "This is a text node")

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {"href": node.url})

    def test_image(self):
        node = TextNode("This is a text node", TextType.IMAGE, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src":node.url, "alt":node.text})

    # split_nodes_delimiter tests

    def test_split_nodes_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        )

    def test_split_nodes_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        )

    def test_split_nodes_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        )

    def test_split_nodes_no_closing_delimiter_error(self):
        node = TextNode("This is text with a `code block' word", TextType.TEXT)
        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

    def test_split_nodes_no_closing_delimiter_error_bold(self):
        node = TextNode("This is text with a **bold* word", TextType.TEXT)
        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )
    
    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        # print(f"new nodes: {new_nodes}")
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_image_first(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png) is the first image and "
        "![second image](https://i.imgur.com/3elNhQu.png) is the second image",
            TextType.TEXT,)
        
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" is the first image and ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" is the second image", TextType.TEXT),
            ], new_nodes)
        
    def test_split_images_no_image(self):
        node = TextNode("This is text with no image tags", TextType.TEXT)
        new_nodes = split_nodes_image([node])

        self.assertListEqual([TextNode("This is text with no image tags", TextType.TEXT)], new_nodes)

    def test_split_images_one_image_first(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png) is the first image",
            TextType.TEXT,)
        
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" is the first image", TextType.TEXT),
            ], new_nodes)
        
    def test_split_images_one_image_second(self):
        node = TextNode("This is the first image ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,)
        
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [   
                TextNode("This is the first image ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),

            ], new_nodes)
        
    
    def test_split_images_three_images(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png) is the first image and "
        "![second image](https://i.imgur.com/3elNhQu.png) is the second image"
        " and the third image is ![third image](https://i.imgur.com/elNhQu.png)",
            TextType.TEXT,)
        
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" is the first image and ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" is the second image and the third image is ", TextType.TEXT),
                TextNode("third image", TextType.IMAGE, "https://i.imgur.com/elNhQu.png")
            ], new_nodes)
        
    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )
        
    def test_split_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

        self.assertListEqual([
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ], new_nodes)

    def test_split_link_first(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev) this is text with a link and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

        self.assertListEqual([
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" this is text with a link and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ], new_nodes)

    def test_split_one_link_first(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev) this is text with a link",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

        self.assertListEqual([
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" this is text with a link", TextType.TEXT),
        ], new_nodes)

    def test_split_one_link_first(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev) this is text with a link",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

        self.assertListEqual([
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" this is text with a link", TextType.TEXT),
        ], new_nodes)

    def test_split_no_link(self):
        node = TextNode(
            "This is text without a link",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

        self.assertListEqual([
            TextNode("This is text without a link", TextType.TEXT),
        ], new_nodes)

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` " \
        "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        new_nodes = text_to_textnodes(text)

        self.assertListEqual([
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
            )

class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
        ```
        This is text that _should_ remain
        the **same** even with inline stuff
        ```
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        # print(html)
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    

    def test_lists(self):
        md = """
        - This is a list
        - with items
        - and _more_ items

        1. This is an `ordered` list
        2. with items
        3. and more items

        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
        # this is an h1

        this is paragraph text

        ## this is an h2
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
        > This is a
        > blockquote block

        this is paragraph text

        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_blockquote_blank_line(self):
        md = '''
            > "I am in fact a Hobbit in all but size."
            >
            > -- J.R.R. Tolkien
            '''
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
        '<div><blockquote>"I am in fact a Hobbit in all but size." -- J.R.R. Tolkien</blockquote></div>'
        )

    def test_paragraph(self):
        md = """
        This is **bolded** paragraph
        text in a p
        tag here

        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        md = "# Hello"

        title = extract_title(md)

        self.assertEqual(
            title,
            "Hello"
        )

    def test_no_title(self):
        md = """
            This is **bolded** paragraph
            text in a p
            tag here

            """
        
        with self.assertRaises(Exception):
            title = extract_title(md)

    def test_title_not_in_first_block(self):
        md = """
            This is **bolded** paragraph
            text in a p
            tag here

            # Hello
            """
        
        title = extract_title(md)

        self.assertEqual(
            title,
            "Hello"
        )