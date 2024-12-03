// Copyright (c) 2024, cltd and contributors
// For license information, please see license.txt

frappe.ui.form.on("Labor Voucher", {
  refresh(frm) {
    if (frm.doc.docstatus > 0) {
      frm.add_custom_button(
        "Accounting Ledger",
        function () {
          frappe.route_options = {
            voucher_no: frm.doc.name,
            from_date: frm.doc.date,
            to_date: moment(frm.doc.modified).format("YYYY-MM-DD"),
            company: frm.doc.company,
            group_by: "Group by Voucher (Consolidated)",
            show_cancelled_entries: frm.doc.docstatus === 2,
          };
          frappe.set_route("query-report", "General Ledger");
        },
        "View"
      );
      frm.add_custom_button(
        "New Invoice",
        function () {
          
          const newDoc = frappe.model.get_new_doc("Labor Voucher");
          newDoc.laborer = frm.doc.laborer;
          newDoc.laborer_name = frm.doc.laborer_name;
          newDoc.project = frm.doc.project;
          frappe.set_route("Form", newDoc.doctype, newDoc.name);
        },
        "Create"
      );
      // frm.add_custom_button(
      //   "Payment",
      //   function () {
      //     frm.call({
      //       doc: frm.doc,
      //       method: "entry_account",
      //       freeze: true,
      //       callback: (response) => {
      //         if (response.message) {
      //           const newDoc = frappe.new_doc("Payment Entry", {
      //             payment_type: "Pay",
      //             party_type: "Employee",
      //             party: frm.doc.laborer,
      //             party_name: frm.doc.laborer,
      //             paid_to: response.message,
      //             project: frm.doc.project,
      //             cost_center: frm.doc.cost_center,
      //           });

      //           frappe.set_route("Form", newDoc.doctype, newDoc.name);
      //         } else {
      //           frappe.throw(
      //             "please set due account first in labor settings page"
      //           );
      //         }
      //       },
      //     });
      //   },
      //   "Create"
      // );
      // frm.add_custom_button(
      //   "Payment",
      //   function () {
      //     const newDoc = frappe.new_doc("Payment Entry", {
      //       payment_type: "Pay",
      //       party_type: "Employee",
      //       party: frm.doc.laborer,
      //       party_name: frm.doc.laborer,
      //       paid_to: frm.doc.contractor_account,
      //       project: frm.doc.project,
      //       cost_center: frm.doc.cost_center,
      //     });

      //     frappe.set_route("Form", newDoc.doctype, newDoc.name);
      //   },
      //   "Create"
      // );
    }
  },
  
  onload(frm) {
    frm.set_query("laborer", () => {
      return {
        filters: {
          is_laborer: 1,
        },
      };
    });
  },
  async laborer(frm) {
    if (frm.doc.laborer && frm.doc.project) {
      // get last doc from backend and set it's values to the fields
      await frm.call({
        doc: frm.doc,
        method: "laborer_number",
        freeze: true,
        callback: (response) => {
          if (response.message) {
            let prevDoc = response.message;
            frm.set_value("voucher_number", prevDoc.voucher_number + 1);
            frm.set_value(
              "prev_working_days",
              prevDoc.prev_working_days + prevDoc.current_working_days
            );
            frm.set_value("prev_daily_rate", prevDoc.current_daily_rate);
            frm.set_value(
              "prev_days_amount",
              prevDoc.prev_days_amount + prevDoc.current_days_amount
            );
            frm.set_value(
              "prev_transportation_amount",
              prevDoc.prev_transportation_amount +
                prevDoc.transportation_total_amount
            );
            frm.set_value(
              "prev_bonus_amount",
              prevDoc.prev_bonus_amount + prevDoc.bonus_total_amount
            );
            frm.set_value(
              "prev_voucher_amount",
              prevDoc.prev_voucher_amount + prevDoc.current_voucher_amount
            );
            frm.set_value(
              "prev_voucher_amount",
              prevDoc.prev_voucher_amount + prevDoc.current_voucher_amount
            );
            frm.set_value(
              "accumulated_working_days",
              frm.doc.prev_working_days + prevDoc.current_working_days
            );
          } else {
            frm.set_value("accumulated_working_days", 0);
            frm.set_value("voucher_number", 1);
            frm.set_value("prev_working_days", 0);
            frm.set_value("prev_daily_rate", 0);
            frm.set_value("prev_days_amount", 0);
            frm.set_value("prev_transportation_amount", 0);
            frm.set_value("prev_bonus_amount", 0);
            frm.set_value("prev_voucher_amount", 0);
          }
        },
      });
      await frm.call({
        doc: frm.doc,
        method: "laborer_payments",
        callback: function (response) {
          if (response.message.length) {
            frm.clear_table("labor_payments_list");
            response.message.forEach((item) => {
              let row = frm.add_child("labor_payments_list");
              row.payment_id = item.name;
              row.date = item.posting_date;
              row.pay_account = item.paid_from;
              row.bank_account = item.bank_account;
              row.amount = item.paid_amount;
              row.currency = item.paid_from_account_currency;
            });
            let paymentsTable = frm.doc.labor_payments_list;
            let totalPayments = 0;
            paymentsTable.forEach((item) => {
              if (item.amount) {
                totalPayments += item.amount;
              }
            });
            frm.set_value("total_payments", parseInt(totalPayments));
            frm.refresh_field("total_payments");
            frm.refresh_field("labor_payments_list");
          } else {
            frm.set_value("labor_payments_list", []);
            frm.set_value("total_payments", 0);
            frm.refresh_field("total_payments");
            frm.refresh_field("labor_payments_list");
          }
        },
      });
    }
    await frm.call({
      doc: frm.doc,
      method: "get_laborer_name",
    });
  },
  async project(frm) {
    if (frm.doc.laborer && frm.doc.project) {
      // get last doc from backend and set it's values to the fields
      await frm.call({
        doc: frm.doc,
        method: "laborer_number",
        freeze: true,
        callback: (response) => {
          if (response.message) {
            let prevDoc = response.message;
            frm.set_value("voucher_number", prevDoc.voucher_number + 1);
            frm.set_value(
              "prev_working_days",
              prevDoc.prev_working_days + prevDoc.current_working_days
            );
            frm.set_value("prev_daily_rate", prevDoc.current_daily_rate);
            frm.set_value(
              "prev_days_amount",
              prevDoc.prev_days_amount + prevDoc.current_days_amount
            );
            frm.set_value(
              "prev_transportation_amount",
              prevDoc.prev_transportation_amount +
                prevDoc.transportation_total_amount
            );
            frm.set_value(
              "prev_bonus_amount",
              prevDoc.prev_bonus_amount + prevDoc.bonus_total_amount
            );
            frm.set_value(
              "prev_voucher_amount",
              prevDoc.prev_voucher_amount + prevDoc.current_voucher_amount
            );
            frm.set_value(
              "prev_voucher_amount",
              prevDoc.prev_voucher_amount + prevDoc.current_voucher_amount
            );
            frm.set_value(
              "accumulated_working_days",
              frm.doc.prev_working_days + frm.doc.current_working_days
            );
          } else {
            frm.set_value("accumulated_working_days", 0);
            frm.set_value("voucher_number", 1);
            frm.refresh_field("voucher_number");
            frm.set_value("prev_working_days", 0);
            frm.set_value("prev_daily_rate", 0);
            frm.set_value("prev_days_amount", 0);
            frm.set_value("prev_transportation_amount", 0);
            frm.set_value("prev_bonus_amount", 0);
            frm.set_value("prev_voucher_amount", 0);
          }
        },
      });
      await frm.call({
        doc: frm.doc,
        method: "laborer_payments",
        callback: function (response) {
          if (response.message.length) {
            frm.clear_table("labor_payments_list");
            response.message.forEach((item) => {
              let row = frm.add_child("labor_payments_list");
              row.payment_id = item.name;
              row.date = item.posting_date;
              row.pay_account = item.paid_from;
              row.bank_account = item.bank_account;
              row.amount = item.paid_amount;
              row.currency = item.paid_from_account_currency;
            });
            let paymentsTable = frm.doc.labor_payments_list;
            let totalPayments = 0;
            paymentsTable.forEach((item) => {
              if (item.amount) {
                totalPayments += item.amount;
              }
            });
            frm.set_value("total_payments", parseInt(totalPayments));
            frm.refresh_field("total_payments");
            frm.refresh_field("labor_payments_list");
          } else {
            frm.set_value("labor_payments_list", []);
            frm.set_value("total_payments", 0);
            frm.refresh_field("total_payments");
            frm.refresh_field("labor_payments_list");
          }
        },
      });
    }
    frappe.call({
      doc: frm.doc,
      method: "labor_cost_center",
      callback: (response) => {
        frm.refresh_field("cost_center");
      },
    });
  },

  current_working_days(frm) {
    frm.set_value(
      "current_days_amount",
      frm.doc.current_working_days * frm.doc.current_daily_rate
    );
    frm.set_value(
      "accumulated_working_days",
      frm.doc.prev_working_days + frm.doc.current_working_days
    );
  },
  current_daily_rate(frm) {
    frm.set_value(
      "current_days_amount",
      frm.doc.current_working_days * frm.doc.current_daily_rate
    );
  },
  transportation_days(frm) {
    frm.set_value(
      "transportation_days_amount",
      frm.doc.transportation_days * frm.doc.transportation_rate
    );
  },
  transportation_rate(frm) {
    frm.set_value(
      "transportation_days_amount",
      frm.doc.transportation_days * frm.doc.transportation_rate
    );
  },
  transportation_days_amount(frm) {
    frm.set_value(
      "transportation_total_amount",
      frm.doc.transportation_days_amount + frm.doc.transportation_fixed_amount
    );
  },
  transportation_fixed_amount(frm) {
    frm.set_value(
      "transportation_total_amount",
      frm.doc.transportation_days_amount + frm.doc.transportation_fixed_amount
    );
  },
  bonus_hours(frm) {
    frm.set_value(
      "bonus_hours_amount",
      frm.doc.bonus_hours * frm.doc.hour_rate
    );
  },
  hour_rate(frm) {
    frm.set_value(
      "bonus_hours_amount",
      frm.doc.bonus_hours * frm.doc.hour_rate
    );
  },
  bonus_hours_amount(frm) {
    frm.set_value(
      "bonus_total_amount",
      frm.doc.bonus_hours_amount + frm.doc.bonus_fixed_amount
    );
  },
  bonus_fixed_amount(frm) {
    frm.set_value(
      "bonus_total_amount",
      frm.doc.bonus_hours_amount + frm.doc.bonus_fixed_amount
    );
  },
  prev_voucher_amount(frm) {
    frm.set_value(
      "total_vouchers_amount",
      frm.doc.prev_voucher_amount + frm.doc.current_voucher_amount
    );
  },
  current_voucher_amount(frm) {
    frm.set_value(
      "total_vouchers_amount",
      frm.doc.prev_voucher_amount + frm.doc.current_voucher_amount
    );
  },
  total_payments(frm) {
    frm.set_value(
      "due_amount",
      frm.doc.total_vouchers_amount - frm.doc.total_payments
    );
  },
  total_vouchers_amount(frm) {
    frm.set_value(
      "due_amount",
      frm.doc.total_vouchers_amount - frm.doc.total_payments
    );
  },
  current_days_amount(frm) {
    frm.set_value(
      "current_voucher_amount",
      frm.doc.current_days_amount +
        frm.doc.transportation_total_amount +
        frm.doc.bonus_total_amount
    );
  },
  transportation_total_amount(frm) {
    frm.set_value(
      "current_voucher_amount",
      frm.doc.current_days_amount +
        frm.doc.transportation_total_amount +
        frm.doc.bonus_total_amount
    );
  },
  bonus_total_amount(frm) {
    frm.set_value(
      "current_voucher_amount",
      frm.doc.current_days_amount +
        frm.doc.transportation_total_amount +
        frm.doc.bonus_total_amount
    );
  },
  prev_working_days(frm) {
    frm.set_value(
      "accumulated_working_days",
      frm.doc.prev_working_days + frm.doc.current_working_days
    );
  },
});
