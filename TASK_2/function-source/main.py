import base64
import json
import time
from google.cloud import storage


def hello_pubsub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """

    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    events = [json.loads(line) for line in pubsub_message.split('\n')
              if len(line) > 0]
    for e in events:
        if e['protoPayload']['methodName'] \
            == 'v1.compute.instances.start':
            Start_time = e['receiveTimestamp']
            Stop_time = 1
        elif e['protoPayload']['methodName'] \
            == 'v1.compute.instances.stop':
            Stop_time = e['receiveTimestamp']
        else:
            exit()
        VM_ID = e['resource']['labels']['instance_id']
        VM_Name = e['protoPayload']['resourceName']
    print (VM_ID)
    print (VM_Name)
    
    bucket_name = 'ss-gce-bucket'
    
    timestr = time.strftime("%Y%m%d_%H%M%S")
    blob_name = 'VM_details'+"_"+timestr'+.txt'

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    if Stop_time == 1:
        with blob.open('w') as f:
            f.write('VM Instance ID:')
            f.write(VM_ID)
            f.write('\n')

            f.write('VM Instance Name:' )
            f.write(VM_Name)
            f.write('\n')

            f.write('VM Start Time:')
            f.write(Start_time)
            f.write('\n')
            f.write('--------------------------- ')
    else:
        with blob.open('w') as f:
            f.write('VM Instance ID:')
            f.write(VM_ID)
            f.write('\n')

            f.write('VM Instance Name:' )
            f.write(VM_Name)
            f.write('\n')

            f.write('VM Stop Time:')
            f.write(Stop_time)
            f.write('\n')
            f.write('--------------------------- ')
    with blob.open('r') as f:
        print (f.read())