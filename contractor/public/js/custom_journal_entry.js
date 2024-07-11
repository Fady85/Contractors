frappe.ui.form.on("Journal Entry", {
  refresh: function(frm) {
    // Disable automatic filling of Party and Party Type by removing the onchange event
    frm.fields_dict.accounts.grid.get_field('party').df.onchange = null;
    frm.fields_dict.accounts.grid.get_field('party_type').df.onchange = null;
}
});

frappe.ui.form.on("Journal Entry Account", {
  accounts_add(frm) {
    let doc = frm.doc;
    var row = doc.accounts[doc.accounts.length - 1];
    if (doc.accounts.length >= 2) {
      let prev_remark = doc.accounts[doc.accounts.length - 2].user_remark;
      row.user_remark = prev_remark;
    }
  },
});

