# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from unusualwhales import Unusualwhales, AsyncUnusualwhales
from unusualwhales._utils import parse_date
from unusualwhales.types.options_flows import GreekRetrieveResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestGreeks:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: Unusualwhales) -> None:
        greek = client.options_flows.greeks.retrieve(
            symbol="symbol",
        )
        assert_matches_type(GreekRetrieveResponse, greek, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Unusualwhales) -> None:
        greek = client.options_flows.greeks.retrieve(
            symbol="symbol",
            expiration=parse_date("2019-12-27"),
            option_type="CALL",
            strike=0,
        )
        assert_matches_type(GreekRetrieveResponse, greek, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Unusualwhales) -> None:
        response = client.options_flows.greeks.with_raw_response.retrieve(
            symbol="symbol",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        greek = response.parse()
        assert_matches_type(GreekRetrieveResponse, greek, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Unusualwhales) -> None:
        with client.options_flows.greeks.with_streaming_response.retrieve(
            symbol="symbol",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            greek = response.parse()
            assert_matches_type(GreekRetrieveResponse, greek, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Unusualwhales) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `symbol` but received ''"):
            client.options_flows.greeks.with_raw_response.retrieve(
                symbol="",
            )


class TestAsyncGreeks:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncUnusualwhales) -> None:
        greek = await async_client.options_flows.greeks.retrieve(
            symbol="symbol",
        )
        assert_matches_type(GreekRetrieveResponse, greek, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncUnusualwhales) -> None:
        greek = await async_client.options_flows.greeks.retrieve(
            symbol="symbol",
            expiration=parse_date("2019-12-27"),
            option_type="CALL",
            strike=0,
        )
        assert_matches_type(GreekRetrieveResponse, greek, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncUnusualwhales) -> None:
        response = await async_client.options_flows.greeks.with_raw_response.retrieve(
            symbol="symbol",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        greek = await response.parse()
        assert_matches_type(GreekRetrieveResponse, greek, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncUnusualwhales) -> None:
        async with async_client.options_flows.greeks.with_streaming_response.retrieve(
            symbol="symbol",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            greek = await response.parse()
            assert_matches_type(GreekRetrieveResponse, greek, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncUnusualwhales) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `symbol` but received ''"):
            await async_client.options_flows.greeks.with_raw_response.retrieve(
                symbol="",
            )
