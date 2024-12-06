# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from unusualwhales import Unusualwhales, AsyncUnusualwhales
from unusualwhales.types import InsiderTradeListResponse
from unusualwhales._utils import parse_date

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestInsiderTrades:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: Unusualwhales) -> None:
        insider_trade = client.insider_trades.list()
        assert_matches_type(InsiderTradeListResponse, insider_trade, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Unusualwhales) -> None:
        insider_trade = client.insider_trades.list(
            date=parse_date("2019-12-27"),
            insider="insider",
            symbol="symbol",
            transaction_type="Buy",
        )
        assert_matches_type(InsiderTradeListResponse, insider_trade, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Unusualwhales) -> None:
        response = client.insider_trades.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        insider_trade = response.parse()
        assert_matches_type(InsiderTradeListResponse, insider_trade, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Unusualwhales) -> None:
        with client.insider_trades.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            insider_trade = response.parse()
            assert_matches_type(InsiderTradeListResponse, insider_trade, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncInsiderTrades:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_list(self, async_client: AsyncUnusualwhales) -> None:
        insider_trade = await async_client.insider_trades.list()
        assert_matches_type(InsiderTradeListResponse, insider_trade, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncUnusualwhales) -> None:
        insider_trade = await async_client.insider_trades.list(
            date=parse_date("2019-12-27"),
            insider="insider",
            symbol="symbol",
            transaction_type="Buy",
        )
        assert_matches_type(InsiderTradeListResponse, insider_trade, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncUnusualwhales) -> None:
        response = await async_client.insider_trades.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        insider_trade = await response.parse()
        assert_matches_type(InsiderTradeListResponse, insider_trade, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncUnusualwhales) -> None:
        async with async_client.insider_trades.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            insider_trade = await response.parse()
            assert_matches_type(InsiderTradeListResponse, insider_trade, path=["response"])

        assert cast(Any, response.is_closed) is True
