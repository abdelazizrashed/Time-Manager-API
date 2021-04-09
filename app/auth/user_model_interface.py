from mypy_extensions import TypedDict

class UserModelInterface(TypedDict, total = False):
    user_id: int
    is_admin: int
    username: str
    password: str
    email: str
    first_name: str
    last_name: str

    #TODO: remove __init__
    def __init__(self, user_id, is_admin, username, password, email, first_name, last_name):
        self.user_id = user_id
        self.is_admin = is_admin
        self.username = username
        self.password = password
        self. email = email
        self.first_name = first_name
        self.last_name = last_name