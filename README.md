# nodeview

Nodeview. A PySide nodal view

## Class **Graph**

Holds all the nodes 

### Constructor

```python
Graph(name)
```

Create a new graph

| Argument | Role |
| --- | --- |
| `name` |  Valid string  |

### **add_node**

```python
Graph.add_node(node)
```

Add a valid Node to the graph

| Argument | Role |
| --- | --- |
| `node` |  Valid Node |
| Returns |  None |

### **from_dict**

```python
Graph.from_dict()
```

Recreates Graph from dict 

| Argument | Role |
| --- | --- |
| Returns |  Graph |

### **to_dict**

```python
Graph.to_dict()
```

Represents Graph to a serializable dict

| Argument | Role |
| --- | --- |
| Returns |  dict |

## Class **Node**

Holds slots and their connections, plus user attributes

### Constructor

```python
Node(name, graph, inputs=None, outputs=None, attributes=None)
```

Create a new node to a given graph

| Argument | Role |
| --- | --- |
| `name` |  Valid string  |
| `graph` |  Parent Graph |
| `inputs` |  List of input names |
| `outputs` |  List of output names |
| `attributes` |  **Serializable** user attributes (OrderedDict recomanded) |

### **attribute_names**

```python
Node.attribute_names()
```

List attributes names

| Argument | Role |
| --- | --- |
| Returns |  List of strings |

### **get**

```python
Node.get(item, default=None)
```

Similar to dict.get()

| Argument | Role |
| --- | --- |
| `item` |  Name of the attribute  |
| `default` |  Default value if attribute missing |
| Returns |  Value |

### **to_dict**

```python
Node.to_dict()
```

Represents Node to a serializable dict

| Argument | Role |
| --- | --- |
| Returns |  dict |

## Class **Slot**

Holds connections, plus user attributes 

### Constructor

```python
Slot(name, role, parent_node, attributes=None)
```

Create a new input/output slot to a given Node

| Argument | Role |
| --- | --- |
| `name` |  Valid string  |
| `role` |  Slot.INPUT or Slot.OUTPUT |
| `parent_node` |  Valid Node to be associated to |
| `attributes` |  **Serializable** user attributes |

### **clear**

```python
Slot.clear()
```

Disconnect **all** slots

| Argument | Role |
| --- | --- |
| Returns |  None |

### **connect**

```python
Slot.connect(target_slot, _mirror_connect=False)
```

Connect blah to bleh

| Argument | Role |
| --- | --- |
| `target_slot` |  Slot |
| `_mirror_connect` |  do not use |
| Returns |  None |

### **disconnect**

```python
Slot.disconnect(target_slot)
```

Disconnect blah from bleh

| Argument | Role |
| --- | --- |
| `target_slot` |  a valid Slot |
| Returns |  None |

### **to_dict**

```python
Slot.to_dict()
```

Represents Slot to a serializable dict

| Argument | Role |
| --- | --- |
| Returns |  dict |

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
