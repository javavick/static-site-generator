import unittest

from leafnode import LeafNode
from textnode import (
    TextNode,
    TextType,
    text_node_to_html_node
)
 

class TestTextNode(unittest.TestCase):
    # --- __init__() ---
    def test_initialization_without_url(self):
        """Test that a TextNode is initialized correctly without a URL."""
        node = TextNode("Test", TextType.TEXT)
        self.assertEqual(node.text, "Test")
        self.assertEqual(node.text_type, TextType.TEXT)
    
    def test_initialization_with_url(self):
        """Test that a TextNode is initialized correctly with a URL."""
        node = TextNode("Test", TextType.LINK, "https://example.com")
        self.assertEqual(node.text, "Test")
        self.assertEqual(node.text_type, TextType.LINK)
        self.assertEqual(node.url, "https://example.com")

    # --- __eq__() ---
    def test_equality_true(self):
        """Test that __eq__() returns True for equal TextNodes."""
        node1 = TextNode("URL", TextType.LINK, "https://example.com")
        node2 = TextNode("URL", TextType.LINK, "https://example.com")
        self.assertEqual(node1, node2)
    
    def test_equality_true_with_self(self):
        """
        Test that __eq__() returns True when a TextNode is compared with itself.
        """
        node1 = TextNode("URL", TextType.LINK, "https://example.com")
        self.assertEqual(node1, node1)

    def test_equality_false_text(self):
        """Test that __eq__() returns False for different text."""
        node1 = TextNode("Test", TextType.TEXT)
        node2 = TextNode("Node", TextType.TEXT)
        self.assertNotEqual(node1, node2)

    def test_equality_false_text_type(self):
        """Test that __eq__() returns False for different text types."""
        node1 = TextNode("Test", TextType.TEXT)
        node2 = TextNode("Test", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_equality_false_url(self):
        """Test that __eq__() returns False for different URLs."""
        node1 = TextNode("URL", TextType.LINK, "https://example.com")
        node2 = TextNode("URL", TextType.LINK, "https://example.org")
        self.assertNotEqual(node1, node2)

    def test_equality_error_non_textnode(self):
        """
        Test that __eq__() raises an AttributeError when compared with a
        non-TextNode due to missing attributes.
        """
        node = TextNode("Test", TextType.TEXT)
        with self.assertRaises(AttributeError):
            node == "Test"
    
    # --- __repr__() ---
    def test_representation_without_url(self):
        """
        Test that __repr__() returns the correct string representation
        without a URL.
        """
        node = TextNode("Test", TextType.TEXT)
        expected = "TextNode(Test, text, None)"
        self.assertEqual(str(node), expected)
    
    def test_representation_with_url(self):
        """
        Test that __repr__() returns the correct string representation
        with a URL.
        """
        node = TextNode("Test", TextType.LINK, "https://example.com")
        expected = "TextNode(Test, link, https://example.com)"
        self.assertEqual(str(node), expected)


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        """
        Test that a TextNode of type TEXT is converted to a LeafNode with
        a `value` and no `tag`.
        """
        text_node = TextNode("Test", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)

        self.assertTrue(isinstance(html_node, LeafNode))
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "Test")

    def test_bold(self):
        """
        Test that a TextNode of type BOLD is converted to a LeafNode with
        a `value` and a `tag` set to 'b'
        """
        text_node = TextNode("Test", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)

        self.assertTrue(isinstance(html_node, LeafNode))
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Test")

    def test_italic(self):
        """
        Test that a TextNode of type ITALIC is converted to a LeafNode with
        a `value` and a `tag` set to 'i'
        """
        text_node = TextNode("Test", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)

        self.assertTrue(isinstance(html_node, LeafNode))
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Test")

    def test_code(self):
        """
        Test that a TextNode of type CODE is converted to a LeafNode with
        a `value` and a `tag` set to 'code'
        """
        text_node = TextNode("Test", TextType.CODE)
        html_node = text_node_to_html_node(text_node)

        self.assertTrue(isinstance(html_node, LeafNode))
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Test")

    def test_link(self):
        """
        Test that a TextNode of type LINK is converted to a LeafNode with
        a `value`, a `tag` set to 'a', and `props` with an href attribute.
        """
        text_node = TextNode("Test", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(text_node)

        self.assertTrue(isinstance(html_node, LeafNode))
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Test")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image(self):
        """
        Test that a TextNode of type IMAGE is converted to a LeafNode with
        a `value`, a `tag` set to 'img', and `props` with src and
        alt attributes.
        """
        text_node = TextNode("Test", TextType.IMAGE, "https://example.com")
        html_node = text_node_to_html_node(text_node)

        self.assertTrue(isinstance(html_node, LeafNode))
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {
            "src": "https://example.com",
            "alt": "Test"
        })

    def test_invalid_type(self):
        """
        Test that an Exception is raised when the passed-in TextNode has
        an invalid type.
        """
        text_node = TextNode("Test", "word")
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(text_node)
        self.assertEqual(str(context.exception), "Invalid TextType.")

    def test_no_type(self):
        """
        Test that an Exception is raised when the passed-in TextNode's type
        is None.
        """
        text_node = TextNode("Test", None)
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(text_node)
        self.assertEqual(str(context.exception), "Invalid TextType.")


if __name__ == "__main__":
    unittest.main()
