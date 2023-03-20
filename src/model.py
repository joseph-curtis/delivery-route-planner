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

# Date: 17 Mar 2023
import datetime


class PackageWGUPS:
    def __int__(self, package_id: int, destination: str, current_address: str,
                deadline: datetime.time, weight_kg: int, notes: str):
        self.package_id = package_id
        self.destination = destination
        self.current_address = current_address
        self.deadline = deadline
        self.weight_kg = weight_kg
        self.notes = notes
        self.delivered = False

    def __eq__(self, other):
        if isinstance(other, PackageWGUPS):
            return self.package_id == other.package_id


class Vehicle:
    def __int__(self, current_address: str = 'HUB', status: str = 'At WGU HUB.'):
        self.inventory = []
        self.current_address = current_address


class Vertex:
    def __init__(self, label: str):
        """
        All vertex objects start with a distance of positive infinity.

        Parameters
        ----------
        label : str
            name of the vertex
        """
        self.label = label
        self.distance = float('inf')
        self.prev_vertex = None


class Graph:
    def __init__(self):
        self.adjacency_list = {}  # vertex dictionary {key:value}
        self.edge_weights = {}  # edge dictionary {key:value}

    def add_vertex(self, new_vertex):
        self.adjacency_list[new_vertex] = []  # {vertex_1: [], vertex_2: [], ...}

    def add_directed_edge(self, from_vertex, to_vertex, weight=1.0):
        self.edge_weights[(from_vertex, to_vertex)] = weight
        # {(vertex_1,vertex_2): 484, (vertex_1,vertex_3): 626, (vertex_2,vertex_6): 1306, ...}
        self.adjacency_list[from_vertex].append(to_vertex)
        # {vertex_1: [vertex_2, vertex_3], vertex_2: [vertex_6], ...}

    def add_undirected_edge(self, vertex_a, vertex_b, weight=1.0):
        self.add_directed_edge(vertex_a, vertex_b, weight)
        self.add_directed_edge(vertex_b, vertex_a, weight)

