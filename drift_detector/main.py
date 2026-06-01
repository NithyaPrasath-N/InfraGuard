from ec2_detector import EC2DriftDetector
from sg_detector import SecurityGroupDriftDetector
from s3_detector import S3DriftDetector
from risk_engine import RiskEngine
from remediation_engine import RemediationEngine
from db import Database


all_findings = []

# ---------------------------
# Run Drift Detectors
# ---------------------------

ec2 = EC2DriftDetector()
all_findings.extend(
    ec2.detect_drifts()
)

sg = SecurityGroupDriftDetector()
all_findings.extend(
    sg.detect_drifts()
)

s3 = S3DriftDetector()
all_findings.extend(
    s3.detect_drifts()
)

# ---------------------------
# Save Findings
# ---------------------------

db = Database()

scan_id = db.get_next_scan_id()

for finding in all_findings:

    db.save_finding(
        finding,
        scan_id
    )

# ---------------------------
# Risk Calculation
# ---------------------------

risk_engine = RiskEngine()

score = risk_engine.calculate_score(
    all_findings
)

status = risk_engine.get_status(
    score
)

# ---------------------------
# Remediation Engine
# ---------------------------

remediation_engine = RemediationEngine()

# ---------------------------
# Report
# ---------------------------

print("\n========== DRIFT REPORT ==========\n")

for finding in all_findings:

    recommendation = (
        remediation_engine.get_recommendation(
            finding
        )
    )

    print(f"Resource  : {finding['resource']}")
    print(f"Attribute : {finding['attribute']}")
    print(f"Expected  : {finding['expected']}")
    print(f"Actual    : {finding['actual']}")
    print(f"Risk      : {finding['risk']}")

    if finding["drift"]:

        print("Status    : 🚨 DRIFT DETECTED")

        print(
            f"Recommendation : {recommendation}"
        )

    else:

        print("Status    : ✅ NO DRIFT")

    print("-" * 50)

print("\n========== RISK SUMMARY ==========\n")

print(
    f"Total Risk Score : {score}"
)

print(
    f"Infrastructure Status : {status}"
)

print("\n==================================")
