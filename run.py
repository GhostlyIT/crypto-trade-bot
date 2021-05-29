from HttpClient.BTCAlphaClient import BTCAlphaClient

client = BTCAlphaClient()

print(client.get_wallet_info('BTC').text)
