// Copyright (c) 2024, Rijosh and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Flight", {
	refresh(frm) {
		frm.add_custom_button(
			"Change Gate Number",
			function () {
				let dialog = new frappe.ui.Dialog({
					title: "Select Gate Number",
					fields: [
						{
							label: "Gate Number",
							fieldname: "seat_number",
							fieldtype: "Data",
							reqd: true,
						},
					],
					primary_action_label: "Change",
					primary_action(values) {
						frm.set_value("gate_number", values.seat_number);
						dialog.hide();
					},
				});

				dialog.show();
			},
			__("Actions")
		);
	},
});
