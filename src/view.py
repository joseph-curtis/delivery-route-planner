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


# Date: 25 Apr 2023

def main_menu(packages_hash_table: ChainingHashTable, truck_list):
    def get_user_time(user_input):
        time_obj = datetime.datetime.strptime(user_input, '%H%M').time()
        return time_obj

    print("\n***   Welcome to WGUPS Package Delivery Route Planner   ***")

    user_quits = False
    while not user_quits:
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
                print(str(pkg.package_id).rjust(2) + ' | ' + pkg.destination.address[:30].ljust(30) + ' | '
                      + pkg.city.ljust(16) + ' | ' + pkg.state.center(5) + ' | ' + pkg.destination.zipcode + ' | '
                      + pkg.deadline_str.center(8) + ' | ' + str(pkg.mass_kg).rjust(4) + ' | '
                      + pkg.status_delivered)
            print("ID | " + "Address".center(30) + " | " + "City".center(16) + " | State | " + "Zip".center(5)
                  + " | Deadline | Mass | " + "Status".center(19))
            print('_' * 110)
            total_miles = 0.0
            for truck in truck_list:
                total_miles += truck.miles_traveled
            print("\nTotal distance traveled is " + "{:.1f}".format(total_miles) + " miles.")

        elif option == "2":
            user_time = None
            quit_menu = False
            valid_time_obj = False
            while not valid_time_obj and not quit_menu:
                try:
                    user_text = input("Enter time in HHMM format (example: 1325 for 1:25pm) : ")
                    if user_text == 'x' or user_text == 'X':
                        quit_menu = True
                        continue
                    user_time = get_user_time(user_text)
                    if user_time < datetime.datetime.strptime('08:00', '%H:%M').time():
                        print("Please enter a time after 8:00 AM (0800)")
                    else:
                        valid_time_obj = True
                except ValueError:
                    print("incorrect time format entered. Try again or enter 'x' to exit.")
            valid_package_id = False
            while not quit_menu and not valid_package_id:
                try:
                    user_text = input("Enter package ID (integer) : ")
                    if user_text == 'x' or user_text == 'X':
                        quit_menu = True
                        continue
                    package_id = int(user_text)
                    if package_id < 1 or package_id > len(packages_hash_table):
                        print("Invalid package ID! Must be between 1 and " + str(len(packages_hash_table)))
                    else:
                        valid_package_id = True
                except ValueError:
                    print("incorrect format. Try again or enter 'x' to exit.")

            pkg = packages_hash_table.get(package_id)
            if user_time < pkg.time_arrived:
                status = pkg.status_arrival
            elif user_time < pkg.time_loaded:
                status = "waiting at HUB"
            elif user_time < pkg.time_delivered:
                status = pkg.status_loaded
            else:
                status = pkg.status_delivered

            print('-' * 110)
            print('|' + ("PACKAGE ID: " + str(pkg.package_id) + " BOUND FOR: " + pkg.destination.label
                         + " @ " + str(user_time)).center(108) + '|')
            print('-' * 110)
            print("Package ID | " + "Address".center(len(pkg.destination.address)) + " | " + "City".center(len(pkg.city))
                  + " | State | " + "Zip".center(5) + " | Deadline | Mass | " + "Status".center(len(status)))
            print(str(pkg.package_id).rjust(10)
                  + ' | ' + pkg.destination.address.ljust(len(pkg.destination.address))
                  + ' | ' + pkg.city.rjust(len(pkg.city))
                  + ' | ' + pkg.state.center(5)
                  + ' | ' + pkg.destination.zipcode
                  + ' | ' + pkg.deadline_str.center(8)
                  + ' | ' + str(pkg.mass_kg).rjust(4)
                  + ' | ' + status)

        elif option == "3":
            pass
        elif option == "4":
            user_quits = True
            sys.exit("Exiting Application. Have a nice day!")
        else:
            print("\nWrong option, please try again!")
