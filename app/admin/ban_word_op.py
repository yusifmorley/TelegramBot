from sqlalchemy.orm import Session

from app.model.models import BanWord


class BanWord_OP:
    def __init__(self, session: Session):
        self.session = session

    def insert(self, text):
        bw = BanWord(id=None, word=text)
        self.session.add(bw)
        self.session.commit()

    def select(self):
        return self.session.query(BanWord).all()
