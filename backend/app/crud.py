from sqlalchemy import func, select
from sqlalchemy.orm import Session

from . import models, schemas


def list_items(
    db: Session,
    search: str | None = None,
    status: str | None = None,
    category: str | None = None,
    brand: str | None = None,
) -> list[models.Item]:
    stmt = select(models.Item).order_by(models.Item.name)

    if search:
        like = f"%{search.strip()}%"
        stmt = stmt.where(
            models.Item.name.ilike(like)
            | models.Item.sku.ilike(like)
            | models.Item.category.ilike(like)
            | models.Item.brand.ilike(like)
        )
    if category:
        stmt = stmt.where(models.Item.category == category)
    if brand:
        stmt = stmt.where(models.Item.brand == brand)

    items = list(db.scalars(stmt).all())

    if status == "low":
        items = [i for i in items if i.low_stock]
    elif status == "out":
        items = [i for i in items if i.out_of_stock]
    elif status == "ok":
        items = [i for i in items if not i.low_stock and not i.out_of_stock]

    return items


def get_item(db: Session, item_id: int) -> models.Item | None:
    return db.get(models.Item, item_id)


def create_item(db: Session, data: schemas.ItemCreate) -> models.Item:
    item = models.Item(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_item(
    db: Session, item: models.Item, data: schemas.ItemUpdate
) -> models.Item:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item


def adjust_stock(
    db: Session, item: models.Item, delta: int
) -> models.Item | None:
    new_quantity = item.quantity + delta
    if new_quantity < 0:
        return None
    item.quantity = new_quantity
    db.commit()
    db.refresh(item)
    return item


def delete_item(db: Session, item: models.Item) -> None:
    db.delete(item)
    db.commit()


def get_stats(db: Session) -> schemas.Stats:
    items = list(db.scalars(select(models.Item)).all())
    categories = sorted({i.category for i in items if i.category})
    brands = sorted({i.brand for i in items if i.brand})
    return schemas.Stats(
        total_items=len(items),
        total_units=sum(i.quantity for i in items),
        total_value=round(sum(i.quantity * i.price for i in items), 2),
        low_stock_count=sum(1 for i in items if i.low_stock),
        out_of_stock_count=sum(1 for i in items if i.out_of_stock),
        categories=categories,
        brands=brands,
    )
