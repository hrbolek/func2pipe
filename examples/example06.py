import func2pipe as fp

def example06():
    @fp.pipesub(lambda input, output: {'source': input, 'letters': output })
    @fp.pipecollecttoarray
    @fp.pipefind(r"[A-Z]", mapper = lambda item: item.group(0))
    @fp.pipeit()
    def letters(item, b):
        return item + b

    resultcreator = fp.createpipe([
        letters(b = '_Z')
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
    example06()
