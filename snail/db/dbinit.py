# coding:utf-8
__author__ = 'hy'

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, AbstractConcreteBase, declared_attr
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer

from snail.logger import log

from settings import DATABASES

engine = create_engine(
    # "mysql+pymysql://root:root@127.0.0.1:3306/dbtest?charset=utf8",
    '{0}+{1}://{2}:{3}@{4}:{5}/{6}?charset=utf8'.format(
        DATABASES.get('ENGINE'),
        DATABASES.get('DRIVER'),
        DATABASES.get('USER'),
        DATABASES.get('PASSWORD'),
        DATABASES.get('HOST'),
        DATABASES.get('PORT'),
        DATABASES.get('NAME'),
    ),
    max_overflow=5)
Base = declarative_base()


def create_table():
    '''
    创建表
    :return:
    '''
    Base.metadata.create_all(engine)


def drop_table():
    '''
    删除表
    :return:
    '''
    Base.metadata.drop_all(engine)


Session = sessionmaker(bind=engine)
session = Session()


def session_wrapper(func):
    '''
    数据库操作如果有异常，则回退;无异常，则提交
    '''
    def inner(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception:
            session.rollback()
            log('db rollback')
        else:
            # 提交即保存到数据库:
            session.commit()
            return func(*args, **kwargs)
        session.close()

    return inner


class Model(AbstractConcreteBase, Base):
    '''
    给继承该类的类（表），一个默认主键id,表名为类的小写
    '''
    id = Column(Integer, primary_key=True, autoincrement=True)

    @declared_attr
    def __tablename__(cls):
        if cls.__name__ != 'Model':
            return cls.__name__.lower()

    @declared_attr
    def __mapper_args__(cls):
        return {'polymorphic_identity': cls.__name__.lower(),
                'concrete': True} if cls.__name__ != "Model" else {}