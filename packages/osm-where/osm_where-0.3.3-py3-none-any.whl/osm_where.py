#!/usr/bin/env python3
import argparse
import logging
import urllib.parse

import xdg.BaseDirectory

from OSMPythonTools.cachingStrategy import CachingStrategy, JSON
from OSMPythonTools.api import Api
from OSMPythonTools.overpass import Overpass

from shapely.geometry import shape

CachingStrategy.use(JSON, cacheDir=xdg.BaseDirectory.save_cache_path("osm_where"))

import logging

logging.basicConfig(
    format="%(levelname)s:%(funcName)s:%(message)s", level=logging.ERROR
)
log = logging.getLogger()

__version__ = "0.3.3"


def parse_name(name, area, lang):
    overpass = Overpass()

    query_str = f'area["name:{lang}"="{name}"]; out center;'
    log.debug("query_str = %s", query_str)

    result = overpass.query(query_str)
    if len(result.elements()) > 0:
        bakhmut = result.elements()[0]
        return bakhmut.centerLat(), bakhmut.centerLon()
    else:
        return None


def parse_URL(url):
    api = Api()

    way = api.query(url.path)
    geom = shape(way.geometry())
    return geom.centroid.y, geom.centroid.x


def main():
    parser = argparse.ArgumentParser(
        prog="osm_where", description="Get geo: URI for given locality from OSM"
    )
    parser.add_argument("url", nargs="?", help="researched location")
    parser.add_argument("-a", "--area", default="UA", help="ISO 3166 area code")
    parser.add_argument("-l", "--lang", default="en", help="ISO 639-1 language code")
    args = parser.parse_args()

    parse_url = urllib.parse.urlparse(args.url)
    logging.debug("parse_url = %s", parse_url)

    if all((parse_url.scheme, parse_url.netloc)):
        geo = parse_URL(parse_url)
    else:
        geo = parse_name(args.url, args.area, args.lang)

    log.debug("geo = %s", geo)
    if geo != (None, None):
        print(f"geo:{geo[0]:.7f},{geo[1]:.7f}")


if __name__ == "__main__":
    main()
