"""
Backend Routes: Flask Blueprint & HTTP Request Handlers
Connects frontend requests to application services.
Enforces session-based Admin authentication.
Contains ZERO SQL queries and NO direct SQLite database connection.
"""

from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from backend.config import ADMIN_PASSWORD
from backend.app.services.lost_found_service import LostFoundService

routes_bp = Blueprint("routes", __name__)

DEMO_USER_ID = 1  # Student: Rahul


def admin_required(f):
    """Decorator ensuring that only authenticated admin sessions can access admin routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect(url_for("routes.admin_login"))
        return f(*args, **kwargs)
    return decorated_function


@routes_bp.context_processor
def inject_global_data():
    """Injects unread notification count, active user info, and admin status into templates."""
    unread_count = LostFoundService.get_unread_count(DEMO_USER_ID)
    return {
        "current_user_name": "Admin" if session.get("is_admin") else "Rahul (Student)",
        "current_user_id": DEMO_USER_ID,
        "unread_notifications": unread_count,
        "is_admin": session.get("is_admin", False)
    }


# =============================================================================
# STUDENT / PUBLIC ROUTES
# =============================================================================

@routes_bp.route("/")
@routes_bp.route("/dashboard")
def dashboard():
    """Central Executive Dashboard: Comprehensive Metrics, Registries, and DBMS Architecture."""
    dashboard_data = LostFoundService.get_dashboard_data()
    return render_template(
        "dashboard.html",
        active_page="dashboard",
        **dashboard_data
    )


@routes_bp.route("/browse")
def browse():
    """Page 1: Browse Found Items."""
    items = LostFoundService.get_browse_items()
    return render_template("browse.html", items=items, active_page="browse")


@routes_bp.route("/browse/remove/<int:found_item_id>", methods=["POST"])
def remove_found_item(found_item_id):
    """User Action: Permanently remove a found item from SQLite."""
    success, msg = LostFoundService.remove_found_item(found_item_id)
    if success:
        flash(msg, "success")
    else:
        flash(msg, "error")
    return redirect(url_for("routes.browse"))


@routes_bp.route("/report", methods=["GET", "POST"])
def report():
    """Page 2: Report Lost Item."""
    if request.method == "POST":
        item_name = request.form.get("item_name", "").strip()
        category = request.form.get("category", "General").strip()
        description = request.form.get("description", "").strip()
        lost_location = request.form.get("lost_location", "").strip()
        lost_date = request.form.get("lost_date", "").strip()

        success, msg, item_id = LostFoundService.report_lost_item(
            user_id=DEMO_USER_ID,
            item_name=item_name,
            category=category,
            description=description,
            lost_location=lost_location,
            lost_date=lost_date
        )

        if success:
            flash(f"Your lost item report for '{item_name}' has been submitted successfully.", "success")
            return redirect(url_for("routes.my_reports"))
        else:
            flash(f"{msg}", "error")

    return render_template("report.html", active_page="report")


@routes_bp.route("/my-reports")
def my_reports():
    """Page 3: Student's Lost Reports."""
    reports = LostFoundService.get_student_reports(DEMO_USER_ID)
    return render_template("my_reports.html", reports=reports, active_page="my_reports")


@routes_bp.route("/notifications")
def notifications():
    """Page 4: Student Notifications."""
    user_notifications = LostFoundService.get_notifications(DEMO_USER_ID)
    return render_template("notifications.html", notifications=user_notifications, active_page="notifications")


# =============================================================================
# ADMIN AUTHENTICATION & MANAGEMENT ROUTES
# =============================================================================

@routes_bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    """Admin Login: Authenticates administrator password."""
    if session.get("is_admin"):
        return redirect(url_for("routes.admin"))

    if request.method == "POST":
        password = request.form.get("password", "")
        if password == ADMIN_PASSWORD:
            session["is_admin"] = True
            return redirect(url_for("routes.admin"))
        else:
            flash("Invalid admin password.", "error")

    return render_template("admin_login.html", active_page="admin")


@routes_bp.route("/admin/logout")
def admin_logout():
    """Admin Logout: Clears admin session and redirects to Browse page."""
    session.pop("is_admin", None)
    return redirect(url_for("routes.browse"))


@routes_bp.route("/api/admin/unlock", methods=["POST"])
def api_admin_unlock():
    """API endpoint: Verify admin credentials with instant JSON feedback."""
    payload = request.get_json(silent=True) or request.form
    password = payload.get("password", "")
    if password == ADMIN_PASSWORD:
        session["is_admin"] = True
        return jsonify({"success": True, "message": "Admin credentials authenticated successfully."})
    return jsonify({"success": False, "message": "Invalid admin password. Try 'admin@123'"}), 401


@routes_bp.route("/api/admin/lock", methods=["POST"])
def api_admin_lock():
    """API endpoint: Lock admin clearance from the dashboard."""
    session.pop("is_admin", None)
    return jsonify({"success": True, "message": "Admin clearance locked."})



@routes_bp.route("/admin")
@admin_required
def admin():
    """Admin Dashboard: Accessible only after authentication."""
    reports = LostFoundService.get_admin_reports()
    return render_template("admin.html", reports=reports, active_page="admin")


@routes_bp.route("/admin/mark-found/<int:lost_item_id>", methods=["POST"])
@admin_required
def mark_found(lost_item_id):
    """Admin Action: Mark item as FOUND (Protected route)."""
    success, msg = LostFoundService.mark_lost_item_as_found(lost_item_id)
    if success:
        flash("Item has been marked as found and the student has been notified.", "success")
    else:
        flash(f"{msg}", "error")
    return redirect(url_for("routes.admin"))
