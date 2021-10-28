from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
@frappe.whitelist()
def get_collection_log(dic):
    if dic['is_rent'] == 'YES':
        c_log=frappe.new_doc('Collection Log')
        c_log.serial = dic['serial']
        c_log.month = dic['month']
        c_log.year = dic['year']
        c_log.is_rent = 'YES'
        c_log.amount = dic['amount']
        c_log.collected_by = dic['collected_by']
        c_log.save()
    if dic['is_advance'] =='YES':
        c_log  =frappe.new_doc('Collection Log')
        c_log.serial = dic['serial']
        c_log.month = dic['month']
        c_log.year = dic['year']
        c_log.is_advance = 'YES'
        c_log.amount = dic['amount']
        c_log.collected_by = dic['collected_by']
        c_log.save()
    if dic['is_others'] == 'YES':
        c_log=frappe.new_doc('Collection Log')
        c_log.serial = dic['serial']
        c_log.month = dic['month']
        c_log.year = dic['year']
        c_log.is_others = 'YES'
        c_log.amount = dic['amount']
        c_log.collected_by = dic['collected_by']
        c_log.save()
   







    


