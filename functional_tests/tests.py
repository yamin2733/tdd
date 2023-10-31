from django.test import LiveServerTestCase
from selenium.common.exceptions import WebDriverException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

MAX_WAIT = 5

class NewVisitorTest(LiveServerTestCase):
	def setUp(self):
	    self.browser = webdriver.Firefox()

	def tearDown(self):
	    self.browser.quit()

	def wait_for_row_in_list_table(self, row_text):
		start_time = time.time()
		while True:
		    try: 
		        table = self.browser.find_element(By.ID,"id_list_table")
		        rows = table.find_elements(By.TAG_NAME, "tr")
		        self.assertIn(row_text,[row.text for row in rows])
		        return
		    except (AssertionError, WebDriverException):
		        if time.time() - start_time > MAX_WAIT:
		            raise
		        time.sleep(0.5)

	def test_can_start_a_todo_list(self):
		self.browser.get(self.live_server_url)

		inputbox = self.browser.find_element(By.ID,"id_new_item")
		inputbox.send_keys("Buy peacock feathers")
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table("1: Buy peacock feathers")

		inputbox = self.browser.find_element(By.ID,"id_new_item")
		inputbox.send_keys("Use peacock feathers to make a fly")
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table("1: Buy peacock feathers")
		self.wait_for_row_in_list_table("2: Use peacock feathers to make a fly")

	def test_multiple_users_can_start_lists_at_different_urls(self):
		self.browser.get(self.live_server_url)
		inputbox = self.browser.find_element(By.ID,"id_new_item")
		inputbox.send_keys("Buy peacock feathers")
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table("1: Buy peacock feathers")
		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url,"/lists/.+")

		self.browser.delete_all_cookies()

		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element(By.TAG_NAME,"body").text
		self.assertNotIn("Buy peacock feathers",page_text)
		self.assertNotIn("make a fly", page_text)

		inputbox = self.browser.find_element(By.ID,"id_new_item")
		inputbox.send_keys("Buy milk")
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table("1:Buy milk")

		francis_list_url = self.browser.current_url
		self.assertRegex(francis_list_url,"/lists/.+")
		self.assertNotEqual(francis_list_url,edith_list_url)

		page_text = self.browser.find_element(By.TAG_NAME,"body").text
		self.assertNotIn("Buy peacock feathers",page_text)
		self.assertIn("Buy milk", page_text)
