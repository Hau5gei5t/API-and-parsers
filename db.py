from sqlalchemy import create_engine, text, Column, Integer, String,ForeignKey,Update
from sqlalchemy.orm import declarative_base, Session, Relationship

Base = declarative_base()


class Price(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    brand_id = Column(Integer,ForeignKey("brands.id"))

    def __repr__(self):
        return f"{self.name} from {self.testing.name}"


class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String)
    items = Relationship("Price",backref="testing")




engine = create_engine(r'sqlite:///price.sqlite')
Base.metadata.create_all(bind=engine)

session = Session(bind=engine)
q = session.query(Brand).all()[1]
print(q.items)


