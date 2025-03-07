import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time



class NewVisitorTest(unittest.TestCase):
    # Step 0.1: Start the browser
    def setUp(self):
        self.browser = webdriver.Firefox()
    
    # Step 0.2: Stop the browser
    def tearDown(self):
        self.browser.quit()


    # Creating Functional Test method
    def test_can_start_a_todo_list(self):
        # Step 1: Open the homepage
        self.browser.get("http://127.0.0.1:8000/")


        # Step 2.1: Verify the page title contains "To-Do"
        self.assertIn("To-Do", self.browser.title)

        # Step 2.2: Locate the header element
        # it is used to examine web pages, also uses the parameter "By" to search using different HTML properties and attributes (just like 'getElementByTagName' in JavaScript)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text

        # Step 2.3: Verify the header contains "To-Do"
        self.assertIn("To-Do", header_text)


        # Step 3.1: Locate the input box by its ID (just like 'getElementByID' in JavaScript))
        input_box = self.browser.find_element(By.ID, "id_new_item")

        # Step 3.2: Verify the input box placeholder text
        self.assertEqual(input_box.get_attribute("placeholder"), "Enter a to-do item")


        # Step 4: Type "Buy peacock feathers" into the input box
        # It is Selenium’s way of typing into an input elements (just like 'set inner_text' in JavaScript) 
        input_box.send_keys("Buy peacock feathers")


        # Step 5.1: lets us send special keys like Enter..
        input_box.send_keys(Keys.ENTER)

        # Step 5.2: When we hit Enter, the page will refresh.
        time.sleep(1)       # time to wait for the page to update


        # Step 6.1: Locate the to-do list table
        table = self.browser.find_element(By.ID, "id_list_table")

        # Step 6.2: Find rows within the table
        rows = table.find_elements(By.TAG_NAME, "tr")

        # Step 6.3: look for and verify the newly added item is in the table
        self.assertTrue(any(row.text == "1. Buy peacock feathers" for row in rows))


        # Step 7: Mark the test as incomplete
        self.fail("Finish the test")


        # Step 8: Print success message (in the terminal)
        print("OK")



# Step 9: Run the test
if __name__ == "__main__":
    unittest.main()

