import func2pipe as fp

def example04():
    @fp.pipesub(lambda input, output: {'source': input, 'letter': output })
    @fp.pipeit(with_yield = True)
    def letters(item):
        for letter in item:
            yield letter

    resultcreator = fp.createpipe([
        letters()
        ], closewitharray = True)


    sourceA = ['ABCDEF', 'GHIJKL']
    sourceB = ['MNOPQR', 'STUVWX']

    print('-- Example 04 --')
    print('first set', sourceA)
    result = resultcreator(sourceA)
    print('result', result)
    print('second set', sourceB)
    result = resultcreator(sourceB)
    print('result', result)

if __name__ == '__main__':
    example04()
