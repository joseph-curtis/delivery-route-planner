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

import sys


# Date: 28 Mar 2023

def main_menu(packages_hash_table, truck_list):
    print("\n*** Welcome to WGUPS Package Delivery Route Planner ***")

    user_quits = False
    while not user_quits:
        print('*' * 80)
        print("\nPlease select option from below:")
        print(" [1] Show All Packages and Total Mileage at End of Day")
        print(" [2] Get a Package Status from Time")
        print(" [3] Show All Packages Status from Time")
        print(" [4] Exit Program")
        print('*' * 80)
        option = input("Chose an option [1],[2],[3], or [4] : ")
        if option == "1":
            print('=' * 80)
            print('=' + "ALL PACKAGES AT END OF DAY".center(78) + '=')
            print('=' * 80)
            print("Package ID | Address | City | State | Zip | Deadline | Mass | Status")
            for key_value_tuple in packages_hash_table:
                key, pkg = key_value_tuple
                print(str(pkg.package_id).rjust(10) + ' | ' + pkg.destination.address.ljust(22) + ' | '
                      + pkg.city.ljust(16) + ' | ' + pkg.state + ' | ' + pkg.destination.zipcode + ' | '
                      + pkg.deadline_str.ljust(8) + ' | ' + str(pkg.mass_kg).rjust(4) + ' | '
                      + "Delivered: " + str(pkg.delivery_time))

        elif option == "2":
            pass
        elif option == "3":
            pass
        elif option == "4":
            user_quits = True
            sys.exit("Exiting Application. Have a nice day!")
        else:
            print("Wrong option, please try again!")
