from sqlalchemy import Column, Integer, String, DateTime, BigInteger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
import datetime
from data.config import host, user, password, db_name
import pg8000

Base = declarative_base()

engine = create_engine(f'postgresql+pg8000://{user}:{password}@{host}/{db_name}', echo=False)

Session = sessionmaker(bind=engine)
session = scoped_session(Session)
conn = engine.connect()


# noinspection PyTypeChecker,PyMethodParameters,PyShadowingNames
class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, index=True)
    username = Column(String(length=32))
    group_id = Column(Integer, default=0)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    def add_user(telegram_id: int, username: str):
        session = Session()
        user = session.query(Users).where(Users.telegram_id == telegram_id).first()
        if user is not None:
            pass
        else:
            user = Users(telegram_id=telegram_id, username=username)
            Users.add_close(user, session)

    def add_close(user, session):
        session.add(user)
        session.commit()
        session.close()

    def add_admin(telegram_id: int, username: str):
        session = Session()
        user = session.query(Users).where(Users.telegram_id == telegram_id).first()
        if user is not None:
            print("User is already in database")
        else:
            user = Users(username=username, telegram_id=telegram_id, group_id=2)
            Users.add_close(user, session)

    def change_access(telegram_id: int, group_id: int):
        session = Session()
        user = session.query(Users).where(Users.telegram_id == telegram_id).first()
        if user is not None:
            user.group_id = group_id
            user.updated_at = datetime.datetime.utcnow()
            session.commit()
            session.close()

    def check_vip(telegram_id: int) -> object:
        user = session.query(Users).where(Users.telegram_id == telegram_id).first()
        user_group = user.group_id
        if user_group >= 1:
            return True
        else:
            return False

    def check_admin(telegram_id: int) -> object:
        user = session.query(Users).where(Users.telegram_id == telegram_id).first()
        user_group = user.group_id
        if user_group >= 2:
            return True
        else:
            return False

    def get_id(telegram_id: int) -> object:
        user = session.query(Users).where(Users.telegram_id == telegram_id).first()
        user_id = user.id
        return user_id


# noinspection PyTypeChecker,PyShadowingNames,PyMethodParameters
class Items(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    hash_name = Column(String(length=30))
    item_count = Column(Integer)

    def add_item(telegram_id: int, hash_name: str, item_count: int):
        session = Session()
        user_id = Users.get_id(telegram_id)
        item = session.query(Items).filter(Items.hash_name == hash_name).where(Items.user_id == user_id).first()
        if item is None:
            item = Items(user_id=user_id, hash_name=hash_name, item_count=item_count)
            session.add(item)
            session.commit()
            session.close()
        else:
            item.item_count = item_count
            session.commit()
            session.close()

    def user_items(telegram_id: int) -> object:
        session = Session()
        user_id = Users.get_id(telegram_id)
        items = session.query(Items).where(Items.user_id == user_id).all()
        user_item = {}
        for i in items:
            hash_name = i.hash_name
            item_count = i.item_count
            u = {hash_name: item_count}
            user_item.update(u)
        return user_item

    def delete_item(telegram_id: int, hash_name: str):
        session = Session()
        user_id = Users.get_id(telegram_id)
        item = session.query(Items).filter(Items.hash_name == hash_name).where(Items.user_id == user_id).first()
        session.delete(item)
        session.commit()


# noinspection PyShadowingNames,PyMethodParameters
class LogBase(Base):
    __tablename__ = "functions_log"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, index=True)
    username = Column(String(length=32))
    function_name = Column(String(length=12))

    def add(telegram_id: int, username: str, function_name: str):
        session = Session()
        func = LogBase(telegram_id=telegram_id, username=username, function_name=function_name)
        session.add(func)
        session.commit()
        session.close()


Base.metadata.create_all(engine)
