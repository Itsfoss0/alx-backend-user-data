"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import (User, Base)


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_pwd: str) -> User:
        """"
        Add a user to the session for persistene
        Args:
            email (str): user email
            hashed_pwd (str): Hashed password
        Returns:
            returns the user object
        """
        # session = Session(bind=self._engine)
        user_creds = {
            "email": email,
            "hashed_password": hashed_pwd
        }
        user = User(**user_creds)
        self._session.add(user)
        self._session.commit()
        return user
