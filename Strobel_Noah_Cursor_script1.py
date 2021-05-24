# Name: Noah Strobel

# Class: GISc-450

# Created: 4/23/2021

# Purpose: This script asks users to input a feature class
# and uses a cursor to locate the input field (ownership) and
# places it into a list. It then identifies field name and
# prints what type of field (text or non-text) they are.
# Finally, it creates an in-memory table that contains
# the number of hydrants and their owners and then
# creates a permanent table


import arcpy
import time
import os
import collections

arcpy.env.overwriteOutput = True

time_start = time.time()


def main():

    print("\nThis script asks users to input a feature class")
    print("and uses a cursor to locate the input field (ownership)")
    print("and places it into a list. It then identifies field name")
    print("and prints what type of field (text or non-text) they are.")
    print("Finally, it creates an in-memory table that contains the")
    print("number of hydrants and their owners and then creates a")
    print("permanent table")

    # Setting the gdb_in location

    gdb = r"C:\GISc450\ArcPy6_Cursors\Corvallis.gdb"
    fc_in_location = r"C:\GISc450\ArcPy6_Cursors\Corvallis.gdb\Hydrant"

    # fc_in = input("\nEnter the feature class name: ")
    #
    # exists = arcpy.Exists(fc_in)
    #
    # if not exists:
    #     print(f"\nYour input,'{fc_in},' does not exist")
    #     return

    # Setting the workspace

    workspace = arcpy.env.workspace = gdb

    # Asking the user to input the field name

    # in_field = str(input("Enter the target field name: "))

    in_field = "OWNERSHIP"
    # out_table_input = str(input("Enter the output table: "))
    out_table = "Strobel_Noah_hydrant"
    out_gdb = "Strobel_Noah_owners"
    out_table_path = os.path.join(workspace, out_table)

    # If the out GDB exists already, it will be deleted

    if os.path.exists(out_table_path):
        arcpy.Delete_management(out_table_path)
        arcpy.CreateFileGDB_management(workspace, out_gdb)

    fields = arcpy.ListFields(fc_in_location)

    print("")

    # Printing the field name and field type

    for field in fields:
        field_name = field.name
        field_type = field.type
        if field_type == "String":
            print(f"The field {field_name} is a TEXT field")
        else:
            print(f"The field {field_name} is a NONTEXT field")

    # Creating a cursor to insert the ownership and count columns

    field_values = []
    with arcpy.da.SearchCursor(fc_in_location, in_field) as cursor:
        for row in cursor:
            field_values.append(row[0])

    # Determining the most common field values

    collection_count = collections.Counter(field_values)
    most_common_val = collection_count.most_common()

    # Creating a table in memory

    memory_table = arcpy.CreateTable_management("memory", "memory_table")
    arcpy.AddField_management(memory_table, in_field, "String")
    arcpy.AddField_management(memory_table, "Count", "Integer")

    # Creating the table in our workspace and inserting the count field

    cursor = arcpy.da.InsertCursor(memory_table, [in_field, "Count"])
    for row in most_common_val:
        cursor.insertRow(row)
    del cursor
    arcpy.CopyRows_management(memory_table, out_table_path)


if __name__ == '__main__':
    main()

time_end = time.time()
total_time = time_end - time_start
minutes = int(total_time / 60)
seconds = total_time % 60
print(f"\n---The script finished in {minutes} minutes {int(seconds)} seconds---")

