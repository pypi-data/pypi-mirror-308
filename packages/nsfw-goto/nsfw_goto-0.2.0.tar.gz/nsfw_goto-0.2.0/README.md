# nsfw_goto

**nsfw_goto** is a Python package that allows you to use goto statements in your Python code.

What it really does is simulate a form of "goto" behavior, letting you jump to specific lines of code in your program. 

*Important disclaimer:* This is primarily intended for educational and experimental purposes. Using goto statements in production code is generally discouraged, as it can make code unpredictable and difficult to read and maintain.

## Installation

To install nsfw_goto, simply run:

```bash

pip install nsfw_goto
```

## Usage

You can use goto to jump to a specific line in your code. Here’s a simple example:

```python
from nsfw_goto import goto

x = 0
x += 1
if x < 3:
    goto(4)

print(x)
```

In this example, the goto(4) will jump the execution back to line 4, causing the code to repeat itself until the condition x < 3 is no longer met.

The goto functionality even allows jumping between methods. Here’s an example demonstrating how it works across different method calls:

```python
from nsfw_goto import goto

global_value = 0

def foo():
    global global_value
    global_value = 100
    local_value = 200
    goto(14)

def bar():
    print(global_value + local_value)

if global_value == 0:
    foo()
```

The code jumps from inside the foo() method to inside bar() method, preserving the values of both global_Value and local_value.


## Development

If you’d like to contribute to the project, pull requests are very welcome!

Tests for this project are located in the tests folder and use Python’s unittest framework. To run the tests, you can use the following command:

```bash

python -m unittest discover tests
```

This will automatically discover and run all the test cases. Because the goto currently breaks unittest, the unittests run an example code in a separate process and verify the success based on stdout output.


## Contribution Guidelines

Feel free to get involved!
Fork the repository and clone it to your local machine.
Open a pull request with a clear description of what you've added or changed.


## License

This project is licensed under the MIT License. See the LICENSE file for details.
