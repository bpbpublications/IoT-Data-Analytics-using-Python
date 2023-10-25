import requests
url = "https://developer.nrel.gov/api/wind-toolkit/v2/wind/central-asia-wind-download.json"
params = {
    "wkt": "POINT(55.81054 46.01222)",
    "api_key": "Your_Api_key",
    "attributes": "temperature_100m,temperature_120m,temperature_80m,winddirection_100m,winddirection_120m,winddirection_80m,windspeed_100m,windspeed_120m,windspeed_80m,pressure_200m,pressure_100m,pressure_0m",
    "names": "2015",
    "full_name": "First_Name Second_Name",
    "email": "your_email_id@abc.com",
    "affiliation": "BPB",
    "mailing_list": "false",
    "reason": "learning",
    "leap_day": "true",
    "utc": "false",
    "interval": "15",
    "csv_format": "csv"
}
response = requests.get(url, params=params)
if response.status_code == 200:
    with open("central-asia-wind-data.json", "wb") as f:
        f.write(response.content)
    print("Data downloaded successfully!")
else:
    print("Failed to download data. Error code:", response.status_code)
