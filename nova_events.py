"""
Class for Handling Nova events in OpenStack's RabbitMQ/QPID
Uses either pika or proton libraries for handling the AMQP protocol, depending whether the message broker is RabbitMQ or QPID, and then implements
the necessary callbacks for Nova events, such as instance creation/deletion
"""

__copyright__ = "Istituto Nazionale di Fisica Nucleare (INFN)"
__license__ = "Apache 2"

import json
import pika
import logging

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

        self.logger = logging.getLogger('ZCP')
        self.logger.info('Nova listener started')

    def nova_amq_qpid(self):
        from qpid.messaging.endpoints import Connection
        connection = Connection(self.rpc_host, username = "guest", password = "guest")
        connection.open()
        session = connection.session()
        receiver = session.receiver('nova/notifications.#')

        self.logger.debug ("Starting nova loop")
        self.nova_qpid_loop(receiver)

    def nova_amq_rabbitmq(self):
        """
        Method used to listen to nova events
        """
        connection = pika.BlockingConnection(pika.ConnectionParameters(host = self.rpc_host, credentials = pika.PlainCredentials(username = self.rpc_user, password = self.rpc_pass)))
        channel = connection.channel()
        result = channel.queue_declare(exclusive = True)
        queue_name = result.method.queue
        channel.exchange_declare(exchange = 'nova', exchange_type = 'topic')
        channel.queue_bind(exchange = 'nova', queue = queue_name, routing_key = 'notifications.#')
        channel.queue_bind(exchange = 'nova', queue = queue_name, routing_key = 'compute.#')
        channel.basic_consume(self.nova_callback_rabbitmq, queue = queue_name, no_ack = True)
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
                self.ceilometer_handler.host_list = self.ceilometer_handler.get_hosts_ID()

                self.logger.info("Instance creation detected : creating host %s (tenant %s) on zabbix server" %(instance_name,tenant_name))
            elif type_of_message == 'compute.instance.delete.end':
                host = payload['payload']['instance_id']
                instance_name = payload['payload']['hostname']
                host_id = self.zabbix_handler.find_host_id(host)
                self.zabbix_handler.set_host_unmonitored(host_id)
                self.ceilometer_handler.host_list = self.ceilometer_handler.get_hosts_ID()

                self.logger.info("Instance removal detected : setting to unmonitored host %s from zabbix server" %(instance_name))
        except KeyError, e:
            self.logger.info("JSON KeyError, skipping message..")
            pass

    def nova_listener(self):
        self.logger.info("Contacting nova rpc on host %s (rpc type %s) " %(self.rpc_host,self.rpc_type))

        if self.rpc_type == 'rabbitmq':
            self.nova_amq_rabbitmq()
        elif self.rpc_type == 'qpid':
            self.nova_amq_qpid()

    def nova_qpid_loop(self,recv):
        while True:
            message = recv.fetch()
            event_type=message.content['event_type']
            self.logger.debug("Caught event %s" %(event_type))
            if event_type == "compute.instance.create.end":
                payload=message.content['payload']
                tenant_name=message.content['_context_project_name']
                instance_id=payload['instance_id']
                instance_name=payload['hostname']
                self.zabbix_handler.create_host(instance_name, instance_id, tenant_name)
                self.ceilometer_handler.host_list = self.ceilometer_handler.get_hosts_ID()

                self.logger.info("Instance creation detected : creating host %s (id %s) (tenant %s) on zabbix server" %(instance_name,instance_id,tenant_name))
            elif event_type == "compute.instance.delete.end":
                payload=message.content['payload']
                instance_id=payload['instance_id']
                instance_name = payload['hostname']
                host_id = self.zabbix_handler.find_host_id(instance_id)
                self.zabbix_handler.delete_host(host_id)
                self.ceilometer_handler.host_list= self.ceilometer_handler.get_hosts_ID()

                self.logger.info("Instance removal detected : deleting host %s (%s) from zabbix server" %(instance_name,instance_id))
            else:
                pass
