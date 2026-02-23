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
			return JSONResponse(status_code=401, content={'error': 'User not found'})
		if not auth_manager.verify_password(auth_data.password, user.get('password_hash')):
			return JSONResponse(status_code=401, content={'error': 'Invalid password'})
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
			status_code=200, content={'message': 'Login successful', 'token': token}
		)
		response.set_cookie(
			key='Authorization',
			value=f'Bearer {token}',
			secure=False,
		)
		return response
	except Exception as e:
		logging.error(f'Error during login: {e}')
		return JSONResponse(status_code=500, content={'error': f'Failed to login: {e}'})


@router.post('/logout')
async def logout():
	response = JSONResponse(status_code=200, content={'message': 'Logout successful'})
	response.delete_cookie(key='Authorization')
	return response


@router.post(
	'/add_user',
	summary='Add a new user',
)
async def add_user(auth_data: AddUserSchema):
	try:
		username = auth_data.username
		password = auth_data.password
		password_hash = auth_manager.hash_password(password)
		role = auth_data.role
		success, id = controller.db_manager.add_user(
			username=username, password_hash=password_hash, role=role
		)
		if not success:
			return JSONResponse(status_code=400, content={'error': 'Failed to add user'})
		return JSONResponse(
			status_code=200, content={'message': 'User added successfully', 'user_id': id}
		)
	except Exception as e:
		logging.error(f'Error adding user: {e}')
		return JSONResponse(status_code=500, content={'error': f'Failed to add user: {e}'})


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
			return JSONResponse(status_code=401, content={'error': 'Unauthorized'})
		if not validate_role(request, 'admin') and user.get('user_id') != user_id:
			return JSONResponse(
				status_code=403,
				content={'error': 'Forbidden: You can only change your own password'},
			)
		new_password_hash = auth_manager.hash_password(new_password)
		success = controller.db_manager.update_user(user_id, password_hash=new_password_hash)
		if not success:
			return JSONResponse(status_code=400, content={'error': 'Failed to change password'})
		return JSONResponse(status_code=200, content={'message': 'Password changed successfully'})
	except Exception as e:
		logging.error(f'Error changing password: {e}')
		return JSONResponse(status_code=500, content={'error': f'Failed to change password: {e}'})
