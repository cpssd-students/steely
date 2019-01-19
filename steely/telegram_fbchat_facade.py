class Client:
    '''Acts as a facade on fbchat bots to allow them to be backed by Telegram
    instead. ie., Provides API compatibility.'''

    def __init__(self, email, password):
        pass

    def listen(self):
        pass

def log(*args, **kwargs):
    print("log:", *args, *kwargs)
