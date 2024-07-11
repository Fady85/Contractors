// Copyright (c) 2024, cltd and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Contractor Master Summery"] = {
  filters: [
    {
      fieldname: "contractor",
      label: __("Contractor"),
      fieldtype: "MultiSelectList",
      get_data: function (txt) {
        return frappe.db.get_link_options("Supplier", txt, {
          is_contractor: 1,
        });
      },
    },
    {
      fieldname: "project",
      label: __("Project"),
      fieldtype: "MultiSelectList",
      get_data: function (txt) {
        return frappe.db.get_link_options("Project", txt);
      },
    },
    {
      fieldname: "contractor_group",
      label: __("Contractor Group"),
      fieldtype: "MultiSelectList",
      get_data: function (txt) {
        return frappe.db.get_link_options("Supplier Group", txt);
      },
    },
    {
      fieldname: "is_master",
      label: __("Is Master"),
      fieldtype: "Check",
      default: 1,
      // "default": frappe.datetime.now_date(),
    },
    {
      fieldname: "date_from",
      label: __("Date From"),
      fieldtype: "Date",
      // "default": frappe.datetime.now_date(),
    },
    {
      fieldname: "date_to",
      label: __("Date To"),
      fieldtype: "Date",
      // "default": frappe.datetime.now_date(),
    },
  ],
};
