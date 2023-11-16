class FileTypeNotImplementedError(Exception):
    """
    Implementation of Exception to be raised when method to extract data from a file type is not implemented

    Args:
        file_path (str): The path to the file.
    Attributes:
        message (str): message to be print on error.
    """
    def __init__(self, file_path: str):
        self.message = f"FileTypeNotImplementedError. File: '{file_path}' has no extraction method"

    def __str__(self):
        return self.message


class FileFormatError(Exception):
    """
    Implementation of Exception to be raised when format of file is not valid for extraction method

    Args:
        file_path (str): The path to the file.
        file_format (str): The format of the file, extracted from the file extension.
        expected_file_format (str): The format expected for the extraction method.
    Attributes:
        message (str): message to be print on error.
    """
    def __init__(self, file_path: str, file_format: str, expected_file_format: str):
        self.message = (f"FileFormatError. Expected '{expected_file_format}', received '{file_format}'. "
                        f" File: '{file_path}' cannot be processed.")

    def __str__(self):
        return self.message


class HeaderNotMatchError(Exception):
    """
    Implementation of Exception to be raised when headers of a source file do not match expected headers

    Args:
        file_path (str): The path to the file.
        headers (str): string containing all headers of source file
        expected_headers (str): string containing expected headers
    Attributes:
        message (str): message to be print on error.
    """
    def __init__(self, file_path: str, headers: str, expected_headers: str):
        self.message = (f"HeaderNotMatchError. Expected '{expected_headers}', received '{headers}'. "
                        f" File: '{file_path}' cannot be processed.")

    def __str__(self):
        return self.message
