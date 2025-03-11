from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag cannot be None.")
        if self.children is None:
            raise ValueError("Children cannot be None.")
        
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
