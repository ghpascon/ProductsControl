from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from smartx_rfid.utils.path import get_prefix_from_path
from app.services.controller import controller
from app.schemas.auth import AddUserSchema
from app.core import get_user, validate_role
from app.services import auth_manager

router_prefix = get_prefix_from_path(__file__)
router = APIRouter(prefix=router_prefix, tags=[router_prefix])


@router.get(
	'/get_users',
	summary='Get all users',
)
async def get_users(request: Request):
	return JSONResponse(content=controller.db_manager.get_users())


@router.get(
	'/get_user_by_id/{user_id}',
	summary='Get a user by ID',
)
async def get_user_by_id(request: Request, user_id: int):
	return JSONResponse(content=controller.db_manager.get_user(user_id))


@router.get(
	'/get_user_by_username/{username}',
	summary='Get a user by username',
)
async def get_user_by_username(request: Request, username: str):
	return JSONResponse(content=controller.db_manager.get_user_by_username(username))


@router.post(
	'/add_user',
	summary='Add a new user',
)
async def add_user(request: Request, user_data: AddUserSchema):
	if not validate_role(request, 'admin'):
		return JSONResponse(status_code=403, content={'error': 'Proibido: Apenas administradores'})
	try:
		password_hash = auth_manager.hash_password(user_data.password)
		controller.db_manager.add_user(
			username=user_data.username,
			password_hash=password_hash,
			role=user_data.role,
		)
		return JSONResponse(content={'message': 'Usuário adicionado com sucesso'})
	except Exception as e:
		return JSONResponse(status_code=500, content={'error': f'Falha ao adicionar usuário: {e}'})


@router.put(
	'/update_password/{user_id}/{new_password}',
	summary="Update an existing user's password",
)
async def update_password(request: Request, user_id: int, new_password: str):
	user = get_user(request)
	own_account = user and user.get('id') == user_id
	if not own_account and not validate_role(request, 'admin'):
		return JSONResponse(
			status_code=403, content={'error': 'Proibido: Você só pode atualizar sua própria senha'}
		)
	try:
		password_hash = auth_manager.hash_password(new_password)
		controller.db_manager.update_user(user_id, password_hash=password_hash)
		return JSONResponse(content={'message': 'Senha do usuário atualizada com sucesso'})
	except Exception as e:
		return JSONResponse(
			status_code=500, content={'error': f'Falha ao atualizar senha do usuário: {e}'}
		)


@router.delete(
	'/delete_user/{user_id}',
	summary='Delete a user by ID',
)
async def delete_user(request: Request, user_id: int):
	if not validate_role(request, 'admin'):
		return JSONResponse(status_code=403, content={'error': 'Proibido: Apenas administradores'})
	try:
		controller.db_manager.delete_user(user_id)
		return JSONResponse(content={'message': 'Usuário deletado com sucesso'})
	except Exception as e:
		return JSONResponse(status_code=500, content={'error': f'Falha ao deletar usuário: {e}'})
