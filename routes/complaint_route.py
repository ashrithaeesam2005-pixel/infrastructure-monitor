from flask import Blueprint, request, jsonify

complaint_bp = Blueprint("complaint_bp", __name__)

@complaint_bp.route("/generate_complaint", methods=["POST"])
def generate_complaint():

    data = request.get_json()

    issue = data.get("issue")
    location = data.get("location")

    complaint = f"""
Dear Municipal Authority,

I would like to report a civic issue.

Issue: {issue}
Location: {location}

This problem may cause inconvenience to the public. 
Kindly take necessary action.

Thank you.
"""

    return jsonify({
        "complaint": complaint
    })