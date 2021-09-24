from __future__ import unicode_literals
import frappe
@frappe.whitelist()
def apikey_generator():
    