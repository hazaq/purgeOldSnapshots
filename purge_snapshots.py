#Delete old Snapshots for a single Volume

import boto3
from datetime import datetime,timedelta
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    #User defined variables 
    snap_vol = 'vol-12345678asdfg' # The volume ID that needs to purged  
    snap_exclude = [ 'snap-09876wxyz' ]  # Any old snapshot you want to exclude from getting purged 
    region = 'us-west-2' # Region where the purge should occure 
    owner_ids = [ '111111111111' ] # Owner id of the snapshot creater
    days = 31   # Retention period of old snapshots

    #Function defined varaibles
    client = boto3.client('ec2', region_name=region)
    now = datetime.now()
    retention = timedelta(days)
    VolSnap = []

    snapshots = client.describe_snapshots( Filters=[ { 'Name': 'volume-id', 'Values': [ snap_vol ]}], OwnerIds=owner_ids )


    for i in range( 0 , len(snapshots["Snapshots"][:])):
        if (now - snapshots["Snapshots"][i]["StartTime"].replace(tzinfo=None) ) > retention :
            VolSnap.append(snapshots["Snapshots"][i]["SnapshotId"])


    for i in range( 0 , len(snap_exclude) ):
        try:
            VolSnap.pop(VolSnap.index(snap_exclude[i]))
            print("Excluding snapshot \"%s\" " % snap_exclude[i])
        except ValueError:
            print("Snapshot \"%s\" does not exsists in my list" % snap_exclude[i])


    for i in range(0 , len(VolSnap)):
        try:
            response = client.delete_snapshot(SnapshotId=VolSnap[i])
            print("Deleting Snapshot with ID %s " % VolSnap[i] )
        except ClientError as e:
            print("Exception found %s " %e )

