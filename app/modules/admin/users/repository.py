from typing import List, Tuple
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Query
from core.logger import logger
from core.exceptions import DatabaseConnectionError, UserAlreadyExistsError
from database.session import session
from app.database.models.user import User, UserRole


class AdminUserRepository:
    def __init__(self):
        self.db = session()

    def _base_query(self) -> Query:
        return self.db.query(User)

    def list_users(
        self, search: str | None, role: str | None, page: int, limit: int
    ) -> Tuple[List[User], int]:
        try:
            q = self._base_query()
            if search:
                like = f"%{search}%"
                q = q.filter((User.fullName.ilike(like)) | (User.email.ilike(like)))
            if role in {"admin", "user"}:
                q = q.filter(User.role == UserRole(role))

            total = q.count()
            items = q.order_by(User.created_at.desc()).offset((page - 1) * limit).limit(limit).all()
            return items, total
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error listing users: {str(e)}")
            raise DatabaseConnectionError()

    def get_user(self, user_id: int) -> User | None:
        try:
            return self._base_query().filter(User.id == user_id).first()
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error get user: {str(e)}")
            raise DatabaseConnectionError()

    def create_user(self, full_name: str, email: str, password_hash: str, role: str) -> User:
        try:
            u = User(fullName=full_name, email=email, password=password_hash, role=UserRole(role))
            self.db.add(u)
            self.db.commit()
            self.db.refresh(u)
            return u
        except IntegrityError:
            self.db.rollback()
            raise UserAlreadyExistsError(email)
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error create user: {str(e)}")
            raise DatabaseConnectionError()

    def update_user(
        self,
        user_id: int,
        full_name: str | None,
        email: str | None,
        role: str | None,
        password_hash: str | None,
    ) -> User | None:
        try:
            u = self.get_user(user_id)
            if not u:
                return None
            if full_name is not None:
                u.fullName = full_name
            if email is not None:
                u.email = email
            if role in {"admin", "user"}:
                u.role = UserRole(role)
            if password_hash is not None:
                u.password = password_hash
            self.db.commit()
            self.db.refresh(u)
            return u
        except IntegrityError:
            self.db.rollback()
            # Likely email unique constraint
            raise UserAlreadyExistsError(email or "")
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error update user: {str(e)}")
            raise DatabaseConnectionError()

    def update_user_role(self, user_id: int, role: str) -> User | None:
        return self.update_user(user_id, None, None, role, None)

    def update_user_password(self, user_id: int, password_hash: str) -> User | None:
        return self.update_user(user_id, None, None, None, password_hash)

    def delete_user(self, user_id: int) -> bool:
        try:
            u = self.get_user(user_id)
            if not u:
                return False
            self.db.delete(u)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error delete user: {str(e)}")
            raise DatabaseConnectionError()


