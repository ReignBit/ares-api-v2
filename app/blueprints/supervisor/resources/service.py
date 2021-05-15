from flask_restful import Resource, reqparse, fields, marshal

from app.blueprints.supervisor.models.shared import db
from app.blueprints.supervisor.models.service import Service # , PublicService
from app.blueprints.kat.common.auth import auth


service_fields = {
    "id": fields.String(),
    "name": fields.String(),
    "timestamp": fields.Integer(),
    "mem": fields.Integer(),
    "status": fields.Boolean(),
    "pid": fields.Integer(),
    "dir": fields.String(),
    "exec": fields.String(),
    "args": fields.String(),
    "can_vote": fields.Boolean(),
    "keep_alive": fields.Boolean(),
}

public_service_fields = {
    "id": fields.String(),
    "status": fields.Integer(),
    "keep_alive": fields.Boolean(),
    "can_vote": fields.Boolean()
}


class ServiceListResource(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("id", type=str, required=True, help="No id provided", location="json")
        self.reqparse.add_argument("name", type=str, location="json")
        self.reqparse.add_argument("timestamp", type=int, location="json")
        self.reqparse.add_argument("mem", type=int, location="json")
        self.reqparse.add_argument("status", type=bool, location="json")
        self.reqparse.add_argument("pid", type=int, location="json")
        self.reqparse.add_argument("dir", type=str, location="json")
        self.reqparse.add_argument("exec", type=str, location="json")
        self.reqparse.add_argument("args", type=str, location="json")
        self.reqparse.add_argument("keep_alive", type=bool, location="json")
        self.reqparse.add_argument("can_vote", type=bool, location="json")
        super(ServiceListResource, self).__init__()

    def get(self):
        services = Service.query.all()
        return {"data": [marshal(service, service_fields) for service in services]}

    def post(self):
        args = self.reqparse.parse_args()

        if Service.query.filter_by(id=args["id"]).first():
            return {"message": f"Service `{args['id']}` already exists!"}, 409

        service = Service.from_dict(args)
        db.session.add(service)
        db.session.commit()
        return {
            "message": "Service added successfully",
            "data": marshal(service, service_fields),
        }, 201


class ServiceResource(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("name", type=str, location="json")
        self.reqparse.add_argument("timestamp", type=int, location="json")
        self.reqparse.add_argument("mem", type=int, location="json")
        self.reqparse.add_argument("status", type=bool, location="json")
        self.reqparse.add_argument("pid", type=int, location="json")
        self.reqparse.add_argument("dir", type=str, location="json")
        self.reqparse.add_argument("exec", type=str, location="json")
        self.reqparse.add_argument("args", type=str, location="json")
        self.reqparse.add_argument("keep_alive", type=bool, location="json")
        self.reqparse.add_argument("can_vote", type=bool, location="json")
        super(ServiceResource, self).__init__()

    def get(self, id):
        service = Service.query.filter_by(id=id).first_or_404(
            description=f"No service with id `{id}`"
        )
        return {"data": [marshal(service, service_fields)]}

    def patch(self, id):
        args = self.reqparse.parse_args()
        service = Service.query.filter_by(id=id).first_or_404(
            description=f"No service with id `{id}`"
        )

        # Update attributes
        for k,v in args.items():
            if v is None:
                setattr(service, k, getattr(service, k))
            else:
                setattr(service, k, v)

        db.session.commit()
        return {
            "message": f"Updated service `{id}`",
            "data": marshal(service, service_fields),
        }

    def delete(self, id):
        service = Service.query.filter_by(id=id).first_or_404(
            description=f"No service with id `{id}`"
        )
        db.session.delete(service)
        db.session.commit()
        return {"message": f"Deleted service `{id}`"}
