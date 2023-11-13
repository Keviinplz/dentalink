from datetime import datetime

import pytest

from dentalink.exceptions import (
    DentalinkClientQueryError,
)
from dentalink.query import DentalinkQueryFactory


def test_dentalink_query_factory_initialization():
    with pytest.raises(DentalinkClientQueryError):
        DentalinkQueryFactory().parse()

    assert DentalinkQueryFactory("foo").parse() == {}


def test_error_when_attempt_to_add_filter_without_field_setted():
    with pytest.raises(DentalinkClientQueryError):
        DentalinkQueryFactory().eq(1)


def test_eq_filter():
    assert DentalinkQueryFactory().field("foo").parse() == {}
    assert DentalinkQueryFactory().field("foo").eq(1).parse() == {"foo": {"eq": "1"}}
    assert DentalinkQueryFactory().field("foo").eq(True).parse() == {"foo": {"eq": "1"}}
    assert DentalinkQueryFactory().field("foo").eq(False).parse() == {
        "foo": {"eq": "0"}
    }
    assert DentalinkQueryFactory().field("foo").eq("bar").parse() == {
        "foo": {"eq": "bar"}
    }
    assert DentalinkQueryFactory().field("foo").eq(datetime(2022, 1, 1)).parse() == {
        "foo": {"eq": "2022-01-01"}
    }
    assert DentalinkQueryFactory().field("foo").eq(
        datetime(2022, 1, 1), dt_format="%Y-%m-%d %H:%M:%S"
    ).parse() == {"foo": {"eq": "2022-01-01 00:00:00"}}
    assert DentalinkQueryFactory().field("foo").eq(1).eq(2).parse() == {
        "foo": [{"eq": "1"}, {"eq": "2"}]
    }


def test_neq_filter():
    assert DentalinkQueryFactory().field("foo").parse() == {}
    assert DentalinkQueryFactory().field("foo").neq(1).parse() == {"foo": {"neq": "1"}}
    assert DentalinkQueryFactory().field("foo").neq(True).parse() == {
        "foo": {"neq": "1"}
    }
    assert DentalinkQueryFactory().field("foo").neq(False).parse() == {
        "foo": {"neq": "0"}
    }
    assert DentalinkQueryFactory().field("foo").neq("bar").parse() == {
        "foo": {"neq": "bar"}
    }
    assert DentalinkQueryFactory().field("foo").neq(datetime(2022, 1, 1)).parse() == {
        "foo": {"neq": "2022-01-01"}
    }
    assert DentalinkQueryFactory().field("foo").neq(
        datetime(2022, 1, 1), dt_format="%Y-%m-%d %H:%M:%S"
    ).parse() == {"foo": {"neq": "2022-01-01 00:00:00"}}
    assert DentalinkQueryFactory().field("foo").neq(1).neq(2).parse() == {
        "foo": [{"neq": "1"}, {"neq": "2"}]
    }


def test_gt_filter():
    assert DentalinkQueryFactory().field("foo").parse() == {}
    assert DentalinkQueryFactory().field("foo").gt(1).parse() == {"foo": {"gt": "1"}}
    assert DentalinkQueryFactory().field("foo").gt(True).parse() == {"foo": {"gt": "1"}}
    assert DentalinkQueryFactory().field("foo").gt(False).parse() == {
        "foo": {"gt": "0"}
    }
    assert DentalinkQueryFactory().field("foo").gt(datetime(2022, 1, 1)).parse() == {
        "foo": {"gt": "2022-01-01"}
    }
    assert DentalinkQueryFactory().field("foo").gt(
        datetime(2022, 1, 1), dt_format="%Y-%m-%d %H:%M:%S"
    ).parse() == {"foo": {"gt": "2022-01-01 00:00:00"}}
    assert DentalinkQueryFactory().field("foo").gt(1).gt(2).parse() == {
        "foo": [{"gt": "1"}, {"gt": "2"}]
    }


def test_gte_filter():
    assert DentalinkQueryFactory().field("foo").parse() == {}
    assert DentalinkQueryFactory().field("foo").gte(1).parse() == {"foo": {"gte": "1"}}
    assert DentalinkQueryFactory().field("foo").gte(True).parse() == {
        "foo": {"gte": "1"}
    }
    assert DentalinkQueryFactory().field("foo").gte(False).parse() == {
        "foo": {"gte": "0"}
    }
    assert DentalinkQueryFactory().field("foo").gte(datetime(2022, 1, 1)).parse() == {
        "foo": {"gte": "2022-01-01"}
    }
    assert DentalinkQueryFactory().field("foo").gte(
        datetime(2022, 1, 1), dt_format="%Y-%m-%d %H:%M:%S"
    ).parse() == {"foo": {"gte": "2022-01-01 00:00:00"}}
    assert DentalinkQueryFactory().field("foo").gte(1).gte(2).parse() == {
        "foo": [{"gte": "1"}, {"gte": "2"}]
    }


def test_lt_filter():
    assert DentalinkQueryFactory().field("foo").parse() == {}
    assert DentalinkQueryFactory().field("foo").lt(1).parse() == {"foo": {"lt": "1"}}
    assert DentalinkQueryFactory().field("foo").lt(True).parse() == {"foo": {"lt": "1"}}
    assert DentalinkQueryFactory().field("foo").lt(False).parse() == {
        "foo": {"lt": "0"}
    }
    assert DentalinkQueryFactory().field("foo").lt(datetime(2022, 1, 1)).parse() == {
        "foo": {"lt": "2022-01-01"}
    }
    assert DentalinkQueryFactory().field("foo").lt(
        datetime(2022, 1, 1), dt_format="%Y-%m-%d %H:%M:%S"
    ).parse() == {"foo": {"lt": "2022-01-01 00:00:00"}}
    assert DentalinkQueryFactory().field("foo").lt(1).lt(2).parse() == {
        "foo": [{"lt": "1"}, {"lt": "2"}]
    }


def test_lte_filter():
    assert DentalinkQueryFactory().field("foo").parse() == {}
    assert DentalinkQueryFactory().field("foo").lte(1).parse() == {"foo": {"lte": "1"}}
    assert DentalinkQueryFactory().field("foo").lte(True).parse() == {
        "foo": {"lte": "1"}
    }
    assert DentalinkQueryFactory().field("foo").lte(False).parse() == {
        "foo": {"lte": "0"}
    }
    assert DentalinkQueryFactory().field("foo").lte(datetime(2022, 1, 1)).parse() == {
        "foo": {"lte": "2022-01-01"}
    }
    assert DentalinkQueryFactory().field("foo").lte(
        datetime(2022, 1, 1), dt_format="%Y-%m-%d %H:%M:%S"
    ).parse() == {"foo": {"lte": "2022-01-01 00:00:00"}}
    assert DentalinkQueryFactory().field("foo").lte(1).lte(2).parse() == {
        "foo": [{"lte": "1"}, {"lte": "2"}]
    }


def test_lk_filter():
    assert DentalinkQueryFactory().field("foo").parse() == {}
    assert DentalinkQueryFactory().field("foo").lk("bar").parse() == {
        "foo": {"lk": "bar"}
    }
    assert DentalinkQueryFactory().field("foo").lk(datetime(2022, 1, 1)).parse() == {
        "foo": {"lk": "2022-01-01"}
    }
    assert DentalinkQueryFactory().field("foo").lk(
        datetime(2022, 1, 1), dt_format="%Y-%m-%d %H:%M:%S"
    ).parse() == {"foo": {"lk": "2022-01-01 00:00:00"}}


def test_docs_example():
    q = (
        DentalinkQueryFactory()
        .field("foo")
        .eq(3)
        .field("bar")
        .gt(1)
        .lt(3)
        .field("now")
        .eq(datetime(2023, 11, 12), dt_format="%Y-%m-%d")
        .parse()
    )

    assert q == {
        "foo": {"eq": "3"},
        "bar": [{"gt": "1"}, {"lt": "3"}],
        "now": {"eq": "2023-11-12"},
    }
