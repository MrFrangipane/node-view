# nodeview
A PySide nodal view

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna 
aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 

Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint 
occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

## Graph

### __init__
```python
Graph.__init__(self, name)
```

### add_node
```python
Graph.add_node(self, node)
```

### from_dict
```python
Graph.from_dict(graph_dict)
```

### to_dict
```python
Graph.to_dict(self)
```

## GraphicNode

### __init__
```python
GraphicNode.__init__(self, node)
```

### update
```python
GraphicNode.update(self)
```

## Node
Class holding data solts bmofjze zelze ze zefze zef ze

f zef zofzefizfoizefze fzefijzef z zef z

ef zefzef zfzef zfeghty nj uj-j rgd trh 

ergerg e

```python
example = Node()
example.connect(a, b)
```

### __init__
```python
Node.__init__(self, name, graph, inputs=None, outputs=None, attributes=None)
```

### attribute_names
```python
Node.attribute_names(self)
```

### get
```python
Node.get(self, item, default=None)
```

### to_dict
```python
Node.to_dict(self)
```

## Slot
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna 
aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 

Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint 
occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

### __init__
```python
Slot.__init__(self, name, role, parent_node, attributes=None)
```

### clear
```python
Slot.clear(self)
```

### connect
```python
Slot.connect(self, target_slot, _mirror_connect=False)
```
Connect blah to bleh

| Argument | Role |
| --- | --- |
| `param target_slot` |  Slot |
| `param _mirror_connect` |  do not use |
| `return` |  None |

### disconnect
```python
Slot.disconnect(self, target_slot)
```

### to_dict
```python
Slot.to_dict(self)
```