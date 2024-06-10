frappe.ui.form.on("Journal Entry", {});

frappe.ui.form.on("Journal Entry Account", {
  accounts_add(frm) {
    let doc = frm.doc;
    var row = doc.accounts[doc.accounts.length - 1];
    console.log(doc.accounts);
    if (doc.accounts.length >= 2) {
      let prev_remark = doc.accounts[doc.accounts.length - 2].user_remark;
      row.user_remark = prev_remark;
    }
  },
});
