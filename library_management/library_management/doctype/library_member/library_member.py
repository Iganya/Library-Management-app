# Copyright (c) 2022, Gift Matthew and contributors
# For license information, please see license.txt

from pydoc import Doc
#import frappe
from frappe.model.document import Document

class LibraryMember(Document):
	#Get the full name from combination of first and last name
	def before_save(self):
		self.full_name = f'{self.first_name} {self.last_name or ""}'
