---
name: lookup
track: core
kind: live_api
provider: Tavily
requires_env: [TAVILY_API_KEY]
inputs: [query, topic, timeframe, max_results, target_date]
outputs: [items]
side_effect: false
---
# lookup

Searches the web via Tavily. Has a `topic` (`general` or `news`) and a
`timeframe` argument.

Optional `target_date` must be an ISO calendar date (YYYY-MM-DD). For exact
event/draw searches, it adds DD/MM/YYYY to the query and disables the publication
recency filter. Returned search matches still require source verification; this
parameter does not validate lottery results or prevent stale pages from appearing.
