#!/usr/bin/env python3

# import psycopg2
# import psycopg2.sql
# import psycopg2.extensions
import Lab.utils
import peewee


from . import DynamicSearch
from .AutoSchema import *


database_proxy = peewee.DatabaseProxy()


class DVD_rental_store_table(peewee.Model):
	class Meta(object):
		database = database_proxy
		schema = f"DVD_rental_store"


class DVD_rental(DVD_rental_store_table):
	address = peewee.CharField(max_length=255, null=False)
	name = peewee.CharField(max_length=255, null=False)
	owner = peewee.CharField(max_length=255, null=False)


class DVD_disk(DVD_rental_store_table):
	DVD_rental_id = peewee.ForeignKeyField(DVD_rental, backref="disks")
	name = peewee.CharField(max_length=255, null=False)
	genre = peewee.CharField(max_length=255, null=False)
	date = peewee.DateTimeField(null=False)
	price = peewee.DecimalField(null=False)


class client(DVD_rental_store_table):
	name = peewee.CharField(max_length=255, null=False)
	surname = peewee.CharField(max_length=255, null=False)


class loan(DVD_rental_store_table):
	DVD_disk_id = peewee.ForeignKeyField(DVD_disk, backref="loanded")
	client_id = peewee.ForeignKeyField(client, backref="loans")
	date_loan = peewee.DateTimeField(null=False)
	date_return = peewee.DateTimeField(null=False)
	status = peewee.CharField(max_length=255, null=False)


class DVD_rentalTable(SchemaTableORM):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.ORM = DVD_rental


class DVD_diskTable(SchemaTableORM):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.ORM = DVD_disk


class clientTable(SchemaTableORM):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.ORM = client


class loanTable(SchemaTableORM):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.ORM = loan


class DVD_rental_store(Schema):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._dynamicsearch = {a.name: a for a in [DynamicSearch.DiskDynamicSearch(self), DynamicSearch.LoanDynamicSearch(self), DynamicSearch.ClientDynamicSearch(self), ]}
		database_proxy.initialize(self.dbconn)
		# self.reoverride()

	def reoverride(self):
		# print(f"reoverride")
		# Table override
		
		# setattr(self.tables, f"DVD-rental", DVD_rentalTable(self, f"DVD-rental"))
		# setattr(self.tables, f"DVD-disk", DVD_diskTable(self, f"DVD-disk"))
		self.tables.Dvd_rental = DVD_rentalTable(self, f"dvd_rental")
		self.tables.Dvd_disk = DVD_diskTable(self, f"dvd_disk")
		self.tables.Client = clientTable(self, f"client")
		self.tables.Loan = loanTable(self, f"loan")

	def reinit(self):
		# sql = f"""
		# 	SELECT table_name FROM information_schema.tables
		# 	WHERE table_schema = '{self}';
		# """
		with self.dbconn.cursor() as dbcursor:
			# dbcursor.execute(sql)
			for a in self.refresh_tables():  # tuple(dbcursor.fetchall()):
				q = f"""DROP TABLE IF EXISTS {a} CASCADE;"""
				# print(q)
				dbcursor.execute(q)
		# self.dbconn.commit()
		self.dbconn.create_tables([DVD_rental, DVD_disk, client, loan])
		self.dbconn.commit()
		tables = self.refresh_tables()
		# print(tables)
		self.reoverride()

	def randomFill(self):
		self.tables.Dvd_rental.randomFill(1_000)
		self.tables.Dvd_disk.randomFill(1_000)
		self.tables.Client.randomFill(2_000)
		self.tables.Loan.randomFill(2_000)


def _test():
	pass


if __name__ == "__main__":
	_test()
