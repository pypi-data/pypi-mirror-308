from paloma_sdk.core.broadcast import SyncTxBroadcastResult
from paloma_sdk.core.skyway import MsgSendToRemote, MsgCancelSendToRemote
from paloma_sdk.core.coin import Coin

from ..wallet import Wallet
from ._base import BaseAsyncAPI, sync_bind
from .tx import CreateTxOptions

__all__ = ["AsyncSkywayAPI", "SkywayAPI"]


class AsyncSkywayAPI(BaseAsyncAPI):
    async def send_tx(
        self,
        wallet: Wallet,
        eth_dest: str,
        denom: str,
        amount: int,
        chain_reference_id: str,
        creator: str,
        signers: list[str],
    ) -> SyncTxBroadcastResult:
        """Grain send transaction
        Args:
            wallet (Wallet): Job creator paloma wallet
            eth_dest (str): ethereum destination address
            denom (str): coin denom
            amount (int): coin amount
            chain_reference_id (str): chain reference id in paloma
            creator (str): job creator
            signers (list[str]): signers list
        Returns:
            SyncTxBroadcastResult: transaction result
        """
        create_tx = await wallet.create_and_sign_tx(
            CreateTxOptions(
                msgs=[
                    MsgSendToRemote(
                        eth_dest,
                        Coin(denom, amount),
                        chain_reference_id,
                        {
                            "creator": creator,
                            "signers": signers,
                        },
                    )
                ]
            )
        )
        create_tx_result = await self._c.tx.broadcast_sync(create_tx)
        return create_tx_result

    async def cancel_tx(
        self,
        wallet: Wallet,
        transaction_id: int,
        creator: str,
        signers: list[str],
    ) -> SyncTxBroadcastResult:
        """Cancel Grain send transaction
        Args:
            wallet (Wallet): Job creator paloma wallet
            transaction_id (int): transaction id
            creator (str): job creator
            signers (list[str]): signers list
        Returns:
            SyncTxBroadcastResult: transaction result
        """
        execute_tx = await wallet.create_and_sign_tx(
            CreateTxOptions(
                msgs=[
                    MsgCancelSendToRemote(
                        transaction_id,
                        {
                            "creator": creator,
                            "signers": signers,
                        },
                    )
                ]
            )
        )
        create_tx_result = await self._c.tx.broadcast_sync(execute_tx)
        return create_tx_result


class SkywayAPI(AsyncSkywayAPI):
    @sync_bind(AsyncSkywayAPI.send_tx)
    def send_tx(
        self,
        wallet: Wallet,
        eth_dest: str,
        denom: str,
        amount: int,
        chain_reference_id: str,
        creator: str,
        signers: list[str],
    ) -> SyncTxBroadcastResult:
        pass

    @sync_bind(AsyncSkywayAPI.cancel_tx)
    def cancel_tx(
        self,
        wallet: Wallet,
        transaction_id: int,
        creator: str,
        signers: list[str],
    ) -> SyncTxBroadcastResult:
        pass

    send_tx.__doc__ = AsyncSkywayAPI.send_tx.__doc__
    cancel_tx.__doc__ = AsyncSkywayAPI.cancel_tx.__doc__
