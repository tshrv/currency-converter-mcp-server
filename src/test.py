import asyncio

from fastmcp import Client


async def main() -> None:
    async with Client("http://localhost:8001/mcp") as client:
        result = await client.call_tool(
            name="get_current_currency_conversion_rate",
            arguments={
                "source_currency_code": "USD",
                "target_currency_code": "INR",
            },
        )
        print(result)


asyncio.run(main())
