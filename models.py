import time
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


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, index=True)
    username = Column(String(length=32))
    group_id = Column(Integer, default=0)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)


class Items(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    hash_name = Column(String(length=30))
    item_count = Column(Integer)


Base.metadata.create_all(engine)


def add_close(user, session):
    session.add(user)
    session.commit()
    session.close()
    print("Successful adding")


def add_user(telegram_id, username):
    session = Session()
    user = session.query(Users).where(Users.telegram_id == telegram_id).first()
    if user is not None:
        print("User is already in database")
    else:
        user = Users(telegram_id=telegram_id, username=username)
        add_close(user, session)


def add_admin(telegram_id, username):
    session = Session()
    user = session.query(Users).where(Users.telegram_id == telegram_id).first()
    if user is not None:
        print("User is already in database")
    else:
        user = Users(username=username, telegram_id=telegram_id, group_id=2)
        add_close(user, session)


def change_access(telegram_id, group_id):
    session = Session()
    user = session.query(Users).where(Users.telegram_id == telegram_id).first()
    if user is not None:
        user.group_id = group_id
        user.updated_at = datetime.datetime.utcnow()
        session.commit()
        session.close()


def check_vip(telegram_id):
    user = session.query(Users).where(Users.telegram_id == telegram_id).first()
    user_group = user.group_id
    if user_group >= 1:
        return True
    else:
        return False


def check_admin(telegram_id):
    user = session.query(Users).where(Users.telegram_id == telegram_id).first()
    user_group = user.group_id
    if user_group >= 2:
        return True
    else:
        return False


def get_id(telegram_id):
    user = session.query(Users).where(Users.telegram_id == telegram_id).first()
    user_id = user.id
    return user_id


def add_item(telegram_id, hash_name, item_count):
    session = Session()
    user_id = get_id(telegram_id)
    item = session.query(Items).filter(Items.hash_name == hash_name).where(Items.user_id == user_id).first()
    if item is None:
        item = Items(user_id=user_id, hash_name=hash_name, item_count=item_count)
        session.add(item)
        session.commit()
        session.close()


def user_items(telegram_id):
    session = Session()
    user_id = get_id(telegram_id)
    items = session.query(Items).where(Items.user_id == user_id).all()
    user_item = {}
    for i in items:
        hash_name = i.hash_name
        item_count = i.item_count
        u = {hash_name: item_count}
        user_item.update(u)
    return user_item
