# Installing the Vlada Health MCP server (for AI agents)

Vlada is a hosted remote MCP server. There is nothing to clone, build or run.

1. Endpoint (Streamable HTTP):
   - OAuth clients (Claude, ChatGPT, Gemini CLI, Claude Code, Cline): `https://mcp-secure.vladahealth.com/mcp`. The first call returns 401 with a `WWW-Authenticate` header pointing at the protected-resource metadata; follow it, and the user signs in or creates a free account in the browser (OAuth 2.1, PKCE).
   - API-key clients: `https://mcp.vladahealth.com/mcp` with header `Authorization: Bearer <VLADA_API_KEY>`. The user gets a key at https://www.vladahealth.com/data-access.
2. Cline (`cline_mcp_settings.json`):
   ```json
   {"mcpServers": {"vlada": {"type": "streamableHttp", "url": "https://mcp.vladahealth.com/mcp", "headers": {"Authorization": "Bearer ${VLADA_API_KEY}"}}}}
   ```
3. Verify: call `find_data_sources` with a question such as "Medicare Advantage enrollment by county". A list of sources with coverage means it works.

Every tool is read-only. No patient records are served.
