import inspect
import sys
import traceback


def goto(line: int) -> None:
    """Make a jump to a specific line in the source code of the same file.

    Args:
        line (int): The line number to jump to.
    """

    # Get source and verify line number
    module = sys.modules["__main__"]
    source_lines, _ = inspect.getsourcelines(module)
    assert 0 <= line <= len(source_lines), f"{line} out of range"

    # Extract any methods defined before line
    scope = []
    for idx, source_line in enumerate(source_lines[:line]):
        if source_line.startswith("def "):
            scope.append(source_line)
            while source_lines[idx + 1].startswith(" "):
                idx += 1
                scope.append(source_lines[idx])

    # Adjust indentation level
    source_lines = source_lines[line - 1 :]
    first_indentation_level = len(source_lines[0]) - len(source_lines[0].lstrip())
    for index, source_line in enumerate(source_lines):
        indentation_level = len(source_line) - len(source_line.lstrip())
        if indentation_level == 0:
            break
        indentation_start = min(indentation_level, first_indentation_level)
        source_lines[index] = source_lines[index][indentation_start:]

    # Get any local variables from the previous stackframe
    last_frame_locals = inspect.stack()[1].frame.f_locals

    # Assemble source and goto!
    source_code = "".join(scope + source_lines)
    exec(source_code, module.__dict__, last_frame_locals)
    sys.exit(0)
