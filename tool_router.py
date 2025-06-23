async def handle_tool_routing(client, query: str):
    """Basic keyword-based routing to tools."""
    if "flipkart" in query.lower():
        return await client.call_tool("puppeteer_puppeteer_navigate", {
            "url": "https://www.flipkart.com"
        })

    elif "wikipedia" in query.lower():
        return await client.call_tool("puppeteer_puppeteer_navigate", {
            "url": "https://en.wikipedia.org/wiki/Computer_vision"
        })

    elif "search" in query.lower():
        query_text = query.replace("search", "").strip()
        return await client.call_tool("duckduckgo_web_search", {
            "query": query_text,
            "count": 5,
            "safeSearch": "moderate"
        })

    return None
