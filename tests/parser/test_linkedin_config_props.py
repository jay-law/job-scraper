from pathlib import Path

import pytest
from bs4 import BeautifulSoup


def test_load_posting_input_file(create_parser, data_dir):
    parser = create_parser
    input_dir = data_dir / "html"
    input_dir.mkdir()

    input_file_name = Path("jobid_1234567890_20220101_123456.html")
    input_file = parser.load_posting_input_file(input_dir, input_file_name)

    assert input_file == input_dir / input_file_name
    assert isinstance(input_file, Path)

    with pytest.raises(TypeError):
        parser.load_posting_input_file()

    with pytest.raises(TypeError):
        parser.load_posting_input_file("/some/dir", "some_file.html")


def test_load_posting_soup(create_parser, data_dir):
    parser = create_parser
    html_dir = data_dir / "html"
    html_dir.mkdir()

    input_file = html_dir / "jobid_1234567890_20220101_123456.html"

    html_string = "<div>hello</div>"
    with open(input_file, "x") as f:
        f.write(html_string)

    soup = parser.load_posting_soup(input_file)
    assert isinstance(soup, BeautifulSoup)

    with pytest.raises(TypeError):
        parser.load_posting_soup()

    # there was a OSError exception but I cannot recreate it

    with pytest.raises(FileNotFoundError):
        parser.load_posting_soup(Path("/some/dir/some_file.html"))

    with pytest.raises(FileNotFoundError):
        parser.load_posting_soup(Path("/some/dir/"))
