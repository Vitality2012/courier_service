from enum import Enum
from datetime import datetime
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database import Base


# Statuses for easy reading
class OrderStatus(Enum):
	in_progress = 1
	completed = 2


# Relationship class to make many to many between District and Courier
# Don't want to make the same records
class Association(Base):
	__tablename__ = "association"
	# Foreighn keys to others classes
	district_id: Mapped[int] = mapped_column(ForeignKey("district.id"), primary_key=True)
	courier_id: Mapped[int] = mapped_column(ForeignKey("courier.id"), primary_key=True)


class Courier(Base):
	__tablename__ = "courier"
	id: Mapped[int] = mapped_column(primary_key=True, index=True)
	name: Mapped[str | None]
	# Relationship
	districts: Mapped[list["District"]] = relationship(secondary="association", back_populates="couriers")
	# Extra info
	active_order_id: Mapped[int | None] = mapped_column(ForeignKey("order.id", use_alter=True))
	active_order: Mapped[Optional["Order"]] = relationship(foreign_keys="Courier.active_order_id", post_update=True)
	# How about add orders relation
	orders: Mapped[Optional[list["Order"]]] = relationship(back_populates="courier", foreign_keys="Order.courier_id")
	avg_order_complete_time: Mapped[datetime | None]
	avg_day_orders: Mapped[int] = mapped_column(default=0)

	def __repr__(self) -> str:
		return f"<Courier({self.id=}, {self.name=})>"


class District(Base):
	__tablename__ = "district"
	id: Mapped[int] = mapped_column(primary_key=True, index=True)
	name: Mapped[str] = mapped_column(unique=True)
	# Relationship
	couriers: Mapped[list["Courier"]] = relationship(secondary="association", back_populates="districts")

	def __repr__(self) -> str:
		return f"<District(id={self.id}, name={self.name})>"


class Order(Base):
	__tablename__ = "order"
	id: Mapped[int] = mapped_column(primary_key=True, index=True)
	name: Mapped[str]
	# Relationships with district
	district_id: Mapped[int] = mapped_column(ForeignKey("district.id"))
	district: Mapped["District"] = relationship()
	# Relationships with courier
	courier_id: Mapped[int] = mapped_column(ForeignKey("courier.id"))
	courier: Mapped["Courier"] = relationship(back_populates="orders", foreign_keys="Order.courier_id")
	# Extra info
	status: Mapped[int] = mapped_column(default=OrderStatus.in_progress.value)
	started_at: Mapped[datetime] = mapped_column(default=datetime.now)
	completed_at: Mapped[datetime | None]

	def __repr__(self) -> str:
		return f"<Order(id={self.id}, name={self.name})>"
