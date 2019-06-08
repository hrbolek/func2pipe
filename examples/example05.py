import func2pipe as fp

def example05():
    @fp.pipesub(lambda input, output: {'source': input, 'letter': output })
    @fp.pipefind(r"[A-Z]", mapper = lambda item: item.group(0))
    @fp.pipeit()
    def letters(item, append):
        return item + append

    resultcreator = fp.createpipe([
        letters(append = '_Z')
        ], closewitharray = True)


    sourceA = ['ABCDEF', 'GHIJKL']
    sourceB = ['MNOPQR', 'STUVWX']

    print('-- Example 05 --')
    print('first set', sourceA)
    result = resultcreator(sourceA)
    print('result', result)
    print('second set', sourceB)
    result = resultcreator(sourceB)
    print('result', result)

if __name__ == '__main__':
    example05()
