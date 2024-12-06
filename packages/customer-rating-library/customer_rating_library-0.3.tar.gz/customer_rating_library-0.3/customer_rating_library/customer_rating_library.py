# customer_rating_library/customer_rating_library.py

class CustomerRating:
    def __init__(self, maximum_rating=10):

        #This initializes the maximium rating value

        self.maximum_rating = maximum_rating

    def calculate_average_customer_rating(self, customer_ratings):

        """It calculates the average rating from the list of customer ratings 
           and return 0 if the list is empty."""
        
        if not customer_ratings:
            return 0
        return sum(customer_ratings) / len(customer_ratings)

    def convert_to_percentage(self, average_customer_rating):

        """" It converts the average rating(float) to percentage based on the maximum customer rating
             and returns the percentage of the rating"""

        return (average_customer_rating / self.maximum_rating) * 100
