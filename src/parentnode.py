from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag cannot be None.")
        if self.children is None:
            raise ValueError("Children cannot be None.")
        
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        
        props = " " + self.props_to_html() if self.props else ""
        return f"<{self.tag}{props}>{children_html}</{self.tag}>"
