import frappe


def get_context(context):
    context.title = "Leave Report"

    employee = frappe.form_dict.get("employee") or ""
    department = frappe.form_dict.get("department") or ""
    from_date = frappe.form_dict.get("from_date") or ""
    to_date = frappe.form_dict.get("to_date") or ""

    filters = {}
    if employee:
        filters["employee"] = employee
    if department:
        filters["department"] = department
    if from_date:
        filters["to_date"] = [">=", from_date]
    if to_date:
        filters["from_date"] = ["<=", to_date]

    context.leaves = frappe.get_all(
        "Leave Application",
        filters=filters,
        fields=[
            "employee_name",
            "department",
            "leave_type",
            "from_date",
            "to_date",
            "total_leave_days",
            "status",
        ],
        order_by="from_date desc",
    )

    context.summary = {
        "total": len(context.leaves),
        "approved": sum(1 for r in context.leaves if r.status == "Approved"),
        "pending": sum(1 for r in context.leaves if r.status == "Open"),
        "rejected": sum(1 for r in context.leaves if r.status == "Rejected"),
    }

    context.employees = frappe.get_all(
        "Employee", fields=["name", "employee_name"], order_by="employee_name"
    )
    context.departments = frappe.get_all(
        "Department", filters={"is_group": 0}, fields=["name"], order_by="name"
    )

    context.selected = {
        "employee": employee,
        "department": department,
        "from_date": from_date,
        "to_date": to_date,
    }
