"""
Unit tests for country, state, and city resolution and filtering.
"""
from leadgen.geo import (normalize_country, normalize_state, resolve_market_details,
                         MARKETS)
from leadgen.pipeline import (_matches_country, _matches_state, _matches_city,
                              ensure_location_columns, run_pipeline)
from leadgen import get_vertical


def test_normalize_country():
    assert normalize_country("Canada") == ("CA", "Canada")
    assert normalize_country("CA") == ("CA", "Canada")
    assert normalize_country("can") == ("CA", "Canada")
    assert normalize_country("United States") == ("US", "United States")
    assert normalize_country("USA") == ("US", "United States")
    assert normalize_country("U.S.A.") == ("US", "United States")
    assert normalize_country("United Kingdom") == ("GB", "United Kingdom")
    assert normalize_country("UK") == ("GB", "United Kingdom")
    assert normalize_country("Germany") == ("DE", "Germany")
    assert normalize_country("Australia") == ("AU", "Australia")
    assert normalize_country("India") == ("IN", "India")
    assert normalize_country("Pakistan") == ("PK", "Pakistan")


def test_normalize_state():
    assert normalize_state("Texas", "US") == "TX"
    assert normalize_state("tx", "US") == "TX"
    assert normalize_state("Ontario", "CA") == "ON"
    assert normalize_state("on", "CA") == "ON"
    assert normalize_state("New South Wales", "AU") == "NSW"


def test_location_matchers():
    assert _matches_country("CA", "Canada") is True
    assert _matches_country("Canada", "CA") is True
    assert _matches_country("US", "Canada") is False
    assert _matches_country("US", "United States") is True

    assert _matches_state("TX", "Texas") is True
    assert _matches_state("Texas", "TX") is True
    assert _matches_state("ON", "Ontario") is True
    assert _matches_state("CA", "Texas") is False

    assert _matches_city("Austin", "austin") is True
    assert _matches_city("Toronto", "toronto") is True
    assert _matches_city("Boulder", "Austin") is False


def test_ensure_location_columns():
    cols = [("Business", "name"), ("City", "city"), ("Phone", "phone")]
    updated = ensure_location_columns(cols)
    keys = [k for _, k in updated]
    assert keys == ["name", "city", "state", "country", "phone"]


def test_demo_location_filters():
    v = get_vertical("web_design")
    
    # All 5 demo records are US
    all_demo = run_pipeline(v, "(demo)", demo=True)
    assert len(all_demo) == 5

    # Filter by city
    boulder_leads = run_pipeline(v, "(demo)", demo=True, city="Boulder")
    assert len(boulder_leads) == 2
    assert all(r["city"] == "Boulder" for r in boulder_leads)

    # Filter by state
    tx_leads = run_pipeline(v, "(demo)", demo=True, state="TX")
    assert len(tx_leads) == 1
    assert tx_leads[0]["city"] == "Austin"

    # Filter by country
    us_leads = run_pipeline(v, "(demo)", demo=True, country="United States")
    assert len(us_leads) == 5

    # Non-matching country filter
    ca_leads = run_pipeline(v, "(demo)", demo=True, country="Canada")
    assert len(ca_leads) == 0


def test_resolve_market_predefined():
    bbox, label, info = resolve_market_details("austin_tx")
    assert bbox == MARKETS["austin_tx"]
    assert info["country_code"] == "US"
    assert info["state"] == "TX"
    assert info["city"] == "Austin"

    bbox_to, label_to, info_to = resolve_market_details("toronto_on")
    assert bbox_to == MARKETS["toronto_on"]
    assert info_to["country_code"] == "CA"
    assert info_to["state"] == "ON"
