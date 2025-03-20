import unittest

from leafnode import LeafNode
from textnode import (
    TextNode,
    TextType,
    text_node_to_html_node,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    extract_markdown_images,
    extract_markdown_links
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


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_bold(self):
        """Test that a TextNode with a bolded word is split correctly."""
        node = TextNode("Test with a **bolded** word.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("Test with a ", TextType.TEXT),
            TextNode("bolded", TextType.BOLD),
            TextNode(" word.", TextType.TEXT),
        ]

        self.assertListEqual(new_nodes, expected)

    def test_bold_two_words(self):
        """Test that a TextNode with two bolded words is split correctly."""
        node = TextNode(
            "Test with **two** separately **bolded** words.", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("Test with ", TextType.TEXT),
            TextNode("two", TextType.BOLD),
            TextNode(" separately ", TextType.TEXT),
            TextNode("bolded", TextType.BOLD),
            TextNode(" words.", TextType.TEXT),
        ]

        self.assertListEqual(new_nodes, expected)

    def test_bold_multiword_string(self):
        """
        Test that a TextNode with a multi-word bolded string is
        split correctly.
        """
        node = TextNode(
            "Test with two **bolded words** in it.", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("Test with two ", TextType.TEXT),
            TextNode("bolded words", TextType.BOLD),
            TextNode(" in it.", TextType.TEXT),
        ]

        self.assertListEqual(new_nodes, expected)

    def test_bold_word_at_the_end(self):
        """
        Test that a TextNode with a bolded word at the end is
        split correctly.
        """
        node = TextNode(
            "Test with a bolded **word**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("Test with a bolded ", TextType.TEXT),
            TextNode("word", TextType.BOLD),
        ]

        self.assertListEqual(new_nodes, expected)

    def test_italic(self):
        """Test that a TextNode with an italicized word is split correctly."""
        node = TextNode("Test with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("Test with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertListEqual(new_nodes, expected)

    def test_bold_and_italic(self):
        """
        Test that a TextNode with bolded and italicized words is
        split correctly.
        """
        node = TextNode("Test with a **bold** and _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        expected = [
            TextNode("Test with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertListEqual(new_nodes, expected)

    def test_code(self):
        """Test that a TextNode with a code block word is split correctly."""
        node = TextNode("Test with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Test with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertListEqual(new_nodes, expected)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extraction_single_image(self):
        """
        Test that a single image's URL and alt text are extracted correctly.
        """
        matches = extract_markdown_images(
            "Here's an ![image](https://example.org/test.png)."
        )
        expected = [("image", "https://example.org/test.png")]
        self.assertListEqual(matches, expected)
    
    def test_extraction_multiple_images(self):
        """
        Test that multiple images' URLs and alt text are extracted correctly.
        """
        markdown = (
            "Here's an ![image](https://example.org/test.png). "
            "Here's ![another](https://example.org/test.jpg)."
        )
        matches = extract_markdown_images(markdown)
        expected = [
            ("image", "https://example.org/test.png"),
            ("another", "https://example.org/test.jpg")
        ]

        self.assertListEqual(matches, expected)
    
    def test_extraction_multiple_nodes(self):
        """
        Test that multiple images' URLs and alt text are extracted correctly
        from multiple TextNodes.
        """
        node1 = TextNode(
            "Here's an ![image](https://example.org/test.png).", TextType.TEXT
        )
        node2 = TextNode(
            "Here's ![another](https://example.org/test.jpg).", TextType.TEXT
        )
        matches = extract_markdown_images(node1.text + node2.text)
        expected = [
            ("image", "https://example.org/test.png"),
            ("another", "https://example.org/test.jpg")
        ]

        self.assertListEqual(matches, expected)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extraction_single_link(self):
        """Test that a single link's URL and text are extracted correctly."""
        markdown = "Here's a [link](https://example.org)."
        matches = extract_markdown_links(markdown)
        expected = [("link", "https://example.org")]
        self.assertListEqual(matches, expected)
    
    def test_extraction_multiple_links(self):
        """Test that multiple links' URLs and text are extracted correctly."""
        markdown = (
            "Here's a [link](https://example.org). "
            "Here's [another](https://example.com)"
        )
        matches = extract_markdown_links(markdown)
        expected = [
            ("link", "https://example.org"),
            ("another", "https://example.com")
        ]
        
        self.assertListEqual(matches, expected)
    
    def test_extraction_multiple_nodes(self):
        """
        Test that multiple links' URLs and text are extracted correctly
        from multiple TextNodes.
        """
        node1 = TextNode("Here's a [link](https://example.org).", TextType.TEXT)
        node2 = TextNode("Here's [another](https://example.com)", TextType.TEXT)
        matches = extract_markdown_links(node1.text + node2.text)
        expected = [
            ("link", "https://example.org"),
            ("another", "https://example.com")
        ]

        self.assertListEqual(matches, expected)


class TestSplitNodesImage(unittest.TestCase):
    def test_with_text(self):
        """
        Test that a TextNode with text and an image is split
        into multiple TextNodes correctly
        """
        node = TextNode(
        "Text with an ![image](https://example.org/example.png)",
        TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Text with an ", TextType.TEXT),
            TextNode(
                "image",
                TextType.IMAGE,
                "https://example.org/example.png"
            )
        ]

        self.assertListEqual(new_nodes, expected)
    
    def test_without_text(self):
        """
        Test that a TextNode with only an image is split into
        a single TextNode correctly.
        """
        node = TextNode(
            "![image](https://example.org/example.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode(
            "image",
            TextType.IMAGE,
            "https://example.org/example.png"
            )
        ]

        self.assertListEqual(new_nodes, expected)
    
    def test_multiple_images(self):
        """
        Test that a TextNode with multiple images is split into
        multiple TextNodes correctly.
        """
        node = TextNode(
            "Text with not one "
            "![image](https://example.org/example1.png), but two "
            "![images](https://example.org/example2.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Text with not one ", TextType.TEXT),
            TextNode(
                "image",
                TextType.IMAGE,
                "https://example.org/example1.png"
            ),
            TextNode(", but two ", TextType.TEXT),
            TextNode(
                "images",
                TextType.IMAGE,
                "https://example.org/example2.png"
            )
        ]

        self.assertListEqual(new_nodes, expected)
    
    def test_multiple_nodes(self):
        """
        Test that multiple TextNodes with images are split into
        multiple TextNodes correctly.
        """
        node1 = TextNode(
            "Text with an ![image](https://example.org/example1.png)",
            TextType.TEXT
        )
        node2 = TextNode(
            " and another ![image](https://example.org/example2.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node1, node2])
        expected = [
            TextNode("Text with an ", TextType.TEXT),
            TextNode(
                "image",
                TextType.IMAGE,
                "https://example.org/example1.png"
            ),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "image",
                TextType.IMAGE,
                "https://example.org/example2.png"
            )
        ]

        self.assertListEqual(new_nodes, expected)
    
    def test_not_text_type_text(self):
        """
        Test that a TextNode with a non-TEXT `text_type` is not split.
        """
        node = TextNode(
            "Text with an ![image](https://example.org/example.png)",
            TextType.BOLD
        )
        new_nodes = split_nodes_image([node])
        expected = [node]

        self.assertListEqual(new_nodes, expected)
    
    def test_no_image(self):
        """
        Test that a TextNode with no image is not split.
        """
        node = TextNode("Text with no image", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [node]

        self.assertListEqual(new_nodes, expected)


class TestSplitNodesLink(unittest.TestCase):
    def test_with_text(self):
        """
        Test that a TextNode with text and a link is split
        into multiple TextNodes correctly.
        """
        node = TextNode(
            "Text with a [link](https://example.org/example)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Text with a ", TextType.TEXT),
            TextNode(
                "link",
                TextType.LINK,
                "https://example.org/example"
            )
        ]

        self.assertListEqual(new_nodes, expected)
    
    def test_without_text(self):
        """
        Test that a TextNode with only a link is split into
        a single TextNode correctly.
        """
        node = TextNode(
            "[link](https://example.org/example)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode(
                "link",
                TextType.LINK,
                "https://example.org/example"
            )
        ]

        self.assertListEqual(new_nodes, expected)
    
    def test_multiple_links(self):
        """
        Test that a TextNode with multiple links is split into
        multiple TextNodes correctly.
        """
        node = TextNode(
            "Text with not one "
            "[link](https://example.org/example1), but two "
            "[links](https://example.org/example2)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Text with not one ", TextType.TEXT),
            TextNode(
                "link",
                TextType.LINK,
                "https://example.org/example1"
            ),
            TextNode(", but two ", TextType.TEXT),
            TextNode(
                "links",
                TextType.LINK,
                "https://example.org/example2"
            )
        ]

        self.assertListEqual(new_nodes, expected)
    
    def test_multiple_nodes(self):
        """
        Test that multiple TextNodes with links are split into
        multiple TextNodes correctly.
        """
        node1 = TextNode(
            "Text with a [link](https://example.org/example1)",
            TextType.TEXT
        )
        node2 = TextNode(
            " and another [link](https://example.org/example2)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node1, node2])
        expected = [
            TextNode("Text with a ", TextType.TEXT),
            TextNode(
                "link",
                TextType.LINK,
                "https://example.org/example1"
            ),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "link",
                TextType.LINK,
                "https://example.org/example2"
            )
        ]

        self.assertListEqual(new_nodes, expected)


if __name__ == "__main__":
    unittest.main()
