import json
import psycopg2

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="IoTDataLake",
    user="postgres",
    password=""
)

# Open the JSON file and load the data
with open("wind_turbine_asset.json") as f:
    data = json.load(f)

# Extract the asset data from the JSON
asset_data = data["asset"]

# Insert the asset data into the asset_master table
cur = conn.cursor()
cur.execute(
    """
    INSERT INTO rawzone.asset_master (
        asset_id,
        asset_name,
        description,
        manufacturer,
        model,
        serial_number,
        location_latitude,
        location_longitude,
        rated_power_unit,
        rated_power_value,
        hub_height_unit,
        hub_height_value
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """,
    (
        asset_data["id"],
        asset_data["name"],
        asset_data["description"],
        asset_data["manufacturer"],
        asset_data["model"],
        asset_data["serial_number"],
        asset_data["location"]["latitude"],
        asset_data["location"]["longitude"],
        asset_data["properties"]["rated_power"]["unit"],
        asset_data["properties"]["rated_power"]["value"],
        asset_data["properties"]["hub_height"]["unit"],
        asset_data["properties"]["hub_height"]["value"]
    )
)
conn.commit()

# Close the database connection
conn.close()