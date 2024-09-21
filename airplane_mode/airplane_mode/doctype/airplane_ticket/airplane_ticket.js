// Copyright (c) 2024, Rijosh and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Ticket", {
	refresh(frm) {
		frm.add_custom_button(
			"Assign seat",
			function () {
				// Create a new dialog
				let seat_dialog = new frappe.ui.Dialog({
					title: "Select seat",
					fields: [
						{
							label: "Seat Number",
							fieldname: "seat_number",
							fieldtype: "Data",
							reqd: true, // make this field mandatory
						},
					],
					primary_action_label: "Set",
					primary_action(values) {
						// Set the seat number in the form field
						frm.set_value("seat", values.seat_number);
						seat_dialog.hide();
					},
				});

				// Show the dialog
				seat_dialog.show();
			},
			__("Actions")
		);
	},
});
