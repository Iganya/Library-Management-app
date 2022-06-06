# Copyright (c) 2022, Gift Matthew and contributors
# For license information, please see license.txt
from __future__ import unicode_literals

import frappe
from frappe.model.document import Document

class LibraryTransaction(Document):
	def before_submit(self):
		if self.type == "Issue":
			self.validate_issue()
			#Set the article status to be Issued
			article = frappe.get_doc("Atricle", self.article)
			article.status = "Issued"
			article.save()
		elif self.type == "Return":
			self.validate_return()
			#This set the article status to be available
			article = frappe.get_doc("Article", self.article)
			article.status = "Available"
			article.save()
	
	def validate_issue(self):
		self.validate_membership()
		article = frappe.get_doc("Article", self.article)
		#Check if article is already issued to another member and throw an error once already issued.
		if article.status == "Issued":
			frappe.throw("Article is already issud by another member")

	def validate_return(self):
		self.validate_membership()
		article = frappe.get_doc("Article", self.article)
		#To return article it should be issued first, this code check if available which means it cannot be returned
		if article.status == "Available":
			frappe.throw("Article cannot be returned without being issued first")

	def validate_maximum_limit(self):
		max_articles = frappe.db.get_single_value("Library Settings", "max_articles")
		count = frappe.db.count(
            "Library Transaction",
            {"library_member": self.library_member, 
			"type": "Issue", 
			"docstatus": 1}, 
        )
		if count >= max_articles:
			frappe.throw("Maximum limit reached for issuing articles")

	def validate_membership(self):
		#This code check the validity of a member
		valid_membership = frappe.db.exists(
			"Library Membership",
			{
				"library_member": self.library_member,
				"docstatus": 1,
				"from_date": ("<", self.date),
				"to_date": (">", self.date),
			},
		)
		if not valid_membership:
			frappe.throw("The meber does not have a valid membership")