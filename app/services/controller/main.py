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

	def sincronize_omie(self):
		# Synchronize all data with Omie
		try:
			logging.info('Starting synchronization with Omie...')
			omie_clients = self.omie_api.get_all_clients()
			omie_products = self.omie_api.get_all_products()
			logging.info(
				f'Fetched {len(omie_clients)} clients and {len(omie_products)} products from Omie.'
			)

			logging.info('Fetching existing customers and products from the database...')
			db_customers = self.db_manager.get_customers()
			db_customers_names = [c.get('NAME') for c in db_customers]
			db_products = self.db_manager.get_product_types()
			logging.info(
				f'Fetched {len(db_customers)} customers and {len(db_products)} products from the database.'
			)
			# Insert clients that don't exist yet
			to_insert_clients = [c for c in omie_clients if c not in db_customers_names]
			logging.info(f'{len(to_insert_clients)} clients to insert into the database.')
			for client in to_insert_clients:
				self.db_manager.add_customer(client)

			to_insert_products = []
			to_update_products = []

			for product in omie_products:
				existing = next(
					(p for p in db_products if p.get('name') == product.get('codigo')), None
				)
				if existing:
					if existing.get('description') != product.get('descricao'):
						# Update only if description changed
						self.db_manager.update_product_type(
							product_type_id=existing.get('id'),
							description=product.get('descricao'),
						)
						to_update_products.append(product)
				else:
					# Insert new product
					self.db_manager.add_product_type(
						name=product.get('codigo'),
						description=product.get('descricao'),
					)
					to_insert_products.append(product)

			return True, {
				'to_insert_clients': len(to_insert_clients),
				'to_insert_products': len(to_insert_products),
				'to_update_products': len(to_update_products),
			}

		except Exception as e:
			logging.error(f'Error fetching clients from Omie: {e}')
			return False, f'Error fetching clients from Omie: {e}'
