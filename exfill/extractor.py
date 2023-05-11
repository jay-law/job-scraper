"""exfill will scrape LinkedIn job postings, parse out details about
each posting, then combine all of the information into a single useable
csv file.
"""
import click
import logging
from argparse import ArgumentParser
from configparser import ConfigParser, ExtendedInterpolation
from pathlib import Path, PurePath

from parsers.parser_factory import ParserFactory
from scrapers.scraper_factory import ScraperFactory

logger = logging.getLogger(__name__)


class ConfigFileMissing(Exception):
    pass


def init_parser() -> dict:
    """Initialize argument parser."""
    parser = ArgumentParser()
    parser.add_argument("site", choices=["linkedin"], help="Site to scrape")
    parser.add_argument(
        "action", choices=["scrape", "parse"], help="Action to perform"
    )
    return vars(parser.parse_args())


def load_config(config_file: PurePath) -> ConfigParser:
    """Load config file"""

    if not Path(config_file).exists():
        raise ConfigFileMissing("Default config.ini is missing")

    config = ConfigParser(interpolation=ExtendedInterpolation())
    config.read(config_file)

    return config


def create_dirs(config: ConfigParser) -> None:
    """Create directories referenced in the config file"""
    for dir_path in config.items("Directories"):
        Path.mkdir(Path.cwd() / dir_path[1], exist_ok=True)


@click.group
@click.option("-c", "--config", "config_file", type=str, required=True)
@click.option("-s", "--site", "site", type=str, required=True)
@click.pass_context
def main(ctx, config_file, site) -> None:
    ctx.ensure_object(dict)
    ctx.obj["config"] = load_config(config_file)
    ctx.obj["site"] = site

    logging.basicConfig(
        # filename="extractor.log",
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] - %(message)s",
        # filemode="w+",
    )


@main.command()
@click.pass_context
def scrape(ctx):
    site = ctx.obj["site"]
    logger.info(f"Scraping {site}")
    scraper = ScraperFactory.create(site, config=ctx.obj["config"])
    scraper.scrape_postings(200)


@main.command()
@click.pass_context
def parse(ctx):
    site = ctx.obj["site"]
    logger.info(f"Parsing {site}")
    parser = ParserFactory.create(site, config=ctx.obj["config"])
    parser.parse_postings()


if __name__ == "__main__":
    main()
