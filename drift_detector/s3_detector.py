import json
import boto3


class S3DriftDetector:

    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            region_name="ap-south-1"
        )

    def detect_drifts(self):

        findings = []

        with open("../terraform/terraform.tfstate", "r") as f:
            state = json.load(f)

        bucket_name = None

        for resource in state["resources"]:

            if resource["type"] == "aws_s3_bucket":

                bucket_name = (
                    resource["instances"][0]
                    ["attributes"]["bucket"]
                )

                break

        if bucket_name is None:
            return findings

        response = self.s3.get_bucket_versioning(
            Bucket=bucket_name
        )

        actual_status = response.get(
            "Status",
            "Suspended"
        )

        expected_status = "Enabled"

        findings.append({
            "resource": "S3",
            "attribute": "versioning",
            "expected": expected_status,
            "actual": actual_status,
            "drift": expected_status != actual_status,
            "risk": "HIGH"
        })

        return findings
