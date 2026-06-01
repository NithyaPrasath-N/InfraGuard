from flask import Flask, render_template
import mysql.connector
from ec2_detector import EC2DriftDetector
from sg_detector import SecurityGroupDriftDetector
from s3_detector import S3DriftDetector
from terraform_executor import TerraformExecutor
from db import Database

from flask import redirect
app = Flask(__name__)


@app.route("/")
def dashboard():

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="2005",
        database="infraguard"
    )

    cursor = conn.cursor(dictionary=True)

    # ----------------------------
    # Latest Scan ID
    # ----------------------------

    cursor.execute("""
        SELECT MAX(scan_id) AS latest_scan
        FROM drift_findings
    """)

    latest_scan = cursor.fetchone()["latest_scan"]

    # ----------------------------
    # Load Only Latest Scan
    # ----------------------------

    cursor.execute("""
        SELECT *
        FROM drift_findings
        WHERE scan_id = %s
        AND drift_status = 1
        ORDER BY id DESC
    """, (latest_scan,))

    findings = cursor.fetchall()

    # ----------------------------
    # Metrics
    # ----------------------------

    total_findings = len(findings)

    critical_count = len([
        f for f in findings
        if f["risk"] == "CRITICAL"
    ])

    high_count = len([
        f for f in findings
        if f["risk"] == "HIGH"
    ])

    medium_count = len([
        f for f in findings
        if f["risk"] == "MEDIUM"
    ])

    low_count = len([
        f for f in findings
        if f["risk"] == "LOW"
    ])

    # ----------------------------
    # Risk Score
    # ----------------------------

    risk_score = 0

    for f in findings:

        if not f["drift_status"]:
            continue

        if f["risk"] == "LOW":
            risk_score += 10

        elif f["risk"] == "MEDIUM":
            risk_score += 25

        elif f["risk"] == "HIGH":
            risk_score += 50

        elif f["risk"] == "CRITICAL":
            risk_score += 100

    # ----------------------------
    # Infrastructure Status
    # ----------------------------

    if risk_score >= 100:
        status = "CRITICAL"

    elif risk_score >= 50:
        status = "WARNING"

    else:
        status = "HEALTHY"
     
    # ----------------------------
    # Recommendations
    # ----------------------------

    for finding in findings:

        if finding["resource"] == "EC2":

            if finding["attribute_name"] == "instance_type":

                finding["recommendation"] = \
                    "Restore instance type via Terraform"

            else:

                finding["recommendation"] = \
                    "Review EC2 configuration"

        elif finding["resource"] == "S3":

            finding["recommendation"] = \
                "Enable bucket versioning"

        elif finding["resource"] == "SECURITY_GROUP":

            finding["recommendation"] = \
                "Remove unauthorized inbound ports"

        else:

            finding["recommendation"] = \
                "Manual review required"
    conn.close()

    return render_template(
        "dashboard.html",
        findings=findings,
        total_findings=total_findings,
        critical_count=critical_count,
        high_count=high_count,
        medium_count=medium_count,
        low_count=low_count,
        latest_scan=latest_scan,
        risk_score=risk_score,
        status=status
    )
@app.route("/scan")
def scan_infrastructure():

    db = Database()

    scan_id = db.get_next_scan_id()

    findings = []

    ec2 = EC2DriftDetector()
    findings.extend(
        ec2.detect_drifts()
    )

    sg = SecurityGroupDriftDetector()
    findings.extend(
        sg.detect_drifts()
    )

    s3 = S3DriftDetector()
    findings.extend(
        s3.detect_drifts()
    )

    for finding in findings:

        db.save_finding(
            finding,
            scan_id
        )

    return redirect("/")
@app.route("/remediate/<int:finding_id>")
def remediate(finding_id):

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="2005",
        database="infraguard"
    )

    cursor = conn.cursor(dictionary=True)

    latest_scan_query = """
    SELECT MAX(scan_id) AS latest_scan
    FROM drift_findings
    """

    cursor.execute(latest_scan_query)

    latest_scan = cursor.fetchone()["latest_scan"]

    

    

    cursor.execute("""
        SELECT *
        FROM drift_findings
        WHERE id = %s
    """, (finding_id,))

    finding = cursor.fetchone()

    if not finding:
        return redirect("/")

    recommendation = ""

    if finding["resource"] == "EC2":

        if finding["attribute_name"] == "instance_type":

            recommendation = (
                "Restore EC2 instance type using Terraform"
            )

        else:

            recommendation = (
                "Review EC2 configuration"
            )

    elif finding["resource"] == "S3":

        recommendation = (
            "Enable bucket versioning"
        )

    elif finding["resource"] == "SECURITY_GROUP":

        recommendation = (
            "Remove unauthorized inbound ports"
        )

    else:

        recommendation = (
            "Manual review required"
        )

    conn.close()

    return render_template(
        "remediation.html",

        finding_id=finding_id,

        resource=finding["resource"],

        risk=finding["risk"],

        attribute=finding["attribute_name"],

        expected=finding["expected_value"],

        actual=finding["actual_value"],

        recommendation=recommendation
    

        )
@app.route("/confirm_remediation/<int:finding_id>")
def confirm_remediation(finding_id):

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="2005",
        database="infraguard"
    )

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT MAX(scan_id) AS latest_scan
        FROM drift_findings
    """)

    latest_scan = cursor.fetchone()["latest_scan"]

    cursor.execute("""
        SELECT *
        FROM drift_findings
        WHERE id = %s
    """, (finding_id,))

    finding = cursor.fetchone()

    recommendation = "Review and remediate drift"

    if finding["resource"] == "S3":
        recommendation = "Enable bucket versioning"

    elif finding["resource"] == "SECURITY_GROUP":
        recommendation = "Remove unauthorized inbound ports"

    elif finding["resource"] == "EC2":
        recommendation = "Restore EC2 configuration"

    # Save remediation request
    cursor.execute("""
        INSERT INTO remediation_logs
        (
            resource,
            action_taken,
            status
        )
        VALUES
        (
            %s,
            %s,
            %s
        )
    """,
    (
        finding["resource"],
        recommendation,
        "INITIATED"
    ))

    conn.commit()

    # Run Terraform
    tf = TerraformExecutor()

    if finding["resource"] == "S3":

        terraform_result = tf.apply_changes(
            "aws_s3_bucket_versioning.bucket_versioning"
        )

    elif finding["resource"] == "SECURITY_GROUP":

        terraform_result = tf.apply_changes(
            "aws_security_group.web_sg"
        )

    elif finding["resource"] == "EC2":

        terraform_result = tf.apply_changes(
            "aws_instance.web_server"
        )

    else:   

        terraform_result = tf.apply_changes()

    status = (
        "SUCCESS"
        if terraform_result["success"]
        else "FAILED"
    )

# Update latest remediation log
    cursor.execute("""
        UPDATE remediation_logs
        SET status = %s
        ORDER BY id DESC
        LIMIT 1
    """, (status,))

    conn.commit()

    conn.close()

    return render_template(
        "remediation_success.html",
        resource=finding["resource"],
        action=recommendation,
        status=status,
        terraform_output=terraform_result["output"]
    )
if __name__ == "__main__":
    app.run(debug=True)
