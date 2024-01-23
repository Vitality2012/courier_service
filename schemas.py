from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from models import OrderStatus


class OrderForm(BaseModel):
	name: str
	district: str

	class Config:
		from_attributes = True


class ActiveOrderInfo(BaseModel):
	id: int = Field(alias="order_id")
	name: str = Field(alias="order_name")

	class Config:
		from_attributes = True
		populate_by_name = True


class OrderCreatingResult(BaseModel):
	id: int = Field(alias="order_id")
	courier_id: int

	class Config:
		populate_by_name = True


class OrderInfo(BaseModel):
	courier_id: int
	status: OrderStatus

	class Config:
		from_attributes = True


class DistrictForm(BaseModel):
	name: str

	class Config:
		frozen = True


class District(BaseModel):
	id: int
	name: str

	class Config:
		from_attributes = True


class CourierForm(BaseModel):
	name: str
	districts: list[str]


class CourierInfo(BaseModel):
	id: int
	name: str

	class Config:
		from_attributes = True


class Courier(BaseModel):
	id: int
	name: str
	districts: list["District"]
	active_order: Optional["ActiveOrderInfo"]
	avg_order_complete_time: datetime | None
	avg_day_orders: int

	class Config:
		from_attributes = True
