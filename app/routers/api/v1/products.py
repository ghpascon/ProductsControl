from fastapi import APIRouter
from fastapi.responses import JSONResponse
from smartx_rfid.utils.path import get_prefix_from_path
from app.schemas.controller import AddType
from app.services.controller import controller
import logging

router_prefix = get_prefix_from_path(__file__)
router = APIRouter(prefix=router_prefix, tags=[router_prefix])


# [ PRODUCT Types ]
@router.get(
	'/get_product_types',
	summary='Get all product types',
)
async def get_product_types():
	return JSONResponse(content=controller.db_manager.get_product_types())


@router.get(
	'/get_product_type/{product_type_id}',
	summary='Get a product type by ID',
)
async def get_product_type(product_type_id: int):
	return JSONResponse(content=controller.db_manager.get_product_type(product_type_id))


@router.post(
	'/add_product_type',
	summary='Add a new product type',
)
async def add_product_type(product_type: AddType):
	success, message = controller.db_manager.add_product_type(**product_type.model_dump())
	if success:
		logging.info(f'{message}')
		return JSONResponse(content={'message': message})
	else:
		logging.warning(f'{message}')
		return JSONResponse(content={'message': message}, status_code=400)


@router.put(
	'/update_product_type/{product_type_id}',
	summary='Update a product type by ID',
)
async def update_product_type(product_type_id: int, product_type: AddType):
	success, message = controller.db_manager.update_product_type(
		product_type_id, **product_type.model_dump()
	)
	if success:
		logging.info(f'product_type_id={product_type_id} | {message}')
		return JSONResponse(content={'message': message})
	logging.warning(f'product_type_id={product_type_id} | {message}')
	return JSONResponse(content={'message': message}, status_code=400)


@router.delete(
	'/delete_product_type/{product_type_id}',
	summary='Delete a product type by ID',
)
async def delete_product_type(product_type_id: int):
	success, message = controller.db_manager.delete_product_type(product_type_id)
	if success:
		logging.info(f'product_type_id={product_type_id} | {message}')
		return JSONResponse(content={'message': message})
	logging.warning(f'product_type_id={product_type_id} | {message}')
	return JSONResponse(content={'message': message}, status_code=400)
