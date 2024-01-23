from sqlalchemy import select, not_
from sqlalchemy.orm import Session, selectinload

from datetime import datetime, timedelta
from models import Courier, District, Order, OrderStatus
import app_exceptions
import schemas


def create_courier(db: Session, courier: schemas.CourierForm) -> None:
	with db:
		courier = Courier(
			name = courier.name,
			# Get districts from DB or creating new
			districts = get_or_create_districts(db=db, districts=courier.districts)
		)
		db.add(courier)
		db.commit()


def get_courier(db: Session, id: int) -> Courier:
	with db:
		query = (
			select(Courier)
			.where(Courier.id == id)
		)
		result = db.execute(query).scalars().first()
		if not result:
			raise app_exceptions.NoCourierInDBException(id=id)
		return result


def get_joined_courier(db: Session, id: int) -> Courier:
	with db:
		query = (
			select(Courier)
			.options(selectinload(Courier.districts))
			.options(selectinload(Courier.active_order))
			.where(Courier.id == id)
			)
		result = db.execute(query).scalars().first()
		if not result:
			raise app_exceptions.NoCourierInDBException(id=id)
		return result


def get_couriers(db: Session) -> list[Courier]:
	with db:
		query = select(Courier)
		result = db.execute(query).scalars().all()
		if not result:
			raise app_exceptions.NoCouriersInDBException()
		return result


def get_free_courier(db: Session, district_name: str) -> Courier:
	with db:
		query = (select(Courier)
			.where(
				not_(Courier.active_order.has()), # Have no active order
				Courier.districts.any(name=district_name)
			)
		)
		result = db.execute(query).scalars().first()
		if not result:
			raise app_exceptions.NoFreeCouriersException()
		return result


def create_district(name: str) -> District:
	return District(name=name)


def get_district(db: Session, name: str) -> District:
	with db:
		query = (
			select(District)
			.where(District.name==name)
			)
		result = db.execute(query).scalars().first()
		if not result:
			raise app_exceptions.NoDistrictInDBException(name=name)
		return result


def get_joined_district(db: Session, name: str) -> District:
	with db:
		query = (
			select(District)
			.options(selectinload(District.couriers))
			.where(District.name==name)
			)
		result = db.execute(query).scalars().first()
		if not result:
			raise app_exceptions.NoDistrictInDBException(name=name)
		return result


# If district in not exists we create it
def get_or_create_districts(db: Session, districts: list[str]) -> list[District]:
	result = []
	for district in districts:
		try:
			new_district = get_district(db=db, name=district)
		except app_exceptions.NoDistrictInDBException:
			result.append(create_district(name=district))
		else:
			result.append(new_district)
	return result


def create_order(db: Session, order: schemas.OrderForm) -> Order:
		with db:
			district = get_district(db=db, name=order.district)
			courier = get_free_courier(db=db, district_name=order.district)
			courier = db.merge(courier)
			order = Order(
				name = order.name,
				district = district,
				courier = courier
			)
			courier.active_order = order
			db.add(order)
			db.commit()
			db.refresh(order)
			return order


def get_order(db: Session, id: int) -> Order:
	with db:
		query = (
			select(Order)
			.where(Order.id == id)
		)
		result = db.execute(query).scalars().first()
		if not result:
			raise app_exceptions.NoOrderInDBException(id=id)
		return result


def get_joined_order(db: Session, id: int) -> Order:
	with db:
		query = (
			select(Order)
			.options(selectinload(Order.courier))
			.options(selectinload(Order.district))
			.where(Order.id == id)
		)
		result = db.execute(query).scalars().first()
		if not result:
			raise app_exceptions.NoOrderInDBException(id=id)
		return result


def update_avg_order_complete_time(db: Session, courier: Courier) -> None:
	with db:
		courier = db.merge(courier)
		counter = 0
		total_time = timedelta(0, 0, 0, 0, 0, 0, 0)
		for order in courier.orders:
			if order.status == OrderStatus.in_progress.value:
				continue
			counter += 1
			total_time += order.completed_at - order.started_at
		if counter != 0:
			avg_order_complete_time = total_time / counter
			avg_order_complete_time = datetime.fromtimestamp(avg_order_complete_time.total_seconds())
			courier.avg_order_complete_time = avg_order_complete_time
			db.commit()


def update_avg_day_orders(db: Session, courier: Courier) -> None:
	with db:
		courier = db.merge(courier)
		days = []
		counter = 0
		for order in courier.orders:
			counter += 1
			if order.completed_at.day not in days:
				days.append(order.completed_at.day)
		if counter != 0:
			avg_day_orders = int(counter / len(days))
			courier.avg_day_orders = avg_day_orders
			db.commit()


def complete_order(db: Session, id: int) -> None:
	with db:
		order = get_order(db=db, id=id)
		if order.status == OrderStatus.completed.value:
			raise app_exceptions.OrderIsAlreadyCompletedException()
		order = db.merge(order)
		order.status = OrderStatus.completed.value
		order.completed_at = datetime.now()
		order.courier.active_order = None
		db.commit()
		update_avg_order_complete_time(db=db, courier=order.courier)
		order = db.merge(order)
		update_avg_day_orders(db=db, courier=order.courier)
		