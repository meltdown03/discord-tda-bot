from datetime import datetime
from dateutil.parser import parse


def orderEntryRequestFormatter(msgDict: dict):
  msgDict = msgDict.get('OrderEntryRequestMessage').get('Order')

  msg = '**'

  sym = msgDict.get('Security').get('Symbol')
  optionTDAString = None
  if '_' in sym:
    symSplit = sym.split('_')
    msg += '$' + symSplit[0] + ' '
    msg += symSplit[1][0:2] + '/' + symSplit[1][2:4] + '/' + symSplit[1][4:6] + ' ' + symSplit[1][6:]
    optionTDAString = '.' + symSplit[0] + symSplit[1][4:6] + symSplit[1][0:2] + symSplit[1][2:4] + symSplit[1][6:]
  else:
    msg += '$' + sym

  msg += ' (' + msgDict.get('Security').get('SecurityType')
  if msgDict.get('Security').get('SymbolUnderlying'):
    msg += ' ' + msgDict.get('Security').get('SymbolUnderlying')

  msg += ') {Order Requested}** - '

  if optionTDAString:
    msg += '(' + optionTDAString + ') '

  msg += datetime.fromisoformat(parse(msgDict.get('OrderEnteredDateTime')).isoformat()).astimezone().strftime("%m-%d-%Y %H:%M:%S %Z")

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



  msg += '\n```'

  return msg

def orderFillFormatter(msgDict: dict):
  order = msgDict.get('OrderFillMessage').get('Order')
  execInfo = msgDict.get('OrderFillMessage').get('ExecutionInformation')

  msg = '**'

  sym = order.get('Security').get('Symbol')
  optionTDAString = None
  if '_' in sym:
    symSplit = sym.split('_')
    msg += '$' + symSplit[0] + ' '
    msg += symSplit[1][0:2] + '/' + symSplit[1][2:4] + '/' + symSplit[1][4:6] + ' ' + symSplit[1][6:]
    optionTDAString = '.' + symSplit[0] + symSplit[1][4:6] + symSplit[1][0:2] + symSplit[1][2:4] + symSplit[1][6:]
  else:
    msg += '$' + sym

  msg += ' (' + order.get('Security').get('SecurityType')
  if order.get('Security').get('SymbolUnderlying'):
    msg += ' ' + order.get('Security').get('SymbolUnderlying')

  msg += ') <<<Order Executed>>> ** - '

  if optionTDAString:
    msg += '(' + optionTDAString + ') '

  msg += datetime.fromisoformat(parse(execInfo.get('Timestamp')).isoformat()).astimezone().strftime("%m/%d/%Y %H:%M:%S %Z")

  msg += '\n```diff\n'

  quantity = execInfo.get('Quantity')
  if order.get('OrderInstructions') == 'Buy':
    msg += '+' + quantity + ' BOT - ' + execInfo.get('ExecutionPrice')

  if order.get('OrderInstructions') == 'Sell':
    msg += '-' + quantity + ' SOLD - ' + execInfo.get('ExecutionPrice')

  if optionTDAString:
    openClose = order.get('OpenClose')
    msg += ' to ' + openClose

  msg += '\n```'

  return msg
