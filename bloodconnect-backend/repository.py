from sqlalchemy.orm import Session
from models import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def create_user(self, user_data: dict):
        new_user = User(**user_data)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def get_pending_users(self):
        return self.db.query(User).filter(User.status == "pending").all()

    def get_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def update_status(self, user_id: int, new_status: str):
        user = self.get_by_id(user_id)
        user.status = new_status
        self.db.commit()
        self.db.refresh(user)
        return user

