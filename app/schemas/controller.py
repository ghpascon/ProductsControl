from pydantic import BaseModel, Field


class AddType(BaseModel):
	name: str = Field('DEVICE')
	description: str | None = Field(None, description='Optional description of the product type')


class AddReader(BaseModel):
	reader_type_id: int = Field(1, description='ID of the reader type')
	serial_number: str = Field('001122abc', description='Serial number of the reader')
	hostname: str | None = Field('reader-hostname', description='Hostname of the reader')


class AddOrder(BaseModel):
	product_type_id: int = Field(1, description='ID of the product type being ordered')
	client_id: int = Field(1, description='ID of the customer placing the order')
	reader_id: int | None = Field(
		1, description='ID of the reader processing the order, must be greater than 0'
	)
	version: str = Field('v1.0.0', description='Version of the product being ordered')
