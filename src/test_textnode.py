import unittest

from textnode import TextNode, TextType
 

class TestTextNode(unittest.TestCase):
    # -*- __init__ -*-
    def test_initialization_without_url(self):
        """Test that a TextNode is initialized correctly without a URL."""
        node = TextNode("Test", TextType.NORMAL)
        self.assertEqual(node.text, "Test")
        self.assertEqual(node.text_type, TextType.NORMAL)
    
    def test_initialization_with_url(self):
        """Test that a TextNode is initialized correctly with a URL."""
        node = TextNode("Test", TextType.LINK, "https://example.com")
        self.assertEqual(node.text, "Test")
        self.assertEqual(node.text_type, TextType.LINK)
        self.assertEqual(node.url, "https://example.com")

    # -*- __eq__ -*-
    def test_equality_true(self):
        """Test that __eq__ returns True for equal TextNodes."""
        node1 = TextNode("URL", TextType.LINK, "https://example.com")
        node2 = TextNode("URL", TextType.LINK, "https://example.com")
        self.assertEqual(node1, node2)
    
    def test_equality_true_with_self(self):
        """
        Test that __eq__ returns True when a TextNode is compared with itself.
        """
        node1 = TextNode("URL", TextType.LINK, "https://example.com")
        self.assertEqual(node1, node1)

    def test_equality_false_text(self):
        """Test that __eq__ returns False for different text."""
        node1 = TextNode("Test", TextType.NORMAL)
        node2 = TextNode("Node", TextType.NORMAL)
        self.assertNotEqual(node1, node2)

    def test_equality_false_text_type(self):
        """Test that __eq__ returns False for different text types."""
        node1 = TextNode("Test", TextType.NORMAL)
        node2 = TextNode("Test", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_equality_false_url(self):
        """Test that __eq__ returns False for different URLs."""
        node1 = TextNode("URL", TextType.LINK, "https://example.com")
        node2 = TextNode("URL", TextType.LINK, "https://example.org")
        self.assertNotEqual(node1, node2)

    def test_equality_error_non_textnode(self):
        """
        Test that __eq__ raises an AttributeError when compared with a
        non-TextNode due to missing attributes.
        """
        node = TextNode("Test", TextType.NORMAL)
        with self.assertRaises(AttributeError):
            node == "Test"
    
    # -*- __repr__ -*-
    def test_repr_without_url(self):
        """
        Test that __repr__ returns the correct string representation
        without a URL.
        """
        node = TextNode("Test", TextType.NORMAL)
        expected = "TextNode(Test, normal, None)"
        self.assertEqual(str(node), expected)
    
    def test_repr_with_url(self):
        """
        Test that __repr__ returns the correct string representation
        with a URL.
        """
        node = TextNode("Test", TextType.LINK, "https://example.com")
        expected = "TextNode(Test, link, https://example.com)"
        self.assertEqual(str(node), expected)

if __name__ == "__main__":
    unittest.main()
