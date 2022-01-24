import argparse
import datetime
import json
import os
from datetime import datetime

from bbs3.application import config
from bbs3.application.utils import user_signature_generator
from bbs3.domain.model.unit_of_work import InboxUnitOfWork
from bbs3.domain.ports.incoming.inbox_service import InboxService
from bbs3.infrastructure.orm import metadata
from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.debug = True

session_factory = sessionmaker(
    bind=create_engine(
        config.db_uri,
    )
)


@app.route("/api/inbox", methods=["POST"])
def create_inbox():
    #  TODO: user jsonschema validator
    data = request.json
    uow = InboxUnitOfWork(session_factory)
    inbox_service = InboxService(uow.inbox)
    inbox_id = inbox_service.create(
        topic=data["topic"],
        owner=user_signature_generator(data["username"], data["secret"]),
        expiration_date=datetime.now(),
        allow_anonymous=data["allow_anonymous"],
    )
    return json.dumps({"inbox_id": str(inbox_id)})


@app.route("/api/inbox", methods=["GET"])
def get_inboxes():
    uow = InboxUnitOfWork(session_factory)
    inboxes = uow.inbox.get_all_inboxes()
    return json.dumps((list(map(str, inboxes))))


@app.route("/api/inbox/<string:inbox_id>/reply", methods=["POST"])
def reply_to_inbox(inbox_id):
    data = request.json
    user_signature = user_signature_generator(data["username"], data["secret"])
    uow = InboxUnitOfWork(session_factory)
    inbox_service = InboxService(
        uow.inbox,
    )
    reply = inbox_service.reply_to_inbox(user_signature, inbox_id, data["reply"])
    return json.dumps(str(reply))


@app.route("/api/inbox/<string:inbox_id>/reply", methods=["GET"])
def get_inbox_replies(inbox_id):
    data = request.args
    user_signature = user_signature_generator(data["username"], data["secret"])
    uow = InboxUnitOfWork(session_factory)
    inbox_replies = InboxService(uow.inbox).get_inbox_replies(user_signature, inbox_id=inbox_id)
    return json.dumps((list(map(str, inbox_replies))))


if __name__ == "__main__":

    def run_app(args):
        app.run(host="0.0.0.0", port=5001)

    def create_db(args):
        if args.force:
            os.remove(config.db_name)
        engine = create_engine(
            config.db_uri,
        )
        metadata.create_all(engine)

    parser = argparse.ArgumentParser(description="Hello in BBS3 app !")

    subparsers = parser.add_subparsers()
    app_parser = subparsers.add_parser("run", help="Starts application :-)")
    app_parser.set_defaults(func=run_app)
    db_subparser = subparsers.add_parser("create-db", help="Database tools.")
    db_subparser.set_defaults(func=create_db)
    db_subparser.add_argument("--force", action="store_true", help="If database exists, remove this beforce crate new.")

    args = parser.parse_args()
    args.func(args)
