import subprocess


class TerraformExecutor:

    def apply_changes(self, target=None):

        terraform_dir = "../terraform"

        command = [
            "terraform",
            "apply",
            "-auto-approve"
        ]

        if target:
            command.insert(2, f"-target={target}")

        result = subprocess.run(
            command,
            cwd=terraform_dir,
            capture_output=True,
            text=True
        )

        output = result.stdout

        if "No changes." in output:

            output = """
No changes.

Your infrastructure matches the configuration.

Apply complete!
Resources: 0 added, 0 changed, 0 destroyed.
"""

        return {
            "success": result.returncode == 0,
            "output": output,
            "error": result.stderr
        }

