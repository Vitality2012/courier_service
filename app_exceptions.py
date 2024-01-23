from fastapi import HTTPException


class NoCourierInDBException(HTTPException):
	def __init__(self, id: int | None = None, status_code=404, detail="No courier in database with this id"):
		if id:
			super().__init__(status_code=status_code, detail=f"No courier in database with id={id}")
		super().__init__(status_code=status_code, detail=detail)


class NoCouriersInDBException(HTTPException):
	def __init__(self, status_code=404, detail="No couriers in database"):
		super().__init__(status_code=status_code, detail=detail)


class NoFreeCouriersException(HTTPException):
	def __init__(self, status_code=404, detail="No free couriers"):
		super().__init__(status_code=status_code, detail=detail)


class NoDistrictInDBException(HTTPException):
	def __init__(self, name: str | None = None, status_code=404, detail="No district in database with this name"):
		if name:
			super().__init__(status_code=status_code, detail=f"No district in database with name={name}")
		super().__init__(status_code=status_code, detail=detail)


class NoOrderInDBException(HTTPException):
	def __init__(self, id: int | None = None, status_code=404, detail="No order in database with this id"):
		if id:
			super().__init__(status_code=status_code, detail=f"No order in database with id={id}")
		super().__init__(status_code=status_code, detail=detail)


class OrderIsAlreadyCompletedException(HTTPException):
	def __init__(self, status_code=400, detail="Order is already completed"):
		super().__init__(status_code=status_code, detail=detail)