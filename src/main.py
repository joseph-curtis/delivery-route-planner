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
# Date: 19 Mar 2023
# Sources: w3schools.com/python, docs.python.org, geeksforgeeks.org,
#          stackoverflow.com, sololearn.com,
#          Lysecky, R., & Vahid, F. (2018, June).
#          C950: Data Structures and Algorithms II. zyBooks.
#           [https://learn.zybooks.com/zybook/WGUC950AY20182019]
import csv
from argparse import ArgumentParser
from datetime import datetime
from itertools import islice
import model
import view
from utilities import HashTableChained

parser = ArgumentParser(description='Process Daily Local Deliveries.')
parser.add_argument('--table', '-t', required=False, default='data/distance-table.csv',
                    help='The file used for the distance table that describes the distances to each node')
parser.add_argument('--packages', '-p', required=False, default='data/package-file.csv',
                    help='The file that includes all packages that will be delivered in the same day.')
args = parser.parse_args()


def main():
    """The entry point for the Daily Local Delivery Route Planner Application"""

    # Load vertices into list:
    vertex_list = []
    with open(args.table, 'r') as distance_file:
        d_table = csv.reader(distance_file, delimiter=',')
        next(d_table, None)  # skip the first row (column labels) in the table
        for row in d_table:
            label = row[0]
            # full address is in row[1]
            start_zip = row[1].index('\n')
            end_zip = row[1].index(')')

            address = row[1][:start_zip]
            zipcode = row[1][start_zip + 2:end_zip]

            vertex_list.append(model.Vertex(label, address, zipcode))

        # Create graph using vertices from list:
        route_graph = model.Graph()
        for vertex in vertex_list:
            route_graph.add_vertex(vertex)

    # Load packages into a Hash Table:
    all_packages = HashTableChained()
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
            all_packages.insert(package_id, package)

    # Hand off control to the view; show main menu
    # view.main_menu()
    for item in vertex_list:
        print(item)

    print(route_graph)


if __name__ == '__main__':
    main()
