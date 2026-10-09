"Defines the functions that generate wrappers for log messages."


from pokerpy.constants import (
    EXTERNAL_WRAPPER_CHAR,
    EXTERNAL_WRAPPER_LEFT_JUST,
    EXTERNAL_WRAPPER_LENGTH,
    INTERNAL_WRAPPER_CHAR,
    INTERNAL_WRAPPER_LEFT_JUST,
    INTERNAL_WRAPPER_LENGTH,
    MIDDLE_WRAPPER_CHAR,
    MIDDLE_WRAPPER_LEFT_JUST,
    MIDDLE_WRAPPER_LENGTH,
)


def wrap_log(
        *,
        message: str,
        wrapper_char: str,
        wrapper_length: int,
        wrapper_left_just: int,
        new_line: bool,
    ):

    "Wraps a message."

    if not message:
        wrapped_message = wrapper_char * wrapper_length

    else:
        wrapped_message = (
            f'{wrapper_char * wrapper_left_just} {message.upper()} '
            .ljust(wrapper_length, wrapper_char)
        )

    if new_line:
        wrapped_message += '\n'

    return wrapped_message


def wrap_internal_log(message: str = '', *, new_line: bool = False):

    "Wraps a message related to the most internal logs."

    return wrap_log(
        message = message,
        wrapper_char = INTERNAL_WRAPPER_CHAR,
        wrapper_length = INTERNAL_WRAPPER_LENGTH,
        wrapper_left_just = INTERNAL_WRAPPER_LEFT_JUST,
        new_line = new_line,
    )


def wrap_middle_log(message: str = '', *, new_line: bool = False):

    "Wraps a message related to the logs from the middle."

    return wrap_log(
        message = message,
        wrapper_char = MIDDLE_WRAPPER_CHAR,
        wrapper_length = MIDDLE_WRAPPER_LENGTH,
        wrapper_left_just = MIDDLE_WRAPPER_LEFT_JUST,
        new_line = new_line,
    )


def wrap_external_log(message: str = '', *, new_line: bool = False):

    "Wraps a message related to the most external logs."

    return wrap_log(
        message = message,
        wrapper_char = EXTERNAL_WRAPPER_CHAR,
        wrapper_length = EXTERNAL_WRAPPER_LENGTH,
        wrapper_left_just = EXTERNAL_WRAPPER_LEFT_JUST,
        new_line = new_line,
    )