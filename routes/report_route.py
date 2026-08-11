from flask import Blueprint, request, jsonify
import sqlite3
from database.db import insert_report

report_bp = Blueprint("report_bp", __name__)


# SUBMIT COMPLAINT

@report_bp.route("/submit_report", methods=["POST"])
def submit_report():

    data = request.get_json()

    issue = data.get("issue")
    location = data.get("location")

    complaint_id = insert_report(issue, location)

    return jsonify({
        "message": "Complaint submitted successfully",
        "complaint_id": complaint_id
    })


# CHECK STATUS

@report_bp.route("/check_status/<int:complaint_id>", methods=["GET"])
def check_status(complaint_id):

    conn = sqlite3.connect("civic_reports.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT issue, location, status FROM reports WHERE id=?",
        (complaint_id,)
    )

    result = cursor.fetchone()

    conn.close()

    if result:

        return jsonify({
            "issue": result[0],
            "location": result[1],
            "status": result[2]
        })

    else:

        return jsonify({
            "issue": None,
            "location": None,
            "status": None,
            "message": "Complaint not found"
        })
# GET ALL REPORTS (FOR MAP MARKERS)

@report_bp.route("/get_reports", methods=["GET"])
def get_reports():

    conn = sqlite3.connect("civic_reports.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, issue, location, status FROM reports")

    rows = cursor.fetchall()

    conn.close()

    reports = []

    for row in rows:

        reports.append({
            "id": row[0],
            "issue": row[1],
            "location": row[2],
            "status": row[3]
        })

    return jsonify(reports)