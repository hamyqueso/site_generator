from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode
from extract_markdown_images_and_links import *

def text_node_to_html_node(text_node):
    text = text_node.text
    html_tag = text_node.return_html_tag()
    url = text_node.url

    if html_tag == 'a':
        props = {"href":url}
        return LeafNode(html_tag, text, props)
    elif html_tag == 'img':
        props = {"src":url, "alt":text}
        return LeafNode(html_tag, "", props)
    else:
        return LeafNode(html_tag, text)
    


def main():
    # dummy_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")

    # print(dummy_node)

    props = {
    "href": "https://www.google.com",
    "target": "_blank",
    }

    node = HTMLNode(tag="p", value="text", props=props)

    print(node)

if __name__ == "__main__":
    main()