#!/usr/bin/env python3

import argparse
import csv
import ipaddress
from collections import defaultdict
from pathlib import Path


COUNTRY_CODES = {
    "CN",
    "DE",
    "ES",
    "FR",
    "GB",
    "HK",
    "IT",
    "JP",
    "KR",
    "NL",
    "RU",
    "SE",
    "SG",
    "TW",
    "US",
}

CONTINENT_EXCLUSIONS = {
    "AF": set(),
    "AS": {"CN", "HK", "JP", "KR", "SG", "TW"},
    "EU": {"DE", "ES", "FR", "GB", "IT", "NL", "RU", "SE"},
    "NA": {"US"},
    "OC": set(),
    "SA": set(),
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate validated IPv4 CIDR lists from MaxMind GeoLite2 CSV files."
    )
    parser.add_argument("locations", type=Path)
    parser.add_argument("blocks", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument(
        "--output-format",
        choices=("cidr", "ipset"),
        default="cidr",
    )
    return parser.parse_args()


def load_locations(path):
    locations = {}
    with path.open(newline="", encoding="utf-8-sig") as stream:
        for row in csv.DictReader(stream):
            geoname_id = row["geoname_id"]
            if geoname_id:
                locations[geoname_id] = (
                    row["country_iso_code"],
                    row["continent_code"],
                )
    return locations


def resolve_location(row, locations):
    for field in (
        "geoname_id",
        "registered_country_geoname_id",
        "represented_country_geoname_id",
    ):
        location = locations.get(row[field])
        if location is not None:
            return location
    return None


def load_networks(path, locations):
    country_networks = defaultdict(set)
    continent_networks = defaultdict(set)

    with path.open(newline="", encoding="utf-8-sig") as stream:
        for row in csv.DictReader(stream):
            location = resolve_location(row, locations)
            if location is None:
                continue

            network = ipaddress.ip_network(row["network"], strict=True)
            if network.version != 4:
                raise ValueError(f"expected an IPv4 network, got {network}")

            country_code, continent_code = location
            if country_code in COUNTRY_CODES:
                country_networks[country_code].add(network)
            if (
                continent_code in CONTINENT_EXCLUSIONS
                and country_code not in CONTINENT_EXCLUSIONS[continent_code]
            ):
                continent_networks[continent_code].add(network)

    return country_networks, continent_networks


def write_networks(path, networks, line_prefix=""):
    if not networks:
        raise ValueError(f"refusing to write empty CIDR list: {path.name}")

    ordered = sorted(
        networks,
        key=lambda network: (int(network.network_address), network.prefixlen),
    )
    path.write_text(
        "".join(f"{line_prefix}{network}\n" for network in ordered),
        encoding="ascii",
    )
    print(f"{path.name}: {len(ordered)} networks")


def main():
    args = parse_args()
    locations = load_locations(args.locations)
    if not locations:
        raise ValueError("the locations CSV did not contain any GeoName IDs")

    country_networks, continent_networks = load_networks(args.blocks, locations)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    network_groups = {
        **{code: country_networks[code] for code in COUNTRY_CODES},
        **{code: continent_networks[code] for code in CONTINENT_EXCLUSIONS},
    }
    for code in sorted(network_groups):
        if args.output_format == "ipset":
            name = f"{code.lower()}route"
            write_networks(
                args.output_dir / f"{name}.txt",
                network_groups[code],
                line_prefix=f"add {name} ",
            )
        else:
            write_networks(
                args.output_dir / f"{code.lower()}_cidr.txt",
                network_groups[code],
            )


if __name__ == "__main__":
    main()
