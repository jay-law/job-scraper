import pytest
from bs4 import BeautifulSoup

from exfill.parsers.linkedin_parser import InvalidFileName

bad_sip = "no soup for you"  # returns 'error'
empty_sip = BeautifulSoup("", "html.parser")  # returns 'missing'


def test_load_posting_jobid(create_parser):
    # config = load_config
    # parser = LinkedinParser(config)
    parser = create_parser

    good_file = "jobid_3080721373_20220516_180204.html"
    jobid = parser.load_posting_jobid(good_file)

    assert jobid == "3080721373"
    assert isinstance(jobid, str)

    with pytest.raises(TypeError):
        parser.load_posting_jobid()

    with pytest.raises(Exception, match="list index out of range") as exc_info:
        parser.load_posting_jobid("")
    assert exc_info.type == InvalidFileName

    with pytest.raises(Exception, match="list index out of range") as exc_info:
        parser.load_posting_jobid("nounderscores")
    assert exc_info.type == InvalidFileName


def test_load_posting_url(create_parser):
    parser = create_parser
    url = parser.load_posting_url("3080721373")

    assert "https://www.linkedin.com/jobs/view/3080721373" == url
    assert isinstance(url, str)

    with pytest.raises(TypeError):
        parser.load_posting_url()


def test_load_posting_title(create_parser):
    parser = create_parser
    good_sip = BeautifulSoup(
        ('<h2 class="t-24 t-bold">' "Senior DevOps Engineer" "</h2>"),
        "html.parser",
    )
    title = parser.load_posting_title(good_sip)

    assert "Senior DevOps Engineer" == title
    assert isinstance(title, str)

    with pytest.raises(TypeError):
        parser.load_posting_title()

    assert "missing" == parser.load_posting_title(empty_sip)
    assert "error" == parser.load_posting_title(bad_sip)


def test_load_posting_workplace_type(create_parser):
    parser = create_parser
    good_sip = BeautifulSoup(
        (
            '<span class="jobs-unified-top-card__workplace-type">'
            "Remote"
            "</span>"
        ),
        "html.parser",
    )
    workplace_type = parser.load_posting_workplace_type(good_sip)

    assert "Remote" == workplace_type
    assert isinstance(workplace_type, str)

    with pytest.raises(TypeError):
        parser.load_posting_workplace_type()

    assert "missing" == parser.load_posting_workplace_type(empty_sip)
    assert "error" == parser.load_posting_workplace_type(bad_sip)
