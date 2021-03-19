from datetime import datetime

from flask_restful import Resource, reqparse, fields, marshal

from app.blueprints.kat.models.shared import db
from app.blueprints.kat.models.user import User
from app.blueprints.kat.common.auth import auth


user_fields = {"id": fields.Integer, "birthday": fields.String, "years": fields.Integer}


class UserListResource(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "id", type=int, required=True, help="No id provided", location="json"
        )
        self.reqparse.add_argument("birthday", type=str, location="json")
        self.reqparse.add_argument("years", type=int, location="json")
        super(UserListResource, self).__init__()

    def get(self):
        users = User.query.all()
        return {"data": [user.id for user in users]}

    def post(self):
        args = self.reqparse.parse_args()

        # TODO: come back to this, i'm not sure if it's needed.
        birthday = None
        if args.get('birthday'):
            try:
                birthday = datetime.strptime(args.get("birthday"), "%Y-%m-%d")
            except TypeError:
                pass

        if User.query.filter_by(id=args["id"]).first():
            return {"message": f"User `{args['id']}` already exists!"}, 409

        user = User(
            id=args["id"],
            birthday=birthday,
            birthday_years=args["years"],
        )
        db.session.add(user)
        db.session.commit()
        return {
            "message": "User added successfully",
            "data": marshal(user, user_fields),
        }, 201


class UserResource(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("birthday", type=str, location="json")
        self.reqparse.add_argument("years", type=int, location="json")
        super(UserResource, self).__init__()

    def get(self, id):
        user = User.query.filter_by(id=id).first_or_404(
            description=f"No user with id `{id}`"
        )
        return {"data": [marshal(user.to_dict(), user_fields)]}

    def patch(self, id):
        args = self.reqparse.parse_args()
        user = User.query.filter_by(id=id).first_or_404(
            description=f"No user with id `{id}`"
        )
        user.birthday = datetime.strptime(
            args.get("birthday", user.birthday_years), "%Y-%m-%d"
        )
        user.birthday_years = args.get("years", user.birthday_years)
        db.session.commit()
        return {"message": f"Updated user `{id}`", "data": marshal(user, user_fields)}

    def delete(self, id):
        user = User.query.filter_by(id=id).first_or_404(
            description=f"No user with id `{id}`"
        )
        db.session.delete(user)
        db.session.commit()
        return {"message": f"Deleted user `{id}`"}
