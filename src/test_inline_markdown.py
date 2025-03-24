import unittest

from textnode import TextNode, TextType
from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    split_nodes_delimiter,
    text_to_textnodes
)


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


class TestTextToTextnodes(unittest.TestCase):
    def test_raw_text(self):
        """
        Test that a raw text string is converted to a single TextNode.
        """
        text = "This is a test."
        nodes = text_to_textnodes(text)
        expected = [TextNode(text, TextType.TEXT)]

        self.assertListEqual(nodes, expected)
    
    def test_bold_text(self):
        """
        Test that a bolded text string is converted to multiple TextNodes.
        """
        text = "This is a **test**."
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("test", TextType.BOLD),
            TextNode(".", TextType.TEXT)
        ]

        self.assertListEqual(nodes, expected)
    
    def test_italic_text(self):
        """
        Test that an italicized text string is converted to multiple TextNodes.
        """
        text = "This is a _test_."
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("test", TextType.ITALIC),
            TextNode(".", TextType.TEXT)
        ]

        self.assertListEqual(nodes, expected)
    
    def test_code_text(self):
        """
        Test that a code block text string is converted to multiple TextNodes.
        """
        text = "This is a `test`."
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("test", TextType.CODE),
            TextNode(".", TextType.TEXT)
        ]

        self.assertListEqual(nodes, expected)
    
    def test_link_text(self):
        """
        Test that a linked text string is converted to multiple TextNodes.
        """
        text = "This is a [link](https://example.com)."
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(".", TextType.TEXT)
        ]

        self.assertListEqual(nodes, expected)
    
    def test_image_text(self):
        """
        Test that an image text string is converted to multiple TextNodes.
        """
        text = "This is an ![image](https://example.com/test.png)."
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/test.png"),
            TextNode(".", TextType.TEXT)
        ]

        self.assertListEqual(nodes, expected)
    
    def test_multiple_text_types(self):
        """
        Test that a text string with multiple text types is converted to
        multiple TextNodes.
        """
        text = (
            "This is a **bolded** _italicized_ `code block` "
            "[link](https://example.com) ![image](https://example.com/test.png)"
        )
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("bolded", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("italicized", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/test.png")
        ]

        self.assertListEqual(nodes, expected)
