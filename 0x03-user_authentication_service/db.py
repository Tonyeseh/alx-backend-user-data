#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine(
            "sqlite:///a.db",
            echo=True,
            connect_args={
                "check_same_thread": False})
        Base.metadata.drop_all(self._engine, )
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

    def add_user(self, email: str, hashed_password: str) -> User:
        """saves a user to the database and returns the user"""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()

        return user

    def find_user_by(self, **kwargs: dict):
        """returns the first row found in users table filtered by kwargs"""
        result = self._session.query(User).filter_by(**kwargs).first()

        if result is None:
            raise NoResultFound("No Result was found")
        return result

    def update_user(self, user_id: int, **kwargs: dict) -> None:
        """updates the user with the given user_id"""
        user = self.find_user_by(id=user_id)

        user_att = vars(user)

        for k, v in kwargs.items():
            if k in user_att.keys():
                setattr(user, k, v)
            else:
                raise ValueError("Invalid attribute")

        self._session.commit()
