import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    # --- __init__() ---
    def test_initialization_with_all_data(self):
        """
        Test that a LeafNode is initialized correctly when all data
        is passed in.
        """
        node = LeafNode("p", "Test", {"class": "text-base"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Test")
        self.assertEqual(node.props, {"class": "text-base"})
        self.assertIsNone(node.children)

    def test_initialization_without_props(self):
        """
        Test that a LeafNode is initialized correctly when no `props`
        are passed in.
        """
        node = LeafNode("div", "Test")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Test")
        self.assertIsNone(node.props)

    def test_initialization_without_value(self):
        """
        Test that a TypeError is raised when a LeafNode is
        initialized without a `value`.
        """
        with self.assertRaises(TypeError):
            LeafNode("p")
    
    def test_initialization_without_data(self):
        """
        Test that a TypeError is raised when a LeafNode is
        initialized without any data.
        """
        with self.assertRaises(TypeError):
            LeafNode()

    # --- __repr__() ---
    def test_representation(self):
        """Test that `__repr__()` returns the correct string representation."""
        node = LeafNode("p", "Test", {"class": "text-base"})
        expected = "LeafNode(p, Test, {'class': 'text-base'})"
        self.assertEqual(str(node), expected)
    
    # --- to_html() ---
    def test_to_html_with_all_data(self):
        """
        Test that to_html() returns the correct HTML string when
        all data is passed in.
        """
        props = {
            "href": "example.html",
            "target": "_blank"
        }
        node = LeafNode("a", "Test", props)
        expected = '<a href="example.html" target="_blank">Test</a>'
        self.assertEqual(node.to_html(), expected)
    
    def test_to_html_without_props(self):
        """
        Test that `to_html()` returns the correct HTML string when
        a node has no properties.
        """
        node = LeafNode("h1", "Test")
        expected = "<h1>Test</h1>"
        self.assertEqual(node.to_html(), expected)

    def test_to_html_without_tag(self):
        """
        Test that `to_html()` returns the `value` in raw text when
        a node has no `tag`.
        """
        node = LeafNode(None, "Test")
        self.assertEqual(node.to_html(), "Test")

    def test_to_html_without_value(self):
        """
        Test that `to_html()` raises a ValueError with 'Value cannot be None.'
        as its message when `value` is set to None.
        """
        with self.assertRaises(ValueError) as context:
            LeafNode("h2", None).to_html()
        self.assertEqual(str(context.exception), "Value cannot be None.")
