from pathlib import Path

import pytest


def test_load_posting_input_file(create_parser):
    parser = create_parser

    input_dir = Path("/some/dir")
    input_file_name = Path("some_file.html")
    input_file = parser.load_posting_input_file(input_dir, input_file_name)

    assert input_file == Path("/some/dir/some_file.html")
    assert isinstance(input_file, Path)

    with pytest.raises(TypeError):
        parser.load_posting_input_file()

    with pytest.raises(TypeError):
        parser.load_posting_input_file("/some/dir", "some_file.html")


# def test_load_posting_soup(create_parser):
#     parser = create_parser
