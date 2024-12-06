# gumsh_py
gumsh_py is a Python interface of charm.sh's shell tool called [gum](https://github.com/charmbracelet/gum). Gum is used to create aesthetically pleasing shell scripts. 

# Installation
Install gum for your environment using the [instructions](https://github.com/charmbracelet/gum).
Then install my python package like so:
```sh
$ pip install gumsh-py
```

# Usage
```python
from gumsh_py import gumsh_py as gp

gumpy.choose(prompt="favorite languages?", options=["python", "javascript", "java", "c++", "c#"])
gumpy.spin(command="sleep 5", show_output=False, spinner="dot", text="Sleeping...")
print(gumpy.confirm(prompt="Are you positive?"))
gumpy.get_input(prompt="Enter your name:", placeholder="John Doe")
gumpy.log(text="Hello, World!", level="info", time="ansic")
```

# Note
Not all command flag options in the gum library are given for each command. And not all commands are included. If this package picks up steam, I will consider adding support.
E.g. `gum choose` for example allows for a limit which I have included functionality for, but there are other [options](https://github.com/charmbracelet/gum/blob/main/choose/options.go) such as `CursorPrefix` that are not included for simplicity's sake. 

To view flags that the Python package uses, go to the [gum](https://github.com/charmbracelet/gum) repository, choose the command you are using `choose` for example, and open the `options.go` file to view flag options. 

# Pypi
[Pypi](https://pypi.org/project/gumsh-py/) details.
