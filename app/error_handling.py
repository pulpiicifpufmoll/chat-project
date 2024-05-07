from flask import Blueprint
from flask import render_template
bp_errors = Blueprint("errors", __name__, template_folder="templates")

@bp_errors.app_errorhandler(404)
def handle_404(err):
    return render_template("base/error_pages/404.html"),404
@bp_errors.app_errorhandler(500)
def handle_500(err):
    return render_template("base/error_pages/500.html"),500
@bp_errors.app_errorhandler(403)
def handle_403(err):
    return render_template("base/error_pages/403.html"),403
@bp_errors.app_errorhandler(403)
def handle_401(err):
    return render_template("base/error_pages/401.html"),401