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
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        else:
            lines = node.text.split(delimiter)
            if len(lines) % 2 == 0:
                raise Exception("Invalid markdown syntax: missing matching closing delimiter")
            nodes = []

            for i in range(len(lines)):
                if lines[i] == "":
                    continue
                elif i % 2 == 0:
                    nodes.append(TextNode(lines[i], TextType.TEXT))
                else:
                    nodes.append(TextNode(lines[i], text_type))
            # line1 = TextNode(lines[0], TextType.TEXT)
            # line2 = TextNode(lines[1], text_type)
            # line3 = TextNode(lines[2], TextType.TEXT)
            new_nodes.extend(nodes)
    
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        images = extract_markdown_images(old_node.text)
        remaining_text = old_node.text
        # print(f"remaining text {remaining_text}")
        if len(images) == 0:
            new_nodes.append(old_node)
            continue

        for image in images:
            sections = remaining_text.split(f"![{image[0]}]({image[1]})")
            if len(sections) !=2:
                # print(sections)
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            remaining_text = sections[1]
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
        # else:
        #     counter = 0
        #     for image_alt, image_link in images:
        #         counter += 1
        #         splits = remaining_text.split(f"![{image_alt}]({image_link})", 1)

        #         if splits[0] == "" and counter == len(images):
        #             nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
        #             nodes.append(TextNode(splits[1], TextType.TEXT))
        #         elif splits[0] == "":
        #             nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
        #             remaining_text = splits[1]
        #         else:
        #             nodes.append(TextNode(splits[0], TextType.TEXT))
        #             nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
        #             remaining_text = splits[1]

        #             if remaining_text and counter == len(images):
        #                 nodes.append(TextNode(remaining_text, TextType.TEXT))
        #     new_nodes.extend(nodes)
    return new_nodes



def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        links = extract_markdown_links(old_node.text)
        remaining_text = old_node.text
        # print(f"remaining text {remaining_text}")
        if len(links) == 0:
            new_nodes.append(old_node)
            continue

        for link in links:
            sections = remaining_text.split(f"[{link[0]}]({link[1]})")
            if len(sections) !=2:
                # print(sections)
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            remaining_text = sections[1]
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    new_nodes = [TextNode(text, TextType.TEXT)]

    new_nodes = split_nodes_delimiter(new_nodes, '**', TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, '_', TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, '`', TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)

    return new_nodes


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