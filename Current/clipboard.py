import pyperclip

def get_clipboard_content():
    """
    Get the current content of the clipboard.
    """
    return pyperclip.paste()

def set_clipboard_content(content):
    """
    Set the content of the clipboard to the specified value.
    """
    pyperclip.copy(content)
