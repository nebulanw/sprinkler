from sprinkler.weather import Weather

weather = Weather(47.6418, -122.0804, "America/Los_Angeles")

resp = weather.query()
print(resp.current_precipitation)
print(resp.total_precipitation)
