from flask_restful import Resource, reqparse, fields, marshal

from app.blueprints.kat.models.shared import db
from app.blueprints.kat.models.member import Member
from app.blueprints.kat.common.auth import auth


member_fields = {
    "gid": fields.Integer,
    "id": fields.Integer,
    "settings": fields.Raw,
    "xp": fields.Integer,
    "level": fields.Integer,
}


class MemberListResource(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "id", type=int, required=True, help="No id provided", location="json"
        )
        self.reqparse.add_argument("settings", type=dict, location="json")
        self.reqparse.add_argument("xp", type=int, location="json")
        self.reqparse.add_argument("level", type=int, location="json")
        super(MemberListResource, self).__init__()

    def get(self, gid):
        members = Member.query.filter_by(gid=gid).all()
        return {"data": [member.to_dict() for member in members]}

    def post(self, gid):
        args = self.reqparse.parse_args()

        if Member.query.filter_by(gid=gid, uid=args["id"]).first():
            return {"message": f"Member `{args['id']}` already exists!"}, 409

        member = Member(
            gid=gid,
            uid=args["id"],
            settings=args["settings"],
            xp=args["xp"],
            level=args["level"],
        )
        db.session.add(member)
        db.session.commit()
        return {
            "message": "Member added successfully",
            "data": marshal(member, member_fields),
        }, 201


class MemberResource(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("xp", type=int, location="json")
        self.reqparse.add_argument("level", type=int, location="json")
        self.reqparse.add_argument("settings", type=dict, location="json")
        super(MemberResource, self).__init__()

    def get(self, gid, uid):
        member = Member.query.filter_by(gid=gid, uid=uid).first_or_404(
            description=f"No member with id `{uid}` in guild `{gid}`"
        )
        return {"data": [marshal(member.to_dict(), member_fields)]}

    def patch(self, gid, uid):
        args = self.reqparse.parse_args()
        member = Member.query.filter_by(gid=gid, uid=uid).first_or_404(
            description=f"No member with id `{uid}` in guild `{gid}`"
        )
        member.settings = args.get("settings", member.settings)
        member.xp = args.get("xp", member.xp)
        member.level = args.get("level", member.level)

        db.session.commit()
        return {
            "message": f"Updated member `{uid}` in guild `{gid}`",
            "data": marshal(member, member_fields),
        }

    def delete(self, gid, uid):
        member = Member.query.filter_by(gid=gid, uid=uid).first_or_404(
            description=f"No member with id `{uid}` in guild `{gid}`"
        )
        db.session.delete(member)
        db.session.commit()
        return {"message": f"Deleted member `{id}`"}
