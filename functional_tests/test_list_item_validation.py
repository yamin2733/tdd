from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from unittest import skip
from selenium.webdriver.common.by import By
from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):
	
	def test_cannot_add_empty_list_items(self):
	     self.browser.get(self.live_server_url)
	     input=self.browser.find_element(By.ID,'id_new_item')
	     input.send_keys(Keys.ENTER)
	     self.wait_for(lambda:self.assertEqual(self.browser.find_element(By.CSS_SELECTOR, '.has-error').text,"You can't have an empty list item"))
	     #self.assertEqual(self.browser.find_element_by_css_selector('.has-error').text,

	     self.browser.find_element(By.ID,'id_new_item').send_keys('Buy milk')
	     self.browser.find_element(By.ID,'id_new_item').send_keys(Keys.ENTER)
	     self.wait_for_row_in_list_table('1: Buy milk')

	     self.browser.find_element(By.ID,'id_new_item').send_keys(Keys.ENTER)

	     self.wait_for(lambda: self.assertEqual(self.browser.find_element(By.CSS_SELECTOR, '.has-error').text,"You can't have an empty list item"))

	     self.browser.find_element(By.ID, 'id_new_item').send_keys('Make tea')
	     self.browser.find_element(By.ID, 'id_new_item').send_keys(Keys.ENTER)
	     self.wait_for_row_in_list_table('1: Buy milk')
	     self.wait_for_row_in_list_table('2: Make tea')
