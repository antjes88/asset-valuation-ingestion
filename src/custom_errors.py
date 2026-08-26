class FileTypeNotImplementedError(Exception):

    def __init__(self, file_path: str):
        message = (
            f"FileTypeNotImplementedError. File: '{file_path}' has no extraction method"
        )

        super().__init__(message)


class FileFormatError(Exception):

    def __init__(self, file_path: str, file_format: str, expected_file_format: str):
        message = (
            f"FileFormatError. Expected '{expected_file_format}', received '{file_format}'. "
            f" File: '{file_path}' cannot be processed."
        )

        super().__init__(message)


class HeaderNotMatchError(Exception):

    def __init__(self, file_path: str, headers: str, expected_headers: str):
        message = (
            f"HeaderNotMatchError. Expected '{expected_headers}', received '{headers}'. "
            f" File: '{file_path}' cannot be processed."
        )

        super().__init__(message)
