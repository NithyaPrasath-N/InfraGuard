import json
import boto3


class SecurityGroupDriftDetector:

    def __init__(self):
        self.ec2 = boto3.client(
            "ec2",
            region_name="ap-south-1"
        )

    def detect_drifts(self):

        findings = []

        with open("../terraform/terraform.tfstate", "r") as f:
            state = json.load(f)

        sg_resource = None

        for resource in state["resources"]:
            if resource["type"] == "aws_security_group":
                sg_resource = resource
                break

        if sg_resource is None:
            return findings

        expected_sg_name = (
            sg_resource["instances"][0]
            ["attributes"]["name"]
        )

        response = self.ec2.describe_security_groups(
            GroupNames=[expected_sg_name]
        )

        sg = response["SecurityGroups"][0]

        expected_ports = {80}

        actual_ports = set()

        for permission in sg["IpPermissions"]:

            if "FromPort" in permission:
                actual_ports.add(
                    permission["FromPort"]
                )

        findings.append({
            "resource": "SECURITY_GROUP",
            "attribute": "inbound_ports",
            "expected": list(expected_ports),
            "actual": list(actual_ports),
            "drift": expected_ports != actual_ports,
            "risk": "CRITICAL"
        })

        return findings
