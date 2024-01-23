from fastapi.testclient import TestClient

from config import TEST_ENV
from main import app


client = TestClient(app)


def test_envs():
	assert TEST_ENV == "test_message"


def test_create_order_district_not_found():
	response = client.post("/order", json={"name": "test_order", "district": "test_district"})
	assert response.status_code == 404
	assert response.json() == {"error": "No district with name=test_district"}


def test_get_couriers_not_found():
	response = client.get("/courier")
	assert response.status_code == 404
	assert response.json() == {"error": "No couriers in DB"}


def test_create_courier_no_valid():
	response = client.post("/courier", json={"name": "test_courier", "districts": "test_district"})
	assert response.status_code == 422
	assert response.json() == {
		"detail": [
			{
				"type": "list_type",
				"loc": [
					"body",
					"districts"
				],
				"msg": "Input should be a valid list",
				"input": "test_district",
				"url": "https://errors.pydantic.dev/2.5/v/list_type"
			}
		]
	}


def test_create_courier():
	response = client.post("/courier", json={"name": "test_courier", "districts": ["test_district"]})
	assert response.status_code == 200
	assert response.json() == {"message": "Courier created successfully"}


def test_get_couriers():
	response = client.get("/courier")
	assert response.status_code == 200
	assert response.json() == [{"id": 1, "name": "test_courier"}]


def test_get_courier_no_valid():
	response = client.get("/courier/test")
	assert response.status_code == 422
	assert response.json() == {
		"detail": [
			{
				"type":"int_parsing",
				"loc":[
					"path",
					"courier_id"
				],
				"msg":"Input should be a valid integer, unable to parse string as an integer",
				"input":"test",
				"url":"https://errors.pydantic.dev/2.5/v/int_parsing"
			}
		]
	}


def test_get_courier_not_found():
	response = client.get("/courier/0")
	response.status_code = 404
	response.json() == {"error": "No courier with id=0"}


def test_get_courier():
	response = client.get("/courier/1")
	assert response.status_code == 200
	assert response.json() == {
		"id": 1,
		"name": "test_courier",
		"districts": [
			{
				"id": 1,
				"name": "test_district"
			},
		],
		"active_order": None,
		"avg_order_complete_time": None,
		"avg_day_orders": 0
	}


def test_create_order_no_valid():
	response = client.post("/order", json={"name": "test_order", "district": 12})
	assert response.status_code == 422
	assert response.json() == {
		"detail": [
			{
				"type": "string_type",
				"loc": [
					"body",
					"district"
				],
				"msg": "Input should be a valid string",
				"input": 12,
				"url": "https://errors.pydantic.dev/2.5/v/string_type"
			}
		]
	}


def test_create_order():
	response = client.post("/order", json={"name": "test_order", "district": "test_district"})
	assert response.status_code == 200
	assert response.json() == {"order_id": 1, "courier_id": 1}


def test_create_order_with_no_free_couriers():
	response = client.post("/order", json={"name": "test_order", "district": "test_district"})
	assert response.status_code == 404
	assert response.json() == {"error": "No free couriers for district with name=test_district"}


def test_get_order_no_valid():
	response = client.get("/order/test")
	assert response.status_code == 422
	assert response.json() == {
		"detail":[
			{
				"type":"int_parsing",
				"loc":[
					"path",
					"order_id"
				],
				"msg":"Input should be a valid integer, unable to parse string as an integer",
				"input":"test",
				"url":"https://errors.pydantic.dev/2.5/v/int_parsing"
			}
		]
	}


def test_get_order_not_found():
	response = client.get("/order/0")
	assert response.status_code == 404
	assert response.json() == {"error": "No order with id=0"}


def test_get_order():
	response = client.get("/order/1")
	assert response.status_code == 200
	assert response.json() == {"courier_id": 1, "status": 1}


def test_complete_order_no_valid():
	response = client.post("/order/test")
	assert response.status_code == 422
	assert response.json() == {
		"detail":[
			{
				"type":"int_parsing",
				"loc":[
					"path",
					"order_id"
				],
				"msg":"Input should be a valid integer, unable to parse string as an integer",
				"input":"test",
				"url":"https://errors.pydantic.dev/2.5/v/int_parsing"
			}
		]
	}


def test_complete_order_not_found():
	response = client.post("/order/0")
	assert response.status_code == 404
	assert response.json() == {"error": "No order with id=0"}


def test_complete_order():
	response = client.post("/order/1")
	assert response.status_code == 200
	assert response.json() == {"message": "Order completed successfully"}


def test_complete_order_already_completed():
	response = client.post("/order/1")
	assert response.status_code == 400
	assert response.json() == {"error": "Order is already completed"}
