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

# Title: Daily Local Delivery Route Planner Application
# Description: Determines an efficient route and delivery distribution
#              for Daily Local Deliveries (DLD)
# Date:    10 Apr 2023
# Sources: w3schools.com/python, docs.python.org, geeksforgeeks.org,
#          stackoverflow.com, sololearn.com,
#          Lysecky, R., & Vahid, F. (2018, June).
#          C950: Data Structures and Algorithms II. zyBooks.
#           [https://learn.zybooks.com/zybook/WGUC950AY20182019]
import csv
from argparse import ArgumentParser
from datetime import datetime

import controller
import model
from utilities import ChainingHashTable

parser = ArgumentParser(description='Process Daily Local Deliveries.')
parser.add_argument('--table', '-t', required=False, default='data/distance-table.csv',
                    help='The file used for the distance table that describes the distances to each node')
parser.add_argument('--packages', '-p', required=False, default='data/package-file.csv',
                    help='The file that includes all packages that will be delivered in the same day.')
args = parser.parse_args()


def main():
    """The entry point for the Daily Local Delivery Route Planner Application"""

    # Load vertices into list:
    salt_lake_city_graph, vertex_list = load_distance_data()

    # Load the HUB with all packages for the day
    all_packages_hash_table = load_package_data(vertex_list)

    # Load each truck with packages, and determine route:
    truck1 = model.DeliveryTruck(vertex_list[0])
    truck1 = controller.truck_load_packages(truck1, salt_lake_city_graph, all_packages_hash_table)

    # Hand off control to the view; show main menu
    # view.main_menu()
    # for item in vertex_list:
    #    print(item)

    for package in all_packages_hash_table:
        print(str(package))
    print(salt_lake_city_graph)
    debug = "place debug marker here to look at data structs in debugger"


def load_distance_data():
    """
    Loads distance data into a graph
    Returns
    -------
    salt_lake_city_graph : model.Graph()
        Graph of all possible destination vertexes with distance data
    vertex_list : list
        An array of all possible destinations for packages
    """
    salt_lake_city_graph = model.Graph()
    vertex_list = list()

    with open(args.table, 'r') as distance_file:
        d_table = csv.reader(distance_file, delimiter=',')
        next(d_table, None)  # skip the first row (column labels) in the table

        row_index = 0
        for row in d_table:
            label = row[0]
            # full address is in row[1]
            start_zip = row[1].index('\n')
            end_zip = row[1].index(')')

            address = row[1][:start_zip]
            zipcode = row[1][start_zip + 2:end_zip]

            new_vertex = model.Vertex(label, address, zipcode)
            vertex_list.append(new_vertex)
            salt_lake_city_graph.add_vertex(new_vertex)

            if row_index == 0:
                dist_array = [[] for _ in range(len(row) - 2)]

            col_index = 0
            for value in row[2:]:
                if value == '':
                    dist_array[row_index].append(None)
                else:
                    dist_array[row_index].append(float(value))
                col_index += 1

            row_index += 1

    # Create graph using vertices from list, and distances from 2-dim array:
    assert len(vertex_list) == len(dist_array)

    for i in range(len(dist_array)):
        for j in range(len(dist_array[i])):
            if j > i:
                dist_array[i][j] = dist_array[j][i]

            salt_lake_city_graph.add_directed_edge(vertex_list[i], vertex_list[j], dist_array[i][j])

    return salt_lake_city_graph, vertex_list


def load_package_data(vertex_list):
    """
    Load packages into a Hash Table
    Parameters
    ----------
    vertex_list :
        List of all vertexes in the main salt_lake_city_graph

    Returns
    -------
    warehouse_package_inventory :
        Hash table of all packages at the beginning of delivery day

    """
    warehouse_package_inventory = ChainingHashTable()
    with open(args.packages, 'r') as package_file:
        pak_table = csv.reader(package_file, delimiter=',')
        next(pak_table, None)  # skip the first row (column labels) in the table
        for row in pak_table:
            package_id = int(row[0])

            address_lbl = model.Vertex('unknown', row[1], row[4])
            destination = address_lbl
            for node in vertex_list:
                if node == address_lbl:
                    destination = node

            if row[5] == 'EOD':
                deadline = datetime.strptime('23:59:59.999999', '%H:%M:%S.%f').time()
            else:
                deadline = datetime.strptime(row[5], '%I:%M %p').time()
            mass_lb = float(row[6])
            note = row[7]

            package = model.PackageWGUPS(package_id, mass_lb, note, destination, deadline)
            warehouse_package_inventory.insert(package_id, package)

    return warehouse_package_inventory


if __name__ == '__main__':
    main()
