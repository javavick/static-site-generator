import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    # --- __init__() ---
    def test_initialization_with_all_data(self):
        """
        Test that a ParentNode is initialized correctly when all data
        is passed in.
        """
        child = LeafNode("p", "Test")
        props = {"class": "container"}
        parent = ParentNode("div", [child], props)

        self.assertEqual(parent.tag, "div")
        self.assertEqual(parent.children, [child])
        self.assertEqual(parent.props, props)

    def test_initialization_without_props(self):
        """
        Test that a ParentNode is initialized correctly when
        no `props` are passed in.
        """
        child = LeafNode("p", "Test")
        parent = ParentNode("div", [child])

        self.assertEqual(parent.tag, "div")
        self.assertEqual(parent.children, [child])
    
    def test_initialization_without_children(self):
        """
        Test that a TypeError is raised when a ParentNode is
        initialized without any `children`.
        """
        with self.assertRaises(TypeError):
            ParentNode("div")
    
    def test_initialization_without_data(self):
        """
        Test that a TypeError is raised when a ParentNode is
        initialized without any data.
        """
        with self.assertRaises(TypeError):
            ParentNode()
    
    # --- __repr()__ ---
    def test_representation(self):
        """Test that `__repr__()` returns the correct string representation."""
        child = LeafNode("span", "Test", {"class": "font-bold"})
        parent = ParentNode("p", [child], {"class": "text-base"})
        expected = (
            "ParentNode(p, [LeafNode(span, Test, {'class': 'font-bold'})], "
            "{'class': 'text-base'})"
        )

        self.assertEqual(str(parent), expected)
    
    # --- to_html() ---
    def test_to_html_without_tag(self):
        """
        Test that `to_html()` raises a ValueError with 'Tag cannot be None.' as
        its message when `tag` is set to None.
        """
        child = LeafNode("b", "Test")
        parent = ParentNode(None, [child])

        with self.assertRaises(ValueError) as context:
            parent.to_html()
        self.assertEqual(str(context.exception), "Tag cannot be None.")
    
    def test_to_html_without_children(self):
        """
        Test that `to_html()` raises a ValueError with 'Children cannot
        be None.' as its message when `children` is set to None.
        """
        child = LeafNode("b", "Test")
        parent = ParentNode("p", None)

        with self.assertRaises(ValueError) as context:
            parent.to_html()
        self.assertEqual(str(context.exception), "Children cannot be None.")
    
    def test_to_html_with_one_child(self):
        """
        Test that `to_html()` returns the the correct HTML string when
        one child is passed in.
        """
        child = LeafNode("b", "Test", {"class": "text-black"})
        parent = ParentNode("p", [child])
        expected = '<p><b class="text-black">Test</b></p>'

        self.assertEqual(parent.to_html(), expected)
    
    def test_to_html_with_multiple_children(self):
        """
        Test that `to_html()` returns the the correct HTML string when
        multiple `children` are passed in.
        """
        child1 = LeafNode("b", "Test")
        child2 = LeafNode("i", "word", {"class": "text-white"})
        child3 = LeafNode("span", "stuff")
        parent = ParentNode(
            "p",
            [child1, child2, child3],
            {"class": 'text-base'}
        )
        expected = (
            '<p class="text-base"><b>Test</b>'
            '<i class="text-white">word</i>'
            "<span>stuff</span></p>"
        )

        self.assertEqual(parent.to_html(), expected)

    def test_to_html_with_grandchildren(self):
        """
        Test that `to_html()` returns the the correct HTML string when
        grandchildren are passed in.
        """
        grandchild1 = LeafNode("b", "Test")
        grandchild2 = LeafNode("i", "word")
        child = ParentNode("p", [grandchild1, grandchild2])
        parent = ParentNode("div", [child])
        expected = "<div><p><b>Test</b><i>word</i></p></div>"

        self.assertEqual(parent.to_html(), expected)
    
    def test_to_html_with_great_grandchildren(self):
        """
        Test that `to_html()` returns the the correct HTML string when
        great grandchildren are passed in.
        """
        great_grandchild1 = LeafNode("i", "word")
        great_grandchild2 = LeafNode("b", "stuff")
        grandchild1 = LeafNode("b", "Test")
        grandchild2 = ParentNode("span", [
            great_grandchild1,
            great_grandchild2
        ])
        child = ParentNode("p", [grandchild1, grandchild2])
        parent = ParentNode("div", [child])
        expected = (
            '<div><p><b>Test</b><span><i>word</i><b>stuff</b></span></p></div>'
        )

        self.assertEqual(parent.to_html(), expected)
