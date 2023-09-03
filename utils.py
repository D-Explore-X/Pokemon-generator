import random

def get_random_element(arr):
    return random.choice(arr)

def remove_random_element(arr):
    index = random.randint(0, len(arr) - 1)
    return arr.pop(index)

def shuffle(arr):
    return random.sample(arr, len(arr))

def random_integer(max_exclusive):
    return random.randint(0, max_exclusive - 1)

def mark_loading(is_loading):
    # Implement logic to toggle loading state in your Flask project
    # You might want to use a template variable or some other mechanism
     pass 
def set_dropdown_if_valid(select, value):
    # Implement logic to set the dropdown value in your Flask project
    # You may need to use Flask's template variable
    pass




def parse_boolean(boolean):
    return boolean.lower() == "true"
