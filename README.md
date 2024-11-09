# Run-TOGT-Planner

This Python package provides an interface to run the [**Time-Optimal Gate-Traversing (TOGT) Planner**](https://github.com/FSC-Lab/TOGT-Planner), originally a C++ project.

With this package, you can generate random racetracks and plan paths using the **TOGT Planner**. It supports looping to generate a large number of high-quality trajectories that prioritize dynamic feasibility.

## Installations

#### 0. Requirements

**Python Packages:** `numpy`, `pyyaml`, `ruamel.yaml`

#### 1. Install TOGT-Planner and Build

**Note:** Please check out to the commit from **May 15, 2024** (commit `f69f3fc9143b02b58bd6a66dc12a531395bf5317`, [Correct plotting bugs](https://github.com/FSC-Lab/TOGT-Planner/commit/f69f3fc9143b02b58bd6a66dc12a531395bf5317)) for a stable version.

#### 2. Clone the Repository

```bash
cd ${YOUR_TOGT_PLANNER_PATH}
git clone https://github.com/KafuuChikai/Run-TOGT-Planner.git
```

#### 3. Modify `CMakeLists.txt`

Add the following code after line 255:

```cmake
add_executable(planners Run-TOGT-Planner/traj_planner/traj_planner_togt.cpp)
target_compile_options(planners PRIVATE
  -fno-finite-math-only
  -Wall                   # Show all warnings
  -Wextra                 # Show extra error information
  -Wpedantic              # Issue all the warnings demanded by strict ISO C and ISO C++
  -Werror                 # Raise all warnings to errors
  -Wunused                # Warn whatever is assigned to, but unused
  -Wno-unused-parameter
  -Wundef                 # Warn if an undefined identifier is evaluated in an #if directive. 
  -Wcast-align            # Warn whenever a pointer is cast such that the required alignment of the target is increased
  -Wmissing-declarations  # Warn if a global function is defined without a previous declaration
  -Wmissing-include-dirs  # Warn if a user-supplied include directory does not exist.
  -Wnon-virtual-dtor      
  -Wredundant-decls       # Warn if anything is declared more than once in the same scope
  -Wodr
  -Wunreachable-code
  -Wno-unknown-pragmas
)
target_link_libraries(planners
        ${LIBRARY_NAME}
        $<$<AND:$<CXX_COMPILER_ID:GNU>,$<VERSION_LESS:$<CXX_COMPILER_VERSION>,9.0>>:stdc++fs>
        )
```

#### 4. Build the Project

Navigate to the build directory, configure the project, and compile:

```bash
cd ${YOUR_TOGT_PLANNER_PATH}/build
cmake ..
make
```

#### 5. Run the Example Script

```bash
python ${YOUR_TOGT_PLANNER_PATH}/Run-TOGT-Planner/run_traj_planner.py
```

## Tools

### 1. Race Generator

We have implemented **3 base classes** for a standard **TOGT-Planner** race track:

#### **RaceClass.State**

```python
class RaceGenerator.RaceClass.State(pos, vel=None, acc=None, jer=None, rot=None, cthrustmass=None, euler=None)
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

    ```python
    to_dict()
    ```

    Returns a dictionary representation of the state without any specific ordering.

    **Return type:**	*Dict[str, Any]*

    ```python
    to_ordered_dict()
    ```

    Returns an ordered dictionary representation of the state, preserving the order of insertion.

    **Return type:**	*CommentedMap*

#### **RaceClass.Gate**

```python
class RaceGenerator.RaceClass.Gate(gate_shape, position, stationary, name=None)
```

The `Gate` class is used to store the Gates of a race track.

**Parameters:**

- **gate_shape** (*BaseShape*) - The shape class of the gate, determining its geometric form. Refer to `RaceGenerator.GateShape` for available shapes and their specifications.
- **position** (*List[float] | ndarray*) - The position of the gate in 3D space, typically represented as `[x, y, z]`.
- **stationary** (*bool*) - Indicates whether the gate is stationary. Set to `True` if the gate does not move.
- **name** (*str | None*) - The name of the gate. This parameter is optional and can be used to uniquely identify the gate.

    ```python
    to_dict()
    ```

    Returns a dictionary representation of the gate without any specific ordering.

    **Return type:**	*Dict[str, Any]*

    ```python
    to_ordered_dict()
    ```

    Returns an ordered dictionary representation of the gate, preserving the order of insertion.

    **Return type:**	*CommentedMap*

#### **RaceClass.RaceTrack**

```python
class RaceGenerator.RaceClass.RaceTrack(init_state, end_state, race_name=None)
```

The `RaceTrack` class is used to represent a race track within the **TOGT-Planner** framework. It encapsulates the initial and final states of the quadrotor and manages the race track's metadata.

**Parameters:**

- **init_state** (*State*) - The initial state (`RaceGenerator.RaceClass.State`) of the quadrotor at the start of the race track.
- **end_state** (*State*) - The final state of the quadrotor at the end of the race track.
- **race_name** (*str | None*) - This parameter is optional and can be used to uniquely identify the race track and name the saved YAML files accordingly.

    ```python
    add_gate(gate, gate_name=None)
    ```

    Adds a gate to the race track.

    **Parameters:**

    - **gate** (*Gate*) - The gate object to be added to the race track. This gate should be an instance of the `RaceGenerator.RaceClass.Gate` class, defining the gate's shape, position, and other attributes.
    - **gate_name** (*str | None*) - The name of the gate. This parameter is optional and can be used to uniquely identify the gate within the race track. If not provided (`None`), a default naming convention will be applied.

    ```python
    get_gate_dict(ordered=False)
    ```

    Retrieves the gate information as a dictionary.

    **Parameters:**

    - **ordered** (*bool*) - Determines the type of dictionary to return. If set to `True`, the method returns an ordered dictionary (*CommentedMap*) that preserves the order of gate insertion. If set to `False`, it returns a standard unordered dictionary (*Dict[str, Any]*). Defaults to `False`.

    **Return type:**	*Dict[str, Any]* | *CommentedMap*

    ```python
    to_dict()
    ```

    Returns a dictionary representation of the race track without any specific ordering.

    **Return type:**	*Dict[str, Any]*

    ```python
    to_ordered_dict()
    ```

    Returns an ordered dictionary representation of the race track, preserving the order of insertion.

    **Return type:**	*CommentedMap*

    ```python
    save_to_yaml(save_dir=None, overwrite=False, standard=True, save_output=True)
    ```

    Saves the race track configuration to a YAML file.

    **Parameters:**

    - **save_dir** (*PathLike* | *str* | *None*) - The directory where the YAML file will be saved. If set to `None`, the file will be saved in the current working directory.
    - **overwrite** (*bool*) - Determines whether to overwrite an existing YAML file with the same name. If set to `True`, the existing file will be overwritten. If set to `False`, the method will create a new file with a different name. Defaults to `False`.
    - **standard** (*bool*) - Indicates whether to save the race track in the standard YAML format expected by the **TOGT-Planner**. If set to `True`, the YAML file will adhere to the predefined schema required for compatibility with the planner. Defaults to True.
    - **save_output** (*bool*) - Determines whether to save informational messages about the save operation. If set to `True`, the method will show details about the save process. Defaults to `True`.

    **Return type:**	*bool* - Returns `True` if the YAML file was successfully saved, and `False` otherwise.