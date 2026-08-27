import frappe


def execute():
	"""Carry forward any value already set in the old single-Gender `applicable_to_gender`
	Link field (from an earlier version of this feature) into the new `applicable_to_genders`
	multiselect table, so no existing configuration is silently lost."""
	if not frappe.db.exists("DocType", "Leave Type Applicable Gender"):
		return

	if not frappe.db.has_column("Leave Type", "applicable_to_gender"):
		return

	rows = frappe.get_all(
		"Leave Type", filters={"applicable_to_gender": ["is", "set"]}, fields=["name", "applicable_to_gender"]
	)
	for row in rows:
		if frappe.db.exists(
			"Leave Type Applicable Gender", {"parent": row.name, "gender": row.applicable_to_gender}
		):
			continue
		doc = frappe.get_doc("Leave Type", row.name)
		doc.append("applicable_to_genders", {"gender": row.applicable_to_gender})
		doc.save()
