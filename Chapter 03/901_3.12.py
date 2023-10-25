# Define specific latitude and longitude values in a tuple
location_lat_long = (51.507351, -0.127758)
# Here is how we can access individual values in the tuple
latitude = location_lat_long[0]
longitude = location_lat_long[1]
print("Latitude:", latitude)
print("Longitude:", longitude)
# We can concatenate two tuples
location_lat_long2 = (51.879650, -0.417560)
location_lat_long3 = location_lat_long + location_lat_long2
print("Merged locations:", location_lat_long3)
# We can expand tuple using multiplications with an integer
multiplied_location = location_lat_long * 3
print("Multiplied location:", multiplied_location)
# We can Unpack a tuple into multiple separate variables
lat_val, lon_val = location_lat_long
print("Unpacked latitude value:", lat_val)
print("Unpacked longitude value:", lon_val)
# Finding the length of a tuple is easy with len function
print("Length of merged location is:", len(location_lat_long))
# Try to change a value in the tuple. Since it is immutable, this will throw error Attempting to change a value in the tuple will raise an error
location[0] = 42.3601
