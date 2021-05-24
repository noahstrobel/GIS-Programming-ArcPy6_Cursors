# Name: Noah Strobel

# Class: GISc-450

# Created: 4/23/2021

# This script deletes records from a table and creates a new GDB entitled
# "Strobel_Noah_ownership" and prints hydrant owners.
# It then promps users to input the feature class (fc) name and gives them
# 3 chances to enter the correct fc before it terminates.
# It then asks users to input a field to delete from the hydrants table (AFC)
# and then deletes said field. Finally, it prints the number of records that were
# deleted and the list of remaining hydrant owners.


import arcpy
import time
import os
import collections

arcpy.env.overwriteOutput = True

time_start = time.time()


def main():

    print("\nThis script deletes records from a table and creates a new GDB entitled")
    print("Strobel_Noah_ownership and prints hydrant owners.")
    print("It then promps users to input the feature class (fc) name and gives them")
    print("3 chances to enter the correct fc before it terminates.")
    print("It then asks users to input a field to delete from the hydrants table (AFC)")
    print("and then deletes said field. Finally, it prints the number of records that were")
    print("deleted and the list of remaining hydrant owners.")

    # Setting the workspace and new GDB name

    new_gdb = "Strobel_Noah_owners.gdb"
    workspace = arcpy.env.workspace = r"C:\GISc450\ArcPy6_Cursors\Data"

    fc_in = r"C:\GISc450\ArcPy6_Cursors\Corvallis.gdb\Hydrant"

    fc_new_location = r"C:\GISc450\ArcPy6_Cursors\Data\Hydrant"

    in_field = "OWNERSHIP"

    new_gdb_path = os.path.join(workspace, new_gdb)

    # If the new GDB already exists, it will be deleted

    if os.path.exists(new_gdb_path):
        arcpy.Delete_management(new_gdb_path)
    arcpy.CreateFileGDB_management(workspace, new_gdb)

    print(f"\n{new_gdb} created")

    # Creating the new hydrant feature class in our new GDB

    hydrant_fc = arcpy.FeatureClassToFeatureClass_conversion(fc_in, new_gdb_path, "Hydrant")

    # Creating the new "owners" table

    in_table = r"C:\GISc450\ArcPy6_Cursors\Corvallis.gdb\Strobel_Noah_Hydrant"
    out_table_name = "owners"
    arcpy.TableToTable_conversion(in_table, new_gdb_path, out_table_name)

    # Asking users to enter the feature class name

    # fc_input = input("\nEnter the feature class to be found: ")
    #
    # exists = arcpy.Exists(fc_input)
    # count = 0
    #
    # while not exists:
    #     fc_input = input("\nInput not recognized. Try again: ")
    #     count += 1
    #     if count == 2:
    #         print("\nSorry, the feature class could not be located")
    #         return
    #
    # if fc_input == fc_new_location:
    #     print("Feature class located")

    # Creating the cursor that will append rows into our feature class table

    field_values = []
    with arcpy.da.SearchCursor(hydrant_fc, in_field) as cursor:
        for row in cursor:
            field_values.append(row[0])

    # Counting the number of owners for hydrants

    collection_count = collections.Counter(field_values)
    most_common_val = collection_count.most_common()
    print("\nOwner list:")
    for row in most_common_val:
        print(row[0])

    # Asking the user to enter an owner to remove from the table

    # value_remove = input("Choose an owner to remove: ")

    value_remove = "AFC"
    remove_count = 0

    # Counting the owners that were deleted
    # Deleting rows with a cursor

    with arcpy.da.UpdateCursor(hydrant_fc, in_field) as cursor:
        for row in cursor:
            if row[0] == value_remove:
                cursor.deleteRow()
                remove_count += 1
    print(f"\n{remove_count} records entitled '{value_remove}' deleted from the ownership table")

    field_values_2 = []
    with arcpy.da.SearchCursor(hydrant_fc, in_field) as cursor:
        for row in cursor:
            field_values_2.append(row[0])

    # Counting remaining owners after deletion

    collection_count_2 = collections.Counter(field_values_2)
    most_common_val_2 = collection_count_2.most_common()
    print("\nRemaining owners:")
    for row in most_common_val_2:
        print(row[0])


if __name__ == '__main__':
    main()

time_end = time.time()
total_time = time_end - time_start
minutes = int(total_time / 60)
seconds = total_time % 60
print(f"\n---The script finished in {minutes} minutes {int(seconds)} seconds---")
