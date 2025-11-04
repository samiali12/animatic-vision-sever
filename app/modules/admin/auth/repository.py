from core.logger import logger
from database.session import session
from app.database.models.user import User, UserRole
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from core.exceptions import (
    DatabaseConnectionError,
    InvalidCredentialsError,
    UserAlreadyExistsError,
)
from core.security import verify_password


class AdminAuthRepository:
    def __init__(self):
        self.db = session()

    def login_admin(self, email: str, password: str) -> User:
        try:
            user = (
                self.db.query(User)
                .filter(User.email == email, User.role == UserRole.admin)
                .first()
            )
            if not user:
                raise InvalidCredentialsError(message="Invalid email or role")
            if not verify_password(user.password, password):
                raise InvalidCredentialsError(message="Invalid password")
            return user
        except InvalidCredentialsError:
            raise
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error during admin login: {str(e)}")
            raise DatabaseConnectionError()

    def me_admin(self, email: str) -> User | None:
        try:
            user = (
                self.db.query(User)
                .filter(User.email == email, User.role == UserRole.admin)
                .first()
            )
            return user
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error during admin me: {str(e)}")
            raise DatabaseConnectionError()

    def create_admin(self, fullName: str, email: str, password_hash: str) -> User:
        try:
            user = User(fullName=fullName, email=email, password=password_hash, role=UserRole.admin)
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except IntegrityError:
            self.db.rollback()
            raise UserAlreadyExistsError(email)
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error during admin creation: {str(e)}")
            raise DatabaseConnectionError()


