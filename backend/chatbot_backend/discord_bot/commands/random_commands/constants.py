import re

# Regular expressions for parsing random command arguments
RANGE_SEPERATORS = ["-", "to", "through", "and"]
RANGE_REGEX = re.compile(r"(\d+)(?:\s*({}))\s*(\d+)".format("|".join(RANGE_SEPERATORS)))

# Regular expressions for parsing choice command arguments
CHOICES_SEPERATORS = ["or", ","]
CHOICES_REGEX = re.compile(r"(\w+)(?:\s*({}))".format("|".join(CHOICES_SEPERATORS)))
