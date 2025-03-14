import unittest

from extract_markdown_images_and_links import extract_markdown_images, extract_markdown_links

class TestExtractMarkdown(unittest.TestCase):
    def test_extract_image(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_link(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_link_none(self):
        matches = extract_markdown_links(
            "this is a text without links"
        ) 
        
        self.assertListEqual([], matches)

    def test_extract_image_none(self):
        matches = extract_markdown_images(
            "this is a text without images"
        )

        self.assertListEqual([], matches)

if __name__ == "__main__":
    unittest.main()