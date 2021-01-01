import dataclasses

from rx import Observable
from rx import operators as ops

from xlab.trading.ibapi.mess.message import IbApiMessageType, IbApiMessage


def collect_account_summary(messages: Observable):
    acct_summary_messages = messages.pipe(
        ops.filter(
            lambda m: is_account_summary(m) or is_account_summary_end(m)),
        ops.take_while(lambda m: not is_account_summary_end(m)),
        ops.filter(lambda m: m.payload[0]))
    return acct_summary_messages.run()


def is_account_summary(m: IbApiMessage) -> bool:
    return m.type == IbApiMessageType.ACCOUNT_SUMMARY


def is_account_summary_end(m: IbApiMessage) -> bool:
    return m.type == IbApiMessageType.ACCOUNT_SUMMARY_END


@dataclasses.dataclass
class AccountSummaryData(object):
    account: str
    tag: str
    value: str
    currency: str


def account_summary_request_id(m: IbApiMessage) -> int:
    return m.payload[0]


def unpack_account_summary(m: IbApiMessage) -> AccountSummaryData:
    if not is_account_summary(m):
        raise TypeError(
            'Trying to unpack a message as account summary, but message is of type: {}'
            .format(m.type.name))

    account, tag, value, currency = m.payload

