from geopy.distance import geodesic

def find_nearest_location(customer_location, seller_locations):
    """
    Finds the nearest seller to the given customer location.

    :param customer_location: A tuple of (latitude, longitude) for the customer.
    :param seller_locations: A list of dictionaries, each containing 'latitude' and 'longitude' keys for the sellers.
    :return: A tuple of (nearest_seller, distance) where nearest_seller is a dictionary of the nearest seller's details
             and distance is the distance to that seller.
    """
    nearest_seller = None
    min_distance = float('inf')

    for seller in seller_locations:
        seller_location = (seller['latitude'], seller['longitude'])
        distance = geodesic(customer_location, seller_location).kilometers

        if distance < min_distance:
            min_distance = distance
            nearest_seller = seller

    return nearest_seller, min_distance

