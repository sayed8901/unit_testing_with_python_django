import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time



class NewVisitorTest(unittest.TestCase):
    # Step 0.1: Start the browser before each test
    def setUp(self):
        self.browser = webdriver.Firefox()
    
    # Step 0.2: Stop the browser after each test
    def tearDown(self):
        self.browser.quit()


    
    # Creating a function to check a to_do item within the table
    def check_for_row_in_list_table(self, row_text):
        # Locate the table by its ID
        table = self.browser.find_element(By.ID, "id_list_table")
        # Get all rows in the table
        rows = table.find_elements(By.TAG_NAME, "tr")
        
        # Assert that the text exists in any row
        self.assertIn(row_text, [row.text for row in rows])




    # Creating Functional Test method to insert to_do items
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


        # Step 3.1 : Locate the input box by its ID (just like 'getElementByID' in JavaScript))
        input_box = self.browser.find_element(By.ID, "id_new_item")

        # Step 3.2 : Type "Use peacock feathers to make a fly" into the input box
        # It is Selenium’s way of typing into an input elements (just like 'set inner_text' in JavaScript) 
        input_box.send_keys("Use peacock feathers to make a fly")

        # Step 3.3 : lets us send special keys like 'Enter key' to submit the form
        input_box.send_keys(Keys.ENTER)     # Submit the form

        # Step 4 : When we hit Enter, the page will refresh.
        time.sleep(10)       # time to wait for the page to update

        # step 5 : Use the helper function to check items
        self.check_for_row_in_list_table("1: Buy peacock feathers")
        self.check_for_row_in_list_table("2: Use peacock feathers to make a fly")


        # Step 6: Mark the test as incomplete
        # This ensures we remember to complete the test later
        self.fail("Finish the test")


        # Step 7: Print success message in the terminal
        # (This line won't run due to self.fail)
        print("Functional Tests OK")



# Final Step : Run the test script
if __name__ == "__main__":
    unittest.main()


