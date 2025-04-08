def min_trips_distance(trips, total_distance=0):
    # Sort to get shortest distance
    # Remove this sort to get the 17 miles value from the example given input [6, 2, 1]
    # 2 + 6 + 8 + 1 = 17 miles.
    trips.sort()

    if len(trips) <= 2:
        # Only two remains, just add them to the value of total_distance - this terminates the recursion
        return total_distance + sum(trips)

    while len(trips):
        # Get the first two and do a sum to get the new trip
        new_trip = sum(trips[0:2])

        # Get the remaining trips (excluding the first two)
        trips = trips[2:]

        # Add the new_trip
        trips.append(new_trip)

        # Recursively calculate the trip until trips are empty
        return min_trips_distance(trips, total_distance + new_trip)


# Example usage:
trips = [6, 2, 1]
# trips = [3, 7, 5, 5, 3, 9, 4, 1, 12, 6, 3, 5, 1]

print(min_trips_distance(trips))
