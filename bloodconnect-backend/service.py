import bcrypt
from repository import UserRepository
from schemas import UserSignupRequest, UserLoginRequest

class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def signup(self, signup_data: UserSignupRequest):
        existing_user = self.repository.get_by_email(signup_data.email)
        if existing_user:
            raise ValueError("Email already registered")

        hashed_password = bcrypt.hashpw(
            signup_data.password.encode("utf-8"), bcrypt.gensalt()
        )

        user_data = signup_data.model_dump(exclude={"password"})
        user_data["password_hash"] = hashed_password.decode("utf-8")

        new_user = self.repository.create_user(user_data)
        return new_user

    def login(self, login_data: UserLoginRequest):
        user = self.repository.get_by_email(login_data.email)
        if not user:
            raise ValueError("Invalid email or password")

        password_matches = bcrypt.checkpw(
            login_data.password.encode("utf-8"),
            user.password_hash.encode("utf-8")
        )
        if not password_matches:
            raise ValueError("Invalid email or password")

        return user

    def verify_admin(self, admin_id: int):
        user = self.repository.get_by_id(admin_id)
        if not user:
            raise ValueError("Invalid user")
        if not user.role=="Admin":
            raise ValueError("User is not Admin")
        return user
