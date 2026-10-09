"Namespace for the functions related to the logger."


from ._logger import get_logger
from ._wrappers import (
    wrap_internal_log,
    wrap_middle_log,
    wrap_external_log,
)