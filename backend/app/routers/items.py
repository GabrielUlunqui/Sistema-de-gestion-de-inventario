from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=list[schemas.ItemOut])
def list_items(
    search: str | None = Query(default=None),
    status: str | None = Query(default=None, pattern="^(ok|low|out)$"),
    category: str | None = Query(default=None),
    brand: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return crud.list_items(
        db, search=search, status=status, category=category, brand=brand
    )


@router.post("/", response_model=schemas.ItemOut, status_code=201)
def create_item(data: schemas.ItemCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_item(db, data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Ya existe un ítem con ese SKU.")


@router.get("/{item_id}", response_model=schemas.ItemOut)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Ítem no encontrado.")
    return item


@router.put("/{item_id}", response_model=schemas.ItemOut)
def update_item(
    item_id: int, data: schemas.ItemUpdate, db: Session = Depends(get_db)
):
    item = crud.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Ítem no encontrado.")
    try:
        return crud.update_item(db, item, data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Ya existe un ítem con ese SKU.")


@router.patch("/{item_id}/stock", response_model=schemas.ItemOut)
def adjust_stock(
    item_id: int, data: schemas.StockAdjust, db: Session = Depends(get_db)
):
    item = crud.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Ítem no encontrado.")
    updated = crud.adjust_stock(db, item, data.delta)
    if updated is None:
        raise HTTPException(
            status_code=400,
            detail="El stock no puede quedar en negativo.",
        )
    return updated


@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Ítem no encontrado.")
    crud.delete_item(db, item)
