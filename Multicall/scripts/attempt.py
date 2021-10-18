import brownie
import jsonlines as jsonl
import time
from brownie import Contract, interface

def main():
    # Get info we have about Uniswap pair creation events
    file_addr = '/Users/vivekmarwah/Documents/Solidity projects/web3Py/EventScanner-UniswapPairs/EventStorage/blocks.jsonl'
    all_info={}
    with jsonl.open(file_addr,'r') as f:
        for newBlk in f:
            all_info.update(newBlk)
    # Store the token0 and token1 addresses as a token_set, which is a set
    token_set= set()
    # Traverse the datastructure provided by JSONifiedState
    for blk in all_info:
        for tx in all_info[blk]:
            for log in all_info[blk][tx]:
                # Store the token0 and token1
                token_set.update(
                    [ 
                        all_info[blk][tx][log]['token0'],
                        all_info[blk][tx][log]['token1']
                    ]
                )
    del all_info
    # # Addresses of WETH, DAI, USDC
    # coin_list = [
    #             '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 
    #             '0x6B175474E89094C44Da98b954EedeAC495271d0F',
    #             '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'
    #             ]

    # Use multicall to simultaneously query symbols for these contracts

    # coin_contracts = [interface.IERC20(addr) for addr in token_set] 
    # coin_symbols = []

    # brownie.multicall(address='0x5BA1e12693Dc8F9c48aAD8770482f4739bEeD696')

    # with brownie.multicall:
    #     coin_symbols = [coin_contract.symbol() for coin_contract in coin_contracts]

    # print(*coin_symbols, sep='\n')

    token_list = []
    n=0
    # Only do a fixed number of calls
    for x in token_set:
        if n>=1300:
            token_list.append(x)
        n+=1
        if n >= 1315:
            break
    token_set = token_list
    brownie.multicall(address='0x5BA1e12693Dc8F9c48aAD8770482f4739bEeD696')

    addrToSymDict={}
    
    token_set = ['0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9', 
                '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 
                '0x6B175474E89094C44Da98b954EedeAC495271d0F', 
                '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', 
                '0xC011a73ee8576Fb46F5E1c5751cA3B9Fe0af2a6F',
                '0x0000000000085d4780B73119b644AE5ecd22b376', 
                '0xdAC17F958D2ee523a2206206994597C13D831ec7', 
                '0x57Ab1ec28D129707052df4dF418D58a2D46d5f51', 
                '0x4Fabb145d64652a948d72533023f6E7A623C7C53', 
                '0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e', 
                '0x0D8775F648430679A709E98d2b0Cb6250d2887EF', 
                '0xE41d2489571d322189246DaFA5ebDe1F4699F498', 
                # This token leads to OverflowError: Python int 
                # too large to convert to C ssize_t. Probably 
                # because it's in bytes32
                # '0x9f8F72aA9304c8B593d555F12eF6589cC3A579A2', 
                '0x0F5D2fB29fb7d3CFeE444a200298f468908cC942', 
                '0x408e41876cCCDC0F92210600ef50372656052a38', 
                '0xdd974D5C2e2928deA5F71b9825b8b646686BD200', 
                '0xF629cBd94d3791C9250152BD8dfBDF380E2a3B9c', 
                '0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599', 
                '0x514910771AF9Ca656af840dff83E8264EcF986CA', 
                '0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984']

    st_time = time.time()

    # Takes 140 Infura requests with Multicall for 100 symbols and 230 without
    # For upto 15 calls- it only takes about 0.1 s
    with brownie.multicall:
        for token_addr in token_set:
            try:
                token_cont = interface.IERC20(token_addr)
                addrToSymDict[token_addr] = token_cont.symbol()
            except Exception as e:
                print("EXCEPTION: ", e)

    fin_time = time.time()
    print("Total time: ", fin_time - st_time)
    # import json
    # print(json.dumps(addrToSymDict, indent=4))


