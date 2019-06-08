import func2pipe as fp

def example03():
    @fp.pipeit(with_yield = True)
    def letters(item, spec):
        for letter in item:
            yield letter + spec

    resultcreator = fp.createpipe([
        letters(spec = '-')
        ], closewitharray = True)


    sourceA = ['ABCDEF', 'GHIJKL']
    sourceB = ['MNOPQR', 'STUVWX']

    print('-- Example 03 --')
    print('first set', sourceA)
    result = resultcreator(sourceA)
    print('result', result)
    print('second set', sourceB)
    result = resultcreator(sourceB)
    print('result', result)

if __name__ == '__main__':
    example03()
