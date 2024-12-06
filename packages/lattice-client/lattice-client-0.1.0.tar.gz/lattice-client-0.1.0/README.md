# Enterprise Platform Compute Python Client

This is the Python client interface for the Enterprise Platform Compute service.

## Installation

1. First set up a virtual environment **with a supported Python version** (see supported versions below).

2. Install the library `pip install enterprise-platform-compute`.

3. Grab an API key from the dashboard.

4. Begin using the library to construct and execute computational graphs.

## Supported python versions

The `cloudpickle` module is used to serialize your functions passed to the computational
graph so that they can be transferred to the platform's runners. Pickling requires that
the version of Python from which the function was pickled must match the version of Python
in which the unpickling is performed. Currently, the platform has support for Python 3.9
runners with 3.10 coming very soon.

### Currently supported versions:

- **3.9.x**

## Example

Here is a very simple example showing how to use the platform.

```python
from lattice import Vector


def solve(value):
    return value * 100


if __name__ == "__main__":
    results = Vector([i for i in range(3)]).map(solve).evaluate(api_key="<your-api-key>")
    print(results)

# >>> [0, 100, 200]
```

For an example of how to use the platform to run **FEMM** simulations see the example in
`examples/getting_started_femm.py`.
