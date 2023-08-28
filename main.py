from web3 import Web3
import random
import os
import concurrent.futures as cf

my_rpc_dict = {
    'etherum': 'https://eth-mainnet.g.alchemy.com/v2/3fjNHIUDQIWk1sC73nuW2bRPIbpY8WxM', 
    'binace': 'https://bsc-dataseed.binance.org/',
    'polygon': 'https://polygon.rpc.blxrbdn.com',
    'optimism': 'https://optimism.api.onfinality.io/public',
}
my_contract_dict = {
    'etherum': '0xb1F8e55c7f64D203C1400B9D8555d050F94aDF39',
    'binace': '0x2352c63A83f9Fd126af8676146721Fa00924d7e4',
    'polygon': '0x2352c63A83f9Fd126af8676146721Fa00924d7e4',
    'optimism': '0xB1c568e9C3E6bdaf755A60c7418C269eb11524FC',
}
with open('abi/abi.txt', 'r') as f:
    my_abi = f.read()

    network_etherum = Web3(Web3.HTTPProvider(my_rpc_dict['etherum']))
    network_binace = Web3(Web3.HTTPProvider(my_rpc_dict['binace']))
    network_polygon = Web3(Web3.HTTPProvider(my_rpc_dict['polygon']))
    network_optimism = Web3(Web3.HTTPProvider(my_rpc_dict['optimism']))

    contract_etherum = network_etherum.eth.contract(address=my_contract_dict['etherum'], abi=my_abi)
    contract_binace = network_binace.eth.contract(address=my_contract_dict['binace'], abi=my_abi)
    contract_polygon = network_polygon.eth.contract(address=my_contract_dict['polygon'], abi=my_abi)
    contract_optimism = network_optimism.eth.contract(address=my_contract_dict['optimism'], abi=my_abi)

    contract_list = [contract_etherum, contract_binace, contract_polygon, contract_optimism]



def save_data(data_input):
    with open('data.csv', 'a') as f:
        f.write(f'{data_input}' + '\n')

def create_private_key():
    private_key = []
    address_list = []
    for i in range(2000):
        # random_bytes = os.urandom(32)
        random_bytes = bytearray(random.getrandbits(8) for _ in range(32))
        # privateKey = Web3.keccak(text=f'{random_bytes}').hex()
        privateKey = ''.join(format(byte, '02x') for byte in random_bytes)
        private_key.append(privateKey)
        address = network_binace.eth.account.from_key(privateKey).address
        address_list.append(address)
    return private_key, address_list

def scanner(contract, address_list,zero_address_list,private_key):
    print(len(address_list))

    balances = contract.functions.balances(address_list,zero_address_list).call()

    for i in range(len(balances)):
        if balances[i] != 0:
            save_data(f'{address_list[i]} - {private_key[i]} - {balances[i]}')

def main():

    address_zero = '0x0000000000000000000000000000000000000000'
    for i in range(1):

        private_key, address = create_private_key()
        zero_address_list = [address_zero] * len(address)

        for contract in contract_list:

            with cf.ThreadPoolExecutor(max_workers=10) as executor:
                executor.submit(scanner, contract, address, zero_address_list, private_key)




            


if __name__ == '__main__':
    main()





