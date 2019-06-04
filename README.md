# func2pipe
python utils for generator function creation

### Example 01
```python
import func2pipe as fp

@fp.pipeit
def addone(item):
    return item + 1

@fp.pipeit
def add(a, b):
    return a + b

resultcreator = fp.createpipe([
    addone(),
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

@fp.pipeit
def add(a, b):
    return a + b

@fp.pipesub(lambda input, output: {'i': input, 'o': output})
@fp.pipeit
def transform(item):
    if (item > 12):
        return True
    else:
        return False

@fp.pipesub(lambda input, output: {'i': input, **output})
@fp.pipeit
def transform2(item, fixed):
    if (item > 12):
        return {'r': True, 'f': fixed }
    else:
        return {'r': False, 'f': fixed }

resultcreator = fp.createpipe([
    addone(),
    add(b = 4),
    transform2(fixed = 'fixed')
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
def letters(item, spec):
    for letter in item:
        yield letter + spec

resultcreator = fp.createpipe([
    letters(spec = '-')
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
    letters()
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
@fp.pipeit
def letters(item, append):
    return item + append

resultcreator = fp.createpipe([
    letters(append = 'x')
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
@fp.pipeit
def letters(item, b):
    return item + b

resultcreator = fp.createpipe([
    letters(b = 'x')
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

### Example GR
```python
import func2pipe as fp

@fp.pipeit
def record_A(item):
    return {**item, 'label': 'A'}

@fp.pipeit
def record_B(item):
    return {**item, 'label': 'B'}

@fp.pipeit
def record_C(item):
    return {**item, 'label': 'C'}

@fp.hasyield
@fp.pipeit
def relation_A_B(item):
    id = item['id']
    relace = [
        {'s': '1', 'd': '2'},
        {'s': '1', 'd': '3'},
        {'s': '2', 'd': '3'},
        ]
    for r in relace:
        if r['s'] == id:
            yield {'id': r['d']}

@fp.hasyield
@fp.pipeit
def relation_B_C(item):
    id = item['id']
    relace = [
        {'s': '1', 'd': '2'},
        {'s': '1', 'd': '3'},
        {'s': '2', 'd': '3'},
        ]
    for r in relace:
        if r['s'] == id:
            yield {'id': r['d']}
    
graph = {
    'nodes': {
        'A': record_A(),
        'B': record_B(),
        'C': record_C()
        },
    'edges': [
        {'from': 'A', 'to': 'B', 'relation': relation_A_B()},
        {'from': 'B', 'to': 'C', 'relation': relation_B_C()},
        ]
    }


def builder(graph, currentnode, filterq = lambda item: True):
    descriptorpipe = graph['nodes'][currentnode]

    def x(relation):
        relationpipe = relation['relation']
        filterq = lambda item: True;
        if ('filter' in relation):
            filterq = relation['filter']

        sub = builder(graph, relation['to'], filterq)
        return fp.createpipe([relationpipe, sub])

    relations = filter(lambda item: item['from'] == currentnode, graph['edges'])
    relationsresult = {}
    for relation in relations:
        itemname = relation['to']
        if ('itemname' in relation):
            itemname = relation['itemname']
        relationsresult[itemname] = fp.createpipe([x(relation)], closewitharray = True)

    @fp.pipeit
    def userelations(item):
        result = { **item }
        for key in relationsresult.keys():
            result[key] = relationsresult[key]([item])
        return result

    return fp.createpipe([descriptorpipe, userelations()], closewitharray = True)

bba = builder(graph, 'A')
result = bba([{'id': '1'}])
print(result)
```
