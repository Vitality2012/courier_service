from typing import Annotated
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database import SessionLocal
import app_exceptions
import crud
import schemas


app = FastAPI()


# Dependencies
def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


@app.post("/courier")
def create_courier(db: Annotated[Session, Depends(get_db)], courier: schemas.CourierForm):
	try:
		crud.create_courier(db=db, courier=courier)
		return JSONResponse(status_code=200, content={"message": "Courier created successfully"})
	except Exception:
		return JSONResponse(status_code=400, content={"error": "Unforeseen error"})


@app.get("/courier", response_model=list[schemas.CourierInfo])
def get_couriers(db: Annotated[Session, Depends(get_db)]):
	try:
		couriers = crud.get_couriers(db=db)
		return couriers
	except app_exceptions.NoCouriersInDBException:
		return JSONResponse(status_code=404, content={"error": "No couriers in DB"})
	except Exception:
		return JSONResponse(status_code=400, content={"error": "Unforeseen error"})


@app.get("/courier/{courier_id}", response_model=schemas.Courier)
def get_courier(db: Annotated[Session, Depends(get_db)], courier_id: int):
	try:
		return crud.get_joined_courier(db=db, id=courier_id)
	except app_exceptions.NoCourierInDBException:
		return JSONResponse(status_code=404, content={"error": f"No courier with id={courier_id}"})
	except Exception:
		return JSONResponse(status_code=400, content={"error": "Unforeseen error"})


@app.post("/order", response_model=schemas.OrderCreatingResult)
def create_order(db: Annotated[Session, Depends(get_db)], order: schemas.OrderForm):
	try:
		return crud.create_order(db=db, order=order)
	except app_exceptions.NoDistrictInDBException:
		return JSONResponse(status_code=404, content={"error": f"No district with name={order.district}"})
	except app_exceptions.NoFreeCouriersException:
		return JSONResponse(status_code=404, content={"error": f"No free couriers for district with name={order.district}"})
	except Exception:
		return JSONResponse(status_code=400, content={"error": "Unforeseen error"})


@app.get("/order/{order_id}", response_model=schemas.OrderInfo)
def get_order(db: Annotated[Session, Depends(get_db)], order_id: int):
	try:
		return crud.get_order(db=db, id=order_id)
	except app_exceptions.NoOrderInDBException:
		return JSONResponse(status_code=404, content={"error": f"No order with id={order_id}"})
	except Exception:
		return JSONResponse(status_code=400, content={"error": "Unforeseen error"})


@app.post("/order/{order_id}")
def complete_order(db: Annotated[Session, Depends(get_db)], order_id: int):
	try:
		crud.complete_order(db=db, id=order_id)
		return JSONResponse(status_code=200, content={"message": "Order completed successfully"})
	except app_exceptions.NoOrderInDBException:
		return JSONResponse(status_code=404, content={"error": f"No order with id={order_id}"})
	except app_exceptions.OrderIsAlreadyCompletedException:
		return JSONResponse(status_code=400, content={"error": "Order is already completed"})
	except Exception:
		return JSONResponse(status_code=400, content={"error": "Unforeseen error"})
	