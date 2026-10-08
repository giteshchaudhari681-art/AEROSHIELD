from typing import Generic, TypeVar, Type, Optional, List, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, func

ModelType = TypeVar("ModelType")

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100, **filters) -> tuple[List[ModelType], int]:
        query = db.query(self.model)
        for attr, value in filters.items():
            if value is not None and hasattr(self.model, attr):
                query = query.filter(getattr(self.model, attr) == value)
        
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return items, total

    def create(self, db: Session, *, obj_in: Any) -> ModelType:
        db.add(obj_in)
        db.flush()
        return obj_in

    def update(self, db: Session, *, db_obj: ModelType, obj_in: dict) -> ModelType:
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        db.add(db_obj)
        db.flush()
        return db_obj

    def delete(self, db: Session, *, id: Any) -> ModelType:
        obj = db.query(self.model).get(id)
        if obj:
            db.delete(obj)
            db.flush()
        return obj
