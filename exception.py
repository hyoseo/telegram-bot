class EmptyTokenError(Exception):
    def __init__(self):
        super().__init__('Token is empty. You must pass token. Ex) TOKEN=f3578dklvbdlja324_324 <- Environment Variable')
