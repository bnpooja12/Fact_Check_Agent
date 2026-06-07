# test_tavily.py

from tavily import TavilyClient

client = TavilyClient(
    api_key="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"
)

result = client.search(
    "India population"
)

print(result)
