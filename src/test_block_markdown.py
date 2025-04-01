import unittest

from block_markdown import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks
)


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


class TestBlockToBlockType(unittest.TestCase):
    def test_empty_block(self):
        """Test that an empty block raises a ValueError."""
        with self.assertRaises(ValueError):
            block_to_block_type("")
    
    def test_heading_1_block(self):
        """Test that a heading 1 block is correctly identified."""
        block = "# This is a heading"
        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.HEADER)
    
    def test_heading_2_block(self):
        """Test that a heading 2 block is correctly identified."""
        block = "## This is a heading"
        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.HEADER)
    
    def test_heading_3_block(self):
        """Test that a heading 3 block is correctly identified."""
        block = "### This is a heading"
        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.HEADER)
    
    def test_heading_4_block(self):
        """Test that a heading 4 block is correctly identified."""
        block = "#### This is a heading"
        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.HEADER)
    
    def test_heading_5_block(self):
        """Test that a heading 5 block is correctly identified."""
        block = "##### This is a heading"
        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.HEADER)
    
    def test_heading_6_block(self):
        """Test that a heading 6 block is correctly identified."""
        block = "###### This is a heading"
        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.HEADER)
    
    def test_heading_7_block(self):
        """Test that a heading 7 block is identified as a regular paragraph."""
        block = "####### This is not a heading"
        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.PARAGRAPH)
    
    def test_heading_block_without_space(self):
        """
        Test that a heading without a space is identified as
        a regular paragraph.
        """
        block = "#This is not a heading"
        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.PARAGRAPH)
    
    def test_heading_block_without_word(self):
        """
        Test that a heading without a word is identified as
        a regular paragraph.
        """
        block = "# "
        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.PARAGRAPH)
    
    def test_code_block(self):
        """Test that a quote block is correctly identified."""
        block = "```\nThis is a code block\n```"
        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.CODE)
    
    def test_quote_block(self):
        """Test that a quote block is correctly identified."""
        block = "> This is a quote"
        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.QUOTE)
    
    def test_quote_block_with_multiple_quotes(self):
        """
        Test that a quote block with multiple quotes is correctly identified.
        """
        block = "> This is a quote\n> with multiple lines"
        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.QUOTE)
    
    def test_unordered_list_block_single_item(self):
        """
        Test that an unordered list block with a single item is
        correctly identified.
        """
        block = "- This is an unordered list"
        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.UNORDERED_LIST)
    
    def test_unordered_list_block_multiple_items(self):
        """
        Test that an unordered list block with multiple items is
        correctly identified.
        """
        block = "- This is an unordered list\n- with multiple items"
        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.UNORDERED_LIST)
    
    def test_unordered_list_invalid_block(self):
        """
        Test that an unordered list block with invalid items is
        identified as a regular paragraph.
        """
        block = "- This is an unordered list\nThis is not a list item"
        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.PARAGRAPH)
    
    def test_ordered_list_block_single_item(self):
        """
        Test that an ordered list block with a single item is
        correctly identified.
        """
        block = "1. This is an ordered list"
        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.ORDERED_LIST)
    
    def test_ordered_list_block_multiple_items(self):
        """
        Test that an ordered list block with multiple items is
        correctly identified.
        """
        block = "1. This is an ordered list\n2. with multiple\n3. items"
        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.ORDERED_LIST)
    
    def test_ordered_list_invalid_block(self):
        """
        Test that an ordered list block with invalid items is
        identified as a regular paragraph.
        """
        block = "1. This is an ordered list\nThis is not a list item"
        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.PARAGRAPH)
    
    def test_paragraph_block(self):
        """Test that a paragraph block is correctly identified."""
        block = "This is a paragraph"
        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.PARAGRAPH)
