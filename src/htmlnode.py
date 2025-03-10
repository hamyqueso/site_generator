

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag  # A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
        self.value = value # A string representing the value of the HTML tag (e.g. the text inside a paragraph)
        self.children = children # A list of HTMLNode objects representing the children of this node
        self.props = props # A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if self.props == None:
            return ""
        return " "+" ".join(list(map(lambda kv: f'{kv[0]}="{kv[1]}"', self.props.items())))
        
    def __repr__(self):
        return f"HTMLNode(tag= {self.tag}, value= {self.value}, children= {self.children}, props= {self.props_to_html()})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):

        if self.value == None:
            raise ValueError("invalid HTML: no value")
        elif self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        # elif self.tag == "a":
        #     return f'<{self.tag} href="{self.props.get("href")}">{self.value}</{self.tag}>'
        # elif self.tag[0] in ["h", "p"]:
        #     return f"<{self.tag}>{self.value}</{self.tag}>"
        # elif self.tag == "b":
        #     return f"<p><{self.value}>{self.value}</{self.tag}>"
        # elif self.tag == "img":
        #     return f'<{self.tag} href="{self.props.get("href")}" alt="{self.props.get("alt")}">'

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("value error, tag must be included")
        
        if not self.children:
            raise ValueError("parent node requires children")
        
        children_string = ""
        for i in range(len(self.children)):
            children_string += self.children[i].to_html()

        return f"<{self.tag}{self.props_to_html()}>{children_string}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"

        
    