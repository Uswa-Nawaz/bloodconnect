import bcrypt
from repository import UserRepository, RequestRepository
from schemas import UserSignupRequest, UserLoginRequest,RequestCreate

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

    def approve_user(self, admin_id: int, user_id: int):
        self.verify_admin(admin_id)
        approved_user=self.repository.update_status(user_id, "approved")
        return approved_user

    def reject_user(self, admin_id: int, user_id: int):
        self.verify_admin(admin_id)
        rejected_user=self.repository.update_status(user_id, "rejected")
        return rejected_user
    
    def suspend_user(self, admin_id: int, user_id: int):
        self.verify_admin(admin_id)
        suspended_user = self.repository.update_status(user_id, "suspended")
        return suspended_user

class RequestService:
    def __init__(self, repository: RequestRepository, user_repository: UserRepository):
        self.repository = repository
        self.user_repository = user_repository

    def verify_owner(self, user_id: int, request_id: int):
        request = self.repository.get_by_id(request_id)
        if not request:
            raise ValueError("Request not found")
        if request.requestor_id != user_id:
            raise ValueError("You do not own this request")
        return request

    def submit_request(self, user_id: int, request_data: RequestCreate):
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("Invalid user")
        if user.status != "approved":
            raise ValueError("Account not approved yet")

        data = request_data.model_dump()
        data["requestor_id"] = user_id
        new_request = self.repository.create_request(data)
        return new_request

    def cancel_request(self, user_id: int, request_id: int):
        request = self.verify_owner(user_id, request_id)
        if request.status != "pending":
            raise ValueError("Only pending requests can be cancelled")
        return self.repository.update_status(request_id, "cancelled")

    def get_my_requests(self, user_id: int):
        return self.repository.get_by_requestor(user_id)