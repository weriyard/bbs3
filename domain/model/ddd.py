from dataclasses import dataclass

from dataclasses import dataclass


@dataclass
class Entity:
    id: str


@dataclass
class AggregateRoot(Entity):
    pass
