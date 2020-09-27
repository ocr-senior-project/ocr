import argparse

with open('samples/CHAR_LIST') as f:
    chars = f.read()

chars = chars.split('\n')

def label_to_text(relativepath):
    """ Converts a list of indices of chars in CHAR_LIST to a readable string """
    with open(relativepath) as f:
        contents = f.read()

    contents = contents.split(' ')
    text = ''
    for index in contents:
        if index:
            text += chars[int(index)]
    text = text.replace('<SPACE>', ' ')
    return text

def text_to_label(relativepath):
    """ Converts a text string into a string of indices of the chars in CHAR_LIST """
    with open(relativepath) as f:
        text = f.read()
    print(text)
    label = ''
    for letter in text:
        if letter == ' ':
            letter = '<SPACE>'
        for ind, char in enumerate(chars):
            if letter == char:
                label += str(ind) + ' '
    return label


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert text file to label string or vice versa.')
    parser.add_argument('relativepath', type=str,
                        help='the relative path to the file.')
    parser.add_argument('textorlabel', type=str,
                        help='"text" if the input is a .txt file, any other input will assume a label file.')
    args = parser.parse_args()
    if args.textorlabel == 'text':
        result = text_to_label(args.relativepath)
    else:
        result = label_to_text(args.relativepath)
    print(result)
