import logging

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from smartx_rfid.utils.path import get_prefix_from_path

from app.schemas.auth import AuthSchema, AddUserSchema
from app.services import auth_manager
from app.services.controller import controller
from app.core import get_user, validate_role

router_prefix = get_prefix_from_path(__file__)
router = APIRouter(prefix=router_prefix, tags=[router_prefix])


@router.post('/login')
async def login(request: Request, auth_data: AuthSchema):
	try:
		user: dict = controller.db_manager.get_user_by_username(auth_data.username)
		if not user:
			return JSONResponse(status_code=401, content={'error': 'Usuário não encontrado'})
		if not auth_manager.verify_password(auth_data.password, user.get('password_hash')):
			return JSONResponse(status_code=401, content={'error': 'Senha inválida'})
		# Generate and return a token or session here
		token = auth_manager.create_token(
			{
				'user_id': user.get('id'),
				'username': user.get('username'),
				'roles': user.get('role').split(','),  # Convert comma-separated roles into a list
			}
		)
		# Add token to the response headers
		response = JSONResponse(
			status_code=200, content={'message': 'Login realizado com sucesso', 'token': token}
		)
		response.set_cookie(
			key='Authorization',
			value=f'Bearer {token}',
			secure=False,
		)
		return response
	except Exception as e:
		logging.error(f'Error during login: {e}')
		return JSONResponse(status_code=500, content={'error': f'Falha ao realizar login: {e}'})


@router.get('/me')
async def get_current_user(request: Request):
	user = get_user(request)
	if not user:
		return JSONResponse(status_code=401, content={'error': 'Não autorizado'})
	return JSONResponse(
		content={
			'user_id': user.get('user_id'),
			'username': user.get('username'),
			'roles': user.get('roles'),
		}
	)


@router.post('/logout')
async def logout():
	response = JSONResponse(status_code=200, content={'message': 'Logout realizado com sucesso'})
	response.delete_cookie(key='Authorization')
	return response


@router.post(
	'/add_user',
	summary='Add a new user',
)
async def add_user(request: Request, auth_data: AddUserSchema):
	if not validate_role(request, 'admin'):
		return JSONResponse(status_code=403, content={'error': 'Proibido: Apenas administradores'})
	try:
		username = auth_data.username
		password = auth_data.password
		password_hash = auth_manager.hash_password(password)
		role = auth_data.role
		success, id = controller.db_manager.add_user(
			username=username, password_hash=password_hash, role=role
		)
		if not success:
			return JSONResponse(status_code=400, content={'error': 'Erro ao adicionar usuário'})
		return JSONResponse(
			status_code=200, content={'message': 'Usuário adicionado com sucesso', 'user_id': id}
		)
	except Exception as e:
		logging.error(f'Error adding user: {e}')
		return JSONResponse(status_code=500, content={'error': f'Erro ao adicionar usuário: {e}'})


@router.put(
	'/change_password/{user_id}/{new_password}',
)
async def change_password(request: Request, user_id: int, new_password: str):
	try:
		user = get_user(request)
		logging.info(
			f"User {user.get('username') if user else 'Unknown'} is attempting to change password for user_id={user_id}"
		)
		if user is None:
			return JSONResponse(status_code=401, content={'error': 'Não autorizado'})
		if not validate_role(request, 'admin') and user.get('user_id') != user_id:
			return JSONResponse(
				status_code=403,
				content={'error': 'Proibido: Você só pode alterar sua própria senha'},
			)
		new_password_hash = auth_manager.hash_password(new_password)
		success = controller.db_manager.update_user(user_id, password_hash=new_password_hash)
		if not success:
			return JSONResponse(status_code=400, content={'error': 'Erro ao alterar senha'})
		return JSONResponse(status_code=200, content={'message': 'Senha alterada com sucesso'})
	except Exception as e:
		logging.error(f'Error changing password: {e}')
		return JSONResponse(status_code=500, content={'error': f'Erro ao alterar senha: {e}'})


@router.put(
	'/change_role/{user_id}/{new_role}',
)
async def change_role(request: Request, user_id: int, new_role: str):
	try:
		user = get_user(request)
		logging.info(
			f"User {user.get('username') if user else 'Unknown'} is attempting to change role for user_id={user_id}"
		)
		if user is None:
			return JSONResponse(status_code=401, content={'error': 'Não autorizado'})
		if not validate_role(request, 'admin'):
			return JSONResponse(
				status_code=403,
				content={'error': 'Proibido: Apenas administradores podem alterar funções'},
			)
		success = controller.db_manager.update_user(user_id, role=new_role)
		if not success:
			return JSONResponse(status_code=400, content={'error': 'Erro ao alterar função'})
		return JSONResponse(status_code=200, content={'message': 'Função alterada com sucesso'})
	except Exception as e:
		logging.error(f'Error changing role: {e}')
		return JSONResponse(status_code=500, content={'error': f'Erro ao alterar função: {e}'})
