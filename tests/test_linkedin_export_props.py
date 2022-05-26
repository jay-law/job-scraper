import pytest

from exfill.parsers.linkedin_parser import InvalidFileName, LinkedinParser


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
