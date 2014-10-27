"""
Class for Handling KeystoneEvents in OpenStack's RabbitMQ

Uses the pika library for handling the AMQP protocol, implementing the necessary callbacks for Keystone events
"""

__authors__ = "Claudio Marques, David Palma, Luis Cordeiro"
__copyright__ = "Copyright (c) 2014 OneSource Consultoria Informatica, Lda"
__license__ = "Apache 2"
__contact__ = "www.onesource.pt"
__date__ = "01/09/2014"

__version__ = "1.0"

import json
import pika


class ProjectEvents:

    def __init__(self, rpc_type, rpc_host, rpc_user, rpc_pass, zabbix_handler):

        self.rpc_type = rpc_type
        self.rpc_host = rpc_host
        self.rpc_user = rpc_user
        self.rpc_pass = rpc_pass
        self.zabbix_handler = zabbix_handler

        print 'Project Listener started'

    def keystone_listener(self):

        print "Starting keystone/%s listener (host %s)" %(self.rpc_type,self.rpc_host)
        if self.rpc_type == 'rabbitmq':
            self.keystone_amq_rabbitmq()
        elif self.rpc_type == 'qpid':
            self.nova_amq_qpid()

    def keystone_amq_rabbitmq(self):
        """
        Method used to listen to keystone events (with rabbitmq amq)
        """

        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.rpc_host,
                                                                       credentials=pika.PlainCredentials(
                                                                           username=self.rpc_user,
                                                                           password=self.rpc_pass)))
        channel = connection.channel()
        result = channel.queue_declare(exclusive=True)
        queue_name = result.method.queue
        # exchange name should be made available as option, maybe advanced
        channel.exchange_declare(exchange='keystone', type='topic')
        channel.queue_bind(exchange='openstack', queue=queue_name, routing_key='notifications.#')
        channel.queue_bind(exchange='keystone', queue=queue_name, routing_key='keystone.#')
        channel.basic_consume(self.keystone_callback_rabbitmq, queue=queue_name, no_ack=True)
        channel.start_consuming()

    def keystone_callback_rabbitmq(self, ch, method, properties, body):
        """
        Method used by method keystone_amq() to filter messages by type of message.

        :param ch: refers to the head of the protocol
        :param method: refers to the method used in callback
        :param properties: refers to the proprieties of the message
        :param body: refers to the message transmitted
        """
        payload = json.loads(body)

        if payload['event_type'] == 'identity.project.created':
            
            tenant_id = payload['payload']['resource_info']
            tenants = self.zabbix_handler.get_tenants()
            tenant_name = self.zabbix_handler.get_tenant_name(tenants, tenant_id)
	    print "New project (%s) created -> Host group created" %(tenant_name)
            self.zabbix_handler.group_list.append([tenant_name, tenant_id])

            self.zabbix_handler.create_host_group(tenant_name)

        elif payload['event_type'] == 'identity.project.deleted':
            print "Project deleted - Host group deleted"
            tenant_id = payload['payload']['resource_info']
            self.zabbix_handler.project_delete(tenant_id)


    ## SUPPORT FOR QPID TO BE ADDED 


