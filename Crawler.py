from heapq import nlargest
import re
from selenium import webdriver


def find_most_common_words(word_count, excluded_words=()):
    # Create web driver and point it to requested site:
    driver = webdriver.Chrome('chromedriver')
    driver.get("https://en.wikipedia.org/wiki/Microsoft")

    # Define limiting and containing elements:
    beginning_element = driver.find_element("xpath", '//*[@id="History"]')
    ending_element = driver.find_element("xpath", '//*[@id="Corporate_affairs"]')
    containing_div = driver.find_element("xpath", '//*[@id="mw-content-text"]/div[1]')

    # Initialize necessary variables:
    is_in_bounds = False
    counted_words = {}

    # Iterate through all elements in containingDiv
    for elem in containing_div.find_elements("xpath", ".//*"):
        if elem == beginning_element:
            is_in_bounds = True  # Set is_in_bounds to true so it will enter the 'if' below from then on
        elif elem == ending_element:
            break  # Exit the for loop when we find the ending_element
            
        if is_in_bounds:
            # We've entered the portion of the div we want to search
            for word in elem.text.split(' '):
                result = re.sub(r'[^a-zA-Z]', '', word).lower()
                # regEx may leave us with empty strings- these shouldn't be counted
                if result not in excluded_words and result != '':
                    if result in counted_words:
                        counted_words[result] += 1
                    else:
                        counted_words[result] = 1
        
    # nlargest returns a list of key value pairs with the highest values from the dict
    results = nlargest(word_count, counted_words, key=counted_words.get)

    for word in results:
        print(f"{word}: {counted_words[word]}")


def different_word_count():
    print("Enter how many words you would like returned: ")
    # Input validation: continue to loop until the user enters an int
    while True:
        try:
            word_count = int(input())
        except ValueError:
            print("Invalid input! Please enter just the digit!")
        else:
            # When they enter an int, call find_most_common_words() with it
            find_most_common_words(word_count)
            break


def exclude_words():
    # Determine how many words to collect from the user:
    print("How many words would you like to exclude?")
    print("Enter your answer as an integer: ")
    while True:
        try:
            word_count = int(input())
        except ValueError:
            print("Invalid input! Please enter just the digit!")
        else:
            break
    
    i = 0
    ignored_words = list()
    # Collect words to ignore:
    while i < word_count:
        print(f"Enter word {i+1}: ")
        ignored_words.append(re.sub(r'[^a-zA-Z]', '', input()).lower())
        i += 1
    
    find_most_common_words(10, ignored_words)


def print_menu():
    print("***********************************")
    print("**** Microsoft History Crawler ****")
    print("***********************************")
    print(" Would you like to:")
    print("  1: Run the default crawler")
    print("  2: Return more/less words")
    print("  3: Exclude words from the search\n")


def get_query():
    print_menu()

    while True:
        try:
            userinput = int(input())
        except ValueError:
            print("Invalid input! Please enter just the digit!")
        if userinput in {1, 2, 3}:
            break
        print("Enter 1, 2, or 3: ")
    
    match userinput:
        case 1:
            find_most_common_words(10)
        case 2:
            different_word_count()
        case 3:
            exclude_words()


get_query()
