frappe.ui.form.on("Supplier", {
  //////////////////////////////////////////
  ///////////// Start Custom //////////////
  ////////////////////////////////////////

  onload: function (frm) {
    frm.set_query("work_account", () => {
      return {
        filters: {
          account_type: "Expense Account",
        },
      };
    });
  },

  //////////////////////////////////////////
  ///////////// Start Custom //////////////
  ////////////////////////////////////////
});