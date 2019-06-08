import func2pipe as fp

def example01():
    @fp.pipeit()
    def addone(item):
        return item + 1

    @fp.pipeit()
    def add(a, b):
        return a + b

    resultcreator = fp.createpipe([
        addone(),
        add(b = 4),
        ], closewitharray = True)


    sourceA = list((range(1, 20)))
    sourceB = [45, 20, 6]
    print('-- Example 01 --')
    print('first set', sourceA)
    result = resultcreator(sourceA)
    print('result', result)
    print('second set', sourceB)
    result = resultcreator(sourceB)
    print('result', result)

if __name__ == '__main__':
    example01()
