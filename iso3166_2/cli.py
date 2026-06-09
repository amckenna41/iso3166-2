"""Command-line interface for the iso3166-2 package."""
import argparse
import dataclasses
import json
import sys
from typing import Any


def _serialise(obj) -> object:
    """Return a JSON-serialisable representation of a Subdivisions query result."""
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        return dataclasses.asdict(obj)
    # CountrySubdivisions and plain dicts are already serialisable
    return obj


def _print_json(obj: Any) -> None:
    print(json.dumps(_serialise(obj), ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="iso3166-2",
        description="Query ISO 3166-2 subdivision data from the command line.",
    )
    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")

    # --- get: iso3166-2 get US  OR  iso3166-2 get US-CA ---
    get_parser = subparsers.add_parser(
        "get",
        help="Get subdivision data for a country code or subdivision code.",
    )
    get_parser.add_argument(
        "code",
        help=(
            "ISO 3166-1 alpha-2/alpha-3/numeric country code or an ISO 3166-2 "
            "subdivision code (e.g. US, GBR, 840, US-CA). "
            "Comma-separated lists are accepted for country codes."
        ),
    )
    get_parser.add_argument(
        "--filter",
        metavar="ATTRS",
        dest="filter_attributes",
        default="",
        help="Comma-separated list of attributes to include (e.g. name,type,latLng).",
    )

    # --- search: iso3166-2 search "California" ---
    search_parser = subparsers.add_parser(
        "search",
        help="Search for subdivisions by name.",
    )
    search_parser.add_argument(
        "name",
        help="Subdivision name (or comma-separated names) to search for.",
    )
    search_parser.add_argument(
        "--likeness",
        type=int,
        default=100,
        metavar="SCORE",
        help="Likeness score threshold 1-100 (default: 100).",
    )
    search_parser.add_argument(
        "--local-names",
        action="store_true",
        help="Include the localOtherName attribute in the search space.",
    )
    search_parser.add_argument(
        "--filter",
        metavar="ATTRS",
        dest="filter_attributes",
        default="",
        help="Comma-separated list of attributes to include (e.g. name,type,latLng).",
    )
    search_parser.add_argument(
        "--type",
        dest="subdivision_type",
        default="",
        help="Filter search results by subdivision type (e.g. State, Region, Canton).",
    )
    search_parser.add_argument(
        "--parent",
        dest="parent_code",
        default="",
        help="Filter search results by parent subdivision code (e.g. GB-ENG).",
    )
    search_parser.add_argument(
        "--region",
        dest="region",
        default="",
        help="Filter search results by country/region (alpha-2, alpha-3, numeric, or country name).",
    )
    search_parser.add_argument(
        "--include-match-score",
        action="store_true",
        help="Include matchScore and return results ranked by relevance.",
    )

    # --- codes: iso3166-2 codes US ---
    codes_parser = subparsers.add_parser(
        "codes",
        help="List all subdivision codes for one or more countries.",
    )
    codes_parser.add_argument(
        "code",
        help="ISO 3166-1 country code(s), comma-separated.",
    )

    # --- names: iso3166-2 names US ---
    names_parser = subparsers.add_parser(
        "names",
        help="List all subdivision names for one or more countries.",
    )
    names_parser.add_argument(
        "code",
        help="ISO 3166-1 country code(s), comma-separated.",
    )

    # --- reverse: iso3166-2 reverse 40.7128 -74.0060 ---
    reverse_parser = subparsers.add_parser(
        "reverse",
        help="Find nearby subdivisions from latitude and longitude.",
    )
    reverse_parser.add_argument("latitude", type=float, help="Latitude in decimal degrees.")
    reverse_parser.add_argument("longitude", type=float, help="Longitude in decimal degrees.")
    reverse_parser.add_argument(
        "--radius-km",
        type=float,
        default=50.0,
        help="Search radius in kilometers (default: 50.0).",
    )
    reverse_parser.add_argument(
        "--max-results",
        type=int,
        default=10,
        help="Maximum number of results (default: 10).",
    )
    reverse_parser.add_argument(
        "--filter",
        metavar="ATTRS",
        dest="filter_attributes",
        default="",
        help="Comma-separated list of attributes to include (e.g. name,type,latLng).",
    )
    reverse_parser.add_argument(
        "--region",
        dest="region",
        default="",
        help="Restrict lookup to one region/country (alpha-2, alpha-3, numeric, or name).",
    )

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    # Lazy import so startup is fast and import errors surface as clean messages
    try:
        from iso3166_2 import (
            Subdivisions,
            ISO3166Error,
        )
    except ImportError as exc:
        print(f"Error: could not import iso3166-2 — {exc}", file=sys.stderr)
        sys.exit(1)

    if args.command == "get":
        iso = Subdivisions(filter_attributes=args.filter_attributes)
        try:
            result = iso[args.code]
        except (ISO3166Error, KeyError, ValueError, TypeError) as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)
        _print_json(result)

    elif args.command == "search":
        iso = Subdivisions()
        try:
            result = iso.search(
                args.name,
                likeness_score=args.likeness,
                filter_attribute=args.filter_attributes,
                local_other_name_search=args.local_names,
                exclude_match_score=not args.include_match_score,
                subdivision_type=args.subdivision_type,
                parent_code=args.parent_code,
                region=args.region,
            )
        except (ISO3166Error, KeyError, ValueError, TypeError) as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)
        _print_json(result)

    elif args.command == "codes":
        iso = Subdivisions()
        try:
            result = iso.subdivision_codes(args.code)
        except (ISO3166Error, KeyError, ValueError, TypeError) as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)
        _print_json(result)

    elif args.command == "names":
        iso = Subdivisions()
        try:
            result = iso.subdivision_names(args.code)
        except (ISO3166Error, KeyError, ValueError, TypeError) as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)
        _print_json(result)

    elif args.command == "reverse":
        iso = Subdivisions()
        try:
            result = iso.reverse_lookup(
                args.latitude,
                args.longitude,
                radius_km=args.radius_km,
                max_results=args.max_results,
                filter_attribute=args.filter_attributes,
                region=args.region,
            )
        except (ISO3166Error, KeyError, ValueError, TypeError) as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)
        _print_json(result)


if __name__ == "__main__":
    main()
