# nodeview

Nodeview. A PySide nodal view

## nodeview.Graph

Holds all the nodes 

### Graph Constructor

```python
Graph.__init__(self, name)
```

Create a new graph

| Argument | Role |
| --- | --- |
| `name` |  Valid string  |

### Graph.add_node

```python
Graph.add_node(self, node)
```

Add a valid Node to the graph

| Argument | Role |
| --- | --- |
| `node` |  Valid Node |
| `return` |  None |

### Graph.from_dict

```python
Graph.from_dict(graph_dict)
```

Recreates Graph from dict 

| Argument | Role |
| --- | --- |
| `return` |  Graph |

### Graph.to_dict

```python
Graph.to_dict(self)
```

Represents Graph to a serializable dict

| Argument | Role |
| --- | --- |
| `return` |  dict |

## nodeview.GraphicNode


### GraphicNode Constructor

```python
GraphicNode.__init__(self, node)
```


### GraphicNode.update

```python
GraphicNode.update(self)
```


## nodeview.Node

Holds slots and their connections, plus user attributes

### Node Constructor

```python
Node.__init__(self, name, graph, inputs=None, outputs=None, attributes=None)
```

Create a new node to a given graph

| Argument | Role |
| --- | --- |
| `name` |  Valid string  |
| `graph` |  Parent Graph |
| `inputs` |  List of input names |
| `outputs` |  List of output names |
| `attributes` |  **Serializable** user attributes (OrderedDict recomanded) |

### Node.attribute_names

```python
Node.attribute_names(self)
```

List attributes names

| Argument | Role |
| --- | --- |
| `return` |  List of strings |

### Node.get

```python
Node.get(self, item, default=None)
```

Similar to dict.get()

| Argument | Role |
| --- | --- |
| `item` |  Name of the attribute  |
| `default` |  Default value if attribute missing |
| `return` |  Value |

### Node.to_dict

```python
Node.to_dict(self)
```

Represents Node to a serializable dict

| Argument | Role |
| --- | --- |
| `return` |  dict |

## nodeview.Slot

Holds connections, plus user attributes 

### Slot Constructor

```python
Slot.__init__(self, name, role, parent_node, attributes=None)
```

Create a new input/output slot to a given Node

| Argument | Role |
| --- | --- |
| `name` |  Valid string  |
| `role` |  Slot.INPUT or Slot.OUTPUT |
| `parent_node` |  Valid Node to be associated to |
| `attributes` |  **Serializable** user attributes |

### Slot.clear

```python
Slot.clear(self)
```

Disconnect **all** slots

| Argument | Role |
| --- | --- |
| `return` |  None |

### Slot.connect

```python
Slot.connect(self, target_slot, _mirror_connect=False)
```

Connect blah to bleh

| Argument | Role |
| --- | --- |
| `target_slot` |  Slot |
| `_mirror_connect` |  do not use |
| `return` |  None |

### Slot.disconnect

```python
Slot.disconnect(self, target_slot)
```

Disconnect blah from bleh

| Argument | Role |
| --- | --- |
| `target_slot` |  a valid Slot |
| `return` |  None |

### Slot.to_dict

```python
Slot.to_dict(self)
```

Represents Slot to a serializable dict

| Argument | Role |
| --- | --- |
| `return` |  dict |
---
Copyright (C) 2017  Valentin Moriceau - moriceau.v@gmail.com
    
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
