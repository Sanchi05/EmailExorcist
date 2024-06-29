import keyring

keyring.set_password("apiKey", "API_KEY", "90345a7be1a806d2b57a03e88a71e6f9c440613f6be9b367cc253c13019f830b")

def getAPIKey():
    return keyring.get_password("apiKey", "API_KEY")

# print(type(getAPIKey()))