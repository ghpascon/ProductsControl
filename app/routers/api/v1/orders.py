from datetime import datetime
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from smartx_rfid.utils.path import get_prefix_from_path
from app.schemas.controller import AddOrder
from app.services.controller import controller
import logging

router_prefix = get_prefix_from_path(__file__)
router = APIRouter(prefix=router_prefix, tags=[router_prefix])


# [ PRODUCT ORDERS ]
@router.get(
	'/get_product_orders',
	summary='Get all product orders',
)
async def get_all_orders():
	return JSONResponse(content=controller.db_manager.get_product_orders())


@router.get(
	'/get_product_order/{order_id}',
	summary='Get a product order by ID',
)
async def get_product_order(order_id: int):
	return JSONResponse(content=controller.db_manager.get_product_order(order_id))


@router.get(
	'/get_product_orders_by_client/{customer_id}',
	summary='Get all product orders by client ID',
)
async def get_product_orders_by_client(customer_id: int):
	return JSONResponse(content=controller.db_manager.get_product_orders_by_client(customer_id))


@router.get(
	'/get_product_orders_by_product_type/{product_type_id}',
	summary='Get all product orders by product type ID',
)
async def get_product_orders_by_product_type(product_type_id: int):
	return JSONResponse(
		content=controller.db_manager.get_product_orders_by_product_type(product_type_id)
	)


@router.get(
	'/get_product_orders_by_date/{start_date}/{end_date}',
	summary='Get all product orders between two dates',
)
async def get_product_orders_by_date(start_date: datetime, end_date: datetime):
	return JSONResponse(
		content=controller.db_manager.get_product_orders_by_date(start_date, end_date)
	)


@router.post(
	'/add_product_order',
	summary='Add a new product order',
)
async def add_product_order(order: AddOrder):
	success, message = controller.db_manager.add_product_order(**order.model_dump())
	if success:
		logging.info(f'{message}')
		return JSONResponse(content={'message': message})
	else:
		logging.warning(f'{message}')
		return JSONResponse(content={'error': message}, status_code=400)


@router.delete(
	'/delete_product_order/{order_id}',
	summary='Delete a product order by ID',
)
async def delete_product_order(order_id: int):
	success, message = controller.db_manager.delete_product_order(order_id)
	if success:
		logging.info(f'order_id={order_id} | {message}')
		return JSONResponse(content={'message': message})
	else:
		logging.warning(f'order_id={order_id} | {message}')
		return JSONResponse(content={'error': message}, status_code=400)


@router.put(
	'/product_order_mount/{order_id}',
	summary='Update the mount status of a product order by ID',
)
async def product_order_mount(order_id: int):
	success, message = controller.db_manager.product_order_mount(order_id)
	if success:
		logging.info(f'order_id={order_id} | {message}')
		return JSONResponse(content={'message': message})
	else:
		logging.warning(f'order_id={order_id} | {message}')
		return JSONResponse(content={'error': message}, status_code=400)


@router.put(
	'/product_order_test/{order_id}',
	summary='Test a product order by ID',
)
async def product_order_test(order_id: int):
	success, message = controller.db_manager.product_order_test(order_id)
	if success:
		logging.info(f'order_id={order_id} | {message}')
		return JSONResponse(content={'message': message})
	else:
		logging.warning(f'order_id={order_id} | {message}')
		return JSONResponse(content={'error': message}, status_code=400)


@router.put(
	'/product_order_ship/{order_id}',
	summary='Update the ship status of a product order by ID',
)
async def product_order_ship(order_id: int):
	success, message = controller.db_manager.product_order_ship(order_id)
	if success:
		logging.info(f'order_id={order_id} | {message}')
		return JSONResponse(content={'message': message})
	else:
		logging.warning(f'order_id={order_id} | {message}')
		return JSONResponse(content={'error': message}, status_code=400)


@router.put(
	'/product_order_activate/{order_id}',
	summary='Update the activate status of a product order by ID',
)
async def product_order_activate(order_id: int):
	success, message = controller.db_manager.product_order_activate(order_id)
	if success:
		logging.info(f'order_id={order_id} | {message}')
		return JSONResponse(content={'message': message})
	else:
		logging.warning(f'order_id={order_id} | {message}')
		return JSONResponse(content={'error': message}, status_code=400)


@router.get(
	'/get_decoded_orders',
	summary='Get all decoded product orders',
)
async def get_decoded_orders():
	return JSONResponse(content=controller.db_manager.get_decoded_orders())


@router.get(
	'/get_decoded_order/{order_id}',
	summary='Get a decoded product order by ID',
)
async def get_decoded_order(order_id: int):
	return JSONResponse(content=controller.db_manager.get_decoded_order(order_id))


@router.get(
	'/get_decoded_orders_by_ids/{order_ids}',
	summary='Get decoded product orders by a list of IDs',
)
async def get_decoded_orders_by_ids(order_ids: str):
	order_ids_list = [int(id) for id in order_ids.split(',')]
	return JSONResponse(content=controller.db_manager.get_decoded_orders_by_ids(order_ids_list))


@router.post(
	'/add_reader_to_order/{order_id}/{reader_id}',
	summary='Add a reader to a product order by ID',
)
async def add_reader_to_order(order_id: int, reader_id: int):
	success, message = controller.db_manager.add_reader_to_product_order(order_id, reader_id)
	if success:
		logging.info(f'order_id={order_id} | reader_id={reader_id} | {message}')
		return JSONResponse(content={'message': message})
	else:
		logging.warning(f'order_id={order_id} | reader_id={reader_id} | {message}')
		return JSONResponse(content={'error': message}, status_code=400)
