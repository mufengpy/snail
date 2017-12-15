# coding:utf-8 
__author__ = 'hy'
from snail.db import Model
from sqlalchemy import Column, Integer, String, UniqueConstraint


class User(Model):
    username = Column(String(32))
    password = Column(String(32))

    __table_args__ = (
        UniqueConstraint('username', 'password', name='uix_id_name'),
    )

