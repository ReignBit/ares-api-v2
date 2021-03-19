import json
from sqlalchemy import Column, BigInteger, TEXT
from app.blueprints.kat.models.shared import db


class Guild(db.Model):
    __bind_key__ = "kat_backend"
    __tablename__ = "guild_data"

    id = Column("guild_id", BigInteger, primary_key=True)
    _settings = Column("guild_settings", TEXT(), default="{}")

    @property
    def settings(self):
        # If the json becomes unreadable then empty it
        try:
            return json.loads(self._settings)
        except json.decoder.JSONDecodeError:
            self._settings = {}
            return {}

    @settings.setter
    def settings(self, new: dict):
        self._settings = json.dumps(new)

    def to_dict(self):
        return {"id": self.id, "settings": self.settings}
