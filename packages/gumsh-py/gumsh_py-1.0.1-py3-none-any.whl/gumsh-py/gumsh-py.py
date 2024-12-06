"""
gumsh-py is a Python library that provides a set 
of utilities for building command-line interfaces.
"""

import subprocess


def choose(prompt: str = None, options: list = None, limit: int = 1) -> list:
    """Choose an option from a list of choices.

    Args:
        prompt (str): The question to ask the user (optional). Defaults to None.
        options (list): A list of choices to present to the user. Defaults to None.
        limit (int, optional): How many choices can be selected. Defaults to 1.

    Returns:
        list: A list of the user's choices.
    """

    command = ["gum", "choose"]
    if prompt:
        print(prompt)
    if limit > 1:
        command.append(f"--limit={limit}")
    if options:
        command += options
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True, check=True)
    if result.returncode != 0:
        print(result.stderr)


def confirm(prompt: str = None) -> bool:
    """Confirm a user's choice.

    Args:
        prompt (str, optional): Prompt you would like to display to user. Defaults to None and will use the default prompt "Are you sure?".

    Returns:
        bool: True if user confirms, False otherwise.
    """

    command = ["gum", "confirm"]
    if prompt:
        command.append(prompt)
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True, check=False)
    if result.returncode == 0:
        return True
    return False


def get_input(prompt: str = None, placeholder: str = None) -> str:
    """Prompt the user for input.

    Args:
        prompt (str, optional): Prompt you would like to display to user. Defaults to None.
        placeholder (str, optional): Placeholder text for the input. Defaults to None.

    Returns:
        str: User's input.
    """

    command = ["gum", "input"]
    if prompt:
        print(prompt)
    if placeholder:
        placeholder = f"--placeholder={placeholder}"
        command.append(placeholder)

    result = subprocess.run(command, stdout=subprocess.PIPE, text=True, check=True)
    return result.stdout


def spin(command: str = None, show_output: bool = False, spinner: str = None, text: str = None) -> None:
    """Display a spinner.

    Args:
        command (str, optional): Command to execute while spinning. Defaults to None.
        show_output (bool, optional): Show or pipe output of command during execution. Defaults to False.
        spinner (str, optional): Style of the spinner. Defaults to None and will use the default spinner.
        text (str, optional): Text to display while spinning. Defaults to None and will use the default text "Loading...".
    
    Returns:
        None

    Note: Look at the gum CLI documentation for more information on the available spinners.    
    """

    cmd = ["gum", "spin", command]

    if text:
        text = f"--title={text}"
        cmd.append(text)
    if spinner:
        spinner = f"--spinner={spinner}"
        cmd.append(spinner)
    if show_output:
        show_output = "--show-output"
        cmd.append(show_output)
    cmd = " ".join(cmd)
    result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True, check=False)
    print(result.stdout)


def log(text: str = None, level: str = None, time: str = None) -> None:
    """Log a message.

    Args:
        text (str, optional): Text to log. Defaults to None.
        level (str, optional): Log level to use. Defaults to None.
        time (str, optional): Time format to use. Defaults to None.
    """

    command = ["gum", "log"]
    if text:
        command.append(text)
    if level:
        command.append(f"--level={level}")
    if time:
        command.append(f"--time={time}")
    subprocess.run(command, stdout=subprocess.PIPE, text=True, check=False)
