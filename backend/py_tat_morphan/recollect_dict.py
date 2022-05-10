# -*- coding: UTF-8 -*-
#!/usr/bin/python

from py_tat_morphan.morphan import Morphan

def main():
    """
        After every rule correction need to recollect dictionary
    """
    morphan = Morphan()
    with open('files/words.csv', 'r') as stream:
        text = stream.read()
    lines = text.split('\n')
    result = ''
    error = ''
    for line in lines:
        word = line.split('\t')
        if len(word) == 2:
            parse = morphan.analyse(word[0])
            if parse:
                result += '%s\t%s\n' % (word[0], parse.encode('utf-8'))
            else:
                error += '%s\n' % word[0]
                result += '%s\t%s\n' % (word[0], word[1])

    with open('files/words.csv', 'w') as stream:
        stream.write(result)
    with open('files/error.csv', 'w') as stream:
        stream.write(error)

if __name__ == '__main__':
    main()
