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

# Date: 6 Apr 2023
from datetime import datetime
from utilities import ChainingHashTable


class Vertex:
    def __init__(self, label: str, address: str, zipcode: str = ''):
        """
        All vertex objects start with a distance of positive infinity.

        Parameters
        ----------
        label : str
            name of the vertex
        address : str
            USPS formatted address
        zipcode : str
            address zipcode
        """
        self.label = label
        self.address = address
        self.zipcode = zipcode
        self.distance = float('inf')
        self.prev_vertex = None

    def __eq__(self, other):
        return isinstance(other, Vertex) \
            and self.address == other.address \
            and self.zipcode == other.zipcode

    def __hash__(self):
        return hash(self.label + self.address + self.zipcode)

    def __repr__(self):
        return f'Vertex("{self.label}", "{self.address}", "{self.zipcode}")'

    def __str__(self):
        return f'({self.label}: {self.address}; {self.zipcode})'


class Graph:
    def __init__(self, adjacency_list=None, edge_weights=None):
        if adjacency_list is None:
            self.adjacency_list = {}  # vertex dictionary {key:value}
        if edge_weights is None:
            self.edge_weights = {}  # edge dictionary {key:value}

    # when referencing this object, use adjacency_list and edge_weights
    def __repr__(self):
        return f'Graph("{self.adjacency_list}", "{self.edge_weights}")'

    # String representation of the Graph's vertices
    def __str__(self):
        return "\n".join(str(item) for item in self.adjacency_list)
        # .join(str(item) for item in self.edge_weights)

    def add_vertex(self, new_vertex: Vertex):
        self.adjacency_list[new_vertex] = []  # {vertex_1: [], vertex_2: [], ...}

    def add_directed_edge(self, from_vertex: Vertex, to_vertex: Vertex,
                          weight=1.0):
        self.edge_weights[(from_vertex, to_vertex)] = weight
        # {(vertex_1,vertex_2): 484, (vertex_1,vertex_3): 626, (vertex_2,vertex_6): 1306, ...}
        self.adjacency_list[from_vertex].append(to_vertex)
        # {vertex_1: [vertex_2, vertex_3], vertex_2: [vertex_6], ...}

    def add_undirected_edge(self, vertex_a: Vertex, vertex_b: Vertex,
                            weight=1.0):
        self.add_directed_edge(vertex_a, vertex_b, weight)
        self.add_directed_edge(vertex_b, vertex_a, weight)


class PackageWGUPS:
    def __init__(self, package_id: int, mass_lb: float, notes: str,
                 destination: Vertex = None,
                 deadline=datetime.strptime('23:59:59.999999', '%H:%M:%S.%f').time()):
        self.package_id = package_id
        self.mass_lb = mass_lb
        self.notes = notes
        self.destination = destination
        self.deadline = deadline
        self.delivered_to = None

    def __repr__(self):
        return f'PackageWGUPS("{self.package_id}", "{self.mass_lb}",' \
               f' "{self.notes}", "{self.destination}", "{self.deadline}")'

    def __str__(self):
        return f'Package(ID# "{self.package_id}": "{self.notes}"; TO: "{self.destination}", BY: "{self.deadline}")'

    def __eq__(self, other):
        return isinstance(other, PackageWGUPS) \
            and self.package_id == other.package_id

    def __hash__(self):
        return hash(self.package_id)


class DeliveryTruck:
    def __init__(self, current_address: Vertex = None, status='parked at WGU hub', mileage: float = 0.0):
        self.current_address = current_address
        self.status = status
        self.mileage = mileage
        self.inventory = ChainingHashTable()
        self.route = Graph()

