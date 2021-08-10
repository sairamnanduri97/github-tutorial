import boto3

region = 'us-east-1'

ec2 = boto3.resource('ec2', region_name='us-east-1')

i=[]

for instance in ec2.instance.all():
    i.append(instance.id)

x = boto3.client('ec2', region_name='us-east-1')

x.stop_instances(InstanceIds= i)





# Check ssm agent is running
for x in i:
    out = ssm.get_connection_status(
        Target = x
    )
    #print(out.Status)