"""
Class which defines an Item for Zabbix

This class defines an item with his attributes. Objects created with this class are useful when using the 'item.create' of the Zabbix API.
"""

__authors__ = "Daniele Belfiore, Andrea Valentini Albanelli, Matteo Pergolesi"
__copyright__ = "None"
__license__ = "Apache 2"
__contact__ = "None"
__date__ = "16/10/2014"

__version__ = "1.0"

class Item(object):

    def __init__(self, item_name, item_key, item_template_id, item_units, item_type = 2, item_value_type = 0, item_history = 90, item_trends = 365,
                       item_formula = 1, item_delay = 60):
        """
        Constructor. Please refer to Zabbix 2.2 documentation for further informations.
        https://www.zabbix.com/documentation/2.2/manual/api/reference/item/object#host
        
        :item_name: Name of the item.
        :item_key: Item key (it should be unique).
        :item_template_id: ID of the parent template item.
        :item_type: Type of the item. Default is 2, Zabbix Trapper (Trapper items accept incoming data instead of querying for it. )
        :item_value_type: Type of information of the item. Default is 0, numeric float.
        :item_history: Number of days to keep item's history data.
        :item_trends: Number of days to keep item's trends data. Trends keep averaged information on hourly basis (less resource-hungry than history).
        :item_units: Value units (any string).
        :item_formula: Custom multiplier (default is 1).
        :item_delay: Update interval of the item in seconds. 
        """
        
        self.name = item_name
        self.key = item_key
        self.template_id = item_template_id
        self.type = item_type
        self.value_type = item_value_type
        self.history = item_history
        self.trends = item_trends
        self.units = item_units
        self.formula = item_formula
        self.delay = item_delay
        

