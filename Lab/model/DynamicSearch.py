#!/usr/bin/env python
import itertools
import pprint

from .dynamicsearch import *

__all__ = [f"DiskDynamicSearch", f"LoanDynamicSearch", f"ClientDynamicSearch", ]


class DiskDynamicSearch(DynamicSearchBaseORM):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name: str = "Disk"
		dvd_disk = self.schema.tables.Dvd_disk.ORM
		dvd_rental = self.schema.tables.Dvd_rental.ORM
		self.search: dict[self.SearchCriteriasORM[CompareConstantORM]] = {
			"DiskName": SearchCriteriasORM(dvd_disk.name),
			"genre": SearchCriteriasORM(dvd_disk.genre),
			"date": SearchCriteriasORM(dvd_disk.date),
			"price": SearchCriteriasORM(dvd_disk.price),
			
			"RentalName": SearchCriteriasORM(dvd_rental.name),
			"RentalAddress": SearchCriteriasORM(dvd_rental.address),
			"RentalOwner": SearchCriteriasORM(dvd_rental.owner),
		}

	@property
	def ORM_join(self):
		dvd_disk = self.schema.tables.Dvd_disk.ORM
		dvd_rental = self.schema.tables.Dvd_rental.ORM
		q = \
			dvd_disk.select(
				dvd_disk.name,
				dvd_disk.genre,
				dvd_disk.date,
				dvd_disk.price,

				dvd_rental.name,
				dvd_rental.address,
				dvd_rental.owner,
			) \
			.join(dvd_rental, on=(dvd_disk.DVD_rental_id == dvd_rental.id))
		return q


class LoanDynamicSearch(DynamicSearchBaseORM):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name: str = "Loan"
		dvd_rental = self.schema.tables.Dvd_rental.ORM
		dvd_disk = self.schema.tables.Dvd_disk.ORM
		client = self.schema.tables.Client.ORM
		loan = self.schema.tables.Loan.ORM
		self.search: dict[self.SearchCriteriasORM[CompareConstantORM]] = {
			"date_loan": SearchCriteriasORM(loan.date_loan),
			"date_return": SearchCriteriasORM(loan.date_return),
			"status": SearchCriteriasORM(loan.status),

			"ClientName": SearchCriteriasORM(client.name),
			"ClientSurname": SearchCriteriasORM(client.surname),

			"DiskName": SearchCriteriasORM(dvd_disk.name),
			"genre": SearchCriteriasORM(dvd_disk.genre),
			"date": SearchCriteriasORM(dvd_disk.date),
			"price": SearchCriteriasORM(dvd_disk.price),
			
			# "RentalName": SearchCriteriasORM(dvd_rental.name),
			# "RentalAddress": SearchCriteriasORM(dvd_rental.address),
			# "RentalOwner": SearchCriteriasORM(dvd_rental.owner),
		}

	@property
	def ORM_join(self):
		dvd_rental = self.schema.tables.Dvd_rental.ORM
		dvd_disk = self.schema.tables.Dvd_disk.ORM
		client = self.schema.tables.Client.ORM
		loan = self.schema.tables.Loan.ORM
		q = \
			loan.select(
				loan.date_loan,
				loan.date_return,
				loan.status,

				client.name,
				client.surname,

				dvd_disk.name,
				dvd_disk.genre,
				dvd_disk.date,
				dvd_disk.price,

				# dvd_rental.name,
				# dvd_rental.address,
				# dvd_rental.owner
			) \
			.join(client, on=(loan.client_id == client.id)) \
			.join(dvd_disk, on=(loan.DVD_disk_id == dvd_disk.id)) \
			.join(dvd_rental, on=(dvd_disk.DVD_rental_id == dvd_rental.id))
		return q


class ClientDynamicSearch(DynamicSearchBaseORM):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name: str = "Client"
		client = self.schema.tables.Client.ORM
		self.search: dict[self.SearchCriteriasORM[CompareConstantORM]] = {
			"id": SearchCriteriasORM(client.id),
			"name": SearchCriteriasORM(client.name),
			"surname": SearchCriteriasORM(client.surname),
		}

	@property
	def ORM_join(self):
		client = self.schema.tables.Client.ORM
		q = client.select()
		return q


def _test():
	pass


if __name__ == "__main__":
	_test()
