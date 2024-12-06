# TODO: I need the ability to qualify contract
from ib_async import Contract


def qualify_contracts(contract: Contract|str):

    if isinstance(contract, str):
        return contract

    if contract.secType in ['FUT']:
        value = {
            '6A': '@AD#',
            '6B': '@BP#',
            '6C': '@CD#',
            '6E': '@EU#',
            '6J': '@JY#',
            '6N': '@NE#',
            '6S': '@SF#',
            '6M': '@PX#',
            'ZN': '@TY#',
            'ES': '@ES#',
            'CL': 'QCL#',
            'GC': 'QGC#',
            'MES': '@ES#',
            'MCL': 'QCL#',
        }.get(contract.symbol)
        return value

    elif contract.secType in ['CASH']:
        return {
            'AUD.USD': '@AD#',
            'GBP.USD': '@BP#',
            'CAD.USD': '@CD#',
            'EUR.USD': '@EU#',
            'JPY.USD': '@JY#',
            'NZD.USD': '@NE#',
            'MXN.USD': '@PX#',
            'CHF.USD': '@SF#',
        }.get(contract.symbol)

    elif contract.secType in ['STK']:
        return contract.symbol

    raise NotImplemented(f'Following contract not mapped: {contract.secType} {contract.symbol}')
