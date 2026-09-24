<img src="assets/logo-400.png" width="72" alt="Vlada">

# Vlada MCP: US healthcare data for AI agents, with receipts

Vlada Health serves the public record of US healthcare as typed tools on one remote MCP server and one REST API. Hospital and payer negotiated prices, Medicare fee-for-service payment, Medicare Advantage benefits, Star ratings and county enrollment, Part D, the ACA Marketplace, Medicaid managed-care enrollment, provider and facility identity, quality measures, and drug pricing. Every answer names its source file, its vintage, how the number was computed and its coverage, and carries a hash you can replay. A number the data cannot support comes back as "not in the data", never as zero.

This repository is the public home of the connector: how to connect, runnable examples, and the registry manifests. The server itself is hosted; you do not run it.

## Connect in one minute

| Client | Endpoint | Auth |
|---|---|---|
| Claude.ai, ChatGPT (developer mode) | `https://mcp-secure.vladahealth.com/mcp` | OAuth, sign in once |
| Claude Code, Claude Desktop, Cursor, VS Code | `https://mcp.vladahealth.com/mcp` | bearer API key |
| Any HTTP client | `https://api.vladahealth.com/v1/tools/{name}` | bearer API key; schemas need no key |

One-click connect and a free account with $5 of starting queries: https://www.vladahealth.com/data-access

Claude Code:

```bash
claude mcp add --transport http vlada https://mcp.vladahealth.com/mcp --header "Authorization: Bearer $VLADA_API_KEY"
```

Gemini CLI:

```bash
gemini extensions install https://github.com/btenner84/vlada-mcp
```

Claude Code plugin (OAuth, no key to paste):

```text
/plugin marketplace add btenner84/vlada-mcp
/plugin install vlada@vlada
```

Cursor, VS Code, or any client that reads an `mcp.json`: see `examples/mcp.json`.

One-click install:

[![Install in Cursor](https://img.shields.io/badge/Cursor-install-000000?logo=cursor)](cursor://anysphere.cursor-deeplink/mcp/install?name=vlada&config=eyJ1cmwiOiAiaHR0cHM6Ly9tY3AudmxhZGFoZWFsdGguY29tL21jcCIsICJoZWFkZXJzIjogeyJBdXRob3JpemF0aW9uIjogIkJlYXJlciAke1ZMQURBX0FQSV9LRVl9In19) [![Install in VS Code](https://img.shields.io/badge/VS_Code-install-0098FF?logo=visualstudiocode&logoColor=fff)](https://vscode.dev/redirect?url=vscode%3Amcp%2Finstall%3F%7B%22name%22%3A%20%22vlada%22%2C%20%22type%22%3A%20%22http%22%2C%20%22url%22%3A%20%22https%3A%2F%2Fmcp.vladahealth.com%2Fmcp%22%2C%20%22headers%22%3A%20%7B%22Authorization%22%3A%20%22Bearer%20%24%7Binput%3Avlada_key%7D%22%7D%2C%20%22inputs%22%3A%20%5B%7B%22id%22%3A%20%22vlada_key%22%2C%20%22type%22%3A%20%22promptString%22%2C%20%22description%22%3A%20%22Vlada%20API%20key%22%2C%20%22password%22%3A%20true%7D%5D%7D) [![Official MCP Registry](https://img.shields.io/badge/MCP_Registry-io.github.btenner84%2Fvlada-2ea44f)](https://registry.modelcontextprotocol.io/v0/servers?search=vlada)


## What you can ask

- Which payers pay a named hospital for CPT 70553, and how that compares with Medicare.
- A Medicare Advantage plan's filed benefits (dental, OTC, MOOP, inpatient, 19 categories) for a year, with the CMS source row and its hash.
- A contract's Star rating for a rating year, as published.
- Medicare Advantage enrollment by county, parent organization and plan, monthly.
- Medicaid managed-care enrollment by state and plan, with the reporting period stated.
- Provider identity by NPI, resolved to facility and CCN.

The tool reference (42 tools, inputs, sources, known gaps) is public at https://www.vladahealth.com/tools. The REST quickstart is at https://www.vladahealth.com/tools/rest-quickstart.

## A worked example: Medicare Advantage benefits, Stars and enrollment, joined

The three CMS sources sit on three clocks (a month, a plan year, a rating year) and two keys (contract-plan for benefits and enrollment, contract alone for Stars). `examples/ma_join.py` reproduces the Los Angeles County join from the write-up at https://www.vladahealth.com/data/medicare-advantage/ca-los-angeles: the four largest non-dual HMO plans, their April 2026 enrollment, the contract's 2026 Star rating, and the filed OTC allowance, including the two plans that file the benefit as offered with no maximum amount. That case comes back as `offered_status: offered` and `numeric_amount_observability: offered_without_numeric_amounts`, not as zero.

## What every answer carries

`source.source_url`, `vintage`, `method`, `caveats`, `response_hash`, `audit_id`. Prove and replay tools (`prove_hospital_price`, `replay_hospital_price`, `prove_commercial_price`, `replay_commercial_price_proof`, `prove_ma_enrollment_trend`) turn any number into a re-runnable receipt.

## What it is not

Not patient records, not a FHIR server, not an EHR connector. Public market, price, coverage, enrollment, provider, quality and drug records only. Read-only: every tool declares `readOnlyHint: true`.

## Registry manifests

`server.json` is the official MCP registry manifest (remote, Streamable HTTP), published automatically by `.github/workflows/publish-mcp.yml` on every change. `glama.json` claims the Glama listing.

## Support

ben@vladahealth.com. Privacy: https://www.vladahealth.com/privacy. Terms: https://www.vladahealth.com/terms.
