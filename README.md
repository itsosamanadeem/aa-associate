# 🎓 Odoo 18 - Scholarship Management Module

A powerful and intuitive Odoo 18 module designed for managing student scholarships with support for multi-campus, donor tracking, fee discounting, and analytical views.

---

## 📦 Features

- Manage scholarship requests for students across multiple campuses and categories
- Support for donor grouping and individual donors
- Automatic calculation of monthly and annual discounts
- Detailed tracking of scholarship lines (periodic disbursements)
- Access controls for users and managers
- Pivot and List views for easy analysis
- Smart buttons to calculate, approve, or reject scholarships
- Clean, user-friendly interface with read-only analytics views

---

## 🧩 Models

### `scholarship.scholarship`
Represents a scholarship request/record with:
- Student, campus, class, section
- Donor and donor group
- Monthly fee, discount, and auto-calculated annual discount
- Status workflow: New → Approved / Rejected
- One2many relation to `scholarship.line`

### `scholarship.line`
Represents a line item (monthly/quarterly installment) for a scholarship:
- Auto-filled student and donor info
- Date, description, fee, and status
- Linked to the parent scholarship
- Computed fields for clarity and reporting

---

## 🖼️ Views

### Scholarship (`scholarship.scholarship`)
- ✅ List View: Compact overview with student and status
- ✅ Form View: All fields with a clean layout, smart actions, and a notebook tab for scholarship lines

### Scholarship Lines (`scholarship.line`)
- 📋 List View:
  - Fully **read-only** (`create="false"`, `edit="false"`, `delete="false"`)
  - Displays relevant info like scholarship, student, donor, fee, status
- 📊 Pivot View:
  - Analyze scholarships by status, date, and fund amounts
- 🔍 Search View:
  - Filter by scholarship, student, donor
  - Custom filters like **Approved Only**
  - Group by donor

---

## 🔐 Access Control

- **Scholarship User**: Can calculate lines
- **Scholarship Manager**: Can approve/reject scholarships

---

## 🚀 Actions & Security

- Actions registered to easily access scholarships and lines
- Helpful no-content messages to guide users
- Full support for record rules and group-based permissions

---

## 🛠️ Custom Buttons

- `Calculate Lines`: Auto-generates line entries from date range and fee
- `Approve`: Approves the scholarship
- `Reject`: Rejects the scholarship

---

## 📈 Reporting & Analytics

Using Pivot view, users can:
- Analyze total scholarship amounts
- Track fund disbursement by donor and date
- Review approval status distribution

---

## ✅ Highlights

- 🔒 **List View is completely read-only**: No accidental creation, editing, or deletion
- 🔄 **Computed fields** enhance clarity and reduce redundancy
- 👨‍🎓 Built for educational institutions with complex scholarship structures

---

## 🧪 Future Improvements

- PDF reports for approved scholarships
- Integration with student fee payment system
- Donor portal to track their funded scholarships

---

## 👨‍💻 Developed By

**Osama Nadeem**  
Odoo Technical Consultant at Xynotech  
📧 osamanadeem20@gmail.com

---

> Built with ❤️ for Nasra School's scholarship management.
