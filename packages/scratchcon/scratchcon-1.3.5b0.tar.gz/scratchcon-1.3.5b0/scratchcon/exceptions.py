class FailedToRetrieve(Exception):
    def __init__(self, message="Failed to retrieve data from URL"):
        super().__init__(message)


class FailedToLogin(Exception):
    def __init__(self, message="Failed to log in"):
        super().__init__(message)
