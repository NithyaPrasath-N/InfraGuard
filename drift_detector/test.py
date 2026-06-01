from terraform_executor import TerraformExecutor

tf = TerraformExecutor()

result = tf.apply_changes()

print(result["success"])
print(result["output"])
print(result["error"])
