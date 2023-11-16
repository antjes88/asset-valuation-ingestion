import source_repository
import custom_errors
import pytest
from tests.data.asset_valuations import ASSET_VALUATIONS_2018


@pytest.mark.parametrize(
    "file_path, file_format",
    [
        ("my_path/my_file.xml", "xml"),
        ("my_file.xml", "xml"),
        ("my_path/my_file.csv", "csv"),
        ("my_file.csv", "csv"),
        ("my_path/my_file.txt", "txt"),
        ("my_file.txt", "txt"),
    ],
)
def test_file_format(file_path, file_format):
    """
    GIVEN file path
    WHEN an object of class file is created
    THEN the attribute file_format should return the format of the file
    """
    file = source_repository.LocalFile(file_path)

    assert file.file_format == file_format


@pytest.mark.parametrize(
    "file_path, file_type",
    [
        ("my_path/my_file.xml", "my"),
        ("assetValuation_file.xml", "assetvaluation"),
        ("my_path/assetValuation_2010_01_01.csv", "assetvaluation"),
    ],
)
def test_file_type(file_path, file_type):
    """
    GIVEN file path
    WHEN an object of class file is created
    THEN the attribute file_type should return the type of the file
    """
    file = source_repository.LocalFile(file_path)

    assert file.file_type == file_type


def test_open():
    """
    GIVEN file
    WHEN _open() method is called
    THEN it should return class to extract content of file
    """
    file = source_repository.LocalFile("tests/data/dummy.txt")
    with file._open() as f:
        content = f.read()

    assert content == "Dummy"


def test_get_asset_valuations_from_generic_source():
    """
    GIVEN a generic source file
    WHEN we call get_asset_valuations()
    THEN it should return a list of asset valuations with the expected values
    """
    file = source_repository.LocalFile("tests/data/generic_2018_12_29.csv")
    asset_valuations = file.get_asset_valuations()

    assert len(asset_valuations) == len(ASSET_VALUATIONS_2018)
    for expected_asset_valuation in ASSET_VALUATIONS_2018:
        assert expected_asset_valuation in asset_valuations


def test_error_file_type_no_implemented():
    """
    GIVEN a file type which method to extract has not been implemented
    WHEN we call get_asset_valuations()
    THEN FileTypeNotImplementedError has to be raised
    """
    file = source_repository.LocalFile(
        "tests/data/errors_check/noImplemented_2018_12_29.csv"
    )
    with pytest.raises(custom_errors.FileTypeNotImplementedError):
        file.get_asset_valuations()


def test_file_format_error_generic_file():
    """
    GIVEN a generic file which format is not csv
    WHEN we call get_asset_valuations()
    THEN FileFormatError has to be raised
    """
    file = source_repository.LocalFile(
        "tests/data/errors_check/generic_2018_12_29.json"
    )
    with pytest.raises(custom_errors.FileFormatError):
        file.get_asset_valuations()


def test_header_do_not_match_generic_file():
    """
    GIVEN a generic file which columns are not the expected ones
    WHEN we call get_asset_valuations()
    THEN HeaderNotMatchError has to be raised
    """
    file = source_repository.LocalFile("tests/data/errors_check/generic_2018_12_29.csv")
    with pytest.raises(custom_errors.HeaderNotMatchError):
        file.get_asset_valuations()
