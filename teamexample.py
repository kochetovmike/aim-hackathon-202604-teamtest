"""
teamexample.py — Example script for hackathon teams

Verifies the proxy is reachable and makes a sample chat request through it.

Usage:
    python examples/teamexample.py

Requirements:
    pip install openai

Environment variables (or edit the constants below):
    PROXY_URL   — proxy base URL, e.g. http://localhost:3000/v1
    TEAM_API_KEY — the key issued to your team, e.g. hack-team_alpha-<hex>
"""

import os
import sys

try:
    from openai import OpenAI
except ImportError:
    print("openai package not found. Install it with:  pip install openai")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Configuration — override via environment variables or edit directly
# ---------------------------------------------------------------------------

PROXY_URL = os.getenv("PROXY_URL", "http://hackathon-proxy.westeurope.azurecontainer.io:3000/v1") # Use /v1/ui to check out your credits in web browser
TEAM_API_KEY = os.getenv("TEAM_API_KEY", "paste your key here or in environment variable")

# ---------------------------------------------------------------------------
# 1. Verify the proxy is reachable
# ---------------------------------------------------------------------------

import urllib.request
import json

print(f"Proxy URL : {PROXY_URL}")
print(f"Team key  : {TEAM_API_KEY[:20]}...")
print()

health_url = PROXY_URL.replace("/v1", "") + "/health"
print(f"Checking proxy health at {health_url} ...")
try:
    with urllib.request.urlopen(health_url, timeout=5) as resp:
        health = json.loads(resp.read())
    print(f"  status : {health.get('status')}")
    print(f"  teams  : {health.get('teams')}")
    print()
except Exception as e:
    print(f"  ERROR: Could not reach proxy — {e}")
    print("  Make sure the proxy is running:  npm run dev")
    sys.exit(1)

# ---------------------------------------------------------------------------
# 2. Create the OpenAI client pointed at the proxy
# ---------------------------------------------------------------------------

client = OpenAI(
    base_url=PROXY_URL,
    api_key=TEAM_API_KEY,
)

# ---------------------------------------------------------------------------
# 3. Make a sample chat request
# ---------------------------------------------------------------------------

QUESTION = "What's the weather like in spring in Dublin?"

print(f"Sending request: \"{QUESTION}\"")
print("-" * 60)

response = client.chat.completions.create(
    model="gpt-4.1",  
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": QUESTION},
    ],
    max_tokens=300,
)

answer = response.choices[0].message.content
print(answer)
print("-" * 60)
print()
print(f"Tokens used  : {response.usage.total_tokens} "
      f"(prompt: {response.usage.prompt_tokens}, "
      f"completion: {response.usage.completion_tokens})")
print()
print("Success! Your team is connected to the proxy.")
