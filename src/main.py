from textnode import TextNode, TextType


def main():
    gh_link = TextNode("GitHub", TextType.LINK, "https://github.com/javavick")
    print(gh_link)


main()
