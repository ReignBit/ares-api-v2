from flask import Blueprint
from flask_restful import Api

from app.blueprints.kat.resources.user import UserListResource, UserResource
from app.blueprints.kat.resources.guild import GuildListResource, GuildResource
from app.blueprints.kat.resources.member import MemberListResource, MemberResource


blueprint = Blueprint("kat_backend", __name__)
api = Api(blueprint)

# User Resources
api.add_resource(UserListResource, "/users", endpoint="users")
api.add_resource(UserResource, "/users/<int:id>", endpoint="user")

# Guild Resources
api.add_resource(GuildListResource, "/guilds", endpoint="guilds")
api.add_resource(GuildResource, "/guilds/<int:id>", endpoint="guild")

# Member Resources
api.add_resource(
    MemberListResource, "/guilds/<int:gid>/members", endpoint="members"
)
api.add_resource(
    MemberResource, "/guilds/<int:gid>/<int:uid>", endpoint="member"
)
