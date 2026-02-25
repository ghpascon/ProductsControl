from datetime import datetime
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from smartx_rfid.utils.path import get_prefix_from_path
from app.services.controller import controller
from app.core import get_user, validate_role


router_prefix = get_prefix_from_path(__file__)
router = APIRouter(prefix=router_prefix, tags=[router_prefix])


# [ PRODUCT ORDERS ]
@router.get(
	'/get_all_orders',
	summary='Get all product orders',
)
async def get_all_orders():
	return JSONResponse(content=controller.db_manager.get_product_orders())


@router.get(
	'/get_order_by_id/{order_id}',
	summary='Get a product order by its ID',
)
async def get_order_by_id(order_id: int):
	return JSONResponse(content=controller.db_manager.get_product_order(order_id))


@router.get(
	'/get_product_orders_by_ids/{ids}',
	summary='Get multiple product orders by their IDs',
)
async def get_product_orders_by_ids(ids: str):
	try:
		order_ids = [int(id.strip()) for id in ids.split(',')]
		orders = controller.db_manager.get_product_orders_by_ids(order_ids)
		return JSONResponse(content=orders)
	except ValueError:
		return JSONResponse(
			status_code=400,
			content={
				'error': 'IDs inválidos. Certifique-se de fornecer uma lista de IDs separados por vírgula.'
			},
		)


@router.get(
	'/get_product_orders_by_client/{client_name}',
	summary='Get product orders by client name',
)
async def get_product_orders_by_client(client_name: str):
	return JSONResponse(content=controller.db_manager.get_product_orders_by_client(client_name))


@router.get(
	'/get_product_orders_by_cnpj/{cnpj}',
	summary='Get product orders by client CNPJ',
)
async def get_product_orders_by_cnpj(cnpj: str):
	# Restaurar barras que foram substituídas por pipes no frontend
	cnpj_decoded = cnpj.replace('|', '/')
	return JSONResponse(content=controller.db_manager.get_product_orders_by_cnpj(cnpj_decoded))


@router.get(
	'/get_product_orders_by_product_code/{product_code}',
	summary='Get product orders by product code',
)
async def get_product_orders_by_product_code(product_code: str):
	return JSONResponse(
		content=controller.db_manager.get_product_orders_by_product_code(product_code)
	)


@router.get(
	'/get_product_orders_by_order_number/{order_number}',
	summary='Get product orders by order number',
)
async def get_product_orders_by_order_number(order_number: str):
	return JSONResponse(
		content=controller.db_manager.get_product_orders_by_order_number(order_number)
	)


@router.get(
	'/get_product_orders_by_reader_type_name/{reader_type_name}',
	summary='Get product orders by reader type name',
)
async def get_product_orders_by_reader_type_name(reader_type_name: str):
	return JSONResponse(
		content=controller.db_manager.get_product_orders_by_reader_type_name(reader_type_name)
	)


@router.get(
	'/get_product_orders_by_date/{start_date}/{end_date}/{field}',
	summary='Get product orders by date range and field',
)
async def get_product_orders_by_date(start_date: str, end_date: str, field: str):
	try:
		start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
		end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
		orders = controller.db_manager.get_product_orders_by_date(start_dt, end_dt, field)
		return JSONResponse(content=orders)
	except (ValueError, TypeError):
		return JSONResponse(
			status_code=400,
			content={
				'error': 'Formato de data inválido. Use formato ISO (YYYY-MM-DD ou YYYY-MM-DDTHH:MM:SS).'
			},
		)


@router.get(
	'/get_product_orders_by_reader_serial/{serial_number}',
	summary='Get product orders by reader serial number',
)
async def get_product_orders_by_reader_serial(serial_number: str):
	reader = controller.db_manager.get_reader_by_serial(serial_number)
	if reader is None:
		return JSONResponse(
			status_code=404,
			content={'error': 'Leitor não encontrado com o serial number fornecido.'},
		)
	return JSONResponse(
		content=controller.db_manager.get_product_orders_by_reader(
			reader.get('id') if reader.get('id') else None
		)
	)


@router.get(
	'/get_product_orders_by_reader/{reader_id}',
	summary='Get product orders by reader ID',
)
async def get_product_orders_by_reader(reader_id: int):
	return JSONResponse(content=controller.db_manager.get_product_orders_by_reader(reader_id))


@router.put(
	'/add_reader_to_product_order/{order_id}/{reader_id}',
	summary='Assign a reader to a product order',
)
async def add_reader_to_product_order(request: Request, order_id: int, reader_id: int):
	if not validate_role(request, ['admin', 'dev', 'assign']):
		return JSONResponse(
			status_code=403,
			content={'error': 'Proibido: Você não tem permissão para realizar esta ação'},
		)

	success, msg = controller.db_manager.add_reader_to_product_order(order_id, reader_id)
	if success:
		return JSONResponse(content={'message': 'Leitor adicionado ao pedido com sucesso'})
	else:
		return JSONResponse(status_code=400, content={'error': msg})


@router.post(
	'/add_comment_to_product_order/{order_id}/{comment}',
	summary='Add a comment to a product order',
)
async def add_comment_to_product_order(request: Request, order_id: int, comment: str):
	user = get_user(request)
	success, msg = controller.db_manager.add_comment_to_product_order(
		order_id, comment, user.get('username') if user else 'Unknown'
	)
	if success:
		return JSONResponse(content={'message': msg})
	else:
		return JSONResponse(status_code=400, content={'error': msg})


# WORKFLOW
@router.put(
	'/product_order_mount/{order_id}',
	summary='Mark a product order as mounted',
)
async def product_order_mount(request: Request, order_id: int):
	if not validate_role(request, ['admin', 'dev', 'mount']):
		return JSONResponse(
			status_code=403,
			content={'error': 'Proibido: Você não tem permissão para realizar esta ação'},
		)
	user = get_user(request)
	success, msg = controller.db_manager.product_order_mount(
		order_id, user.get('user_id') if user else None
	)
	if success:
		return JSONResponse(content={'message': msg})
	else:
		return JSONResponse(status_code=400, content={'error': msg})


@router.put(
	'/product_order_test/{order_id}',
	summary='Mark a product order as tested',
)
async def product_order_test(request: Request, order_id: int):
	if not validate_role(request, ['admin', 'dev', 'test']):
		return JSONResponse(
			status_code=403,
			content={'error': 'Proibido: Você não tem permissão para realizar esta ação'},
		)
	user = get_user(request)
	success, msg = controller.db_manager.product_order_test(
		order_id, user.get('user_id') if user else None
	)
	if success:
		return JSONResponse(content={'message': msg})
	else:
		return JSONResponse(status_code=400, content={'error': msg})


@router.put(
	'/product_order_ship/{order_id}',
	summary='Mark a product order as shipped',
)
async def product_order_ship(request: Request, order_id: int):
	if not validate_role(request, ['admin', 'dev', 'ship']):
		return JSONResponse(
			status_code=403,
			content={'error': 'Proibido: Você não tem permissão para realizar esta ação'},
		)
	user = get_user(request)
	success, msg = controller.db_manager.product_order_ship(
		order_id, user.get('user_id') if user else None
	)
	if success:
		return JSONResponse(content={'message': msg})
	else:
		return JSONResponse(status_code=400, content={'error': msg})


@router.put(
	'/product_order_activate/{order_id}',
	summary='Mark a product order as activated',
)
async def product_order_activate(request: Request, order_id: int):
	if not validate_role(request, ['admin', 'dev', 'activate']):
		return JSONResponse(
			status_code=403,
			content={'error': 'Proibido: Você não tem permissão para realizar esta ação'},
		)
	user = get_user(request)
	success, msg = controller.db_manager.product_order_activate(
		order_id, user.get('user_id') if user else None
	)
	if success:
		return JSONResponse(content={'message': msg})
	else:
		return JSONResponse(status_code=400, content={'error': msg})


# UTILS
@router.get(
	'/get_customers',
	summary='Get all customers',
)
async def get_customers():
	return JSONResponse(content=controller.db_manager.get_customers())


@router.get(
	'/get_cnpjs',
	summary='Get all unique CNPJs from product orders',
)
async def get_cnpjs():
	return JSONResponse(content=controller.db_manager.get_cnpjs())


@router.get(
	'/get_orders_numbers',
	summary='Get all unique order numbers from product orders',
)
async def get_orders_numbers():
	return JSONResponse(content=controller.db_manager.get_orders_numbers())


@router.get(
	'/get_product_codes',
	summary='Get all unique product codes from product orders',
)
async def get_product_codes():
	return JSONResponse(content=controller.db_manager.get_product_codes())
