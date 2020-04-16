import boto3
import os

def lambda_handler(event, context):
    dest_id = os.environ['DEST_ACCOUNT_ID']
    src_rgn = os.environ['SRC_REGION']

    ec2 = boto3.resource('ec2', region_name=src_rgn, )
    
    # Access the image that needs to be copied
    ec2_client = boto3.client('ec2', region_name=src_rgn, )
    ami_filters = [
        {
            'Name': 'state',
            'Values': [
                'available'
            ]

        }
    ]

    amis = ec2_client.describe_images(Filters=ami_filters, Owners=['self'])

    images = [ami['ImageId'] for ami in amis['Images']]
  
    for ami_id in images:
        
        image = ec2.Image(ami_id)
        
        response = ec2_client.modify_image_attribute(
            ImageId=ami_id,
            LaunchPermission={
                'Add': [
                    {
                        'UserId': dest_id,
                    },
                ],
            },
        )
        
        
    snapshots = ec2_client.describe_snapshots(OwnerIds=['self'])
    
    snapshots_list = [snapshot['SnapshotId'] for snapshot in snapshots['Snapshots']]
    
    for snap_id in snapshots_list:
        snap = ec2.Snapshot(snap_id)
        
        response = ec2_client.modify_snapshot_attribute(
        Attribute='createVolumePermission',
        OperationType='add',
        SnapshotId=snap_id,
        UserIds=[
            dest_id,
        ],
    )
