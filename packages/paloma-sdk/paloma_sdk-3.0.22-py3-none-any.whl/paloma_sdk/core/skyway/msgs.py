from __future__ import annotations

import json
from typing import Union

import attr

from paloma_sdk.core import Coin
from paloma_sdk.core.msg import Msg
from paloma_sdk.util.json import JSONSerializable
from paloma_sdk.util.remove_none import remove_none

from .data import MsgSendToRemote as MsgSendToRemote_pb
from .data import MsgCancelSendToRemote as MsgCancelSendToRemote_pb
from .data import Metadata as Metadata_pb

__all__ = [
    "MsgSendToRemote",
    "MsgCancelSendToRemote"
]

@attr.s
class MsgSendToRemote(Msg):
    """Send grain to evm chain
    Args:
        creator: Job creator paloma address
        job: Paloma job details
    """

    type_amino = "skyway/MsgSendToRemote"
    type_url = "/palomachain.paloma.skyway.MsgSendToRemote"
    prototype = MsgSendToRemote_pb

    eth_dest: str = attr.ib()
    amount: Coin = attr.ib()
    chain_reference_id: str = attr.ib()
    metadata: dict = attr.ib()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "eth_dest": remove_none(self.eth_dest),
                "amount": self.amount.to_amino(),
                "chain_reference_id": remove_none(self.chain_reference_id),
                "metadata": remove_none(self.metadata),
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgSendToRemote:
        return cls(
            eth_dest=parse_msg(data["eth_dest"]),
            amount=parse_msg(data["amount"]),
            chain_reference_id=parse_msg(data["chain_reference_id"]),
            metadata=parse_msg(data["metadata"]),
        )

    def to_proto(self) -> MsgSendToRemote_pb:
        return MsgSendToRemote_pb(
            eth_dest=self.eth_dest,
            amount=self.amount.to_proto(),
            chain_reference_id=self.chain_reference_id,
            metadata=Metadata_pb(
                creator=bytes(self.metadata["creator"], "ascii"),
                signers=[bytes(signer, "ascii") for signer in self.metadata["signers"]],
            ),
        )

    @classmethod
    def from_proto(cls, proto: MsgSendToRemote_pb) -> MsgSendToRemote:
        return cls(
            eth_dest=parse_msg(proto.eth_dest),
            amount=parse_msg(proto.amount),
            chain_reference_id=parse_msg(proto.chain_reference_id),
            metadata=parse_msg(proto.metadata),
        )


@attr.s
class MsgCancelSendToRemote(Msg):
    """Paloma job details attribute
    Args:
        creator: Job runner paloma address
        job_id: Job ID to execute
        payload: The payload for the job execute.
    """

    type_amino = "skyway/MsgCancelSendToRemote"
    type_url = "/palomachain.paloma.skyway.MsgCancelSendToRemote"
    prototype = MsgCancelSendToRemote_pb

    transaction_id: int = attr.ib()
    metadata: dict = attr.ib()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "transaction_id": self.transaction_id,
                "metadata": self.metadata,
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgCancelSendToRemote:
        return cls(
            transaction_id=data["transaction_id"],
            metadata=parse_msg(data["metadata"]),
        )

    def to_proto(self) -> MsgCancelSendToRemote_pb:
        return MsgCancelSendToRemote_pb(
            transaction_id=self.transaction_id,
            metadata=Metadata_pb(
                creator=bytes(self.metadata["creator"], "ascii"),
                signers=[bytes(signer, "ascii") for signer in self.metadata["signers"]],
            ),
        )

    @classmethod
    def from_proto(cls, proto: MsgCancelSendToRemote_pb) -> MsgCancelSendToRemote:
        return cls(
            transaction_id=proto.transaction_id,
            metadata=proto.metadata
        )


def parse_msg(msg: Union[dict, str, bytes]) -> dict:
    if type(msg) is dict:
        return msg
    return json.loads(msg)
