from sqlalchemy.schema import Column, MetaData, Table
from sqlalchemy.types import Integer, Text

metadata = MetaData()

Inbox = Table(
    "inbox",
    metadata,
    Column("id", Text(), unique=True, nullable=False, primary_key=True),
    Column("topic", Text(), nullable=False),
    Column("owner", Text(), nullable=False),
    Column("expiration_date", Text(), nullable=False),
    Column("allow_anonymous", Integer(), nullable=False),
)

Reply = Table(
    "reply",
    metadata,
    Column("inbox_id", Text(), nullable=False),
    Column("body", Text(), nullable=True),
    Column("user", Text(), nullable=True),
    Column("timestamp", Text(), nullable=False),
)
