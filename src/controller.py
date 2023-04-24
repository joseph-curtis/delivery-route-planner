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

from datetime import datetime

import model
from utilities import ChainingHashTable


# Date: 24 Apr 2023


def truck_load_packages(truck: model.DeliveryTruck, city_map: model.Graph,
                        hub_inventory: ChainingHashTable):
    for _ in range(truck.capacity):
        try:
            next_stop = min_distance_address_from(truck.current_address, city_map, hub_inventory)

            closest_package = hub_inventory.__iter__().__next__()
            for item in hub_inventory:
                min_distance_address_from(truck.current_address, city_map)
        except StopIteration:
            return truck

    return truck


def load_trucks_manual(starting_address: model.Vertex, packages: ChainingHashTable):
    truck1a = model.DeliveryTruck(starting_address, datetime.strptime('08:00', '%H:%M').time())
    truck1b = model.DeliveryTruck(starting_address, datetime.strptime('09:05', '%H:%M').time())
    truck2a = model.DeliveryTruck(starting_address, datetime.strptime('08:00', '%H:%M').time())
    truck2b = model.DeliveryTruck(starting_address, datetime.strptime('10:20', '%H:%M').time())

    # manual loading:
    truck1a.truck_packages = \
        [packages.get(13), packages.get(14), packages.get(15), packages.get(16), packages.get(19),
         packages.get(20), packages.get(21), packages.get(34), packages.get(39),
         packages.get(27), packages.get(35), ]
    truck2a.truck_packages = \
        [packages.get(1), packages.get(3), packages.get(4), packages.get(7), packages.get(8),
         packages.get(18), packages.get(29), packages.get(30), packages.get(31), packages.get(36),
         packages.get(37), packages.get(38), packages.get(40), ]
    truck1b.truck_packages = \
        [packages.get(6), packages.get(25), packages.get(26), packages.get(28), packages.get(32),
         packages.get(11), packages.get(12), packages.get(17), packages.get(22), packages.get(23), ]
    truck2b.truck_packages = \
        [packages.get(5), packages.get(9),
         packages.get(2), packages.get(10), packages.get(24), packages.get(33), ]

    return truck1a, truck1b, truck2a, truck2b


def truck_deliver_packages(truck: model.DeliveryTruck):
    return truck
