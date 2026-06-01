class RemediationEngine:

    def get_recommendation(self, finding):

        resource = finding["resource"]
        attribute = finding["attribute"]

        if not finding["drift"]:
            return "No action required"

        if resource == "EC2" and attribute == "instance_type":
            return "Run Terraform Apply to restore EC2 instance type"

        if resource == "SECURITY_GROUP":
            return "Remove unauthorized inbound rules using Terraform"

        if resource == "S3":
            return "Enable S3 versioning using Terraform"

        return "Manual review required"
