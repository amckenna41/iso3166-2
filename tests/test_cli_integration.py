import json
import subprocess
import sys


def run_cli(args):
    cmd = [sys.executable, "-m", "iso3166_2.cli", *args]
    return subprocess.run(cmd, capture_output=True, text=True, check=False)


def test_cli_get_country_success():
    result = run_cli(["get", "DE"])
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert "DE-BE" in payload


def test_cli_search_with_filters_success():
    result = run_cli([
        "search",
        "Berlin",
        "--include-match-score",
        "--type",
        "Land",
        "--region",
        "DE",
        "--filter",
        "name,type",
    ])
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert isinstance(payload, list)
    assert payload[0]["countryCode"] == "DE"
    assert payload[0]["subdivisionCode"] == "DE-BE"
    assert payload[0]["name"] == "Berlin"


def test_cli_reverse_lookup_success():
    result = run_cli([
        "reverse",
        "52.5174",
        "13.3951",
        "--radius-km",
        "15",
        "--max-results",
        "2",
        "--region",
        "DE",
    ])
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert isinstance(payload, list)
    assert len(payload) >= 1
    assert payload[0]["subdivisionCode"] == "DE-BE"


def test_cli_get_invalid_code_has_suggestion():
    result = run_cli(["get", "UAS"])
    assert result.returncode == 1
    assert "Did you mean" in result.stderr
