from bbs3.infrastructure.inbox_adapter import IndexRepositoryAdapeter


class InboxUnitOfWork:
    def __init__(self, session_factory):
        self.session = session_factory()

    @property
    def inbox(self) -> IndexRepositoryAdapeter:
        return IndexRepositoryAdapeter(self.session)
