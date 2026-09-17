# MCP

`mcp.json` is the portable MCP configuration and `.mcp.json` is the Claude-compatible overlay. Keep
the two files aligned when a server is intended for both hosts.

The `mcp/` directory contains policy, notes, and optional server-specific assets. Server commands
must be self-contained and must not rely on a sibling checkout. Put credentials in environment
references such as `${SERVICE_API_KEY}`; never commit secret values.
