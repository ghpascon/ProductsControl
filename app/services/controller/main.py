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
			omie_products_codes = [
				p.get('codigo') for p in omie_products if p.get('codigo') is not None
			]

		except Exception as e:
			logging.error(f'Error fetching clients from Omie: {e}')
			return False, f'Error fetching clients from Omie: {e}'
