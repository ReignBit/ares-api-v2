from sqlalchemy import Column, BigInteger, Date, Integer
from app.blueprints.kat.models.shared import db


class User(db.Model):
    __bind_key__ = "kat_backend"
    __tablename__ = "user_data"

    id = Column("user_id", BigInteger, primary_key=True)
    birthday = Column(Date, default=None)
    birthday_years = Column(Integer, default=0)

    def to_dict(self):
        return {'id': self.id, 'birthday': str(self.birthday), 'years': self.birthday_years}
