import re

from enum import Enum


class BlockType(Enum):
    HEADER = "header"
    PARAGRAPH = "paragraph"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    stripped_markdown = markdown.strip('\n')
    blocks = stripped_markdown.split('\n\n')
    filtered_blocks = filter(
        lambda block: not re.fullmatch(r'^\s*$', block),
        blocks
    )
    return list(filtered_blocks)


def block_to_block_type(block):
    if not block:
        raise ValueError("Block cannot be empty.")
    
    if re.match(r"^(#{1,6})\s(.+)$", block):
        return BlockType.HEADER
    
    if block[:3] == "```" and block[-3:] == "```":
        return BlockType.CODE
    
    if block.startswith(">"):
        if "\n" in block:
            for line in block.split("\n"):
                if ">" not in line:
                    return BlockType.PARAGRAPH
        return BlockType.QUOTE
    
    if block.startswith("- "):
        if "\n" in block:
            for line in block.split("\n"):
                if not line.startswith("- "):
                    return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    
    if block.startswith("1. "):
        if "\n" in block:
            item_number = 1
            for line in block.split("\n"):
                if not line.startswith(f"{item_number}. "):
                    return BlockType.PARAGRAPH
                item_number += 1
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH
