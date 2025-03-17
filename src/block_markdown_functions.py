def main():
    md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
    
    print(markdown_to_blocks(md))

def markdown_to_blocks(text):
    result = []
    sections = list(map(lambda x: x.strip(), text.split("\n\n")))
    
    for section in sections:
        if section:
            text = "\n".join([x.strip() for x in section.split("\n")])
            result.append(text)
            
    return result

if __name__ == "__main__":
    main()