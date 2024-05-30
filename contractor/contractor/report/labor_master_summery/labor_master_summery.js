// Copyright (c) 2024, cltd and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Labor Master Summery"] = {
  filters: [
    {
      fieldname: "laborer",
      label: __("Laborer"),
      fieldtype: "MultiSelectList",
      get_data: function (txt) {
        return frappe.db.get_link_options("Employee", txt, {
          is_laborer: 1,
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
      fieldname: "is_master",
      label: __("Is Master"),
      fieldtype: "Check",
      default: 1,
    },
  ],
};
