from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class NewVisitorTest(FunctionalTest):
	def test_can_start_a_todo_list(self):
		self.browser.get(self.live_server_url)

		inputbox = self.get_item_input_box()
		inputbox.send_keys("Buy peacock feathers")
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table("1: Buy peacock feathers")

		inputbox2 = self.get_item_input_box()
		inputbox2.send_keys("Use peacock feathers to make a fly")
		inputbox2.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table("1: Buy peacock feathers")
		self.wait_for_row_in_list_table("2: Use peacock feathers to make a fly")

	def test_multiple_users_can_start_lists_at_different_urls(self):
		self.browser.get(self.live_server_url)
		
		inputbox = self.get_item_input_box()
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

		inputbox = self.get_item_input_box()
		inputbox.send_keys("Buy milk")
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table("1: Buy milk")

		francis_list_url = self.browser.current_url
		self.assertRegex(francis_list_url,"/lists/.+")
		self.assertNotEqual(francis_list_url,edith_list_url)

		page_text = self.browser.find_element(By.TAG_NAME,"body").text
		self.assertNotIn("Buy peacock feathers",page_text)
		self.assertIn("Buy milk", page_text)

