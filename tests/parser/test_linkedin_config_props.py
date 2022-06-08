from pathlib import Path

import pytest
from bs4 import BeautifulSoup


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


def test_load_posting_soup(create_parser):
    parser = create_parser

    # fix later
    input_file = (
        Path.cwd().__str__()
        + "/data/html/jobid_3080882196_20220608_131434.html"
    )

    soup = parser.load_posting_soup(input_file)
    assert isinstance(soup, BeautifulSoup)

    with pytest.raises(TypeError):
        parser.load_posting_soup()

    # there was a OSError exception but I cannot recreate it

    with pytest.raises(FileNotFoundError):
        parser.load_posting_soup(Path("/some/dir/some_file.html"))

    with pytest.raises(FileNotFoundError):
        parser.load_posting_soup(Path("/some/dir/"))
