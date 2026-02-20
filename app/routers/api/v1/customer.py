from fastapi import APIRouter
from fastapi.responses import JSONResponse
from smartx_rfid.utils.path import get_prefix_from_path
from app.services.controller import controller

router_prefix = get_prefix_from_path(__file__)
router = APIRouter(prefix=router_prefix, tags=[router_prefix])


# [ CUSTOMER ]
@router.get(
	'/get_customer',
	summary='Get all customers',
)
async def get_customers():
	return JSONResponse(content=controller.db_manager.get_customers())


@router.get(
	'/get_customer/{customer_id}',
	summary='Get a customer by ID',
)
async def get_customer(customer_id: int):
	return JSONResponse(content=controller.db_manager.get_customer(customer_id))
