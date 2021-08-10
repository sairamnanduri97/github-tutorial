import boto3
import paramiko

def ssh_connect_with_retry(ssh, ip_address, retries):
    privkey = paramiko.RSAKey.from_private_key_file('/Users/sairaghuramnanduri/Downloads/python/lab-kp.pem')
    interval = 0
    try:
        retries += 1
        print('SSH into the instance: {}'.format(ip_address))
        #print('key: {}'.format(privkey))
        ssh.connect(hostname=ip_address, username="ec2-user", pkey=privkey)
        return True
    except Exception as e:
        print(e)
        #time.sleep(interval)
        print('Retrying SSH connection to {}'.format(ip_address))
        ssh_connect_with_retry(ssh, ip_address, retries)

# get your instance ID from AWS dashboard

# get instance
ec2 = boto3.resource('ec2', region_name='us-east-1')
i = []

# Get information for all running instances
running_instances = ec2.instances.filter(Filters=[{
    'Name': 'instance-state-name',
    'Values': ['running']}])

for instance in running_instances:
    i.append(instance.id)

current_instance = list(ec2.instances.filter(InstanceIds=i))
ip_address = current_instance[0].public_ip_address

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh_connect_with_retry(ssh, ip_address, 0)
print("***********test***************")
stdin, stdout, stderr = ssh.exec_command("sudo yum install -y https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/linux_amd64/amazon-ssm-agent.rpm; sudo systemctl status amazon-ssm-agent")
print('stdout:', stdout.read())
print('stderr:', stderr.read())




 