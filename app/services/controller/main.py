from smartx_rfid.smtx_db.main import SmtxDb
from smartx_rfid.api.omie import ApiOmie
from app.core import settings
import logging


class Controller:
	def __init__(self, db_url: str | None = None):
		self.db_url = db_url
		self.db_manager = SmtxDb(db_url)
		if settings.APP_KEY is None or settings.APP_SECRET is None:
			raise ValueError('APP_KEY and APP_SECRET must be set in the configuration.')
		self.omie_api = ApiOmie(app_key=settings.APP_KEY, app_secret=settings.APP_SECRET)

	async def sincronize_omie(self):
		# Synchronize all data with Omie
		try:
			result = await self.omie_api.get_all_orders()
			success = result.get('success', False)
			total_items = result.get('total_items', 0)
			orders = result.get('orders', [])
			orders_db = self.db_manager.get_product_orders()
			orders_db_dict = {order.get('order_number'): order for order in orders_db}
			to_insert = []
			errors = []
			for order in orders:
				order_db = orders_db_dict.get(order.get('numero_pedido'))
				if not order_db:
					to_insert.append(order)

			logging.info(
				f'Fetched {total_items} orders from Omie. {to_insert} new orders to insert into the database.'
			)

			for order in to_insert:
				success, message = self.db_manager.add_product_order(
					order_number=order.get('numero_pedido'),
					client_name=order.get('nome_cliente'),
					client_cnpj=order.get('cnpj_cliente'),
					product_code=order.get('codigo_produto'),
					product_description=order.get('descricao_produto'),
					product_family=order.get('familia_produto'),
				)
				if not success:
					logging.error(f'Error inserting order {order.get("numero_pedido")}: {message}')
					errors.append({'order_number': order.get('numero_pedido'), 'error': message})
				logging.info(
					f'Inserting order {order.get("numero_pedido")}: success={success}, message={message}'
				)

			return True, {
				'all_orders_fetched': success,
				'total_items_fetched': total_items,
				'new_orders_inserted': len(to_insert),
				'errors': errors,
			}

		except Exception as e:
			logging.error(f'Error during Omie synchronization: {e}')
			return False, str(e)
