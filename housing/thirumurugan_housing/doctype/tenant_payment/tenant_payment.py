# -*- coding: utf-8 -*-
# Copyright (c) 2021, Aerele Technologies Private Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import date_diff
from frappe.utils import today
from datetime import datetime
from datetime import date
from calendar import monthrange
class TenantPayment(Document):
	def before_save(self):
		if(self.rent and self.paid_amount):
			self.outstanding=abs(self.rent-self.paid_amount)
		else:
			self.outstanding=self.rent
		rent_bal = frappe.db.sql('''select tenant_name,sum(outstanding) from `tabTenant Payment` where outstanding > 0 and serial=%s and name!=%s''', (self.serial,self.name), as_dict=1)
		if(rent_bal[0]['sum(outstanding)']):
			self.total_outstanding=self.outstanding+rent_bal[0]['sum(outstanding)']
		else:
			self.total_outstanding=self.outstanding
@frappe.whitelist()
def get_date(tenant_name):
	start_date=""
	if frappe.db.exists("Tenant Payment",{"tenant_name": tenant_name}):
		
		start_date=str(datetime.strptime(frappe.utils.today(), '%Y-%m-%d').replace(day=1))
		sd=start_date.split()
		start_date = sd[0]
	else:
		start_date = frappe.db.get_value('Residence', {'tenant_name':tenant_name}, ['start_date'])
	return start_date
def rent_payment():
	Date=date.today()
	if(Date.day!=1):
		return
	oc_res = frappe.db.get_list('Residence',{'current_status': 'Occupied'})
	Month=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
	for res in oc_res:
		res_details =frappe.db.get_list('Residence',{'name': res['name']},['serial', 'tenant_name', 'phone_number', 'rent','start_date'])
		tenant_entry =frappe.new_doc('Tenant Payment')
		tenant_entry.serial = res_details[0]['serial']
		tenant_entry.tenant_name = res_details[0]['tenant_name']
		tenant_entry.tenant_mobile_number = res_details[0]['phone_number']
		tenant_entry.month = Month[Date.month-1]
		tenant_entry.start_date = res_details[0]['start_date']
		tenant_entry.year=Date.year
		if res_details[0]['start_date'].day!=1 and res_details[0]['start_date'].month ==Date.month-1:
			num_days = monthrange(res_details[0]['start_date'].year,res_details[0]['start_date'].month )[1]
			amount=(res_details[0]['rent']/num_days)*(num_days-(res_details[0]['start_date'].day-1))
			tenant_entry.rent=amount
		else:
			tenant_entry.rent = res_details[0]['rent']
		rent_bal = frappe.db.sql('''select tenant_name,sum(outstanding) from `tabTenant Payment` where outstanding > 0 and serial=%s and name!=%s''', (tenant_entry.serial,tenant_entry.name), as_dict=1)
		if len(rent_bal):
			tenant_entry.total_outstanding = rent_bal[0]['sum(outstanding)']
		tenant_entry.save()


@frappe.whitelist()
def make_tenant_payment(self):
	# Make sure the Residence is changed to Vacant on absconing and vacating
	oc_res = frappe.db.get_list('Residence',{'current_status': 'Occupied'})
	for res in oc_res:
		res_details =frappe.db.get_list('Residence',{'name': res['name']},['serial', 'tenant_name', 'phone_number', 'rent'])
		tenant_entry =frappe.new_doc('Tenant Payment')
		tenant_entry.serial = res_details[0]['serial']
		tenant_entry.tenant_name = res_details[0]['tenant_name']
		tenant_entry.tenant_mobile_number = res_details[0]['phone_number']
		tenant_entry.rent = res_details[0]['rent']
		tenant_entry.month = self.month
		tenant_entry.start_date = get_date(res_details[0]['tenant_name'])
		tenant_entry.paid_on = date.today()
		tot_bal = frappe.db.sql('''select tenant_name, sum(outstanding) from `tabTenant Payment` where outstanding > 0 and serial=%s ''', (tenant_entry.serial), as_dict=1)
		tenant_entry.total_outstanding = tot_bal[0]['sum(outstanding)']
		#tenant_entry.save()
		self.paid_on = frappe.db.get_value('Collection Log',{'serial':self.serial},'paid_on')
		tot=date_diff(self.start_date,self.paid_on)
		tot = abs(tot)+1
		if abs(tot) <=30 or abs(tot) <=31:
			tot_amt = (abs(tot)/30)*self.rent
			self.outstanding = tot_amt-self.paid_amount
		else:
			self.outstanding = self.rent-self.paid_amount
			print(self.outstanding)
		self.total_outstanding += self.outstanding



	
	





		








		

		


	
