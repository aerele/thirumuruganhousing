# -*- coding: utf-8 -*-
# Copyright (c) 2021, Aerele Technologies Private Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import today
class CollectionLog(Document):
	def before_submit(self):
		if self.is_rent =='YES':
			p_key=frappe.db.get_value('Tenant Payment', {'serial': self.serial, 'month': self.month, 'year': self.year}, 'name')
			get_amt=frappe.db.get_value('Tenant Payment', {'serial': self.serial, 'month': self.month, 'year': self.year}, 'outstanding')
			if not self.amount and (float(self.amount) > (get_amt)):
				frappe.throw('Amount is Exceeded then Outstanding')
			t_doc=frappe.get_doc('Tenant Payment', p_key)
			t_doc.paid_amount=t_doc.paid_amount+ float(self.amount)
			t_doc.paid_on = today()
			t_doc.collected_by = self.collected_by
			t_doc.save()

		if  self.is_advance =='YES':
			p_key=frappe.db.get_value('Residence', {'serial': self.serial})
			res_doc=frappe.get_doc('Residence', p_key)
			res_doc.paid_advance=res_doc.paid_advance+ float(self.amount)
			res_doc.save()
			res_doc.reload()
		if self.is_others =='YES':
			pass
	def on_cancel(self):
		if(self.is_advance=="YES"):
			p_key=frappe.db.get_value('Residence', {'serial': self.serial})
			res_doc=frappe.get_doc('Residence', p_key)
			res_doc.paid_advance=res_doc.paid_advance-float(self.amount)
			res_doc.save()
			res_doc.reload()
			pass
		else:
			p_key=frappe.db.get_value('Tenant Payment', {'serial':self.serial, 'month':self.month, 'year':self.year}, 'name')
			t_doc=frappe.get_doc('Tenant Payment', p_key)
			t_doc.paid_amount = t_doc.paid_amount - float(self.amount)
			t_doc.save()


			



	
