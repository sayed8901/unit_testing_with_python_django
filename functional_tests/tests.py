from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.common.exceptions import WebDriverException
import time


MAX_WAIT = 5



class NewVisitorTest(LiveServerTestCase):
    # Step 0.1: Start the browser before each test
    def setUp(self):
        self.browser = webdriver.Firefox()
    
        
    # Step 0.2: Stop the browser after each test
    def tearDown(self):
        self.browser.quit()


    
    # Creating a function to handle wait mechanism 
    # and also to check a to_do item within the table
    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()

        while True:
            try:
                # Locate the table by its ID
                table = self.browser.find_element(By.ID, "id_list_table")
                # Find rows within the table
                rows = table.find_elements(By.TAG_NAME, "tr")

                # Assert that the text exists in any row
                self.assertIn(row_text, [row.text for row in rows])
                return

            except (AssertionError, WebDriverException):
                if time.time() - start_time > MAX_WAIT:
                    raise
                time.sleep(0.5)




    # Creating Functional Test method to insert to_do items
    def test_can_start_a_todo_list(self):
        # Step 1: Open the homepage
        # we are using here django provided 'live_server_url' instead of hardcoded "http://127.0.0.1:8000/"
        self.browser.get(self.live_server_url)



        # Step 2.1: Verify the page title contains "To-Do"
        self.assertIn("To-Do", self.browser.title)

        # Step 2.2: Locate the header element
        # it is used to examine web pages, also uses the parameter "By" to search using different HTML properties and attributes (just like 'getElementByTagName' in JavaScript)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text

        # Step 2.3: Verify the header contains "To-Do"
        self.assertIn("To-Do", header_text)



        # Step 3.1 : Locate the input box by its ID (just like 'getElementByID' in JavaScript))
        input_box = self.browser.find_element(By.ID, "id_new_item")

        # step 3.2: type a placeholder text in the input box
        self.assertEqual(input_box.get_attribute("placeholder"), "Enter a to-do item")



        # Step 4 : Type "Buy peacock feathers" into the input box
        # It is Selenium’s way of typing into an input elements (just like 'set inner_text' in JavaScript) 
        input_box.send_keys("Buy peacock feathers")



        # Step 5.1 : lets us send special keys like 'Enter key'
        input_box.send_keys(Keys.ENTER)     # To submit the form

        # Step 5.2 : When we hit Enter, the page will refresh.
        # time to wait for the page to update to check items
        self.wait_for_row_in_list_table("1: Buy peacock feathers")



        # There is still a text box inviting to add another item.
        # Step 6.1 : Locate the input box by its ID
        input_box = self.browser.find_element(By.ID, "id_new_item")

        # Step 6.2 : Type "Use peacock feathers to make a fly" into the input box
        input_box.send_keys("Use peacock feathers to make a fly")

        # Step 6.3 : Again using the 'Enter key' to submit it
        input_box.send_keys(Keys.ENTER)



        # Step 7 : Use the helper function to check items
        self.wait_for_row_in_list_table("1: Buy peacock feathers")
        self.wait_for_row_in_list_table("2: Use peacock feathers to make a fly")



        # Step 8: Print success message in the terminal
        print("Functional test 1 - OK")






    def test_multiple_users_can_lists_at_different_urls(self):
        # Tasmi starts a new to-do list
        self.browser.get(self.live_server_url)
        input_box = self.browser.find_element(By.ID, "id_new_item")
        input_box.send_keys("Buy peacock feathers")
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy peacock feathers")


        # She notices that her list has a unique URL
        tasmi_list_url = self.browser.current_url

        # assertRegex is a helper function from unittest that checks whether a string matches a regular expression.
        self.assertRegex(tasmi_list_url, "/lists/.+")



        # Now a new user, Sayed, comes along to the site

        ## We delete all the browser cookies first as a  way of simulating a brand new user session
        self.browser.delete_all_cookies()



        # Sayed visits the home page, there is no sign of Tasmi's List
        self.browser.get(self.live_server_url)

        page_text = self.browser.find_element(By.TAG_NAME, "body").text

        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertNotIn("make a fly", page_text)


        # Sayed starts a new list by entering a new item. He is less interesting then Tasmi....
        input_box = self.browser.find_element(By.ID, "id_new_item")
        input_box.send_keys("Buy milk")
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")



        # Sayed gets his own unique URL
        sayed_list_URL = self.browser.current_url
        self.assertRegex(sayed_list_URL, "/lists/.+")

        # checking weather the both url are not equal...
        self.assertNotEqual(sayed_list_URL, tasmi_list_url)



        # Again, there is no sign of Tasmi's List
        page_text = self.browser.find_element(By.TAG_NAME, "body").text

        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertIn("Buy milk", page_text)



        # Satisfied, they both go back to sleep
        print("Functional test 2 - OK")
