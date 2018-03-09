import unittest
import random

# We need to do some weird loading because BitBar needs a .5m in the filename
import imp
travel_time = imp.load_source('travel_time.5m', 'travel_time.5m.py')


class GetColourTestCase(unittest.TestCase):

    def test_less_than_ten_minutes_is_green(self):
        """A duration of less than 10 minutes will have a colour of green."""
        duration = random.randint(1, 50)
        diff = random.randint(0, 9)
        duration_in_traffic = duration + diff

        colour = travel_time.get_colour(f"{duration} mins",
                                        f"{duration_in_traffic} mins")

        self.assertEqual("green", colour)

    def test_between_ten_mins_and_twenty_five_is_orange(self):
        """A duration of between 10 mins and 25 is orange."""
        duration = random.randint(1, 35)
        diff = random.randint(10, 24)
        duration_in_traffic = duration + diff

        colour = travel_time.get_colour(f"{duration} mins",
                                        f"{duration_in_traffic} mins")

        self.assertEqual("orange", colour)

    def test_over_twenty_five_mins_is_red(self):
        """A duration over 25 minutes is red."""
        duration = 1
        diff = random.randint(25, 59)
        duration_in_traffic = duration + diff

        colour = travel_time.get_colour(f"{duration} mins",
                                        f"{duration_in_traffic} mins")

        self.assertEqual("red", colour)

    def test_will_handle_durations_in_hours(self):
        """If the duration will take over an hour it will be in the format:
        "2 hours 48 mins". durations like this should be handled correctly"""
        duration = random.randint(1, 50)
        diff = random.randint(0, 9)
        duration_in_traffic = duration + diff

        colour = travel_time.get_colour(f"1 hour {duration} mins",
                                        f"1 hour {duration_in_traffic} mins")

        self.assertEqual("green", colour)

    def test_will_be_orange_even_with_hours(self):
        """If the duration will take over an hour it will be in the format:
        "2 hours 48 mins". durations like this should be handled correctly.
        A duration of between 10 mins and 25 is orange."""
        duration = random.randint(1, 35)
        diff = random.randint(10, 25)
        duration_in_traffic = duration + diff

        colour = travel_time.get_colour(f"1 hour {duration} mins",
                                        f"1 hour {duration_in_traffic} mins")

        self.assertEqual("orange", colour)

    def test_will_be_red_even_with_hours(self):
        """If the duration will take over an hour it will be in the format:
        "2 hours 48 mins". durations like this should be handled correctly.
        A duration over 25 minutes is red."""
        duration = 1
        diff = random.randint(25, 59)
        duration_in_traffic = duration + diff

        colour = travel_time.get_colour(f"1 hour {duration} mins",
                                        f"1 hour {duration_in_traffic} mins")

        self.assertEqual("red", colour)

    def test_negative_difference_should_be_green(self):
        """If we are lucky enough for the expected time to be negative, the
        colour should be green."""
        duration = 60
        diff = random.randint(1, 59)
        duration_in_traffic = duration - diff

        colour = travel_time.get_colour(f"{duration} mins",
                                        f"{duration_in_traffic} mins")

        self.assertEqual("green", colour)


if __name__ == "__main__":
    unittest.main()
