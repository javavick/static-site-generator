import re


def markdown_to_blocks(markdown):
    stripped_markdown = markdown.strip('\n')
    blocks = stripped_markdown.split('\n\n')
    filtered_blocks = filter(
        lambda block: not re.fullmatch(r'^\s*$', block),
        blocks
    )
    return list(filtered_blocks)
