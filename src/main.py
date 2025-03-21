from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode
from extract_markdown_images_and_links import *
from block_markdown_functions import *
from inline_markdown_functions import *
import re

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
    
def markdown_to_html_node(markdown):
    block_nodes = []
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.HEADING:
            children_nodes = []
            heading_tag = f"h{len(block.split()[0])}"
            heading_text_nodes = text_to_textnodes(block.lstrip("# "))
            for node in heading_text_nodes:
                children_nodes.append(text_node_to_html_node(node))
            
            block_nodes.append(ParentNode(heading_tag, children_nodes))

        elif block_type == BlockType.CODE:
            outer_heading_tag = "pre"
            text_node = TextNode(block.strip("```").lstrip("\n"), TextType.CODE)
            inner_node = text_node_to_html_node(text_node)
            outer_node = ParentNode(outer_heading_tag, [inner_node])

            block_nodes.append(outer_node)

        elif block_type == BlockType.QUOTE:
            outer_tag = "blockquote"
            children_nodes = []
            text_nodes = text_to_textnodes(block.replace("\n> ", " ").lstrip("> "))
            for node in text_nodes:
                children_nodes.append(text_node_to_html_node(node))

            block_nodes.append(ParentNode(outer_tag, children_nodes))

        elif block_type == BlockType.ORDERED_LIST:
            outer_tag = "ol"
            list_tag = "li"
            children_nodes = []
            list_items = block.split("\n")
            for item in list_items:
                item_children = text_to_textnodes(re.sub("([0-9])+. ", "", item))
                item_parent = ParentNode(list_tag, [text_node_to_html_node(child) for child in item_children])
                children_nodes.append(item_parent)
            
            block_nodes.append(ParentNode(outer_tag, children_nodes))

        elif block_type == BlockType.UNORDERED_LIST:
            outer_tag = "ul"
            list_tag = "li"
            children_nodes = []
            list_items = block.split("\n")
            for item in list_items:
                item_children = text_to_textnodes(item.lstrip("- "))
                item_parent = ParentNode(list_tag, [text_node_to_html_node(child) for child in item_children])
                children_nodes.append(item_parent)
            
            block_nodes.append(ParentNode(outer_tag, children_nodes))

        elif block_type == BlockType.PARAGRAPH:
            outer_tag = "p"
            children_nodes = []
            text_nodes = text_to_textnodes(block.replace("\n", " "))
            
            block_nodes.append(ParentNode(outer_tag, [text_node_to_html_node(node) for node in text_nodes]))
    
    return ParentNode("div", block_nodes)
    


def main():
    # dummy_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")

    # print(dummy_node)

    # props = {
    # "href": "https://www.google.com",
    # "target": "_blank",
    # }


    # node = HTMLNode(tag="p", value="text", props=props)

    # print(node)

    md = """###### This is a heading with a **bolded** word.

    ```This is a code block 
    with a **bold** word```

    > This is a quote block with some _italics_.
    > A second line in the quote block.

    1. This is an ordered list
    2. Second item with a **bold** word

    - This is an unordered list.
    - The second item with some _fancy_ italics.

    This is a normal paragraph block.
    This is a newline in the same paragraph block.

    """
    

    # for node in markdown_to_html_node(md):
    #     print(node.to_html())
    print(markdown_to_html_node(md).to_html())

if __name__ == "__main__":
    main()