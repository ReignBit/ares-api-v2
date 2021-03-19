import json
from sqlalchemy import Column, BigInteger, TEXT, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.blueprints.kat.models.shared import db


class Member(db.Model):
    __bind_key__ = "kat_backend"
    __tablename__ = "member_data"

    gid = Column("guild_id", BigInteger, ForeignKey('guild_data.guild_id'), primary_key=True)
    uid = Column("user_id", BigInteger, ForeignKey('user_data.user_id'), primary_key=True)
    _settings = Column("data", TEXT, default="{}")
    xp = Column("xp", Integer, default=1)
    level = Column("lvl", Integer, default=1)

    user = relationship("User")
    guild = relationship("Guild")

    @property
    def settings(self):
        # If the json becomes unreadable then empty it
        try:
            return json.loads(self._settings)
        except (json.decoder.JSONDecodeError, TypeError):
            self._settings = {}
            return {}

    @settings.setter
    def settings(self, new: dict):
        self._settings = json.dumps(new)

    def to_dict(self):
        return {
            "gid": self.gid,
            "id": self.uid,
            "xp": self.xp,
            "level": self.level,
            "settings": self.settings
        }
