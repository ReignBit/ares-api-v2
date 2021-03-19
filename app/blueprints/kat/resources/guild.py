from flask_restful import Resource, reqparse, fields, marshal

from app.blueprints.kat.models.shared import db
from app.blueprints.kat.models.guild import Guild
from app.blueprints.kat.common.auth import auth


guild_fields = {
    "id": fields.Integer,
    "settings": fields.Raw,
}


class GuildListResource(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "id", type=int, required=True, help="No id provided", location="json"
        )
        self.reqparse.add_argument("settings", type=dict, location="json")
        super(GuildListResource, self).__init__()

    def get(self):
        guilds = Guild.query.all()
        return {"data": [guild.id for guild in guilds]}

    def post(self):
        args = self.reqparse.parse_args()

        if Guild.query.filter_by(id=args["id"]).first():
            return {"message": f"Guild `{args['id']}` already exists!"}, 409

        guild = Guild(id=args["id"], _settings=args["settings"])
        db.session.add(guild)
        db.session.commit()
        return {
            "message": "Guild added successfully",
            "data": marshal(guild, guild_fields),
        }, 201


class GuildResource(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("settings", type=dict, location="json")
        super(GuildResource, self).__init__()

    def get(self, id):
        guild = Guild.query.filter_by(id=id).first_or_404(
            description=f"No guild with id `{id}`"
        )
        return {"data": [marshal(guild.to_dict(), guild_fields)]}

    def patch(self, id):
        args = self.reqparse.parse_args()
        guild = Guild.query.filter_by(id=id).first_or_404(
            description=f"No guild with id `{id}`"
        )

        guild.settings = args.get("settings", guild.settings)
        db.session.commit()
        return {
            "message": f"Updated guild `{id}`",
            "data": marshal(guild, guild_fields),
        }

    def delete(self, id):
        guild = Guild.query.filter_by(id=id).first_or_404(
            description=f"No guild with id `{id}`"
        )
        db.session.delete(guild)
        db.session.commit()
        return {"message": f"Deleted guild `{id}`"}
