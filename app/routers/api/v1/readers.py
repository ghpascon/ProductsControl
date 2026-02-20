from fastapi import APIRouter
from fastapi.responses import JSONResponse
from smartx_rfid.utils.path import get_prefix_from_path
from app.schemas.controller import AddType, AddReader
from app.services.controller import controller
import logging

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
	'/get_reader_type/{reader_type_id}',
	summary='Get a reader type by ID',
)
async def get_reader_type(reader_type_id: int):
	return JSONResponse(content=controller.db_manager.get_reader_type(reader_type_id))


@router.post(
	'/add_reader_type',
	summary='Add a new reader type',
)
async def add_reader_type(reader_type: AddType):
	success, message = controller.db_manager.add_reader_type(**reader_type.model_dump())
	if success:
		logging.info(f'{message}')
		return JSONResponse(content={'message': message})
	else:
		logging.warning(f'{message}')
		return JSONResponse(content={'message': message}, status_code=400)


@router.put(
	'/update_reader_type/{reader_type_id}',
	summary='Update a reader type by ID',
)
async def update_reader_type(reader_type_id: int, reader_type: AddType):
	success, message = controller.db_manager.update_reader_type(
		reader_type_id, **reader_type.model_dump()
	)
	if success:
		logging.info(f'reader_type_id={reader_type_id} | {message}')
		return JSONResponse(content={'message': message})
	else:
		logging.warning(f'reader_type_id={reader_type_id} | {message}')
		return JSONResponse(content={'message': message}, status_code=400)


@router.delete(
	'/delete_reader_type/{reader_type_id}',
	summary='Delete a reader type by ID',
)
async def delete_reader_type(reader_type_id: int):
	success, message = controller.db_manager.delete_reader_type(reader_type_id)
	if success:
		logging.info(f'reader_type_id={reader_type_id} | {message}')
		return JSONResponse(content={'message': message})
	else:
		logging.warning(f'reader_type_id={reader_type_id} | {message}')
		return JSONResponse(content={'message': message}, status_code=400)


@router.get(
	'/get_readers',
	summary='Get all readers',
)
async def get_readers():
	return JSONResponse(content=controller.db_manager.get_readers())


@router.get(
	'/get_reader/{reader_id}',
	summary='Get a reader by ID',
)
async def get_reader(reader_id: int):
	return JSONResponse(content=controller.db_manager.get_reader(reader_id))


@router.get(
	'/get_available_readers',
	summary='Get all available readers',
)
async def get_available_readers():
	return JSONResponse(content=controller.db_manager.get_available_readers())


@router.post(
	'/add_reader',
	summary='Add a new reader',
)
async def add_reader(reader: AddReader):
	success, message = controller.db_manager.add_reader(**reader.model_dump())
	if success:
		logging.info(f'{message}')
		return JSONResponse(content={'message': message})
	else:
		logging.warning(f'{message}')
		return JSONResponse(content={'message': message}, status_code=400)


@router.put(
	'/update_reader/{reader_id}',
	summary='Update a reader by ID',
)
async def update_reader(reader_id: int, reader: AddReader):
	success, message = controller.db_manager.update_reader(reader_id, **reader.model_dump())
	if success:
		logging.info(f'reader_id={reader_id} | {message}')
		return JSONResponse(content={'message': message})
	else:
		logging.warning(f'reader_id={reader_id} | {message}')
		return JSONResponse(content={'message': message}, status_code=400)


@router.delete(
	'/delete_reader/{reader_id}',
	summary='Delete a reader by ID',
)
async def delete_reader(reader_id: int):
	success, message = controller.db_manager.delete_reader(reader_id)
	if success:
		logging.info(f'reader_id={reader_id} | {message}')
		return JSONResponse(content={'message': message})
	else:
		logging.warning(f'reader_id={reader_id} | {message}')
		return JSONResponse(content={'message': message}, status_code=400)


@router.get(
	'/get_decoded_readers',
	summary='Get all decoded readers',
)
async def get_decoded_readers():
	return JSONResponse(content=controller.db_manager.get_decoded_readers())


@router.get(
	'/get_decoded_reader/{reader_id}',
	summary='Get a decoded reader by ID',
)
async def get_decoded_reader(reader_id: int):
	return JSONResponse(content=controller.db_manager.get_decoded_reader(reader_id))


@router.get(
	'/get_decoded_readers_by_ids/{reader_ids}',
	summary='Get decoded readers by a list of IDs',
)
async def get_decoded_readers_by_ids(reader_ids: str):
	ids = [int(id.strip()) for id in reader_ids.split(',')]
	return JSONResponse(content=controller.db_manager.get_decoded_readers_by_ids(ids))
