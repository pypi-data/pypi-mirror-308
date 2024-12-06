from paloma_sdk.core.broadcast import SyncTxBroadcastResult
from paloma_sdk.core.coins import Coins
from paloma_sdk.core.wasm import MsgExecuteContract, MsgInstantiateContract

from ..wallet import Wallet
from ._base import BaseAsyncAPI, sync_bind
from .tx import CreateTxOptions

__all__ = ["AsyncCw20API", "Cw20API"]


class AsyncCw20API(BaseAsyncAPI):
    async def instantiate(
        self,
        wallet: Wallet,
        code_id: int,
        name: str,
        symbol: str,
        decimals: int,
        total_supply: int,
    ) -> SyncTxBroadcastResult:
        """instantiate the Cw20 smart contract using code id.
            total supply amount is minted to deployer wallet.
        Args:
            wallet (Wallet): CW20 deployer wallet
            code_id (int): Code_id of CW20 code
            name (str): CW20 token name
            symbol (str): CW20 token symbol
            decimals (int): CW20 token decimals
            total_supply (int): CW20 token total supply
        Returns:
            SyncTxBroadcastResult: Transaction Broadcast Result
        """
        instantiate_msg = {
            "name": name,
            "symbol": symbol,
            "decimals": decimals,
            "initial_balances": [
                {"address": wallet.key.acc_address, "amount": str(total_supply)}
            ],
        }
        funds = Coins()
        tx = await wallet.create_and_sign_tx(
            CreateTxOptions(
                msgs=[
                    MsgInstantiateContract(
                        wallet.key.acc_address,
                        None,
                        code_id,
                        "CW20",
                        instantiate_msg,
                        funds,
                    )
                ]
            )
        )
        result = await self._c.tx.broadcast_sync(tx)
        return result

    async def send(
        self, wallet: Wallet, token: str, contract: str, amount: int, msg: str
    ) -> SyncTxBroadcastResult:
        """Send CW20 token to the other address and run msg
        Args:
            wallet (Wallet): CW20 sender wallet
            token (str): token address
            contract (str): token receiver contract address
            amount (str): send amount
            msg (str): base64 encoded message
        Returns:
            SyncTxBroadcastResult: Transaction Broadcast Result
        """
        execute_msg = {
            "send": {"contract": contract, "amount": str(amount), "msg": msg}
        }
        funds = Coins()
        tx = await wallet.create_and_sign_tx(
            CreateTxOptions(
                msgs=[
                    MsgExecuteContract(
                        wallet.key.acc_address, token, execute_msg, funds
                    )
                ]
            )
        )
        result = await self._c.tx.broadcast_sync(tx)
        return result

    async def transfer(
        self, wallet: Wallet, token: str, recipient: str, amount: int
    ) -> SyncTxBroadcastResult:
        """Transfer CW20 token to the other address.
        Args:
            wallet (Wallet): CW20 sender wallet
            token (str): token address
            recipient (str): token receiver address
            amount (str): send amount
        Returns:
            SyncTxBroadcastResult: Transaction Broadcast Result
        """
        execute_msg = {
            "transfer": {
                "recipient": recipient,
                "amount": str(amount),
            }
        }
        funds = Coins()
        tx = await wallet.create_and_sign_tx(
            CreateTxOptions(
                msgs=[
                    MsgExecuteContract(
                        wallet.key.acc_address, token, execute_msg, funds
                    )
                ]
            )
        )
        result = await self._c.tx.broadcast_sync(tx)
        return result

    async def burn(
        self, wallet: Wallet, token: str, amount: int
    ) -> SyncTxBroadcastResult:
        """Burn CW20 token from the wallet address.
        Args:
            wallet (Wallet): CW20 wallet to burn token
            token (str): token address
            amount (str): send amount
        Returns:
            SyncTxBroadcastResult: Transaction Broadcast Result
        """
        execute_msg = {
            "burn": {
                "amount": str(amount),
            }
        }
        funds = Coins()
        tx = await wallet.create_and_sign_tx(
            CreateTxOptions(
                msgs=[
                    MsgExecuteContract(
                        wallet.key.acc_address, token, execute_msg, funds
                    )
                ]
            )
        )
        result = await self._c.tx.broadcast_sync(tx)
        return result


class Cw20API(AsyncCw20API):
    @sync_bind(AsyncCw20API.instantiate)
    def instantiate(
        self,
        wallet: Wallet,
        code_id: int,
        name: str,
        symbol: str,
        decimals: int,
        total_supply: int,
    ) -> SyncTxBroadcastResult:
        pass

    @sync_bind(AsyncCw20API.send)
    def send(
        self, wallet: Wallet, token: str, recipient: str, amount: int, msg: str
    ) -> SyncTxBroadcastResult:
        pass

    @sync_bind(AsyncCw20API.transfer)
    def transfer(
        self, wallet: Wallet, token: str, recipient: str, amount: int
    ) -> SyncTxBroadcastResult:
        pass

    @sync_bind(AsyncCw20API.burn)
    def burn(self, wallet: Wallet, token: str, amount: int) -> SyncTxBroadcastResult:
        pass

    instantiate.__doc__ = AsyncCw20API.instantiate.__doc__
    send.__doc__ = AsyncCw20API.send.__doc__
    transfer.__doc__ = AsyncCw20API.transfer.__doc__
    burn.__doc__ = AsyncCw20API.burn.__doc__
