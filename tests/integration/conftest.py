import os

import boa
import pytest

boa.set_etherscan(api_key=os.getenv("ETHERSCAN_API_KEY"))


@pytest.fixture(scope="module")
def rpc_url():
    return os.getenv("ETH_RPC_URL") or "https://rpc.ankr.com/eth"


@pytest.fixture(scope="module", autouse=True)
def forked_env(rpc_url):
    block_to_fork = 20742069
    with boa.swap_env(boa.Env()):
        boa.fork(url=rpc_url, block_identifier=block_to_fork)
        print(f"\nForked the chain on block {boa.env.evm.vm.state.block_number}!")
        boa.env.enable_fast_mode()
        yield


@pytest.fixture(scope="module")
def controller_factory():
    return boa.from_etherscan("0xC9332fdCB1C491Dcc683bAe86Fe3cb70360738BC", "controller_factory")


@pytest.fixture(scope="module")
def lens(controller_factory):
    return boa.load("contracts/StablecoinLens.vy", controller_factory)
