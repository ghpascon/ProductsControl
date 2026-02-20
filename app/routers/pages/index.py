from fastapi import APIRouter, Request
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse

from app.core import settings, templates

router = APIRouter(prefix='', tags=['Pages'])


@router.get('/', response_class=HTMLResponse)
async def index(request: Request):
	return templates.TemplateResponse(
		'pages/index/main.html',
		{'request': request, 'title': settings.TITLE},
		media_type='text/html; charset=utf-8',
	)


@router.get('/docs', response_class=HTMLResponse)
async def docs():
	return get_swagger_ui_html(
		openapi_url='/openapi.json',
		title=settings.TITLE + ' - Docs',
		swagger_js_url='/static/docs/swagger-ui-bundle.js',
		swagger_css_url='/static/docs/swagger-ui.css',
		swagger_favicon_url='/static/images/logo.png',
	)


# [ ORDERS ]
@router.get('/add_reader_page', response_class=HTMLResponse)
async def add_reader_page(request: Request):
	return templates.TemplateResponse(
		'pages/index/add_reader.html',
		{'request': request, 'title': 'Adicionar Leitor'},
		media_type='text/html; charset=utf-8',
	)


@router.get('/add_order_page', response_class=HTMLResponse)
async def add_order_page(request: Request):
	return templates.TemplateResponse(
		'pages/index/add_order.html',
		{'request': request, 'title': 'Criar Pedido'},
		media_type='text/html; charset=utf-8',
	)


@router.get('/add_product_type_page', response_class=HTMLResponse)
async def add_product_type_page(request: Request):
	return templates.TemplateResponse(
		'pages/index/add_product_type.html',
		{'request': request, 'title': 'Adicionar Tipo de Produto'},
		media_type='text/html; charset=utf-8',
	)


@router.get('/add_reader_type_page', response_class=HTMLResponse)
async def add_reader_type_page(request: Request):
	return templates.TemplateResponse(
		'pages/index/add_reader_type.html',
		{'request': request, 'title': 'Adicionar Tipo de Leitor'},
		media_type='text/html; charset=utf-8',
	)


@router.get('/view_order/{order_id}', response_class=HTMLResponse)
async def view_order_page(request: Request, order_id: int):
	return templates.TemplateResponse(
		'pages/index/view_order.html',
		{'request': request, 'title': f'Visualizar Pedido {order_id}', 'order_id': order_id},
		media_type='text/html; charset=utf-8',
	)
