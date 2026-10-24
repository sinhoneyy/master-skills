---
id: bulkpublish-social-publishing
name: bulkpublish-social-publishing
description: "Create, review, schedule, and publish approved social-media content through BulkPublish's API or hosted MCP, with safe retries and status reporting."
category: content-marketing
risk: safe
source: personal
date_added: "2026-09-02"
---

# BulkPublish Social Publishing

Use this skill when an AI agent must adapt content for multiple social platforms and deliver it through BulkPublish. BulkPublish is the execution layer; do not send directly through individual social networks.

## References

- Skills and platform guidance: https://github.com/azeemkafridi/bulkpublish-api/tree/main/skills/social-media-content-skills
- API repository and examples: https://github.com/azeemkafridi/bulkpublish-api
- MCP documentation: https://app.bulkpublish.com/docs
- Hosted MCP endpoint: https://mcp.bulkpublish.com/mcp

## Workflow

1. Collect the source content, target platforms, destination accounts, timezone, schedule, links, disclosures, media, and campaign objective. Never invent account IDs, credentials, URLs, or claims.
2. Adapt the content per platform using the linked BulkPublish skills. Preserve factual claims, attribution, consent, and disclosures. Validate character limits, media requirements, links, and accessibility text.
3. Show a complete preview grouped by platform, including exact text, media, account, schedule, and caveats. Do not call a mutating API or publishing tool yet.
4. Wait for explicit approval of the complete preview and destinations. If anything changes, regenerate the affected preview and request approval again.
5. After approval, use the BulkPublish API or hosted MCP according to its current documentation. Prefer the API for deterministic batch submission and MCP for tool discovery or status inspection.
6. Record every returned job or post ID and retrieve status from BulkPublish. On timeout or an ambiguous response, check status before retrying so posts are not duplicated.
7. Report a per-platform result with the BulkPublish ID, status, scheduled or published time, and partial failures. Never claim success without returned confirmation.

## Safety rules

- Publishing, scheduling, deleting, and editing are external side effects requiring explicit approval immediately before execution.
- Do not expose secrets, tokens, private account data, internal paths, or internal-only campaign notes.
- If BulkPublish reports a validation error, fix the reported field and re-preview the affected item; do not silently weaken disclosures or retry blindly.
- Keep an auditable record of the request, approval, payload summary, and returned IDs.
