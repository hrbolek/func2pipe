import func2pipe as fp

def example02():
    @fp.pipeit()
    def addone(item):
        return item + 1

    @fp.pipesub(lambda input, output: {'i': input, **output})
    @fp.pipeit()
    def transform2(item, fixed):
        if (item > 12):
            return {'r': True, 'f': fixed }
        else:
            return {'r': False, 'f': fixed }

    resultcreator = fp.createpipe([
        addone(),
        transform2(fixed = 'fixed')
        ], closewitharray = True)

    sourceA = list(range(1, 20))
    sourceB = [45, 20, 6]
    print('-- Example 02 --')
    print('first set', sourceA)
    result = resultcreator(sourceA)
    print('result', result)
    print('second set', sourceB)
    result = resultcreator(sourceB)
    print('result', result)

if __name__ == '__main__':
    example02()
