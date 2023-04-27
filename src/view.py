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
import datetime

from utilities import ChainingHashTable


# Date: 26 Apr 2023

class ExitMenu(Exception):
    pass


def input_valid_time_obj():
    while True:
        try:
            user_input = input("Enter time in HHMM format, example: 1325 for 1:25pm ('x' to exit) : ")
            if 'x' in user_input or 'X' in user_input:
                raise ExitMenu("User request to exit submenu.")
            time_obj = datetime.datetime.strptime(user_input.strip(), '%H%M').time()
            if time_obj < datetime.datetime.strptime('08:00', '%H:%M').time():
                print("Time must be after 8:00 AM (0800) Try again or enter 'x' to exit.")
            else:
                return time_obj
        except ValueError:
            print("incorrect time format entered. Try again or enter 'x' to exit.")


def input_valid_package_id(packages_hash_table: ChainingHashTable):
    while True:
        try:
            user_input = input("Enter package ID (a positive integer) or 'x' to exit : ")
            if 'x' in user_input or 'X' in user_input:
                raise ExitMenu("User request to exit submenu.")
            package_id = int(user_input.strip())
            if package_id < 1 or package_id > len(packages_hash_table):
                print("Invalid package ID! Must be between 1 and " + str(len(packages_hash_table)))
            else:
                return package_id
        except ValueError:
            print("incorrect format. Try again or enter 'x' to exit.")


def main_menu(packages_hash_table: ChainingHashTable, truck_list):
    print("\n***   Welcome to WGUPS Package Delivery Route Planner   ***")

    while True:
        print("\nPlease select option from below:")
        print("  [1] Show All Packages and Total Mileage at End of Day")
        print("  [2] Get a Package Status from Time")
        print("  [3] Show All Packages Status from Time")
        print("  [4] Exit Program")
        option = input("Chose an option [1],[2],[3], or [4] : ")
        if option == "1":
            print('-' * 110)
            print('|' + "ALL PACKAGES AT END OF DAY".center(108) + '|')
            print('-' * 110)
            print("ID | " + "Address".center(30) + " | " + "City".center(16) + " | State | " + "Zip".center(5)
                  + " | Deadline | Mass | " + "Status".center(19))
            for key_value_tuple in packages_hash_table:
                key, pkg = key_value_tuple
                print(str(pkg.package_id).rjust(2)
                      + ' | ' + pkg.destination.address[:30].ljust(30)
                      + ' | ' + pkg.city.ljust(16)
                      + ' | ' + pkg.state.center(5)
                      + ' | ' + pkg.destination.zipcode
                      + ' | ' + pkg.deadline_str.center(8)
                      + ' | ' + str(pkg.mass_kg).rjust(4)
                      + ' | ' + pkg.status_delivered)
            print("ID | " + "Address".center(30) + " | " + "City".center(16) + " | State | " + "Zip".center(5)
                  + " | Deadline | Mass | " + "Status".center(19))
            print('_' * 110)
            total_miles = 0.0
            for truck in truck_list:
                total_miles += truck.miles_traveled
            print("\nTotal distance traveled is " + "{:.1f}".format(total_miles) + " miles.")

        elif option == "2":
            try:
                chosen_time = input_valid_time_obj()
                package_id = input_valid_package_id(packages_hash_table)
            except ExitMenu:
                continue
            pkg = packages_hash_table.get(package_id)

            if chosen_time < pkg.time_arrived:
                status = pkg.status_arrival
            elif chosen_time < pkg.time_loaded:
                status = "waiting at HUB"
            elif chosen_time < pkg.time_delivered:
                status = pkg.status_loaded
            else:
                status = pkg.status_delivered

            print('-' * 110)
            print('|' + ("PACKAGE: " + str(pkg.package_id) + "  BOUND FOR: " + pkg.destination.label
                         + "  STATUS AT: " + str(chosen_time)).center(108) + '|')
            print('-' * 110)
            print(
                "ID | " + "Address".center(len(pkg.destination.address)) + " | " + "City".center(len(pkg.city))
                + " | State | " + "Zip".center(5) + " | Deadline | Mass | " + "Status".center(len(status)))
            print(str(pkg.package_id).rjust(2)
                  + ' | ' + pkg.destination.address.ljust(len(pkg.destination.address))
                  + ' | ' + pkg.city.rjust(len(pkg.city))
                  + ' | ' + pkg.state.center(5)
                  + ' | ' + pkg.destination.zipcode
                  + ' | ' + pkg.deadline_str.center(8)
                  + ' | ' + str(pkg.mass_kg).rjust(4)
                  + ' | ' + status)

        elif option == "3":
            try:
                chosen_time = input_valid_time_obj()
            except ExitMenu:
                continue

            print('-' * 110)
            print('|' + ("ALL PACKAGES STATUS AT: " + str(chosen_time)).center(108) + '|')
            print('-' * 110)
            print("ID | " + "Address".center(30) + " | " + "City".center(16) + " | State | " + "Zip".center(5)
                  + " | Deadline | Mass | " + "Status".center(19))
            for key_value_tuple in packages_hash_table:
                key, pkg = key_value_tuple
                if chosen_time < pkg.time_arrived:
                    status = pkg.status_arrival
                elif chosen_time < pkg.time_loaded:
                    status = "waiting at HUB"
                elif chosen_time < pkg.time_delivered:
                    status = pkg.status_loaded
                else:
                    status = pkg.status_delivered

                print(str(pkg.package_id).rjust(2)
                      + ' | ' + pkg.destination.address[:30].ljust(30)
                      + ' | ' + pkg.city.ljust(16)
                      + ' | ' + pkg.state.center(5)
                      + ' | ' + pkg.destination.zipcode
                      + ' | ' + pkg.deadline_str.center(8)
                      + ' | ' + str(pkg.mass_kg).rjust(4)
                      + ' | ' + status)
            print("ID | " + "Address".center(30) + " | " + "City".center(16) + " | State | " + "Zip".center(5)
                  + " | Deadline | Mass | " + "Status".center(19))
            print('_' * 110)

        elif option == "4":
            sys.exit("Exiting Application. Have a nice day!")
        else:
            print("\nWrong option, please try again!")
