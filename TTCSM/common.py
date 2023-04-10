import os
import arcpy


def get_distinct_values_from_field(featureClass, field):
    valuesList = []
    values = [row[0] for row in arcpy.da.SearchCursor(featureClass, field)]
    for val in values:
        if val not in values:
            valuesList.append(val)
    return valuesList


def add_fields_to_feature(feature, fields):
    for field in fields:
        arcpy.AddField_management(feature, field[0], field[1], "", "", "", "", "", "", "")


def get_ID_field_from_feature(feature, ID_Fields=('OBJECTID', 'FID')):
    """
    Returns the name of the first ID field encountered in the feature class
    """
    fields = arcpy.ListFields(feature)
    for field in fields:
        if str(field.name) in ID_Fields:
            return str(field.name)
        else:
            return None


def create_Geodatabase(gdb):
    if not os.path.exists(gdb):
        baseWorkGdb = os.path.basename(gdb)
        workspace = os.path.dirname(gdb)
        arcpy.CreateFileGDB_management(workspace, baseWorkGdb, "CURRENT")


def create_directory(directoryName):
    if not os.path.exists(directoryName):
        os.makedirs(directoryName)


def check_if_file_exists(featureName):
    """
    Will check if file or feature class exists
    Returns
        True if exists
        False if not
    """

    if os.path.exists(featureName):
        return True
    else:
        check = featureName
        gdbTest = ".gdb"
        if gdbTest in check:
            name = os.path.basename(featureName)
            gdbPath = featureName.replace("\\" + name, "")
            arcpy.geoprocessing.env.workspace = gdbPath
            fcList = arcpy.ListFeatureClasses()
            if name in fcList:
                return True
            else:
                return False
        else:
            return False


def quit(message='TERMINATING PROGRAM'):
    """
    A basic exit with some indication of what validation failed
    """
    import sys
    print(message)
    sys.exit()
