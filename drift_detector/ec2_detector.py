import json
import boto3


class EC2DriftDetector:

    def __init__(self):

        self.ec2 = boto3.client(
            "ec2",
            region_name="ap-south-1"
        )

    def detect_drifts(self):

        findings = []

        # Read Terraform State
        with open("../terraform/terraform.tfstate", "r") as f:
            state = json.load(f)

        # Find EC2 Resource in Terraform State
        attributes = None

        for resource in state["resources"]:

            if resource["type"] == "aws_instance":

                attributes = (
                    resource["instances"][0]
                    ["attributes"]
                )

                break

        if attributes is None:
            raise Exception(
                "EC2 resource not found in terraform state"
            )

        terraform_instance_type = attributes["instance_type"]

        instance_id = attributes["id"]

        terraform_name_tag = (
            attributes.get("tags", {})
            .get("Name", "")
        )

        # Get AWS Instance Details
        response = self.ec2.describe_instances(
            InstanceIds=[instance_id]
        )

        instance = (
            response["Reservations"][0]
            ["Instances"][0]
        )

        aws_instance_type = instance["InstanceType"]

        # Extract AWS Name Tag
        aws_name_tag = ""

        for tag in instance.get("Tags", []):

            if tag["Key"] == "Name":

                aws_name_tag = tag["Value"]
                break

        # Instance Type Drift
        findings.append({

            "resource": "EC2",

            "attribute": "instance_type",

            "expected": terraform_instance_type,

            "actual": aws_instance_type,

            "drift": (
                terraform_instance_type
                != aws_instance_type
            ),

            "risk": "MEDIUM"

        })

        # Name Tag Drift
        findings.append({

            "resource": "EC2",

            "attribute": "name_tag",

            "expected": terraform_name_tag,

            "actual": aws_name_tag,

            "drift": (
                terraform_name_tag
                != aws_name_tag
            ),

            "risk": "LOW"

        })

        return findings
