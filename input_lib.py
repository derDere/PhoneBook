"""This module provides methods to savely input certain types like int date bool and so on.
"""
import re
import os
from datetime import date


DATE_PATTERN = r"^(\d{4,})[-. ]+(\d{1,2})[-. ]+(\d{1,2})$"
PHONE_NR_PATTERN = r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"
EMAIL_PATTERN = (
    r"^(([^<>()\[\]\\.,;:\s@\"]+(\.[^<>()\[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\." +
    r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$"
)
ABORT_INPUT_KEY_SEQUENCE = '\x01' # ^A
EXIT_INPUT_KEY_SEQUENCE = '\x18' # ^E
DELETE_INPUT_KEY_SQEUNECE = '\x04' # ^D
HELP_INPUT_KEY_SEQUENCE = '?'


class InputAbortException(Exception):
    """Gets thrown once the user aborts the editing using ^A
    """
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InputExitException(Exception):
    """Gets thrown once the user aborts the editing using ^A
    """
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class HelpOutput:
    """Changes the default help output inside a with statement.
    """

    def __init__(self, new_help_out_method) -> None:
        self.old_help_out = HelpOutput._help_out
        self.new_help_out = new_help_out_method

    def __enter__(self):
        HelpOutput._help_out = self.new_help_out
        return self

    def __exit__(self, *args):
        HelpOutput._help_out = self.old_help_out

    @staticmethod
    def _default_help_output():
        print("^A = abort action; ^X = exit action; ^D = delete content; ? = display help")

    @staticmethod
    def _reset_help_out() -> None:
        """Resets the help_out to the default output
        """
        HelpOutput.help_out = HelpOutput._default_help_output

    _help_out = _default_help_output

    @staticmethod
    def print():
        """Use this to exec the default Help Output function.
        """
        HelpOutput._help_out()


def input_rex(
    label:str = "",
    error:str = "Entered string musst match the pattern!",
    pattern:str = ".*",
    default:str = "",
    show_default:bool = False,
    default_display = lambda d: f" ({d})",
    empty_value=""
) -> str:
    """Returns a string that will be checked by an regular expression to make sure the user input is correct.

    Args:
        label (str, optional): Gets displayed in front of the input. Defaults to "".
        error (str, optional): Gets displayed if the input does not match the expression. Defaults to "Entered string musst match the pattern!".
        pattern (str, optional): the regular expression that will be matched aginst the input. Defaults to ".*".
        default (str, optional): the default value that gets returned if the user cancels by inputing nothing. Defaults to "".

    Returns:
        str: regex matched user input
    """
    if "%s" in label:
        if show_default:
            value_display = default_display(default)
            label = label % value_display
        else:
            label = label % ""
    while True:
        line = input(label)
        if line == ABORT_INPUT_KEY_SEQUENCE:
            raise InputAbortException()
        if line == EXIT_INPUT_KEY_SEQUENCE:
            raise InputExitException()
        if line == HELP_INPUT_KEY_SEQUENCE:
            HelpOutput.print()
        if line == DELETE_INPUT_KEY_SQEUNECE:
            return empty_value
        if line.strip() == "":
            return default
        if re.match(pattern, line) is None:
            print(error)
        else:
            return line


def input_date(
    label:str = "",
    default:date = None,
    show_default:bool = False,
    default_display = lambda d: f" ({d})",
    empty_value=date(1800,1,1)
) -> date:
    """Lets the user input a date using a certain pattern that getch checked by reg ex and returns a date

    Args:
        label (str, optional): Gets displayed in front of the input. Defaults to "".
        default (date, optional): the default date that gets returned if the user cancels by entering nothing. Defaults to None.

    Returns:
        date: the entered date
    """
    if "%s" in label:
        if show_default:
            value_display = default_display(default)
            label = label % value_display
        else:
            label = label % ""
    while True:
        line = input_rex(label, "Please use format: yyyy-mm-dd", DATE_PATTERN, "")
        if line == ABORT_INPUT_KEY_SEQUENCE:
            raise InputAbortException()
        if line == EXIT_INPUT_KEY_SEQUENCE:
            raise InputExitException()
        if line == HELP_INPUT_KEY_SEQUENCE:
            HelpOutput.print()
        if line == DELETE_INPUT_KEY_SQEUNECE:
            return empty_value
        if line.strip() == "":
            return default
        match = re.match(DATE_PATTERN, line)
        year = int(match[1])
        month = int(match[2])
        day = int(match[3])
        try:
            date_value = date(year, month, day)
            return date_value
        except ValueError as vex:
            print(vex)


def input_int(
    label:str = "",
    error:str = "Please enter a number!",
    default:int = 0,
    min_value:int = None,
    max_value:int = None,
    show_default:bool = False,
    default_display = lambda d: f" ({d})"
) -> int:
    """Lets the user input a number. Input gets validated range checked.

    Args:
        label (str, optional): Gets displayed in front of the input. Defaults to "".
        error (str, optional): Gets displayed if the input does not match. Defaults to "Please enter a number!".
        default (int, optional): Gets returned of the user cancels the unput by entering nothing. Defaults to 0.
        min (int, optional): If not None will limit the value to a minimum.
        max (int, optional): If not None will limit the value to a maximum.

    Returns:
        int: the entered value as int
    """
    if "%s" in label:
        if show_default:
            value_display = default_display(default)
            label = label % value_display
        else:
            label = label % ""
    while True:
        line = input(label)
        if line == ABORT_INPUT_KEY_SEQUENCE:
            raise InputAbortException()
        if line == EXIT_INPUT_KEY_SEQUENCE:
            raise InputExitException()
        if line == HELP_INPUT_KEY_SEQUENCE:
            HelpOutput.print()
        if line.strip() == "":
            return default
        if not line.isnumeric():
            print(error)
        else:
            value = int(line)
            if min_value is None and max_value is None:
                return value
            if min_value is None:
                if max_value >= value:
                    return value
                print(f"Please entered a value with a maximum of {max_value}!")
            elif max_value is None:
                if min_value <= value:
                    return value
                print(f"Please entered a value with a minimum of {max_value}!")
            else:
                if min_value <= value <= max_value:
                    return value
                print(f"Please enter a value between {min_value} and {max_value}!")


def input_bool(
    label:str = "",
    val_true:str = "t",
    val_false:str = "f",
    error:str = "DEFAULT",
    default:bool = False,
    show_default:bool = False,
    default_display = lambda d: f" ({d})"
) -> bool:
    """Lets the user Input one of two values which will eigther represent true or false. which two values can be inputed can be set.

    Args:
        label (str, optional): Will be displayed in front of the input. Defaults to "".
        val_true (str, optional): this value has to be entered to make the function return True. Defaults to "t".
        val_false (str, optional): this value has to be entered to make the function return False. Defaults to "f".
        error (str, optional): This message will be displayed if the user enteres something else but those two numbers.
                               Defaults to f"Please enter eigther '{val_true}' or '{val_false}'!".
        default (bool, optional): the default value that gets returned once the user canceles the input by entering nothing. Defaults to False.

    Returns:
        bool: a bool balue defined by the two entered values
    """
    if "%s" in label:
        if show_default:
            val = val_false
            if default:
                val = val_true
            value_display = default_display(val)
            label = label % value_display
        else:
            label = label % ""
    if error == "DEFAULT":
        error = f"Please enter eigther '{val_true}' or '{val_false}'!"
    while True:
        line = input(label)
        if line == ABORT_INPUT_KEY_SEQUENCE:
            raise InputAbortException()
        if line == EXIT_INPUT_KEY_SEQUENCE:
            raise InputExitException()
        if line == HELP_INPUT_KEY_SEQUENCE:
            HelpOutput.print()
        if line.strip() == "":
            return default
        if not line.lower() in [val_true.lower(), val_false.lower()]:
            print(error)
        else:
            return line.lower() == val_true.lower()


def input_choice(
    title:str,
    options:dict,
    error:str = "Please enter one of the listed options via its number!",
    bottom:str="",
    label:str=": "
) -> any:
    """Lets the user pic a choice from a given dictionary. The dictionary keys will be displayed to
    the user and the value of the choosen key will be returned.

    Args:
        title (str): Will be displayed at the top of the option list
        options (dict): a dictionary containing the options that can be choosen
        error (str, optional): an error that gets displayed if the entered option in not in the options dict.
                               Defaults to "Please enter one of the listed options via its number!".
        bottom (str, optional): gets displayed at the bottom of the options list. Defaults to "".
        label (str, optional): gets displayed infront of the input. Defaults to ": ".

    Returns:
        any: the value of the choosen key from the options dict
    """
    while True:
        print(title)
        i = 1
        length = len(str(len(options)))
        for key in options:
            print("  (" + ((" " * length + str(i))[-length:]) + f") {key}")
            i += 1
        if len(bottom) > 0:
            print(bottom)
        i = input_int(label, error)
        if i > len(options) or i <= 0:
            print(error)
        else:
            return options[list(options.keys())[i - 1]]


def input_multiline(
    title:str = "Edit multiline text:",
    old_val:list[str] = None,
    bottom:str = None,
    clear_screen:bool = False,
    line_start = "",
    line_column = "|",
    line_end = "",
    empty_text = "<No lines added jet>"
) -> list[str]:
    """Inputs a multilined text.

    Args:
        title (str, optional): String displayed at the top of the input. Defaults to "Edit multiline text:".
        old_val (list[str], optional): Start value that can be edited. Defaults to [].
        bottom (str, optional): String displayed at the bottom of the input.
                                Defaults to "Enter new lines or enter line number followed by text to edit the line.".
        clear_screen (bool, optional): Set to True to clear the screen after every input. Defaults to False.

    Returns:
        list[str]: A list of lines entered by the user.
    """
    if old_val is None:
        old_val = []
    lines = [ line for line in old_val ]
    show_help = True
    while True:
        if clear_screen:
            os.system('cls' if os.name == 'nt' else 'clear')
        print(title)
        if len(lines) > 0:
            line_len = len(str(len(lines)))
            for index, line in enumerate(lines):
                index += 1
                print(line_start, end="")
                print(" " * (line_len - len(str(index))), end="")
                print(index, end=line_column)
                print(line, end="")
                print(line_end)
        else:
            print(empty_text)
        if bottom is not None:
            print(bottom)
        if show_help:
            HelpOutput.print()
        show_help = False
        line = input(": ").strip()
        if line == ABORT_INPUT_KEY_SEQUENCE:
            return old_val
        if line == EXIT_INPUT_KEY_SEQUENCE:
            return lines
        if line == DELETE_INPUT_KEY_SQEUNECE:
            lines = []
        elif line == HELP_INPUT_KEY_SEQUENCE:
            show_help = True
        else:
            sol = line.strip().split(" ")[0]
            if sol.isnumeric():
                index = int(sol) - 1
                line = line[len(sol) + 1:]
                if 0 <= index < len(lines):
                    if line == DELETE_INPUT_KEY_SQEUNECE:
                        del lines[index]
                    else:
                        lines[index] = line
            elif line != DELETE_INPUT_KEY_SQEUNECE:
                if len(lines) <= 0 or lines[-1].strip() != line.strip():
                    lines.append(line)


if __name__ == "__main__":
    def main():
        """main funktion to test the input_lib.
        """
        list_in = input_multiline()
        str_in = input("String: ")
        int_in = input_int("Integer: ")
        bool_in = input_bool("Bool: ")
        date_in = input_date("Date: ")
        choice_in = input_choice(
            "Options:",
            {
                "Opt1":  "Option 1 was choosen!",
                "Opt2":  "Option 2 was choosen!",
                "Opt3":  "Option 3 was choosen!",
                "Opt4":  "Option 4 was choosen!",
                "Opt5":  "Option 5 was choosen!",
                "Opt6":  "Option 6 was choosen!",
                "Opt7":  "Option 7 was choosen!",
                "Opt8":  "Option 8 was choosen!",
                "Opt9":  "Option 9 was choosen!",
                "Opt10": "Option 10 was choosen!",
                "Opt11": "Option 11 was choosen!",
            })
        print(f"str_in:    {str_in}")
        print(f"int_in:    {int_in}")
        print(f"bool_in:   {bool_in}")
        print(f"date_in:   {date_in}")
        print(f"choice_in: {choice_in}")
        print("---------")
        print("\n".join(list_in))
        print("---------")
    main()
