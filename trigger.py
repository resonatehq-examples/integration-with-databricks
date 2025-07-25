#!/usr/bin/env python3
import argparse
import requests
import sys


def main():
    parser = argparse.ArgumentParser(
        description="Call the ngrok endpoint with a given ID."
    )
    parser.add_argument(
        "--id",
        help="The ID to send to the server",
        required=True,
    )
    parser.add_argument(
        "--url",
        help="Base URL of the ngrok endpoint (default: %(default)s)",
        required=True,
    )
    args = parser.parse_args()

    params = {"id": args.id, "url": args.url}
    try:
        response = requests.get(f"{args.url}/run", params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error calling {args.url}/run with id={args.id}: {e}")
        sys.exit(1)

    print("Response:", response.text)


if __name__ == "__main__":
    main()
