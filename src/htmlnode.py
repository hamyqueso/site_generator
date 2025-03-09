

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag  # A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
        self.value = value # A string representing the value of the HTML tag (e.g. the text inside a paragraph)
        self.children = children # A list of HTMLNode objects representing the children of this node
        self.props = props # A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        return " ".join(list(map(lambda kv: f'{kv[0]}="{kv[1]}"', self.props.items())))
        
    def __repr__(self):
        return f"HTMLNode(tag= {self.tag}, value= {self.value}, children= {self.children}, props= {self.props_to_html()})"