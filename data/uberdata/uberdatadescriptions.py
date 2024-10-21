uberdata_description = """
    **The dataset contains the following columns:**\n
    1. **VendorID**: A code indicating the TPEP provider.
    2. **tpep_pickup_datetime**: The date and time when the meter was engaged.
    3. **tpep_dropoff_datetime**: The date and time when the meter was disengaged.
    4. **passenger_count**: Number of passengers in the vehicle.
    5. **trip_distance**: Distance traveled in miles.
    6. **pickup_longitude**: Longitude where the trip started.
    7. **pickup_latitude**: Latitude where the trip started.
    8. **dropoff_longitude**: Longitude where the trip ended.
    9. **dropoff_latitude**: Latitude where the trip ended.
    10. **fare_amount**: Fare amount calculated by the meter.
    11. **tip_amount**: Tip amount (for credit card tips).
    12. **total_amount**: Total amount charged to passengers (excluding cash tips).\n
    **The dataset contains 1,000,000 rows and 12 columns.**
    """

dataset_overview_text = """
The histograms above show the distribution of the fare amount, and tip amount, and total earnings in the dataset. The dashed lines represent the 25th, 50th, and 75th percentiles, while the solid red line represents the mean value. As we can see from the histograms, the fare amount, tip amount, and total earnings are right-skewed, with most values concentrated on the lower end of the distribution. This suggests that there are a few rides with very high fare amounts, tip amounts, and total earnings, which could be outliers. What we can infer from this is that earning a high tip seems to be dependent on the fare amount, as the two distributions are similar.

You can **zoom on the plots** by **selecting an area with your mouse**. Double-click to reset the zoom level.
"""