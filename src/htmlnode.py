class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        
        prop_to_string = lambda prop: f'{prop[0]}="{prop[1]}"'
        prop_strings = list(map(prop_to_string, self.props.items()))
        return " ".join(prop_strings)
