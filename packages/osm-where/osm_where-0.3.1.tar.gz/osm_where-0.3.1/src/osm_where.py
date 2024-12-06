#!/usr/bin/env python3
import argparse
import urllib.parse

import xdg.BaseDirectory

from OSMPythonTools.cachingStrategy import CachingStrategy, JSON
from OSMPythonTools.api import Api
from OSMPythonTools.overpass import Overpass

from shapely.geometry import shape

CachingStrategy.use(JSON, cacheDir=xdg.BaseDirectory.save_cache_path("osm_where"))

import logging

logging.getLogger("OSMPythonTools").setLevel(logging.ERROR)

__version__ = '0.3.1'

def parse_name(name, area, lang):
    overpass = Overpass()

    result = overpass.query(
        f'area["ISO3166-1"="{area}"][admin_level=2];relation["name:{lang}"="{name}"](area);out center;'
    )
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

    if all((parse_url.scheme, parse_url.netloc)):
        geo = parse_URL(parse_url)
    else:
        geo = parse_name(args.url, args.area, args.lang)

    if geo:
        print(f"geo:{geo[0]:.7f},{geo[1]:.7f}")


if __name__ == "__main__":
    main()
