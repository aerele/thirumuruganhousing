// Copyright (c) 2021, Aerele Technologies Private Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Residence', {
	// refresh: function(frm) {

	// }
	tenant_absconed: function (frm) {
		frappe.call({
			method: "housing.thirumurugan_housing.doctype.residence.residence.absconded_entry",
			args: { doc: frm.doc },
			callback: function (r) {
				frm.doc.current_status = r.message
				frm.refresh_field('current_status');
				cur_frm.save()
				
				
				
			}
		})
	}
});
