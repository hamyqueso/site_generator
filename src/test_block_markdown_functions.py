import unittest
from block_markdown_functions import *

class TestBlockMarkdownModule(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
            md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

    def test_block_to_block_type(self):
        md = """
            # This is a heading

            This is **bolded** paragraph

            This is another paragraph with _italic_ text and `code` here
            This is the same paragraph on a new line

            - This is a list
            - with items

            1. This is an ordered list
            2. Second item

            ```This is a code block```

            > This is a quote block
            """
        
        blocks = markdown_to_blocks(md)
        results = []

        for block in blocks:
             results.append(block_to_block_type(block))

        self.assertListEqual(
             results,
             [
                  BlockType.HEADING,
                  BlockType.PARAGRAPH,
                  BlockType.PARAGRAPH,
                  BlockType.UNORDERED_LIST,
                  BlockType.ORDERED_LIST,
                  BlockType.CODE,
                  BlockType.QUOTE
             ]
        )

    def test_block_to_block_type_no_block(self):
        md = """
            """
        
        blocks = markdown_to_blocks(md)
        results = []

        for block in blocks:
             results.append(block_to_block_type(block))

        self.assertRaises(ValueError)

    def test_block_to_block_types2(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
         

if __name__ == "__main__":
    main()