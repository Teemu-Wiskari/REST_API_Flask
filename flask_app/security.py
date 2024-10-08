from hashlib import md5


def hash_password(password: str) -> str:
    password: bytes = password.encode()
    hashed_password = md5(password).hexdigest()
    return hashed_password


class HttpError(Exception):
    """Класс ошибок"""

    def __init__(
            self,
            status_code: int,
            message: dict | list | str
            ):

        self.status_code = status_code
        self.message = message