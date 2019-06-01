# func2pipe
python utils for generator function creation

### Example 01
```python
import func2pipe as fp

@fp.pipeit
def addone(item):
    return item + 1

@fp.pipeitwithnamedparams
def add(a, b):
    return a + b

resultcreator = fp.createpipe([
    addone,
    add(b = 4),
    ], closewitharray = True)


sourceA = iter(range(1, 20))
sourceB = [45, 20, 6]
print('first set')
result = resultcreator(sourceA)
print(result)
print('second set')
result = resultcreator(sourceB)
print(result)
```

### Example 02
```python
import func2pipe as fp

@fp.pipeit
def addone(item):
    return item + 1

@fp.pipeitwithnamedparams
def add(a, b):
    return a + b

@fp.pipesub(lambda input, output: {'i': input, 'o': output})
@fp.pipeit
def transform(item):
    if (item > 12):
        return True
    else:
        return False

resultcreator = fp.createpipe([
    addone,
    add(b = 4),
    transform
    ], closewitharray = True)

sourceA = iter(range(1, 20))
sourceB = [45, 20, 6]
print('first set')
result = resultcreator(sourceA)
print(result)
print('second set')
result = resultcreator(sourceB)
print(result)
```

### Example 03
```python
import func2pipe as fp

@fp.hasyield
@fp.pipeit
def letters(item):
    for letter in item:
        yield letter

resultcreator = fp.createpipe([
    letters
    ], closewitharray = True)


sourceA = ['ABCDEF', 'GHIJKL']
sourceB = ['MNOPQR', 'STUVWX']

print('first set')
result = resultcreator(sourceA)
print(result)
print('second set')
result = resultcreator(sourceB)
print(result)
```

### Example 04
```python
import func2pipe as fp

@fp.pipesub(lambda input, output: {'source': input, 'letter': output })
@fp.hasyield
@fp.pipeit
def letters(item):
    for letter in item:
        yield letter

resultcreator = fp.createpipe([
    letters
    ], closewitharray = True)


sourceA = ['ABCDEF', 'GHIJKL']
sourceB = ['MNOPQR', 'STUVWX']

print('first set')
result = resultcreator(sourceA)
print(result)
print('second set')
result = resultcreator(sourceB)
print(result)
```

### Example 05
```python
import func2pipe as fp

@fp.pipesub(lambda input, output: {'source': input, 'letter': output })
@fp.pipefind(r"[A-Z]", mapper = lambda item: item.group(0))
def letters(item):
    return item

resultcreator = fp.createpipe([
    letters
    ], closewitharray = True)


sourceA = ['ABCDEF', 'GHIJKL']
sourceB = ['MNOPQR', 'STUVWX']

print('first set')
result = resultcreator(sourceA)
print(result)
print('second set')
result = resultcreator(sourceB)
print(result)
```

### Example 06
```python
import func2pipe as fp

@fp.pipesub(lambda input, output: {'source': input, 'letters': output })
@fp.pipecollecttoarray
@fp.pipefind(r"[A-Z]", mapper = lambda item: item.group(0))
def letters(item):
    return item

resultcreator = fp.createpipe([
    letters
    ], closewitharray = True)


sourceA = ['ABCDEF', 'GHIJKL']
sourceB = ['MNOPQR', 'STUVWX']

print('first set')
result = resultcreator(sourceA)
print(result)
print('second set')
result = resultcreator(sourceB)
print(result)
```
