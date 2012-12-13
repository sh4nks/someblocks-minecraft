from flask import Blueprint, render_template, g
from flask.ext.login import login_required

mod = Blueprint('admin', __name__, url_prefix='/admin')

@mod.route("/")
@login_required
def admin_panel():
    return render_template("admin/overview.html",
                           title = "Admin Panel",
                           user = g.user)
