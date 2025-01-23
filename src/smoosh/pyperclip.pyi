from typing import Optional

# Main clipboard functions
def copy(text: str) -> None: ...
def paste() -> str: ...
def waitForPaste(timeout: Optional[float] = None) -> str: ...
def waitForNewPaste(timeout: Optional[float] = None) -> str: ...

# Clipboard handling functions
def init_osx_pbcopy_clipboard() -> None: ...
def init_osx_pyobjc_clipboard() -> None: ...
def init_dev_clipboard_clipboard() -> None: ...
def init_gtk_clipboard() -> None: ...
def init_qt_clipboard() -> None: ...
def init_xclip_clipboard() -> None: ...
def init_xsel_clipboard() -> None: ...
def init_klipper_clipboard() -> None: ...
def init_no_clipboard() -> None: ...

# Exceptions
class PyperclipException(RuntimeError): ...
class PyperclipWindowsException(PyperclipException): ...

# Constants
EXCEPT_MSG: str
ENCODING: str

# Determine clipboard
def determine_clipboard() -> None: ...

# Check platform support
def is_available() -> bool: ...

# Get primary selection (X11)
def get_primary_selection() -> Optional[str]: ...
def set_primary_selection(text: str) -> None: ...

# Internal helpers
def _executable_exists(name: str) -> bool: ...
def _stringifyText(text: str) -> str: ...
