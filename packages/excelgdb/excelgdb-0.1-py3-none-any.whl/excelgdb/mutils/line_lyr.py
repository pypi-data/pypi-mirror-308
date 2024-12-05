import arcpy
from excelgdb.model.mainClass import BaseLayer

class LineLayer(BaseLayer):
    def __init__(self, gdb_path, layer_name, sort_field):
        super().__init__(gdb_path, layer_name, "POLYLINE")
        self.sort_field = sort_field
        
        # Check if 'ORIG_FID' exists in the layer, if not, add it
        field_names = [f.name for f in arcpy.ListFields(self.layer_path)]
        if self.sort_field not in field_names:
            arcpy.management.AddField(self.layer_path, self.sort_field, "LONG")

    def add_line_xls(self, coordinates_grouped):
        # Open an InsertCursor to add lines directly to the output layer
        with arcpy.da.InsertCursor(self.layer_path, ["SHAPE@", self.sort_field]) as cursor:
            for sort_id, coordinates in coordinates_grouped.items():
                # Create an Array of points for each line
                array = arcpy.Array([arcpy.Point(x, y) for x, y in coordinates])
                
                # Create a Polyline object from the points array
                polyline = arcpy.Polyline(array, self.spatial_reference)
                
                # Insert the polyline directly into the output layer
                cursor.insertRow([polyline, sort_id])
    def delete_null_records(self):
        # Use UpdateCursor to delete rows where the sort_field is null
        with arcpy.da.UpdateCursor(self.layer_path, [self.sort_field]) as cursor:
            for row in cursor:
                if row[0] is None:  # Check if sort_field is null
                    cursor.deleteRow()  # Delete the row
                    
    def add_line_handy(self, coordinates):
        with arcpy.da.InsertCursor(self.layer_path, ["SHAPE@"]) as cursor:
            array = arcpy.Array([arcpy.Point(x, y) for x, y in coordinates])
            polyline = arcpy.Polyline(array, self.spatial_reference)
            cursor.insertRow([polyline])                    