import json
from sqlalchemy import Column, Integer, TEXT, Boolean, VARCHAR
from sqlalchemy.sql.expression import column
from app.blueprints.supervisor.models.shared import db

class Service(db.Model):
    __bind_key__ = "supervisor_backend"
    __tablename__ = "services"

    id          = Column("id",          VARCHAR(11), primary_key=True)
    name        = Column("name",        TEXT(), default="Untitled Service")
    timestamp   = Column("timestamp",   Integer(), default=0)
    mem         = Column("ram_req",     Integer(), default=0)
    status      = Column("status",      Boolean(), default=False)
    pid         = Column("pid",         Integer(), default=-1)
    dir         = Column("dir",         TEXT(), default="")
    exec        = Column("exec",        TEXT(), default="")
    args        = Column("args",        TEXT(), default="")
    keep_alive  = Column("keep_alive",  Boolean(), default=False)
    can_vote    = Column("can_vote",    Boolean(), default=False)

    @classmethod
    def from_dict(cls, data):
        service = cls(
            id=data['id'],
            name=data["name"],
            timestamp=data["timestamp"],
            mem=data["mem"],
            status=data["status"],
            pid=data["pid"],
            dir=data["dir"],
            exec=data["exec"],
            args=data["args"],
            keep_alive=data["keep_alive"],
            can_vote=data["can_vote"]
        )
        return service


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "timestamp": self.timestamp,
            "mem": self.mem,
            "status": self.status,
            "pid": self.pid,
            "dir": self.dir,
            "exec": self.exec,
            "args": self.args,
            "keep_alive": self.keep_alive,
            "can_vote": self.can_vote
        }

