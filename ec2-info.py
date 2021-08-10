import boto3

ssm = boto3.client('ssm', region_name='us-east-1')
ec2 = boto3.resource('ec2', region_name='us-east-1')
i = []

# Get information for all running instances
running_instances = ec2.instances.filter(Filters=[{
    'Name': 'instance-state-name',
    'Values': ['running']}])

for instance in running_instances:
    i.append(instance.id)

# Check ssm agent is running
for x in i:

    print("\n",x)
    out = ssm.get_connection_status(
        Target = x
    )
    
    status = out['Status']

    if status == "connected":
        print("ssm insttalled. installing inspector")
        response = ssm.send_command(
        InstanceIds = [x],
        DocumentName = 'AmazonInspector-ManageAWSAgent',
        )
        print("inspector agent installed")
    else:
        print("ssm not installed. installing ssm")