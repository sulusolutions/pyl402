# pyl402: L402 tools for Python
Take the L402 pill...

## Overview
pyl402  is a Python package designed to handle HTTP requests with integrated payment functionality, specifically focusing on the [Lightning Network protocol L402](https://docs.sulu.sh/docs/l402-demonstration) and automatic handling of HTTP 402 Payment Required responses. It integrates seamlessly with Lightning wallets to provide a smooth experience when dealing with paid resources.

**Note: This project is currently in alpha stage and is considered Work-In-Progress (WIP). Features and functionality are subject to change, and more testing is needed to ensure stability and reliability.**

## Installation

To install pyl402, you can use pip:

```bash
pip install pyl402
```
Please note that this package requires Python 3.7 or later.

## Features

- __Automatic Token Handling__: Manages L402 tokens automatically, storing and retrieving tokens as needed.
- __Integrated Payment__: Automatically handles payment processes if a resource requires payment, through compatible wallet implementations.
- __Extensible__: Easily extend the library to support different wallet types and token storage mechanisms.

## Usage
Here's a quick example to get you started with the L402 Client:

```python
from pyl402.wallet import AlbyWallet
from pyl402.token_store import MemoryTokenStore
from pyl402.client import L402Client

# Initialize wallet and token store
wallet = AlbyWallet(token="your_alby_api_token_here")
store = MemoryTokenStore()

# Create the L402 Client
client = L402Client(wallet=wallet, store=store)

# Use the client to send HTTP requests
response = client.get('http://rnd.ln.sulu.sh/randomnumber')
print(response.text)
```

This example demonstrates creating an L402 client using an Alby wallet and a memory-based token store to access a resource that may require payment. 

## Contributions
Contributions are welcome! If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## Licensing
The code in this project is licensed under the MIT license. See LICENSE for details. 

## Disclaimer
This is an alpha release, and as such, it might contain bugs and incomplete features. We do not recommend using it in a production environment.