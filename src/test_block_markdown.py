import unittest

from block_markdown import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_normal_markdown(self):
        """Test that markdown is split into blocks properly."""
        markdown = """
# This is a heading

This is a **paragraph** of _text_.

- This is a list
- with items
"""
        blocks = markdown_to_blocks(markdown)
        expected = [
            "# This is a heading",
            "This is a **paragraph** of _text_.",
            "- This is a list\n- with items"
        ]

        self.assertEqual(blocks, expected)
    
    def test_extra_newlines(self):
        """
        Test that markdown with extra newlines is split into blocks properly.
        """
        markdown = """
# This is a heading

 

This is a paragraph.

- This is a list
- with items
"""
        blocks = markdown_to_blocks(markdown)
        expected = [
            "# This is a heading",
            "This is a paragraph.",
            "- This is a list\n- with items"
        ]
        
        self.assertEqual(blocks, expected)

    def test_no_newlines(self):
        """Test that markdown with no newlines is split into blocks properly."""
        markdown = "# This is a heading"
        blocks = markdown_to_blocks(markdown)
        expected = ["# This is a heading"]

        self.assertEqual(blocks, expected)
