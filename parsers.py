from datetime import datetime


def orderEntryRequestFormatter(msgDict: dict, timestamp):
    msgDict = msgDict.get('OrderEntryRequestMessage').get('Order')

    msg = '**'

    sym = msgDict.get('Security').get('Symbol')
    optionTDAString = None
    if '_' in sym:
        symSplit = sym.split('_')
        msg += '$' + symSplit[0] + ' '
        msg += symSplit[1][0:2] + '/' + symSplit[1][2:4] + \
            '/' + symSplit[1][4:6] + ' ' + symSplit[1][6:]
        optionTDAString = '.' + symSplit[0] + symSplit[1][4:6] + \
            symSplit[1][0:2] + symSplit[1][2:4] + symSplit[1][6:]
    else:
        msg += '$' + sym

    msg += ' (' + msgDict.get('Security').get('SecurityType')
    if msgDict.get('Security').get('SymbolUnderlying'):
        msg += ' ' + msgDict.get('Security').get('SymbolUnderlying')

    msg += ')** - '

    if optionTDAString:
        msg += '(' + optionTDAString + ') '

    msg += datetime.fromtimestamp(timestamp /
                                  1000.0).astimezone().strftime("%m-%d-%Y %H:%M:%S %Z")

    msg += '\n```diff\n'

    quantity = msgDict.get('OriginalQuantity')
    if msgDict.get('OrderInstructions') == 'Buy':
        msg += '+' + quantity + ' Buy'

    if msgDict.get('OrderInstructions') == 'Sell':
        msg += '-' + quantity + ' Sell'

    if optionTDAString:
        openClose = msgDict.get('OpenClose')
        msg += ' to ' + openClose

    if msgDict.get('OrderType') == 'Limit':
        price = msgDict.get('OrderPricing').get('Limit')
        msg += ' at ' + price

    msg += '\n```\n||@everyone||'

    return msg


def orderFillFormatter(msgDict: dict, timestamp):
    order = msgDict.get('OrderFillMessage').get('Order')
    execInfo = msgDict.get('OrderFillMessage').get('ExecutionInformation')

    msg = '**'

    sym = order.get('Security').get('Symbol')
    optionTDAString = None
    if '_' in sym:
        symSplit = sym.split('_')
        msg += '$' + symSplit[0] + ' '
        msg += symSplit[1][0:2] + '/' + symSplit[1][2:4] + \
            '/' + symSplit[1][4:6] + ' ' + symSplit[1][6:]
        optionTDAString = '.' + symSplit[0] + symSplit[1][4:6] + \
            symSplit[1][0:2] + symSplit[1][2:4] + symSplit[1][6:]
    else:
        msg += '$' + sym

    msg += ' (' + order.get('Security').get('SecurityType')
    if order.get('Security').get('SymbolUnderlying'):
        msg += ' ' + order.get('Security').get('SymbolUnderlying')

    msg += ')** - '

    if optionTDAString:
        msg += '(' + optionTDAString + ') '

    msg += datetime.fromtimestamp(timestamp /
                                  1000.0).astimezone().strftime("%m-%d-%Y %H:%M:%S %Z")

    msg += '\n```diff\n'

    quantity = execInfo.get('Quantity')
    if order.get('OrderInstructions') == 'Buy':
        msg += '+' + quantity + ' BOT'

    if order.get('OrderInstructions') == 'Sell':
        msg += '-' + quantity + ' SOLD'

    if optionTDAString:
        openClose = order.get('OpenClose')
        msg += ' to ' + openClose

    msg += ' - ' + execInfo.get('ExecutionPrice')

    msg += '\n```\n||@everyone||'

    return msg


def orderCancelledFormatter(msgDict: dict, timestamp):
    msgDict = msgDict.get('UROUTMessage').get('Order')

    msg = '**'

    sym = msgDict.get('Security').get('Symbol')
    optionTDAString = None
    if '_' in sym:
        symSplit = sym.split('_')
        msg += '$' + symSplit[0] + ' '
        msg += symSplit[1][0:2] + '/' + symSplit[1][2:4] + \
            '/' + symSplit[1][4:6] + ' ' + symSplit[1][6:]
        optionTDAString = '.' + symSplit[0] + symSplit[1][4:6] + \
            symSplit[1][0:2] + symSplit[1][2:4] + symSplit[1][6:]
    else:
        msg += '$' + sym

    msg += ' (' + msgDict.get('Security').get('SecurityType')
    if msgDict.get('Security').get('SymbolUnderlying'):
        msg += ' ' + msgDict.get('Security').get('SymbolUnderlying')

    msg += ')** - '

    if optionTDAString:
        msg += '(' + optionTDAString + ') '

    msg += datetime.fromtimestamp(timestamp /
                                  1000.0).astimezone().strftime("%m-%d-%Y %H:%M:%S %Z")

    msg += '\n```diff\n'

    quantity = msgDict.get('OriginalQuantity')
    if msgDict.get('OrderInstructions') == 'Buy':
        msg += '+' + quantity + ' Buy'

    if msgDict.get('OrderInstructions') == 'Sell':
        msg += '-' + quantity + ' Sell'

    if optionTDAString:
        openClose = msgDict.get('OpenClose')
        msg += ' to ' + openClose

    if msgDict.get('OrderType') == 'Limit':
        price = msgDict.get('OrderPricing').get('Limit')
        msg += ' at ' + price

    msg += '\n```\n||@everyone||'

    return msg
