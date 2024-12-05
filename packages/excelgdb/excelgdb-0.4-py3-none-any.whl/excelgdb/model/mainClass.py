import arcpy
import os

# Define the BaseLayer class, which provides basic layer setup functionality in a geodatabase
class BaseLayer:
    
    # Class variable to track if the geodatabase (GDB) check has been performed
    gdb_checked = False
        
    # Constructor for the BaseLayer class
    def __init__(self, gdb_path, layer_name, geometry_type, spatial_reference=4326):
        # Initialize instance variables with geodatabase path, layer name, geometry type, and spatial reference
        self.gdb_path = gdb_path
        self.layer_name = layer_name
        self.geometry_type = geometry_type
        self.spatial_reference = arcpy.SpatialReference(spatial_reference)
        
        # Only check and create the geodatabase once for all instances of this class
        if not BaseLayer.gdb_checked:
            self.create_gdb_if_not_exists()  # Check if GDB exists, create if not
            BaseLayer.gdb_checked = True     # Set flag to avoid redundant checks
        
        # Define the path to the layer within the geodatabase
        self.layer_path = f"{self.gdb_path}\\{self.layer_name}"
        
        # Create the specified layer in the geodatabase
        self.create_layer()
    
    # Method to create the geodatabase if it does not already exist
    def create_gdb_if_not_exists(self):
        # Check if the geodatabase path exists
        if not arcpy.Exists(self.gdb_path):
            # Get the directory and geodatabase name
            gdb_directory = os.path.dirname(self.gdb_path)
            gdb_name = os.path.basename(self.gdb_path)
            # Create the geodatabase using arcpy
            arcpy.management.CreateFileGDB(gdb_directory, gdb_name)
            print(f"Geodatabase '{gdb_name}' created in '{gdb_directory}'")
        else:
            print("Geodatabase already exists.")
    
    # Method to create the layer in the geodatabase if it does not already exist
    def create_layer(self):
        # Check if the layer path exists within the geodatabase
        if not arcpy.Exists(self.layer_path):
            # Create the feature class (layer) with the specified geometry type and spatial reference
            arcpy.management.CreateFeatureclass(self.gdb_path, self.layer_name, 
                                                self.geometry_type, 
                                                spatial_reference=self.spatial_reference)
            print(f"Layer '{self.layer_name}' created with geometry type '{self.geometry_type}'")
        else:
            print(f"Layer '{self.layer_name}' already exists.")
