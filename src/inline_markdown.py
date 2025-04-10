import re

from textnode import TextNode, TextType


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes(old_nodes, type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        
        extracted_items = None
        if type == TextType.IMAGE:
            extracted_items = extract_markdown_images(node.text)
        if type == TextType.LINK:
            extracted_items = extract_markdown_links(node.text)

        if len(extracted_items) == 0:
            if node.text:
                new_nodes.append(node)
            continue

        node_text = node.text
        for item in extracted_items:
            split_text = None
            if type == TextType.IMAGE:
                split_text = node_text.split(f"![{item[0]}]({item[1]})", 1)
            if type == TextType.LINK:
                split_text = node_text.split(f"[{item[0]}]({item[1]})", 1)
            
            if split_text[0] != "":
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            new_nodes.append(TextNode(item[0], type, item[1]))
            node_text = split_text[1]
        
        if node_text != "":
            new_nodes.append(TextNode(node_text, TextType.TEXT))

    return new_nodes


def split_nodes_image(old_nodes):
    return split_nodes(old_nodes, TextType.IMAGE)


def split_nodes_link(old_nodes):
    return split_nodes(old_nodes, TextType.LINK)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            split_text = node.text.split(delimiter)

            if len(split_text) % 2 == 0:
                raise ValueError(
                    "Invalid Markdown: formatted section was not closed."
                )

            converted_nodes = []
            for i in range(len(split_text)):
                if split_text[i]:
                    type = TextType.TEXT if i % 2 == 0 else text_type
                    converted_nodes.append(TextNode(split_text[i], type))

            new_nodes.extend(converted_nodes)
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
