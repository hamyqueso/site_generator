from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE= "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"



def main():
    # md = ""
    md = """
        # This is a heading

        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items

        1. This is an ordered list
        2. Second item
        """

    # md = """### This is a heading with a **bolded** word.

    # ```This is a code block with a **bold** word```
    
    # """
    blocks = markdown_to_blocks(md)
    print(blocks)
    for block in blocks:
        print(block_to_block_type(block))

def markdown_to_blocks(text):
    if not text:
        raise ValueError("invalid markdown, no text value")
    result = []
    sections = list(map(lambda x: x.strip(), text.split("\n\n")))
    
    for section in sections:
        if section:
            text = "\n".join([x.strip() for x in section.split("\n")])
            result.append(text)
            
    return result

def block_to_block_type(block):
    if not block:
        raise ValueError("invalid block, either empty string or None value")
    identifier = None
    if block.startswith("```") and block.endswith("```"):
        identifier = "code"
    elif re.match("^(#+)", block):
        identifier = "heading"
    elif block.startswith("> "):
        identifier = "quote"
    elif re.match("([0-9])+.", block):
        identifier = "ordered list"
    elif block.startswith("- "):
        identifier = "unordered list"

    match identifier:
        case "heading":
            return BlockType.HEADING
        case "code":
            return BlockType.CODE
        case "quote":
            return BlockType.QUOTE
        case "unordered list":
            return BlockType.UNORDERED_LIST
        case "ordered list":
            return BlockType.ORDERED_LIST
        case _:
            return BlockType.PARAGRAPH

if __name__ == "__main__":
    main()