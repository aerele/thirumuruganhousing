from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from datetime import date



@frappe.whitelist()
def get_transactions():
	today = date.today()
	api_key = frappe.request.headers.get('Authorization').split(' ')[1].split(':')[0]
	user = frappe.db.get_value("User",{'api_key':api_key})
	list = []
	#outstanding_rent =[]
	for i in frappe.db.get_list("Collection Log", {"paid_on": today, "collected_by":user, "docstatus":["!=", 2]}, ["name", "serial", "amount","month","year"]):
		outstanding=frappe.db.get_value("Tenant Payment",{"serial" : i.serial},"total_outstanding")
		t=0
		t1=frappe.db.get_value('Residence',{'serial':i.serial},"Advance")
		t2=frappe.db.get_value('Residence',{'serial':i.serial},"paid_advance")
		t=t1-t2
		list.append({
				"name":i.name,
				"serial":i.serial,
				"customer_name": frappe.db.get_value("Residence", i.serial, "tenant_name"),
				"customer_mobile_number": frappe.db.get_value("Residence", i.serial, "phone_number"),
				"area":frappe.db.get_value("Residence",i.serial,"area"),
				"paid_due_amount": i.amount,
				"outstandig":[str(outstanding)+"-"+str(i.month)+"-"+str(i.year),"Advance-"+str(t), "Others"]
				})
	return list

@frappe.whitelist()
def get_collection_log(**dic):
	try:
		api_key = frappe.request.headers.get('Authorization').split(' ')[1].split(':')[0]
		user = frappe.db.get_value("User",{'api_key':api_key})
		if dic['is_rent'] == 'YES':
			c_log=frappe.new_doc('Collection Log')
			c_log.paid_on = date.today()
			c_log.serial = dic['serial']
			c_log.month = dic['month']
			c_log.year = dic['year']
			c_log.is_rent = 'YES'
			c_log.amount = dic['amount']
			c_log.collected_by = user
			c_log.save()
			c_log.submit()
		if dic['is_advance'] =='YES':
			c_log  =frappe.new_doc('Collection Log')
			c_log.serial = dic['serial']
			c_log.paid_on = date.today()
			c_log.month = dic['month']
			c_log.year = dic['year']
			c_log.is_advance = 'YES'
			c_log.amount = dic['amount']
			c_log.collected_by = user
			c_log.save()
			c_log.submit()
		if dic['is_others'] == 'YES':
			c_log=frappe.new_doc('Collection Log')
			c_log.serial = dic['serial']
			c_log.paid_on = date.today()
			c_log.month = dic['month']
			c_log.year = dic['year']
			c_log.is_others = 'YES'
			c_log.amount = dic['amount']
			c_log.collected_by = user
			c_log.save()
			c_log.submit()
	except Exception as e:
		traceback = frappe.get_traceback()
		frappe.log_error(message=traceback)
@frappe.whitelist()
def user_validation():
	return "success"


@frappe.whitelist()
def user_validation():
	return "success"

@frappe.whitelist()
def set_detail_to_app(house_no):
	outstanding_rent =[]
	a = frappe.db.get_value('Residence',{'serial' : house_no},["tenant_name","phone_number", "area"])
	if not a:
		res=frappe.db.sql('''select name  from `tabResidence` where name like '%,%'  ''', as_dict=1)
		res_list=res[0]["name"].split(',')
		if(str(house_no) in res_list):
			house_no=res[0]["name"]
			print(house_no)
			a = frappe.db.get_value('Residence',{'serial' : house_no},["tenant_name","phone_number", "area"])
		
	if frappe.db.get_value('Tenant Payment',{'serial' : house_no},'total_outstanding'):
		l=frappe.db.get_list('Tenant Payment',{'serial' :house_no},['outstanding','month','year'])
		for i in l:
			s = str(i['outstanding'])+"-"+str(i['month'])+"-"+str(i['year'])
			if i['outstanding'] > 0:
				outstanding_rent.append(s)
	t=0
	t1=frappe.db.get_value('Residence',{'serial':house_no},"Advance")
	t2=frappe.db.get_value('Residence',{'serial':house_no},"paid_advance")
	t=t1-t2
	if t:
		outstanding_rent += ["advance-" + str(t)]
	return [a,outstanding_rent ]

@frappe.whitelist()
def cancel_log(logname):
	doc=frappe.get_doc("Collection Log",logname)
	doc.cancel()
