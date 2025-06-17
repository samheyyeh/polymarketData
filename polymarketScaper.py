#!/usr/bin/env python3
import requests
import json

def get_all_active_markets():
    url = "https://gamma-api.polymarket.com/markets"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def get_markets_by_token_ids(token_ids, markets):
    token_set = set(token_ids)
    filtered_markets = []
    for market in markets:
        market_tokens = json.loads(market.get('clobTokenIds', '[]'))
        if any(token in token_set for token in market_tokens):
            filtered_markets.append(market)
    return filtered_markets

def main():
    markets = get_all_active_markets()

    all_active_asset_ids = []
    for market in markets:
        if market.get('active'):
            tokens = json.loads(market.get('clobTokenIds', '[]'))
            all_active_asset_ids.extend(tokens)

    first_10_tokens = all_active_asset_ids[:10]

    selected_markets = get_markets_by_token_ids(first_10_tokens, markets)

    print(f"Found {len(selected_markets)} markets matching first 10 tokens.\n")

    for market in selected_markets:
        event_title = market.get('question', 'Unknown Title')
        clob_tokens = json.loads(market.get('clobTokenIds', '[]'))
        outcome_prices = json.loads(market.get('outcomePrices', '[]'))
        outcomes = json.loads(market.get('outcomes', '[]'))

        print(f"Market ID: {market.get('id')}")
        print(f"Event Title: {event_title}")
        print(f"Volume: ${float(market.get('volume', 0)):.2f}")
        print(f"Tokens: {clob_tokens}")
        print("Outcomes and Odds:")
        for outcome, price in zip(outcomes, outcome_prices):
            print(f"  - {outcome}: {price}")
        print("-" * 40)


if __name__ == "__main__":
    main()
