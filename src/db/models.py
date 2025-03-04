from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Barcode(Base):
    __tablename__ = "barcodes"

    barcode = Column(String, primary_key=True)
    product_name = Column(String)
    brand = Column(String)

    def __repr__(self):
        return f"<Barcode(barcode={self.barcode}, product_name={self.product_name}, brand={self.brand})>"


class DatabaseManager:
    def __init__(self, db_url="sqlite:///database.db"):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def init_db(self):
        Base.metadata.create_all(self.engine)

    def get_session(self):
        return self.Session()

    def add_barcode(self, barcode: str, product_name: str, brand: str) -> Barcode:
        session = self.get_session()
        try:
            barcode_entry = Barcode(
                barcode=barcode, product_name=product_name, brand=brand
            )
            session.add(barcode_entry)
            session.commit()
            # Make a detached copy of attributes before closing the session
            result = {
                "barcode": barcode_entry.barcode,
                "product_name": barcode_entry.product_name,
                "brand": barcode_entry.brand,
            }
            return result
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_barcode(self, barcode: str) -> Barcode:
        session = self.get_session()
        try:
            return session.query(Barcode).filter(Barcode.barcode == barcode).first()
        finally:
            session.close()

    def get_all_barcodes(self) -> list[Barcode]:
        session = self.get_session()
        try:
            return session.query(Barcode).all()
        finally:
            session.close()

    def delete_barcode(self, barcode: str) -> bool:
        session = self.get_session()
        try:
            result = session.query(Barcode).filter(Barcode.barcode == barcode).delete()
            session.commit()
            return result > 0
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
