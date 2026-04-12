"""
backend/routes/datalog.py
Routes: /log_stats, /download_log, /clear_log
"""
import os, csv, datetime
from flask import Blueprint, request, jsonify, send_file
from backend.utils.logger  import get_log_file, get_log_lock, LOG_HEADERS

datalog_bp = Blueprint("datalog", __name__)


@datalog_bp.route("/log_stats", methods=["GET"])
def log_stats():
    LOG_FILE = get_log_file()
    if not LOG_FILE or not os.path.exists(LOG_FILE):
        return jsonify({"total_rows": 0, "message": "No data logged yet"})
    try:
        rows = []
        with open(LOG_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
        if not rows:
            return jsonify({"total_rows": 0, "message": "Log is empty"})
        numeric_keys = ["temperature","moisture","ec","ph",
                        "nitrogen","phosphorus","potassium","health_score"]
        avgs = {}
        for k in numeric_keys:
            vals = []
            for r in rows:
                try:
                    v = float(r[k])
                    if v not in (-1, None):
                        vals.append(v)
                except: pass
            avgs[k] = round(sum(vals) / len(vals), 2) if vals else None
        return jsonify({
            "total_rows":    len(rows),
            "first_reading": rows[0]["timestamp"],
            "last_reading":  rows[-1]["timestamp"],
            "log_size_kb":   round(os.path.getsize(LOG_FILE) / 1024, 1),
            "averages":      avgs,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@datalog_bp.route("/download_log", methods=["GET"])
def download_log():
    LOG_FILE = get_log_file()
    if not LOG_FILE or not os.path.exists(LOG_FILE):
        return jsonify({"error": "No data logged yet"}), 404
    fname = f"FarmCare_DataLog_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    return send_file(LOG_FILE, mimetype="text/csv", as_attachment=True, download_name=fname)


@datalog_bp.route("/clear_log", methods=["POST"])
def clear_log():
    LOG_FILE  = get_log_file()
    _log_lock = get_log_lock()
    try:
        with _log_lock:
            with open(LOG_FILE, "w", newline="") as f:
                csv.writer(f).writerow(LOG_HEADERS)
        return jsonify({"status": "ok", "message": "Log cleared — headers preserved"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
