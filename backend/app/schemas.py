from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class ItemBase(BaseModel):
    name: str
    sku: str | None = None
    category: str | None = None
    brand: str | None = None
    quantity: int = 0
    price: float = 0.0
    min_stock: int = 5

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("El nombre no puede estar vacío.")
        return v.strip()

    @field_validator("quantity", "min_stock")
    @classmethod
    def not_negative(cls, v: int) -> int:
        if v < 0:
            raise ValueError("El valor no puede ser negativo.")
        return v

    @field_validator("price")
    @classmethod
    def price_not_negative(cls, v: float) -> float:
        if v < 0:
            raise ValueError("El precio no puede ser negativo.")
        return v


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: str | None = None
    sku: str | None = None
    category: str | None = None
    brand: str | None = None
    quantity: int | None = None
    price: float | None = None
    min_stock: int | None = None

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            raise ValueError("El nombre no puede estar vacío.")
        return v.strip() if v is not None else v

    @field_validator("price", "min_stock", "quantity")
    @classmethod
    def not_negative(cls, v):
        if v is not None and v < 0:
            raise ValueError("El valor no puede ser negativo.")
        return v


class StockAdjust(BaseModel):
    delta: int

    @field_validator("delta")
    @classmethod
    def delta_not_zero(cls, v: int) -> int:
        if v == 0:
            raise ValueError("El ajuste no puede ser 0.")
        return v


class ItemOut(ItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    low_stock: bool
    out_of_stock: bool
    created_at: datetime
    updated_at: datetime


class Stats(BaseModel):
    total_items: int
    total_units: int
    total_value: float
    low_stock_count: int
    out_of_stock_count: int
    categories: list[str]
    brands: list[str]
