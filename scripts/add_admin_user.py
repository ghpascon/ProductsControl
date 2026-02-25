from smartx_rfid.smtx_db import SmtxDb
from smartx_rfid.auth import AuthManager


def main():
	auth_manager = AuthManager()
	password = auth_manager.hash_password('Smtx4321$')
	db = SmtxDb('mysql+pymysql://root:admin@localhost:3306/orders')
	success, message = db.add_user('admin', password, 'admin')
	if success:
		print('Admin user added successfully.')
	else:
		print(f'Failed to add admin user: {message}')


if __name__ == '__main__':
	main()
