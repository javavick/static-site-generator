from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("Value cannot be None.")
        if self.tag is None:
            return f"{self.value}"

        props = " " + self.props_to_html() if self.props else ""
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"
