# -*- coding: utf-8 -*-
# Copyright (c) 2021, Aerele Technologies Private Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe,json
from frappe.model.document import Document
from six import string_types
from frappe.utils import today

class Residence(Document):
	def before_save(self):
		if(self.tenant_name is not None):
			self.current_status="Occupied"
		if(self.paid_advance and self.current_status=="Occupied"):
			self.pending_advance=self.advance-self.paid_advance

@frappe.whitelist()
def absconded_entry(doc):
	if isinstance(doc, string_types):
		doc = frappe._dict(json.loads(doc))
	
	rent_bal = frappe.db.sql('''select tenant_name,sum(outstanding) from `tabTenant Payment` where outstanding > 0 and serial=%s ''', (doc.serial), as_dict=1)
	frappe.msgprint("Linked To Vacated tenants")
	abs_doc=frappe.new_doc('Vacated tenants')
	abs_doc.tenant_name = doc.tenant_name
	abs_doc.tenant_mobile_number = doc.phone_number
	abs_doc.tenant_id_proof_number = doc.proof
	abs_doc.tenant_id_proof_iamge = doc.id_img
	abs_doc.date_of_abscond=today()
	abs_doc.rent_balance=rent_bal[0]['sum(outstanding)']
	abs_doc.advance_paid=doc.paid_advance
	ten_pay=frappe.db.get_list('Tenant Payment', {'tenant_name':doc.tenant_name})
	for i in ten_pay:
		wri_off=frappe.get_doc('Tenant Payment',i.name)
		wri_off.write_off = 1
		wri_off.save()
	abs_doc.save()
	return "Vacant"




	
	
	
	
			

