# To run use: 
# brownie run scripts/attempt\ copy.py --interactive --network mainnet
import brownie
import json
import time
from brownie import Contract, interface

def main():
    token_list = []
    token_list= json.load(open('token_list','r'))

    brownie.multicall(address='0x5BA1e12693Dc8F9c48aAD8770482f4739bEeD696')

    addrToSymDict={}
    token_list_multicall = token_list[:100]

    st_time_multicall = time.time()
    with brownie.multicall:
        for token_addr in token_list_multicall:
            try:
                token_cont = interface.IERC20(token_addr)
                addrToSymDict[token_addr] = token_cont.symbol()
            except Exception as e:
                print("EXCEPTION: ", e)

    fin_time_multicall = time.time()
    print("Multicall Total time: ", fin_time_multicall - st_time_multicall)

    addrToSymDict={}
    token_list_reg_call = token_list[100:200]
    st_time_reg_call = time.time()

    for token_addr in token_list_reg_call:
        try:
            token_cont = interface.IERC20(token_addr)
            addrToSymDict[token_addr] = token_cont.symbol()
        except Exception as e:
            print("EXCEPTION: ", e)

    fin_time_reg_call = time.time()
    print("Regular calls Total time: ", fin_time_reg_call - st_time_reg_call)

