# Run-TOGT-Planner

This Python package provides an interface to run the [**Time-Optimal Gate-Traversing (TOGT) Planner**](https://github.com/FSC-Lab/TOGT-Planner), originally a C++ project.

With this package, you can generate random racetracks and plan paths using the **TOGT Planner**. It supports looping to generate a large number of high-quality trajectories that prioritize dynamic feasibility.

## Installations

#### 0. Requirements

**Python Packages:** `numpy`, `pyyaml`

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

Coming soon ...