from dataclasses import dataclass
from typing import List
from terra_proto.cosmos.base.v1beta1 import Coin

import betterproto

@dataclass(eq=False, repr=False)
class Metadata(betterproto.Message):
    creator: bytes = betterproto.bytes_field(1)
    signers: List[bytes] = betterproto.message_field(2)

@dataclass(eq=False, repr=False)
class MsgSendToRemote(betterproto.Message):
    eth_dest: str = betterproto.string_field(2)
    amount: "Coin" = betterproto.message_field(3)
    chain_reference_id: str = betterproto.string_field(4)
    metadata: "Metadata" = betterproto.message_field(5)

@dataclass(eq=False, repr=False)
class MsgCancelSendToRemote(betterproto.Message):
    transaction_id: int = betterproto.uint64_field(1)
    metadata: "Metadata" = betterproto.message_field(3)
