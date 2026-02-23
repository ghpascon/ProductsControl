import inspect
import logging
import sys
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.gzip import GZipMiddleware
from app.core import get_user
# =====================
#  AUTO-REGISTRATION
# =====================


def setup_middlewares(app):
	"""Automatically register all BaseHTTPMiddleware subclasses defined in this module"""

	# CORS middleware
	app.add_middleware(
		CORSMiddleware,
		allow_origins=['*'],
		allow_credentials=True,
		allow_methods=['GET', 'POST', 'PUT', 'DELETE'],
		allow_headers=['*'],
	)

	# Auto-register custom middlewares
	current_module = sys.modules[__name__]
	for name, obj in inspect.getmembers(current_module, inspect.isclass):
		if issubclass(obj, BaseHTTPMiddleware) and obj is not BaseHTTPMiddleware:
			app.add_middleware(obj)
			print(f'[Middleware] Registered: {name}')

	app.add_middleware(GZipMiddleware, minimum_size=1000)
	Instrumentator().instrument(app).expose(app, include_in_schema=False)


class SafeRequestMiddleware(BaseHTTPMiddleware):
	"""
	Middleware that wraps every request in a try/except block.
	Returns a JSON error response if any unhandled exception occurs.
	"""

	async def dispatch(self, request, call_next):
		try:
			response = await call_next(request)
			return response
		except Exception as e:
			# Log the error with traceback
			logging.error(f'[Middleware Error] {type(e).__name__}: {e}', exc_info=True)

			# Return JSON error response with safe serialization
			return JSONResponse(
				status_code=500,
				content={
					'message': str(e),
					'error_type': type(e).__name__,
					'path': request.url.path,
				},
			)


class LoggingMiddleware(BaseHTTPMiddleware):
	"""Middleware that logs incoming requests and outgoing responses."""

	async def dispatch(self, request, call_next):
		# Check if the route is 'auth' or 'login'
		paths = ['/auth', '/api/v1/auth/login']
		if request.url.path in paths or request.url.path.startswith('/static'):
			return await call_next(request)

		# Check for token in Authorization header or cookies
		token = request.cookies.get('Authorization') or request.headers.get('Authorization')
		if token:
			if token.startswith('Bearer '):
				token = token[7:]  # Remove 'Bearer ' prefix
			user = get_user(request)
			if user:
				return await call_next(request)

		# Redirect if the URL does not start with '/api'
		if not request.url.path.startswith('/api'):
			return RedirectResponse(url='/auth')

		# Return error response for unauthenticated API requests
		return JSONResponse(status_code=401, content={'error': 'Not logged in'})
