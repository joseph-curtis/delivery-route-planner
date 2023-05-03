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

# Date: 29 Apr 2023
from datetime import datetime, timedelta
from typing import Optional


class Vertex:
    """
    A class representing a vertex in a graph.

    Attributes
    ----------
    label : str
        name of the vertex
    address : str
        USPS formatted address
    zipcode : str
        A string representing the zipcode of the address (optional).
    distance : float
        The distance from the starting vertex (default is infinity).
    prev_vertex : Vertex
        A Vertex object representing the previous vertex in the shortest path to this vertex.
    """
    def __init__(self, label: str, address: str, zipcode: str = ''):
        """
        Initializes a new Vertex object.

        Parameters
        ----------
        label : str
            name of the vertex
        address : str
            USPS formatted address
        zipcode : str
            A string representing the zipcode of the address (optional).
        """
        self.label = label
        self.address = address
        self.zipcode = zipcode
        self.distance = float('inf')
        self.prev_vertex = None

    def __eq__(self, other):
        """
        Compares two Vertex objects for equality.

        Parameters
        ----------
        other : Vertex
            A Vertex object to compare.

        Returns
        -------
        bool
            True if the objects are equal, False otherwise.
        """
        return isinstance(other, Vertex) \
            and self.address == other.address \
            and self.zipcode == other.zipcode

    def __hash__(self):
        """
        Computes the hash value of a Vertex object.

        Returns
        -------
        int
            The hash value of the object.
        """
        return hash(self.label + self.address + self.zipcode)

    def __repr__(self):
        """
        Returns a string representation of a Vertex object.

        Returns
        -------
        str
            A string representation of the object.
        """
        return f'Vertex("{self.label}", "{self.address}", "{self.zipcode}")'

    def __str__(self):
        """
        Returns a string representation of a Vertex object.

        Returns
        -------
        str
            A string representation of the object.
        """
        return f'({self.label}: {self.address}; {self.zipcode})'


class Graph:
    """
    A class representing a graph.

    Attributes
    ----------
    adjacency_list : dict
        The graph's vertices and their neighbors.
    edge_weights : dict
        The graph's edges and their weights.

    Methods
    -------
    add_vertex(new_vertex: Vertex):
        Adds a new vertex to the graph.
    add_directed_edge(from_vertex: Vertex, to_vertex: Vertex, weight=1.0):
        Adds a new directed edge to the graph with a given weight.
    add_undirected_edge(vertex_a: Vertex, vertex_b: Vertex, weight=1.0):
        Adds a new undirected edge to the graph with a given weight.
    """
    def __init__(self, adjacency_list=None, edge_weights=None):
        """
        Initializes a Graph object with an empty adjacency list and edge weights dictionary.

        Parameters
        ----------
        adjacency_list : dict, optional
            A dictionary to store the vertices and their neighbors.
        edge_weights : dict, optional
            A dictionary to store the weights of the edges.
        """
        if adjacency_list is None:
            self.adjacency_list = {}  # vertex dictionary {key:value}
        if edge_weights is None:
            self.edge_weights = {}  # edge dictionary {key:value}

    def __repr__(self):
        """
        Returns a string representation of the Graph object.

        Returns
        -------
        str
            A string representation of the Graph object.
        """
        return f'Graph("{self.adjacency_list}", "{self.edge_weights}")'

    def __str__(self):
        """
        Returns a string representation of the Graph's vertices and their edges.

        Returns
        -------
        str
            A string representation of the Graph's vertices and their edges.
        """
        return_string = ''
        for key, value in self.edge_weights.items():
            vertex_a, vertex_b = key
            return_string += str(vertex_a) + "-->" + str(vertex_b) + " : " + str(value) + "\n"
        return "\n".join(str(item) for item in self.adjacency_list) \
            + "\n" + return_string

    def add_vertex(self, new_vertex: Vertex):
        """
        Adds a new vertex to the graph.

        Parameters
        ----------
        new_vertex : Vertex
            The new vertex to be added to the graph.
        """
        if not (new_vertex in self.adjacency_list):
            self.adjacency_list[new_vertex] = []  # {vertex_1: [], vertex_2: [], ...}

    def add_directed_edge(self, from_vertex: Vertex, to_vertex: Vertex, weight=1.0):
        """
        Adds a new directed edge to the graph with a given weight.

        Parameters
        ----------
        from_vertex : Vertex
            The starting vertex of the edge.
        to_vertex : Vertex
            The ending vertex of the edge.
        weight : float, optional
            The weight of the edge. Default is 1.0.
        """
        self.edge_weights[(from_vertex, to_vertex)] = weight
        # {(vertex_1,vertex_2): 484, (vertex_1,vertex_3): 626, (vertex_2,vertex_6): 1306, ...}
        self.adjacency_list[from_vertex].append(to_vertex)
        # {vertex_1: [vertex_2, vertex_3], vertex_2: [vertex_6], ...}

    def add_undirected_edge(self, vertex_a: Vertex, vertex_b: Vertex, weight=1.0):
        """Adds an undirected edge between vertex_a and vertex_b to the graph.

        Parameters
        ----------
        vertex_a : Vertex
            The first vertex of the edge.
        vertex_b : Vertex
            The second vertex of the edge.
        weight : float, optional
            The weight of the edge. Default is 1.0.
        """
        self.add_directed_edge(vertex_a, vertex_b, weight)
        self.add_directed_edge(vertex_b, vertex_a, weight)


class PackageWGUPS:
    """
    A class representing a package in the WGUPS delivery system.

    Attributes
    ----------
    package_id : int
        The ID of the package.
    city : str
        The city where the package is to be delivered.
    state : str
        The state where the package is to be delivered.
    mass_kg : float
        The mass of the package in kilograms.
    notes : str
        Any notes associated with the package.
    destination : Vertex
        The destination vertex for the package.
    deadline_str : str
        The deadline for the package in string format (e.g., "10:30 AM").
    deadline : datetime.time
        The deadline for the package as a datetime.time object.
    status_arrival : str
        The arrival status of the package.
    status_loaded : str
        The loading status of the package.
    status_delivered : str
        The delivery status of the package.
    time_arrived : datetime.time
        The arrival time of the package.
    time_loaded : datetime.time, optional
        The loading time of the package. Defaults to None.
    time_delivered : datetime.time, optional
        The delivery time of the package. Defaults to None.
    """
    def __init__(self, package_id: int, city: str, state: str, mass_kg: float, notes: str,
                 destination: Vertex, deadline_str: str,
                 deadline: Optional[datetime.time] = None,
                 status_arrival: str = "waiting at HUB",
                 time_arrived: Optional[datetime.time] = None):
        """
        Initializes a package class with attributes

        Parameters
        ----------
        package_id : int
            The ID of the package.
        city : str
            The city where the package is to be delivered.
        state : str
            The state where the package is to be delivered.
        mass_kg : float
            The mass of the package in kilograms.
        notes : str
            Any notes associated with the package.
        destination : Vertex
            The destination vertex for the package.
        deadline_str : str
            The deadline for the package in string format (e.g., "10:30 AM").
        deadline : datetime.time, optional
            The deadline for the package as a datetime.time object. Defaults to 23:59:59.999999.
        status_arrival : str, optional
            The arrival status of the package. Defaults to "waiting at HUB".
        time_arrived : datetime.time, optional
            The arrival time of the package. Defaults to 08:00.
        """
        self.package_id = package_id
        self.city = city
        self.state = state
        self.mass_kg = mass_kg
        self.notes = notes
        self.destination = destination
        self.deadline_str = deadline_str
        self.deadline = deadline or datetime.time(hour=23, minute=59, second=59, microsecond=999999)
        self.status_arrival = status_arrival
        self.status_loaded = "awaiting loading"
        self.status_delivered = "not delivered"
        self.time_arrived = time_arrived or datetime.time(hour=8, minute=0)
        self.time_loaded = None
        self.time_delivered = None

    def __repr__(self):
        """
        Returns a string representation of the package.

        Returns
        -------
        str
            A string representation of the package.
        """
        return f'PackageWGUPS("{self.package_id}", "{self.mass_kg}",' \
               f' "{self.notes}", "{self.destination}", "{self.deadline}")'

    def __str__(self):
        """
        Returns a human-readable string representation of the package.

        Returns
        -------
        str
            A string representation of the package.
        """
        return f'Package(ID# "{self.package_id}": "{self.notes}"; TO: "{self.destination}", BY: "{self.deadline}", ' \
               f'DELIVERED: "{self.time_delivered}")'

    def __eq__(self, other):
        """
        Checks if this package is equal to another package.

        Parameters
        ----------
        other : PackageWGUPS
            The other package to compare.

        Returns
        -------
        bool
            True if the packages are equal, False otherwise.
        """
        return isinstance(other, PackageWGUPS) \
            and self.package_id == other.package_id

    def __hash__(self):
        """
        Returns the hash value of the package.

        Returns
        -------
        int
            The hash value of the package.
        """
        return hash(self.package_id)


class DeliveryTruck:
    """
    A class to represent a delivery truck.

    Attributes
    ----------
    current_address : Vertex
        The current address of the truck.
    departure_time : datetime.time, optional
        The time the truck departs from the warehouse, by default 8:00 AM.
    miles_traveled : float, optional
        The number of miles the truck has traveled, by default 0.0.
    speed_mi_hr : float, optional
        The speed of the truck in miles per hour, by default 18.0.
    capacity : int, optional
        The maximum number of packages the truck can carry, by default 16.

    Methods
    -------
    deliver_package(package: Package) -> None:
        Delivers a package to the destination address.
    """
    def __init__(self, current_address: Vertex, label: str,
                 departure_time: datetime.time = datetime.strptime('08:00', '%H:%M').time(),
                 miles_traveled: float = 0.0, speed_mi_hr: float = 18.0, capacity: int = 16):
        """
        Initializes a DeliveryTruck object with the given attributes.

        Parameters
        ----------
        current_address : Vertex
            The current address of the truck.
        label : str
            The identifying name of the truck (eg. Truck #1, Truck #2, etc.)
        departure_time : datetime.time, optional
            The time the truck departs from the warehouse, by default 8:00 AM.
        miles_traveled : float, optional
            The number of miles the truck has traveled, by default 0.0.
        speed_mi_hr : float, optional
            The speed of the truck in miles per hour, by default 18.0.
        capacity : int, optional
            The maximum number of packages the truck can carry, by default 16.
        """
        self.current_address = current_address
        self.label = label
        self.miles_traveled = miles_traveled
        self.speed_mi_hr = speed_mi_hr
        self.capacity = capacity
        self.departure_time = departure_time
        self.travel_delta = timedelta(0)
        self.route_list = [current_address]
        self.inventory = []


def distance_between(address1: Vertex, address2: Vertex, city_map: Graph):
    """
    Calculates the distance between two Vertex objects in a Graph.

    Parameters
    ----------
    address1 : Vertex
        The starting address.
    address2 : Vertex
        The destination address.
    city_map : Graph
        The graph containing the addresses and distances between them.

    Returns
    -------
    float
        The distance between the two addresses.

    Raises
    ------
    KeyError
        If the edge between the two addresses is not found in the graph.
    """
    try:
        distance = city_map.edge_weights[(address1, address2)]
        return distance
    except KeyError:
        print('Edge not found in Graph between: ' + address1.label + ', AND: ' + address2.label)


def min_distance_address_from(from_address: Vertex, city_map: Graph, truck_packages: list):
    """
    Finds the address in a list of packages that is closest to a given address.

    Parameters
    ----------
    from_address : Vertex
        The address to find the closest package destination to.
    city_map : Graph
        The graph containing the addresses and distances between them.
    truck_packages : list
        The list of packages to search through.

    Returns
    -------
    Vertex
        The address of the package destination that is closest to the given address.
    """
    closest_address = from_address
    closest_distance = float('inf')
    for item in truck_packages:
        if distance_between(from_address, item.destination, city_map) < closest_distance:
            closest_address = item.destination
            closest_distance = distance_between(from_address, item.destination, city_map)

    return closest_address
