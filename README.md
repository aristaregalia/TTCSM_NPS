# TTCSM_NPS
Travel-time cost surface model (TTCSM) migrated from python 2.x to 3.x with accompanying ArcGIS Pro toolbox. TTCSM outputs are a least cost vector file and a cost surface grid (travel time in minutes). The TTCSM can be used to estimate travel time from defined staring points to defined ending points with custom cost surface input.
User defined cost surface inputs for this model include the following layers: DEM, landcover, roads, trails, streams, lakes, destinations, starting points. 
The travel speed associated with the stacked layers determines the cost surface value (i.e., resistance) and associated least cost path output between given destinations and starting points.
The original reference document and detailed SOP for running the model can be found at https://irma.nps.gov/DataStore/Reference/Profile/2220993. Note, the model version found at this link is only compatible with Python 2.x and ArcMap. For use in ArcGIS Pro/Python 3 download the code from this repository.
### Users Notes ###
- To run the TTCSM outside of ArcGIS Pro, the user needs to use a python environment with the ArcGIS and ArcPy libraries installed. If you have ArcGIS Pro installed locally it may be easiest to create a clone of the ArcGIS Pro environment within your Python distribution (e.g. Anaconda, MiniConda, PyPy etc.). Instructions for cloning an environment within ArcGIS Pro are found at https://pro.arcgis.com/en/pro-app/latest/arcpy/get-started/clone-an-environment.htm 
- When creating layers for use in the TTCSM, the data type of layer fields is important. Make sure the data type for the 'PMTS' field is float or integer. A text data type will default the value of the field to 1 (100% of normal speed/no resistance).
## TTCSM_NPS/TTCSM ##
This folder contains the various Python scripts that create the model.
### TCSM_GUI.py
To run the model outside of the ArcGIS Pro interface, alter the argument paths in this document to point to where ever the testing data is sorted on your local device. The argument key is listed between lines 13-32 in this script file.
## TTCSM_NPS/TestingData ##
This folder contains geospatial data for testing the model in the form of raster layers and shapefiles for the various model inputs. When the model is ran succesfully with the testing data provided in this folder, the cost surface path should look like the red line in the image below:  <br /> <br> <img width="330" alt="TTCSM_ran" src="https://github.com/aristaregalia/TTCSM_NPS/assets/123115368/5b178b36-fe7b-4f0e-a880-95c5843ec38d"> </br>
## TTCSM_NPS/TTCSM_TBOX.py
Python toolbox used for debugging model. 
## TTCSM_NPS/TTCSM_Toolbox.tbx
Toolbox for running the model through the ArcGIS Pro GUI.

## Credits ##
Authors of the original code: Brent Frakes; Thomas Flowe; Kirk R. Sherrill
</br> Authors of 3.x migration: Arista Regalia; Kirk R. Sherrill
