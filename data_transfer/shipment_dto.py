__author__ = 'ashutosh.banerjee'
from IPython import embed

class ShipmentDto:
    def __init__(self, shipments):
        self.shipments = shipments

    def format(self):
        results = []
        for shipment in self.shipments:
            dict = {}
            dict['shipment_id'] = shipment.shipment_id
            dict['creator_organisation'] = shipment.creator_organisation
            dict['body'] = shipment.body
            results.append(dict)
        return results



