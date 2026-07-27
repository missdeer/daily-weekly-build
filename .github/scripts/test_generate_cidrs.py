import csv
import ipaddress
import tempfile
import unittest
from pathlib import Path

import generate_cidrs


class GenerateCidrsTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        root = Path(self.temp_dir.name)
        self.locations_path = root / "locations.csv"
        self.blocks_path = root / "blocks.csv"

        with self.locations_path.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(
                stream,
                fieldnames=["geoname_id", "continent_code", "country_iso_code"],
            )
            writer.writeheader()
            writer.writerows(
                [
                    {"geoname_id": "1", "continent_code": "AS", "country_iso_code": "CN"},
                    {"geoname_id": "2", "continent_code": "AS", "country_iso_code": "IN"},
                    {"geoname_id": "3", "continent_code": "NA", "country_iso_code": "US"},
                    {"geoname_id": "4", "continent_code": "NA", "country_iso_code": "CA"},
                ]
            )

    def write_blocks(self, rows):
        with self.blocks_path.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(
                stream,
                fieldnames=[
                    "network",
                    "geoname_id",
                    "registered_country_geoname_id",
                    "represented_country_geoname_id",
                ],
            )
            writer.writeheader()
            writer.writerows(rows)

    def test_preserves_prefixes_and_excludes_selected_countries(self):
        self.write_blocks(
            [
                {
                    "network": "1.0.1.0/24",
                    "geoname_id": "1",
                    "registered_country_geoname_id": "",
                    "represented_country_geoname_id": "",
                },
                {
                    "network": "1.0.2.0/23",
                    "geoname_id": "2",
                    "registered_country_geoname_id": "",
                    "represented_country_geoname_id": "",
                },
                {
                    "network": "8.8.8.0/24",
                    "geoname_id": "",
                    "registered_country_geoname_id": "3",
                    "represented_country_geoname_id": "",
                },
                {
                    "network": "24.0.0.0/8",
                    "geoname_id": "4",
                    "registered_country_geoname_id": "",
                    "represented_country_geoname_id": "",
                },
            ]
        )

        locations = generate_cidrs.load_locations(self.locations_path)
        countries, continents = generate_cidrs.load_networks(self.blocks_path, locations)

        self.assertEqual(countries["CN"], {ipaddress.ip_network("1.0.1.0/24")})
        self.assertEqual(countries["US"], {ipaddress.ip_network("8.8.8.0/24")})
        self.assertEqual(continents["AS"], {ipaddress.ip_network("1.0.2.0/23")})
        self.assertEqual(continents["NA"], {ipaddress.ip_network("24.0.0.0/8")})

        output_path = Path(self.temp_dir.name) / "cn_cidr.txt"
        generate_cidrs.write_networks(output_path, countries["CN"])
        self.assertEqual(output_path.read_text(encoding="ascii"), "1.0.1.0/24\n")

        ipset_path = Path(self.temp_dir.name) / "cnroute.txt"
        generate_cidrs.write_networks(ipset_path, countries["CN"], "add cnroute ")
        self.assertEqual(
            ipset_path.read_text(encoding="ascii"),
            "add cnroute 1.0.1.0/24\n",
        )

    def test_rejects_non_network_addresses(self):
        self.write_blocks(
            [
                {
                    "network": "1.0.1.1/24",
                    "geoname_id": "1",
                    "registered_country_geoname_id": "",
                    "represented_country_geoname_id": "",
                }
            ]
        )

        locations = generate_cidrs.load_locations(self.locations_path)
        with self.assertRaises(ValueError):
            generate_cidrs.load_networks(self.blocks_path, locations)


if __name__ == "__main__":
    unittest.main()
