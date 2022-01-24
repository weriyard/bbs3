from bbs3.domain.model.ddd import Entity


class EntityJsonSerializer:
    def to_json(self, entity: Entity):
        pass

    def from_json(self, json: str) -> Entity:
        pass
