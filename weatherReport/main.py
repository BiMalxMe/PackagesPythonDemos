import requests  # to make http requests to the weather api
import matplotlib.pyplot as plt  # to plot temperature graph
from datetime import datetime  # to convert datetime strings into datetime objects

API_KEY = "2e00f4736d30be74aae64c5815ab919e"  # your openweathermap api key

# step 1: function to fetch weather data from api
def fetch_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"  # api endpoint with city, key, and metric units
    response = requests.get(url)  # send get request to the api
    data = response.json()  # parse the response into json format
    return data  # return the whole json data

# step 2: function to extract useful info from raw json
def parse_forecast(data):
    forecast_list = data['list']  # get the list of forecast entries
    parsed = []  # create an empty list to store cleaned data

    for entry in forecast_list:  # loop through each 3-hour forecast
        dt_txt = entry['dt_txt']  # get datetime as string
        temp = entry['main']['temp']  # get temperature in celsius
        weather = entry['weather'][0]['description']  # get weather condition text like 'clear sky'

        parsed.append({
            'datetime': datetime.strptime(dt_txt, "%Y-%m-%d %H:%M:%S"),  # convert string to datetime object
            'temp': temp,  # store temperature
            'weather': weather  # store weather description
        })

    return parsed  # return the cleaned list

# step 3: function to plot the temperature forecast
def plot_forecast(forecast):
    times = [f['datetime'] for f in forecast]  # extract datetime values
    temps = [f['temp'] for f in forecast]  # extract temperature values

    plt.figure(figsize=(10, 5))  # create a 10x5 inch figure
    plt.plot(times, temps, marker='o', linestyle='-', color='tab:blue')  # plot line graph with circles on data points
    plt.title("5-Day Temperature Forecast")  # set chart title
    plt.xlabel("Date & Time")  # set x-axis label
    plt.ylabel("Temperature (°C)")  # set y-axis label
    plt.grid(True)  # enable background grid
    plt.xticks(rotation=45)  # rotate x-axis labels for better visibility
    plt.tight_layout()  # automatically adjust layout to fit labels
    plt.show()  # display the plot

# step 4: main execution block
if __name__ == "__main__":
    city = input("Enter city name: ")  # ask user for city input
    data = fetch_weather(city, API_KEY)  # fetch weather data for the city

    if data.get("cod") != "200":  # check if the api returned an error
        print("Error:", data.get("message", "Failed to fetch weather"))  # print the error message
    else:
        forecast = parse_forecast(data)  # clean and structure the forecast data
        plot_forecast(forecast)  # show the temperature chart
