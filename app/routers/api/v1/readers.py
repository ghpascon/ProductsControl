from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from smartx_rfid.utils.path import get_prefix_from_path
from app.schemas.controller import AddType, AddReader
from app.services.controller import controller
import logging
from app.core import validate_role

router_prefix = get_prefix_from_path(__file__)
router = APIRouter(prefix=router_prefix, tags=[router_prefix])


# [ READER TYPES ]
@router.get(
	'/get_reader_types',
	summary='Get all reader types',
)
async def get_reader_types():
	return JSONResponse(content=controller.db_manager.get_reader_types())


@router.get(
	'get_reader_type_by_id/{reader_type_id}',
	summary='Get a reader type by its ID',
)
async def get_reader_type_by_id(reader_type_id: int):
	return JSONResponse(content=controller.db_manager.get_reader_type(reader_type_id))


@router.post(
	'/add_reader_type',
	summary='Add a new reader type',
)
async def add_reader_type(request: Request, reader_type_data: AddType):
	if not validate_role(request, ['admin', 'dev']):
		return JSONResponse(
			status_code=403,
			content={'error': 'Proibido: Você não tem permissão para realizar esta ação'},
		)
	try:
		success, msg = controller.db_manager.add_reader_type(
			name=reader_type_data.name,
			description=reader_type_data.description,
		)
		if success:
			return JSONResponse(content={'message': 'Tipo de leitor adicionado com sucesso'})
		else:
			return JSONResponse(status_code=400, content={'error': msg})
	except Exception as e:
		logging.error(f'Error adding reader type: {e}')
		return JSONResponse(
			status_code=500, content={'error': f'Falha ao adicionar tipo de leitor: {e}'}
		)


@router.put(
	'/update_reader_type/{reader_type_id}',
	summary='Update an existing reader type',
)
async def update_reader_type(request: Request, reader_type_id: int, reader_type_data: AddType):
	if not validate_role(request, ['admin', 'dev']):
		return JSONResponse(
			status_code=403,
			content={'error': 'Proibido: Você não tem permissão para realizar esta ação'},
		)
	try:
		controller.db_manager.update_reader_type(
			reader_type_id=reader_type_id,
			name=reader_type_data.name,
			description=reader_type_data.description,
		)
		return JSONResponse(content={'message': 'Tipo de leitor atualizado com sucesso'})
	except Exception as e:
		logging.error(f'Error updating reader type: {e}')
		return JSONResponse(
			status_code=500, content={'error': f'Falha ao atualizar tipo de leitor: {e}'}
		)


@router.delete(
	'/delete_reader_type/{reader_type_id}',
	summary='Delete a reader type',
)
async def delete_reader_type(request: Request, reader_type_id: int):
	if not validate_role(request, ['admin', 'dev']):
		return JSONResponse(
			status_code=403,
			content={'error': 'Proibido: Você não tem permissão para realizar esta ação'},
		)
	try:
		controller.db_manager.delete_reader_type(reader_type_id)
		return JSONResponse(content={'message': 'Tipo de leitor deletado com sucesso'})
	except Exception as e:
		logging.error(f'Error deleting reader type: {e}')
		return JSONResponse(
			status_code=500, content={'error': f'Falha ao deletar tipo de leitor: {e}'}
		)


@router.post(
	'/add_reader',
	summary='Add a new reader',
)
async def add_reader(request: Request, reader_data: AddReader):
	if not validate_role(request, ['admin', 'dev']):
		return JSONResponse(
			status_code=403,
			content={'error': 'Proibido: Você não tem permissão para realizar esta ação'},
		)
	try:
		success, msg = controller.db_manager.add_reader(**reader_data.model_dump())
		if success:
			return JSONResponse(content={'message': 'Leitor adicionado com sucesso'})
		else:
			return JSONResponse(status_code=400, content={'error': msg})
	except Exception as e:
		logging.error(f'Error adding reader: {e}')
		return JSONResponse(status_code=500, content={'error': f'Falha ao adicionar leitor: {e}'})


@router.get(
	'/get_readers',
	summary='Get all readers',
)
async def get_readers():
	return JSONResponse(content=controller.db_manager.get_readers())


@router.get(
	'/get_reader_by_id/{reader_id}',
	summary='Get a reader by its ID',
)
async def get_reader_by_id(reader_id: int):
	return JSONResponse(content=controller.db_manager.get_reader(reader_id))


@router.get(
	'/get_available_readers',
	summary='Get all available readers (not assigned to any order)',
)
async def get_available_readers():
	return JSONResponse(content=controller.db_manager.get_available_readers())


@router.get(
	'/get_readers_by_type/{reader_type_id}',
	summary='Get all readers of a specific type',
)
async def get_readers_by_type(reader_type_id: int):
	return JSONResponse(content=controller.db_manager.get_readers_by_type(reader_type_id))


@router.get(
	'/get_readers_by_type_name/{reader_type_name}',
	summary='Get all readers of a specific type by type name',
)
async def get_readers_by_type_name(reader_type_name: str):
	return JSONResponse(content=controller.db_manager.get_readers_by_type_name(reader_type_name))


@router.get(
	'/get_reader/{reader_id}',
	summary='Get a reader by its ID',
)
async def get_reader(reader_id: int):
	return JSONResponse(content=controller.db_manager.get_reader(reader_id))


@router.get(
	'/get_reader_by_hostname/{hostname}',
	summary='Get a reader by its hostname',
)
async def get_reader_by_hostname(hostname: str):
	return JSONResponse(content=controller.db_manager.get_reader_by_hostname(hostname))


@router.get(
	'/get_reader_by_serial/{serial_number}',
	summary='Get a reader by its serial number',
)
async def get_reader_by_serial(serial_number: str):
	return JSONResponse(content=controller.db_manager.get_reader_by_serial(serial_number))


@router.put(
	'/update_reader/{reader_id}',
	summary='Update an existing reader',
)
async def update_reader(request: Request, reader_id: int, reader_data: AddReader):
	if not validate_role(request, ['admin', 'dev']):
		return JSONResponse(
			status_code=403,
			content={'error': 'Proibido: Você não tem permissão para realizar esta ação'},
		)
	try:
		controller.db_manager.update_reader(reader_id=reader_id, **reader_data.model_dump())
		return JSONResponse(content={'message': 'Leitor atualizado com sucesso'})
	except Exception as e:
		logging.error(f'Error updating reader: {e}')
		return JSONResponse(status_code=500, content={'error': f'Falha ao atualizar leitor: {e}'})


@router.delete(
	'/delete_reader/{reader_id}',
	summary='Delete a reader',
)
async def delete_reader(request: Request, reader_id: int):
	if not validate_role(request, ['admin', 'dev']):
		return JSONResponse(
			status_code=403,
			content={'error': 'Proibido: Você não tem permissão para realizar esta ação'},
		)
	try:
		controller.db_manager.delete_reader(reader_id)
		return JSONResponse(content={'message': 'Leitor deletado com sucesso'})
	except Exception as e:
		logging.error(f'Error deleting reader: {e}')
		return JSONResponse(status_code=500, content={'error': f'Falha ao deletar leitor: {e}'})
