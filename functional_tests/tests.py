from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class NewVisitorTest(LiveServerTestCase):
	def setUp(self):
	    self.browser = webdriver.Firefox()

	def tearDown(self):
	    self.browser.quit()

	def check_for_row_in_list_table(self, row_text):
		table = self.browser.find_element(By.ID,"id_list_table")
		rows = table.find_elements(By.TAG_NAME, "tr")
		self.assertIn(row_text,[row.text for row in rows])

	def test_can_start_a_todo_list(self):
		self.browser.get(self.live_server_url)

		inputbox = self.browser.find_element(By.ID,"id_new_item")
		inputbox.send_keys("Buy peacock feathers")
		inputbox.send_keys(Keys.ENTER)
		time.sleep(5)
		self.check_for_row_in_list_table("1: Buy peacock feathers")

		inputbox = self.browser.find_element(By.ID,"id_new_item")
		inputbox.send_keys("Use peacock feathers to make a fly")
		inputbox.send_keys(Keys.ENTER)
		time.sleep(5)

		self.check_for_row_in_list_table("1: Buy peacock feathers")
		self.check_for_row_in_list_table("2: Use peacock feathers to make a fly")
