from mypy_extensions import TypedDict

class UserModelInterface(TypedDict, total = False):
    user_id: int
    is_admin: int
    username: str
    password: str
    email: str
    first_name: str
    last_name: str