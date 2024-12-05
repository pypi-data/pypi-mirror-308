import arcpy
from excelgdb.model.mainClass import BaseLayer

# Define the PointLayer class, inheriting from BaseLayer
class PointLayer(BaseLayer):
    
    # Constructor for PointLayer; it calls the BaseLayer constructor with "POINT" geometry type
    def __init__(self, gdb_path, layer_name):
        super().__init__(gdb_path, layer_name, "POINT")
        
    # Method to add a point feature to the layer
    def add_point(self, x, y):
        # Open an InsertCursor to add a new point feature with XY coordinates
        with arcpy.da.InsertCursor(self.layer_path, ["SHAPE@XY"]) as cursor:
            # Insert a new point with the specified x and y coordinates
            cursor.insertRow([(x, y)])