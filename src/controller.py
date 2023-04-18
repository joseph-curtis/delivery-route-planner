__author__ = "Joseph Curtis"
__license__ = "BSD 4-Clause"
__copyright__ = """Copyright 2023 Joseph Curtis 

 Licensed under the BSD 4-Clause License, (the “Original” or “Old” License);
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

  https://choosealicense.com/licenses/bsd-4-clause/

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 License for the specific language governing permissions and limitations under
 the License.

 If you use this software, please cite it using the metadata from the
 CITATION.cff file.

"""

import model
import utilities


# Date: 11 Apr 2023

def distance_between(address1: model.Vertex, address2: model.Vertex, city_map: model.Graph):
    distance = city_map.edge_weights[(address1, address2)]
    return distance


def min_distance_address_from(from_address: model.Vertex, city_map: model.Graph,
                              truck_packages: utilities.ChainingHashTable):
    closest_address = from_address
    closest_distance = 0.0
    for item in truck_packages:
        if distance_between(from_address, item.destination, city_map) < closest_distance:
            closest_address = item.destination
            closest_distance = distance_between(from_address, item.destination, city_map)

    return closest_address


def truck_load_packages(truck: model.DeliveryTruck, city_map: model.Graph,
                        hub_inventory: utilities.ChainingHashTable):
    # for _ in range(truck.capacity):
    #     try:
    #         next_stop = min_distance_address_from(truck.current_address, city_map, hub_inventory)
    #
    #         closest_package = hub_inventory.__iter__().__next__()
    #         for item in hub_inventory:
    #             min_distance_address_from(truck.current_address, city_map)
    #     except StopIteration:
    #         return truck

    return truck


def truck_deliver_packages(truck: model.DeliveryTruck):
    return truck
