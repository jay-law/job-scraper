"""
Contains functions to test the following 'export properties' in the
LinkedinParser class:
- jobid
- url
- title
- company_name
- workplace_type
- company_url
- company_industry
- hours
- level

Except for 'jobid' and 'url', each prop has a loader method that parses
a BeautifulSoup object.  The tests below use different 'sips' to
represent BeautifulSoup objects.  Each sip should ideally return the same
response (either 'missing' or 'error').

These sips are unique to each method and are set in each test def:
- good_sip - returns desired value
- dirty_sip - Should return 'missing' but might return 'error'
    - Used to test sip that require chained find() or attribute
    access like find("a")["href"]

These sips are generic and are globally available:
- bad_sip - returns 'error'
- empty_sip - returns 'missing'

Caught exceptions:
- AttributeError - Occurs on find().  Returns 'missing'
    - all methods - Thrown with first or second find()
- KeyError - Occurs on attribut access.  Returns 'missing'
    - load_posting_company_url() - ["href"]
"""

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


def test_load_posting_company_name(create_parser):
    parser = create_parser
    good_sip = BeautifulSoup(
        (
            '<span class="jobs-unified-top-card__company-name">'
            '<a class="ember-view t-black t-normal"'
            'href="/company/sap/life/" id="ember146">'
            "SAP"
            "</a>"
            "</span>"
        ),
        "html.parser",
    )
    company_name = parser.load_posting_company_name(good_sip)

    assert "SAP" == company_name
    assert isinstance(company_name, str)

    with pytest.raises(TypeError):
        parser.load_posting_company_name()

    assert "missing" == parser.load_posting_company_name(empty_sip)
    assert "error" == parser.load_posting_company_name(bad_sip)

    dirty_sip = BeautifulSoup(
        ('<span class="jobs-unified-top-card__company-name">' "</span>"),
        "html.parser",
    )
    assert "missing" == parser.load_posting_company_name(dirty_sip)


def test_load_posting_company_url(create_parser):
    parser = create_parser
    good_sip = BeautifulSoup(
        (
            '<span class="jobs-unified-top-card__company-name">'
            '<a class="ember-view t-black t-normal"'
            'href="/company/sap/life/" id="ember146">'
            "SAP"
            "</a>"
            "</span>"
        ),
        "html.parser",
    )
    url = parser.load_posting_company_url(good_sip)
    assert "/company/sap/life/" == url
    assert isinstance(url, str)

    with pytest.raises(TypeError):
        parser.load_posting_company_url()

    assert "missing" == parser.load_posting_company_url(empty_sip)
    assert "error" == parser.load_posting_company_url(bad_sip)

    # Throws KeyError as the anchor tag exists but not the href attr
    dirty_sip = BeautifulSoup(
        (
            '<span class="jobs-unified-top-card__company-name">'
            '<a class="ember-view t-black t-normal"'
            "</a>"
            "</span>"
        ),
        "html.parser",
    )
    assert "missing" == parser.load_posting_company_url(dirty_sip)

    # Throws TypeError - should ideally return 'missing'
    dirty_sip = BeautifulSoup(
        ('<span class="jobs-unified-top-card__company-name">' "</span>"),
        "html.parser",
    )
    assert "error" == parser.load_posting_company_url(dirty_sip)


def test_load_posting_company_details(create_parser):
    parser = create_parser
    good_sip = BeautifulSoup(
        (
            "<span>"
            '<a class="app-aware-link" href="#SALARY" target="_self">'
            "<!-- -->"
            "$80,000/yr - $125,000/yr"
            "<!-- -->"
            "</a>"
            '<span class="white-space-pre">'
            "</span>"
            " · Full-time · Mid-Senior level"
            "<!-- -->"
            "</span>"
            "<span>"
            "<!-- -->"
            "51-200 employees · Internet Publishing "
            "<!-- -->"
            "</span>"
        ),
        "html.parser",
    )
    (
        company_size,
        company_industry,
        hours,
        level,
    ) = parser.load_posting_company_details(good_sip)

    assert "51-200 employees" == company_size
    assert "Internet Publishing" == company_industry
    assert "Full-time" == hours
    assert "Mid-Senior level" == level

    assert isinstance(company_size, str)
    assert isinstance(company_industry, str)
    assert isinstance(hours, str)
    assert isinstance(level, str)

    with pytest.raises(TypeError):
        parser.load_posting_company_details()

    assert (
        "missing",
        "missing",
        "missing",
        "missing",
    ) == parser.load_posting_company_details(empty_sip)

    assert (
        "error",
        "error",
        "error",
        "error",
    ) == parser.load_posting_company_details(bad_sip)

    dirty_sip = BeautifulSoup(" · one  · two  · three  · ", "html.parser")
    assert (
        "missing",
        "missing",
        "missing",
        "missing",
    ) == parser.load_posting_company_details(dirty_sip)
