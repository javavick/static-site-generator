import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    # --- __init__ ---
    def test_initialization_with_data(self):
        """Test that an HTMLNode is initialized correctly with data."""
        p = HTMLNode("p", "Test")
        div_props = {"class": "container"}
        div = HTMLNode("div", "Test", p, div_props)
        
        self.assertEqual(div.tag, "div")
        self.assertEqual(div.value, "Test")
        self.assertEqual(div.children, p)
        self.assertEqual(div.props, div_props)

    def test_initialization_without_data(self):
        """Test that an HTMLNode is initialized correctly without data."""
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    # --- __repr__ ---
    def test_representation(self):
        """Test that __repr__ returns the correct string representation."""
        p = HTMLNode("p", "Test")
        div_props = {"class": "container"}
        div = HTMLNode("div", "Test", p, div_props)
        expected = "HTMLNode(div, Test, HTMLNode(p, Test, None, None), {'class': 'container'})"

        self.assertEqual(str(div), expected)

    # --- to_html ---
    def test_to_html(self):
        """Test that to_html raises a NotImplementedError."""
        node = HTMLNode("p", "Test")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    # --- props_to_html ---
    def test_props_to_html_with_props(self):
        """
        Test that props_to_html returns the correct string of
        the node's properties.
        """
        props = {
            "id": "main",
            "class": "container",
        }
        node = HTMLNode("p", "Test", props=props)
        expected = 'id="main" class="container"'

        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_without_props(self):
        """
        Test that props_to_html returns an empty string when
        a node has no properties.
        """
        node = HTMLNode("p", "Test")
        self.assertEqual(node.props_to_html(), "")
