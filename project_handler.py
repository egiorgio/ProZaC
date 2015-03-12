"""
Class for Handling KeystoneEvents in OpenStack's RabbitMQ/QPID

Uses either pika or proton libraries for handling the AMQP protocol, depending whether the message broker is RabbitMQ or QPID, and then implements
the necessary callbacks for Keystone events, such as tenant creation

"""

__copyright__ = "Istituto Nazionale di Fisica Nucleare (INFN)"
__license__ = "Apache 2"

import json
import pika
import logging

class ProjectEvents:
    def __init__(self, rpc_type, rpc_host, rpc_user, rpc_pass, zabbix_handler):
        self.rpc_type = rpc_type
        self.rpc_host = rpc_host
        self.rpc_user = rpc_user
        self.rpc_pass = rpc_pass
        self.zabbix_handler = zabbix_handler

        self.logger = logging.getLogger('ZCP')
        self.logger.info('Projects listener started')

    def keystone_amq_rabbitmq(self):
        """
        Method used to listen to keystone events (with rabbitmq amq)
        """
        connection = pika.BlockingConnection(pika.ConnectionParameters(host = self.rpc_host, credentials = pika.PlainCredentials(username = self.rpc_user, password = self.rpc_pass)))
        channel = connection.channel()
        result = channel.queue_declare(exclusive = True)
        queue_name = result.method.queue
        # exchange name should be made available as option, maybe advanced
        channel.exchange_declare(exchange = 'openstack', type = 'topic')
        channel.exchange_declare(exchange = 'keystone', type = 'topic')
        channel.queue_bind(exchange = 'openstack', queue = queue_name, routing_key = 'notifications.#')
        channel.queue_bind(exchange = 'keystone', queue = queue_name, routing_key = 'keystone.#')
        channel.basic_consume(self.keystone_callback_rabbitmq, queue = queue_name, no_ack = True)
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
        try:
            if payload['event_type'] == 'identity.project.created':
                tenant_id = payload['payload']['resource_info']
                tenants = self.zabbix_handler.get_tenants()
                tenant_name = self.zabbix_handler.get_tenant_name(tenants, tenant_id)
                self.zabbix_handler.group_list.append([tenant_name, tenant_id])
                self.zabbix_handler.create_host_group(tenant_name)
                self.logger.info("New project (%s) created -> corresponding host group created on zabbix" %(tenant_name))

            elif payload['event_type'] == 'identity.project.deleted':
                tenant_id = payload['payload']['resource_info']
                tenants = self.zabbix_handler.get_tenants()
                tenant_name = self.zabbix_handler.get_tenant_name(tenants, tenant_id)
                self.zabbix_handler.project_delete(tenant_id)
                self.logger.info("Project %s deleted -> Corresponding host group deleted from zabbix" %(tenant_name))

        except KeyError, e:
            self.logger.info("JSON KeyError, skipping message..")
            pass

    def keystone_listener(self):
        self.logger.info("Contacting keystone rpc on host %s (rpc type %s) " %(self.rpc_host, self.rpc_type))

        if self.rpc_type == 'rabbitmq':
            self.keystone_amq_rabbitmq()
        elif self.rpc_type == 'qpid':
            self.nova_amq_qpid()

    ## SUPPORT FOR QPID TO BE ADDED

