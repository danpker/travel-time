import unittest
import random

# We need to do some weird loading because BitBar needs a .5m in the filename
import imp
travel_time = imp.load_source('travel_time.5m', 'travel_time.5m.py')

class GetColourTestCase(unittest.TestCase):

    def test_less_than_ten_minutes_is_green(self):
        """A duration of less than 10 minutes will have a colour of green."""
        duration = random.randint(1, 50)
        diff = random.randint(0,9)
        duration_in_traffic = duration + diff

        colour = travel_time.get_colour(f"{duration} mins",
                                        f"{duration_in_traffic} mins")

        self.assertEqual(colour, "green")

    def test_between_ten_mins_and_twenty_five_is_orange(self):
        """A duration of between 10 mins and 25 is orange."""
        duration = random.randint(1, 35)
        diff = random.randint(9, 25)
        duration_in_traffic = duration + diff

        colour = travel_time.get_colour(f"{duration} mins",
                                        f"{duration_in_traffic} mins")

        self.assertEqual(colour, "orange")

    def test_over_twenty_five_mins_is_red(self):
        """A duration over 25 minutes is red."""
        duration = 1
        diff = random.randint(25, 59)
        duration_in_traffic = duration + diff

        colour = travel_time.get_colour(f"{duration} mins",
                                        f"{duration_in_traffic} mins")

        self.assertEqual(colour, "red")

if __name__ == "__main__":
    unittest.main()
