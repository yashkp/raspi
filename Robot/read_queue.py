from azure.servicebus import ServiceBusService, Message, Queue

bus_service = ServiceBusService(service_namespace='debrisbot-ns',
    shared_access_key_name='RootManageSharedAccessKey',
    shared_access_key_value='QPxUGbIzO33d5oeTjv3NRPe+DLkzP+f+lPwwken6K00=')

#bus_service.create_queue('botqueue')
while(True):
    msg = bus_service.receive_queue_message('botqueue', peek_lock=False)
    if(msg):
        msg = msg.body
        msg = msg.split(' ')[1]
        print(msg)
