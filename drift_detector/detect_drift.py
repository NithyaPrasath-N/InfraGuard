import json
import boto3

# Read Terraform State File
with open("../terraform/terraform.tfstate", "r") as f:
    state = json.load(f)

terraform_instance_type = (
    state["resources"][0]
    ["instances"][0]
    ["attributes"]["instance_type"]
)

instance_id = (
    state["resources"][0]
    ["instances"][0]
    ["attributes"]["id"]
)

print("Terraform Instance Type:", terraform_instance_type)
print("Instance ID:", instance_id)

# Connect AWS
ec2 = boto3.client(
    "ec2",
    region_name="ap-south-1"
)

response = ec2.describe_instances(
    InstanceIds=[instance_id]
)

aws_instance_type = (
    response["Reservations"][0]
    ["Instances"][0]
    ["InstanceType"]
)

print("AWS Instance Type:", aws_instance_type)

print("\nChecking Drift...\n")

if terraform_instance_type != aws_instance_type:
    print("🚨 DRIFT DETECTED!")
else:
    print("✅ NO DRIFT FOUND")
