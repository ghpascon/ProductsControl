from fastapi import APIRouter
from fastapi.responses import JSONResponse
from smartx_rfid.utils.path import get_prefix_from_path
from app.services.controller import controller

router_prefix = get_prefix_from_path(__file__)
router = APIRouter(prefix=router_prefix, tags=[router_prefix])


# [ CUSTOMER ]
@router.post(
	'/sincronize_omie',
	summary='Synchronize all data with Omie',
)
async def sincronize_omie():
	success, data = await controller.sincronize_omie()
	if success:
		return JSONResponse(content=data)
	return JSONResponse(
		content={'message': f'Erro ao sincronizar com Omie: {data}'}, status_code=400
	)
