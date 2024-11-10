# Tools

# 1. Race Generator

## GateShape

### SingleBall

```python
class RaceGenerator.GateShape.SingleBall(radius, margin)
```

**Parameters:**

- **radius** (*float*): The radius of the single ball gate, defining its size.

- **margin** (*float*): The margin around the gate, specifying the clearance space.

#### get_shape_info()

```python
RaceGenerator.GateShape.SingleBall.get_shape_info()
```

Returns a dictionary representation of the shape.

**Return type:**    *Dict[str, Any]*

### TrianglePrisma

```python
class RaceGenerator.GateShape.TrianglePrisma(rpy, length, midpoints, width, height, margin)
```

**Parameters:**

- **rpy** (*List[float] | ndarray*): Represents the rotation of the gate in Roll, Pitch, and Yaw angles.

- **length** (*float*): The length of the triangular prism, determining its extension along the track.

- **midpoints** (*int*): The number of midpoints used to define the gate's curvature or segmentation.

- **width** (*float*): The width of the triangular prism, specifying its horizontal spread.

- **height** (*float*): The height of the triangular prism, indicating its vertical dimension.

- **margin** (*float*): The margin around the gate, providing necessary clearance.

#### get_shape_info()

```python
RaceGenerator.GateShape.TrianglePrisma.get_shape_info()
```

Returns a dictionary representation of the shape.

**Return type:**    *Dict[str, Any]*

### RectanglePrisma

```python
class RaceGenerator.GateShape.RectanglePrisma(rpy, length, midpoints, width, height, marginW, marginH)
```

**Parameters:**

- **rpy** (*List[float] | ndarray*): Represents the rotation of the gate in Roll, Pitch, and Yaw angles.

- **length** (*float*): The length of the rectangular prism, determining its extension along the track.

- **midpoints** (*int*): The number of midpoints used to define the gate's curvature or segmentation.

- **width** (*float*): The width of the rectangular prism, specifying its horizontal spread.

- **height** (*float*): The height of the rectangular prism, indicating its vertical dimension.

- **marginW** (*float*): The horizontal margin around the gate, ensuring adequate clearance laterally.

- **marginH** (*float*): The vertical margin around the gate, providing necessary clearance vertically.

#### get_shape_info()

```python
RaceGenerator.GateShape.RectanglePrisma.get_shape_info()
```

Returns a dictionary representation of the shape.

**Return type:**    *Dict[str, Any]*

### PentagonPrisma

```python
class RaceGenerator.GateShape.PentagonPrisma(rpy, length, midpoints, radius, margin)
```

**Parameters:**

- **rpy** (*List[float] | ndarray*): Represents the rotation of the gate in Roll, Pitch, and Yaw angles.

- **length** (*float*): The length of the pentagonal prism, determining its extension along the track.

- **midpoints** (*int*): The number of midpoints used to define the gate's curvature or segmentation.

- **radius** (*float*): The radius of the pentagonal prism, specifying the size of its base.

- **margin** (*float*): The margin around the gate, ensuring sufficient clearance to avoid collisions.

#### get_shape_info()

```python
RaceGenerator.GateShape.PentagonPrisma.get_shape_info()
```

Returns a dictionary representation of the shape.

**Return type:**    *Dict[str, Any]*

### HexagonPrisma

```python
class RaceGenerator.GateShape.HexagonPrisma(rpy, length, midpoints, side, margin)
```

**Parameters:**

- **rpy** (*List[float] | ndarray*): Represents the rotation of the gate in Roll, Pitch, and Yaw angles.

- **length** (*float*): The length of the hexagonal prism, determining its extension along the track.

- **midpoints** (*int*): The number of midpoints used to define the gate's curvature or segmentation.

- **side** (*float*): The length of each side of the hexagonal base, determining its size and shape.

- **margin** (*float*): The margin around the gate, ensuring sufficient clearance to avoid collisions.

#### get_shape_info()

```python
RaceGenerator.GateShape.HexagonPrisma.get_shape_info()
```

Returns a dictionary representation of the shape.

**Return type:**    *Dict[str, Any]*

## BaseRaceClass

### State

```python
class RaceGenerator.BaseRaceClass.State(pos, vel=None, acc=None, jer=None, rot=None, cthrustmass=None, euler=None)
```

The `State` class is used to store the states of a race track. It represents the initial and end states of the quadrotor.

**Parameters:**

- **pos** (*List[float] | ndarray*) - The position of the quadrotor in 3D space, typically represented as `[x, y, z]`.

- **vel** (*List[float] | ndarray | None*) - The velocity vector of the quadrotor, representing its movement speed along the X, Y, and Z axes. If not provided (`None`), it defaults to `[0.0, 0.0, 0.0]`.

- **acc** (*List[float] | ndarray | None*) - The acceleration vector of the quadrotor, indicating its rate of change of velocity along each axis. If not provided (`None`), it defaults to `[0.0, 0.0, 0.0]`.

- **jer** (*List[float] | ndarray | None*) - The jerk vector of the quadrotor, representing the rate of change of acceleration. Defaults to `None`. If not provided (`None`), it defaults to `[0.0, 0.0, 0.0]`.

- **rot** (*List[float] | ndarray | None*) - The quaternion of the quadrotor, typically represented as `[roll, pitch, yaw]`. Defaults to `None`. If not provided (`None`), it defaults to `[0.0, 0.0, 0.0， 0.0]`.

- **cthrustmass** (*float | None*) - The *collective thrust 2 mass* of the quadrotor. Defaults to `None`. If not provided (`None`), it defaults to `0.0`.

- **euler** (*List[float] | ndarray | None*) - The Euler angles of the quadrotor, representing its orientation in space as `[phi, theta, psi]`. Defaults to `None`. If not provided (`None`), it defaults to `[0.0, 0.0, 0.0]`.

#### to_dict()

```python
RaceGenerator.BaseRaceClass.State.to_dict()
```

Returns a dictionary representation of the state without any specific ordering.

**Return type:**    *Dict[str, Any]*

#### to_ordered_dict()

```python
RaceGenerator.BaseRaceClass.State.to_ordered_dict()
```

Returns an ordered dictionary representation of the state, preserving the order of insertion.

**Return type:**    *CommentedMap*

### Gate

```python
class RaceGenerator.BaseRaceClass.Gate(gate_shape, position, stationary, name=None)
```

The `Gate` class is used to store the Gates of a race track.

**Parameters:**

- **gate_shape** (*BaseShape*) - The shape class of the gate, determining its geometric form. Refer to [`RaceGenerator.GateShape`](##GateShape) for available shapes and their specifications.

- **position** (*List[float] | ndarray*) - The position of the gate in 3D space, typically represented as `[x, y, z]`.

- **stationary** (*bool*) - Indicates whether the gate is stationary. Set to `True` if the gate does not move.

- **name** (*str | None*) - The name of the gate. This parameter is optional and can be used to uniquely identify the gate.

#### to_dict()

```python
RaceGenerator.BaseRaceClass.Gate.to_dict()
```

Returns a dictionary representation of the gate without any specific ordering.

**Return type:**    *Dict[str, Any]*

#### to_ordered_dict()

```python
RaceGenerator.BaseRaceClass.Gate.to_ordered_dict()
```

Returns an ordered dictionary representation of the gate, preserving the order of insertion.

**Return type:**    *CommentedMap*

## RaceTrack

### RaceTrack

```python
class RaceGenerator.RaceTrack.RaceTrack(init_state, end_state, race_name=None)
```

The `RaceTrack` class is used to represent a race track within the **TOGT-Planner** framework. It encapsulates the initial and final states of the quadrotor and manages the race track's metadata.

**Parameters:**

- **init_state** (*State*) - The initial state ([`RaceGenerator.BaseRaceClass.State`](###State)) of the quadrotor at the start of the race track.

- **end_state** (*State*) - The final state of the quadrotor at the end of the race track.

- **race_name** (*str | None*) - This parameter is optional and can be used to uniquely identify the race track and name the saved YAML files accordingly.

#### add_gate()

```python
RaceGenerator.RaceClass.RaceTrack.add_gate(gate, gate_name=None)
```

Adds a gate to the race track.

**Parameters:**

- **gate** (*Gate*) - The gate object to be added to the race track. This gate should be an instance of the [`RaceGenerator.BaseRaceClass.Gate`](###Gate) class, defining the gate's shape, position, and other attributes.

- **gate_name** (*str | None*) - The name of the gate. This parameter is optional and can be used to uniquely identify the gate within the race track. If not provided (`None`), a default naming convention will be applied.

#### clear_gate()

```python
RaceGenerator.RaceClass.RaceTrack.clear_gate()
```

Clear gates of the race track.

#### get_gate_dict()

```python
RaceGenerator.RaceClass.RaceTrack.get_gate_dict(ordered=False)
```

Retrieves the gate information as a dictionary.

**Parameters:**

- **ordered** (*bool*) - Determines the type of dictionary to return. If set to `True`, the method returns an ordered dictionary (*CommentedMap*) that preserves the order of gate insertion. If set to `False`, it returns a standard unordered dictionary (*Dict[str, Any]*). Defaults to `False`.

**Return type:**    *Dict[str, Any] | CommentedMap*

#### to_dict()

```python
RaceGenerator.RaceClass.RaceTrack.to_dict()
```

Returns a dictionary representation of the race track without any specific ordering.

**Return type:**    *Dict[str, Any]*

#### to_ordered_dict()

```python
RaceGenerator.RaceClass.RaceTrack.to_ordered_dict()
```

Returns an ordered dictionary representation of the race track, preserving the order of insertion.

**Return type:**    *CommentedMap*

#### save_to_yaml()

```python
RaceGenerator.RaceClass.RaceTrack.save_to_yaml(save_dir=None, overwrite=False, standard=True, save_output=True)
```

Saves the race track configuration to a YAML file.

**Parameters:**

- **save_dir** (*PathLike | str | None*) - The directory where the YAML file will be saved. If set to `None`, the file will be saved in the current working directory.

- **overwrite** (*bool*) - Determines whether to overwrite an existing YAML file with the same name. If set to `True`, the existing file will be overwritten. If set to `False`, the method will create a new file with a different name. Defaults to `False`.

- **standard** (*bool*) - Indicates whether to save the race track in the standard YAML format expected by the **TOGT-Planner**. If set to `True`, the YAML file will adhere to the predefined schema required for compatibility with the planner. Defaults to True.

- **save_output** (*bool*) - Determines whether to save informational messages about the save operation. If set to `True`, the method will show details about the save process. Defaults to `True`.

**Return type:**    *bool* - Returns `True` if the YAML file was successfully saved, and `False` otherwise.


#### load_from_yaml()

```python
RaceGenerator.RaceClass.RaceTrack.load_from_yaml(load_dir)
```

Loads the race track configuration from a YAML file.

**Parameters:**

- **load_dir** (*PathLike | str | None*) - The directory where the YAML file will be loaded.

## GenerationTools

### quote_specific_keys()

```python
RaceGenerator.GenerationTools.quote_specific_keys(data, keys_to_quote=KEYS_TO_QUOTE)
```

Sets specific keys in the data with single quotes and prepares the data for saving to a YAML file.

**Parameters:**

- **data** (*Dict | List[Dict] | str*) - The data structure to process, which can be a dictionary, list of dictionaries, or a string.

- **keys_to_quote** (*List[Dict]*) - The list of keys whose string values should be quoted. Defaults to `KEYS_TO_QUOTE = ['type', 'name']`.

**Return type**:    *Dict | List[Dict] | SingleQuotedScalarString*

### get_shape_class()

```python
RaceGenerator.GenerationTools.get_shape_class(gate_shape)
```

Finds and returns the shape class corresponding to the given gate shape name within [`RaceGenerator.GateShape`](##GateShape)

**Parameters:**

- **gate_shape** (*str*) - The name of the shape class to retrieve.

**Return type:**    *GateShape*

### create_state()

```python
RaceGenerator.GenerationTools.create_state(state_kwargs)
```

Creates and returns a `State` object based on the provided keyword arguments. Refer to [`RaceGenerator.BaseRaceClass.State`](###State) for more details.

**Parameters:**

- **state_kwargs** (*Dict*) - A dictionary of state parameters used to initialize the state.

**Return type:**    *State*

### create_gate()

```python
RaceGenerator.GenerationTools.create_gate(gate_type, position, stationary, shape_kwargs, name=None)
```

Creates and returns a `Gate` object based on the provided parameters. Refer to [`RaceGenerator.BaseRaceClass.Gate`](###Gate) for more details.

**Parameters:**

- **gate_type** (*Type[GateShape]*) - The type of shape class to use for the gate.

- **position** (*List[float] | ndarray*) - The position coordinates of the gate.

- **stationary** (*bool*) - Indicates whether the gate is stationary.

- **shape_kwargs** (*Dict*) - A dictionary of shape-specific parameters.

- **name** (*str | None*) - The name of the gate. Defaults to `None`.

**Return type:**    *Gate*