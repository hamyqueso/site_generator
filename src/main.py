from textnode import TextNode, TextType

from htmlnode import HTMLNode, ParentNode, LeafNode

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