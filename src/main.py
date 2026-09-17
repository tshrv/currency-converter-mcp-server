import httpx
from fastmcp import FastMCP
from loguru import logger

mcp = FastMCP("Currency Service")


@mcp.tool
async def get_current_currency_conversion_rate(
    source_currency_code: str,
    target_currency_code: str,
) -> dict:
    """
    Get today's currency conversion rate from source currency to target currency.
    Use currency codes like INR, USD, etc.

    Args:
        source_currency_code: code of currency you want to convert from, example INR, USD
        target_currency_code: code of currency you want to convert to, example INR, USD
    """
    logger.info(
        f"mcp.get_current_currency_conversion_rate {source_currency_code} {target_currency_code}"
    )
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.frankfurter.dev/v2/rate/{source_currency_code}/{target_currency_code}",
            )

            response.raise_for_status()
            data = response.json()

        data["source_currency_code"] = data.pop("base")
        data["target_currency_code"] = data.pop("quote")

        logger.info(f"Data: {data}")
        return data
    except Exception as e:
        logger.error(f"get_current_currency_conversion_rate failed: {e}")
        return {"error": str(e)}


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8001,
    )
