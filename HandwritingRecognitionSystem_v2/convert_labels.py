
with open('samples/Labels/000033/READ17.000033_01_01_pg_line_1486644351571_780.tru') as f:
    contents = f.read()

with open('samples/CHAR_LIST') as f:
    chars = f.read()

contents = contents.split(' ')
chars = chars.split('\n')


def label_to_text(contents):
    text = ''
    for index in contents:
        if index:
            text += chars[int(index)]
    text = text.replace('<SPACE>', ' ')
    return text

def text_to_label(text):
    label = ''
    for letter in text:
        if letter == ' ':
            letter = '<SPACE>'
        for ind, char in enumerate(chars):
            if letter == char:
                label += str(ind) + ' '
    return label

text = label_to_text(contents)
print(text)
print(text_to_label(text))