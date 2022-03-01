# Copyright (c) 2022, Aerele Technologies Private Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Vacatedtenants(Document):
	def before_submit(self):
		res_details =frappe.get_doc('Residence',{'name': self.serial})
		res_details.tenant_name=None
		res_details.phone_number=None
		res_details.id_proof_number=None
		res_details.id_proof=None
		res_details.paid_advance=None
		res_details.pending_advance=None
		res_details.start_date=None
		res_details.current_status="Vacant"
		res_details.save()
