// Copyright (c) 2024, cltd and contributors
// For license information, please see license.txt

frappe.ui.form.on("Labor Settings", {
  onload(frm) {
    frm.set_query("labor_due_account", () => {
      return {
        filters: {
          is_group: 0,
        },
      };
    });
    frm.set_query("labor_expense_account", () => {
      return {
        filters: {
          is_group: 0,
        },
      };
    });
  },
});
