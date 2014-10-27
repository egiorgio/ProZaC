"""
Class for Handling Nova events in OpenStack's RabbitMQ

Uses the pika library for handling the AMQP protocol, implementing the necessary callbacks for Nova events
"""

__authors__ = "Claudio Marques, David Palma, Luis Cordeiro"
__copyright__ = "Copyright (c) 2014 OneSource Consultoria Informatica, Lda"
__license__ = "Apache 2"
__contact__ = "www.onesource.pt"
__date__ = "01/09/2014"

__version__ = "1.0"

import json
import pika


class NovaEvents:

    def __init__(self, rpc_type, rpc_host, rpc_user, rpc_pass, zabbix_handler, ceilometer_handler):

        """
        TODO
        :type self: object
        """
        self.rpc_type = rpc_type
        self.rpc_host = rpc_host
        self.rpc_user = rpc_user
        self.rpc_pass = rpc_pass
        self.zabbix_handler = zabbix_handler
        self.ceilometer_handler = ceilometer_handler
        print 'Nova listener started'

    def nova_listener(self):

        if self.rpc_type == 'rabbitmq':
            self.nova_amq_rabbitmq()
        elif self.rpc_type == 'qpid':
            self.nova_amq_qpid()

    def nova_amq_rabbitmq(self):
        """
        Method used to listen to nova events

        """

        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.rpc_host,
                                                                       credentials=pika.PlainCredentials(
                                                                           username=self.rpc_user,
                                                                           password=self.rpc_pass)))
        channel = connection.channel()
        result = channel.queue_declare(exclusive=True)
        queue_name = result.method.queue
        channel.exchange_declare(exchange='nova', exchange_type='topic')
        channel.queue_bind(exchange='nova', queue=queue_name, routing_key='notifications.#')
        channel.queue_bind(exchange='nova', queue=queue_name, routing_key='compute.#')
        channel.basic_consume(self.nova_callback_rabbitmq, queue=queue_name, no_ack=True)
        channel.start_consuming()

    def nova_callback_rabbitmq(self, ch, method, properties, body):
        """
        Method used by method nova_amq() to filter messages by type of message.

        :param ch: refers to the head of the protocol
        :param method: refers to the method used in callback
        :param properties: refers to the proprieties of the message
        :param body: refers to the message transmitted
        """
        payload = json.loads(body)

        try:

            tenant_name = payload['_context_project_name']
            type_of_message = payload['event_type']

            if type_of_message == 'compute.instance.create.end':
                instance_id = payload['payload']['instance_id']
                instance_name = payload['payload']['hostname']
                self.zabbix_handler.create_host(instance_name, instance_id, tenant_name)
                print "Creating a host in Zabbix Server"
                self.ceilometer_handler.host_list = self.ceilometer_handler.get_hosts_ID()

            elif type_of_message == 'compute.instance.delete.end':
                host = payload['payload']['instance_id']
                try:
                    host_id = self.zabbix_handler.find_host_id(host)
                    self.zabbix_handler.delete_host(host_id)
                    print "Deleting host from Zabbix Server"
                    self.ceilometer_handler.host_list = self.ceilometer_handler.get_hosts_ID()

                except:
                    pass    # TODO
            else:
                pass    # TODO
        except:
            pass    # TODO


    def nova_amq_qpid(self):

        from qpid.messaging.endpoints import Connection

        connection = Connection(self.rpc_host,username="guest",password="guest")
        connection.open()
        session = connection.session()
        receiver = session.receiver('nova/notifications.#')
        print "starting loop"
        self.nova_qpid_loop (receiver)
        

    def nova_qpid_loop(self,recv):

        while True:

            print "in the loop"
            message = recv.fetch()
            event_type=message.content['event_type'] 
            print "Event %s "%(event_type)

            if event_type == "compute.instance.create.end":
                payload=message.content['payload']
                tenant_name=message.content['_context_project_name']
                instance_id=payload['instance_id']
                instance_name=payload['hostname']
                self.zabbix_handler.create_host(instance_name,
                                                instance_id, tenant_name) 
                print "Creating a host in Zabbix Server" 
                self.ceilometer_handler.host_list = self.ceilometer_handler.get_hosts_ID()

            elif event_type == "compute.instance.delete.end":
                payload=message.content['payload']
                instance_id=payload['instance_id'] 
                host_id = self.zabbix_handler.find_host_id(instance_id)
                self.zabbix_handler.delete_host(host_id) 
                print "Deleting host from Zabbix Server" 
                self.ceilometer_handler.host_list= self.ceilometer_handler.get_hosts_ID() 

            else: pass  
        
