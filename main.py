# "postgresql://username:password@host/dbname"
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

DATABASE_URL = "postgresql://hello:1@localhost/product_items"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    string = Column(String)
    description = Column(String)
    price = Column(Integer)

Base.metadata.create_all(bind=engine)

ItemPydantic = sqlalchemy_to_pydantic(Item, exclude=['id'])

db_item = ItemPydantic(string='Item 3', description='pesc', price=100)


def create_item(db_item: ItemPydantic):
    db_item = Item(**db_item.dict())
    with SessionLocal() as db:
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
    return db_item


def get_items():
    result = []
    with SessionLocal() as db:
        items = db.query(Item).all()
        for item in items:
            result.append({'name': item.string, 'description': item.description, 'price': item.price})
    return result


def retrieve_item(item_id):
    with SessionLocal() as db:
        retrieved_item = db.query(Item).filter_by(id=item_id).first()
    return {'name': retrieved_item.string, 'description': retrieved_item.description, 'price': retrieved_item.price}


def update_item(item_id, n_name, n_desc, n_price):
    with SessionLocal() as db:
        db.query(Item).filter_by(id=item_id).update({'string': n_name, 'description': n_desc, 'price': n_price})
        db.commit()
        updated_item = db.query(Item).filter_by(id=item_id).first()
    return {'name': updated_item.string, 'description': updated_item.description, 'price': updated_item.price}


def delete_item(item_id):
    with SessionLocal() as db:
        deleted_item = db.query(Item).filter_by(id=item_id).first()
        if deleted_item:
            db.delete(deleted_item)
            db.commit()
            return {'message': f"Item with ID {item_id} deleted successfully"}
        else:
            return {'message': f"Item with ID {item_id} not found"}


# Создание товара
create_item(db_item)

# Обновление товара
update_item(2, 'Карандаш', 'Красный карандаш', 30)

# Удаление товара
# del_item = delete_item(3)
# print(del_item)

# Получение и вывод всех товаров
print(get_items())


# retrive - searching on id
# update
# delete
