# Currency Converter MCP Server

A small [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server built with [FastMCP](https://gofastmcp.com/) that provides current currency conversion rates through the [Frankfurter API](https://www.frankfurter.app/).

The server uses Streamable HTTP transport and listens on `http://localhost:8001` by default.

## Requirements

- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/)
- Internet access to reach `api.frankfurter.dev`

## Quick start

Install the locked dependencies:

```bash
uv sync
```

Start the MCP server:

```bash
uv run python src/main.py
```

The MCP endpoint is:

```text
http://localhost:8001/mcp
```

The server binds to `0.0.0.0`, so it can also accept connections from outside the local machine when the host or container firewall allows port `8001`.

## Available tool

### `get_current_currency_conversion_rate`

Returns the latest rate for a source currency and target currency.

Arguments:

| Name | Type | Description |
| --- | --- | --- |
| `source_currency_code` | `string` | ISO 4217-style source currency code, such as `USD` or `INR` |
| `target_currency_code` | `string` | ISO 4217-style target currency code, such as `EUR` or `INR` |

Example request arguments:

```json
{
	"source_currency_code": "USD",
	"target_currency_code": "INR"
}
```

Example successful result:

```json
{
	"date": "2026-09-17",
	"rate": 83.12,
	"source_currency_code": "USD",
	"target_currency_code": "INR"
}
```

The returned date and rate come from Frankfurter, so the exact values depend on the provider's latest available data. Provider or validation failures are returned by the tool as an object containing an `error` string.

## Test with the included client

Start the server in one terminal, then run the example MCP client in another:

```bash
uv run python src/test.py
```

The client connects to `http://localhost:8001/mcp` and calls the tool for `USD` to `INR`.

## Docker

Build and start the service with Docker Compose:

```bash
docker compose up --build
```

The service is available at `http://localhost:8001/mcp`. Stop it with:

```bash
docker compose down
```

To build and run the image directly:

```bash
docker build -t currency-converter-mcp-server .
docker run --rm -p 8001:8001 currency-converter-mcp-server
```

## Project layout

```text
.
├── src/
│   ├── main.py       # FastMCP server and currency conversion tool
│   └── test.py       # Example MCP client
├── Dockerfile
├── docker-compose.yaml
├── pyproject.toml
└── uv.lock
```

## Configuration and limitations

- The port and host are currently defined directly in `src/main.py` (`8001` and `0.0.0.0`); there are no environment-variable overrides.
- Rates are fetched from Frankfurter on each tool call; the server does not cache results.
- Currency codes should be supplied in uppercase ISO-style format.
- The server does not expose an authentication layer. Do not publish it directly to an untrusted network without adding appropriate access controls.
