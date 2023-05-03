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

from datetime import datetime, time
import datetime

import model
from utilities import ChainingHashTable


# Date: 29 Apr 2023


def truck_load_packages(truck: model.DeliveryTruck, city_map: model.Graph, hub_inventory):
    for _ in range(truck.capacity):
        try:
            next_stop = model.min_distance_address_from(truck.current_address, city_map, hub_inventory)

            closest_package = hub_inventory.__iter__().__next__()
            for item in hub_inventory:
                model.min_distance_address_from(truck.current_address, city_map)
        except StopIteration:
            return truck

    return truck


def load_trucks_manual(starting_address: model.Vertex, packages: ChainingHashTable):
    """
    Load the delivery trucks manually with the given packages.

    Parameters
    ----------
    starting_address: model.Vertex
        The starting address of the delivery trucks.
    packages: ChainingHashTable
        The package hash table that contains all the packages to be loaded on the trucks.

    Returns
    -------
    tuple of model.DeliveryTruck
        A tuple of four delivery trucks, each loaded with packages according to the manual loading instructions.
    """

    # Set the departure times for each truck
    load_time_truck1a = time(hour=8, minute=0)
    load_time_truck2a = time(hour=8, minute=0)
    load_time_truck1b = time(hour=9, minute=37)
    load_time_truck2b = time(hour=10, minute=20)

    # Create four delivery trucks with their respective departure times
    truck1a = model.DeliveryTruck(starting_address, "Truck 1", load_time_truck1a)
    truck1b = model.DeliveryTruck(starting_address, "Truck 1", load_time_truck1b)
    truck2a = model.DeliveryTruck(starting_address, "Truck 2", load_time_truck2a)
    truck2b = model.DeliveryTruck(starting_address, "Truck 2", load_time_truck2b)

    # Load the packages on each truck manually and update package statuses
    truck1a.inventory = \
        [packages.get(13), packages.get(14), packages.get(15), packages.get(16), packages.get(19),
         packages.get(20), packages.get(21), packages.get(34), packages.get(39),
         packages.get(27), packages.get(35), ]
    for package in truck1a.inventory:
        package.time_loaded = load_time_truck1a
        package.status_loaded = truck1a.label + " En Route"

    truck2a.inventory = \
        [packages.get(1), packages.get(3), packages.get(4), packages.get(7), packages.get(8),
         packages.get(18), packages.get(29), packages.get(30), packages.get(31), packages.get(36),
         packages.get(37), packages.get(38), packages.get(40), ]
    for package in truck2a.inventory:
        package.time_loaded = load_time_truck2a
        package.status_loaded = truck2a.label + " En Route"

    truck1b.inventory = \
        [packages.get(6), packages.get(25), packages.get(26), packages.get(28), packages.get(32),
         packages.get(11), packages.get(12), packages.get(17), packages.get(22), packages.get(23), ]
    for package in truck1b.inventory:
        package.time_loaded = load_time_truck1b
        package.status_loaded = truck1b.label + " En Route"

    truck2b.inventory = \
        [packages.get(5), packages.get(9),
         packages.get(2), packages.get(10), packages.get(24), packages.get(33), ]
    for package in truck2b.inventory:
        package.time_loaded = load_time_truck2b
        package.status_loaded = truck2b.label + " En Route"

    # Return a tuple of the four delivery trucks
    return truck1a, truck1b, truck2a, truck2b


def truck_deliver_packages(truck: model.DeliveryTruck, city_map: model.Graph):
    """
    Delivers all packages on the given delivery truck by traveling to each package destination in the inventory
    and unloading the packages at each destination.

    Parameters
    ----------
    truck : model.DeliveryTruck
        The delivery truck object containing the packages to be delivered and the current location.
    city_map : model.Graph
        The graph object representing the city map.

    Returns
    -------
    model.DeliveryTruck
        The delivery truck object after completing all deliveries.
    """
    def go_to_next_stop(next_stop=None):
        """
        Finds the next stop (package destination or starting location) and
        updates the truck's location, route, miles traveled and travel delta.

        Parameters
        ----------
        next_stop : model.Vertex, optional
            The next package destination to travel to. If not specified, the closest package destination is used.

        Returns
        -------
        None
        """
        if next_stop is None:
            next_stop = model.min_distance_address_from(truck.current_address, city_map, truck.inventory)
        truck.miles_traveled += model.distance_between(truck.current_address, next_stop, city_map)
        delivery_time_hours = truck.miles_traveled / truck.speed_mi_hr
        truck.travel_delta = datetime.timedelta(hours=delivery_time_hours)

        truck.route_list.append(next_stop)
        truck.current_address = next_stop

    def unload_packages():
        """
        Unloads packages at the current stop and updates their delivery time and status.

        Returns
        -------
        None
        """
        for package in truck.inventory:
            if package.destination == truck.current_address:
                # convert departure time to datetime.datetime object
                departure_datetime = datetime.datetime.combine(datetime.date.today(), truck.departure_time)
                # add travel delta to departure time
                delivery_datetime = departure_datetime + truck.travel_delta
                # extract time component from delivery datetime
                delivery_time = delivery_datetime.time()

                package.time_delivered = delivery_time
                package.status_delivered = truck.label + " Delivered " + str(delivery_time)
                truck.inventory.remove(package)

    # Main delivery loop
    starting_address = truck.current_address
    # repeat travel and delivery for each item in the truck
    for _ in range(len(truck.inventory)):
        go_to_next_stop()
        unload_packages()

    # Return to starting location
    go_to_next_stop(starting_address)
    return truck
