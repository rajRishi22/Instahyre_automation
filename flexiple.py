from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from dotenv import load_dotenv
import os
import random

load_dotenv()
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')

class FlexipleBot:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.applications_count = 0
        
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=chrome_options)

    def login(self):
        try:
            self.driver.get("https://app.flexiple.com/talent/login")
            time.sleep(2)

            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='email']"))
            )
            email_field.send_keys(self.email)
            
            password_field = self.driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            password_field.send_keys(self.password)
            
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            time.sleep(2)
            
        except Exception as e:
            print(f"Login error: {str(e)}")

    def select_yes_option(self):
        try:
            # Wait for and find combobox button
            combobox = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button[role="combobox"]'))
            )
            
            # Click the combobox
            self.driver.execute_script("arguments[0].click();", combobox)
            time.sleep(1)
            
            # Try multiple approaches to select Yes
            try:
                # Approach 1: Using hidden select element
                self.driver.execute_script("""
                    var select = document.querySelector('select[aria-hidden="true"]');
                    select.value = 'true';
                    select.dispatchEvent(new Event('change', {bubbles: true}));
                    
                    // Update button text
                    document.querySelector('button[role="combobox"] span').textContent = 'Yes';
                """)
            except:
                try:
                    # Approach 2: Click Yes option directly
                    yes_option = self.driver.find_element(By.XPATH, "//select[@aria-hidden='true']/option[@value='true']")
                    yes_option.click()
                except:
                    # Approach 3: Force selection via JavaScript
                    self.driver.execute_script("""
                        // Set value on hidden select
                        document.querySelector('select[aria-hidden="true"]').value = 'true';
                        
                        // Update visible button text
                        document.querySelector('button[role="combobox"] span').textContent = 'Yes';
                        
                        // Trigger events
                        const select = document.querySelector('select[aria-hidden="true"]');
                        select.dispatchEvent(new Event('change', {bubbles: true}));
                        select.dispatchEvent(new Event('input', {bubbles: true}));
                    """)
            
            time.sleep(1)
            
        except Exception as e:
            print(f"Error selecting Yes option: {e}")

    def select_yes_and_submit(self):
        try:
            # Select Yes option first
            self.select_yes_option()
            
            # Click on blank space to dismiss dropdown if needed
            self.driver.execute_script("""
                document.body.click();
            """)
            time.sleep(1)
            
            # Find and click Complete Submission button with multiple attempts
            try:
                # Try normal click first
                submit_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, 
                        "//button[@type='submit'][contains(text(), 'Complete Submission')]"))
                )
                submit_button.click()
            except:
                # If normal click fails, try JavaScript click
                self.driver.execute_script("""
                    document.querySelector("button[type='submit']").click();
                """)
            
            time.sleep(2)
            
        except Exception as e:
            print(f"Error in submission process: {e}")

    def apply_to_jobs(self):
        while True:
            try:
                # Find and click Apply Now button
                apply_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Apply Now')]"))
                )
                apply_button.click()
                time.sleep(2)
                
                # Fill salary
                salary_field = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "expectedCtc.formattedAmount"))
                )
                salary_field.clear()
                salary_field.send_keys("15")
                
                # Replace separate select and submit steps with combined function
                self.select_yes_and_submit()
                
                self.applications_count += 1
                print(f"Successfully applied to job #{self.applications_count}")

                # Navigate to next job
                explore_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, 
                        "//a[contains(text(), 'Explore similar jobs')]"))
                )
                explore_button.click()
                time.sleep(random.uniform(1, 3))
                
            except Exception as e:
                print(f"Error in application process: {str(e)}")
                try:
                    explore_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, 
                            "//a[contains(text(), 'Explore similar jobs')]"))
                    )
                    explore_button.click()
                    time.sleep(1)
                except:
                    print("Could not find Explore similar jobs button. Refreshing...")
                    self.driver.refresh()
                    time.sleep(2)
                continue
    
    def close_browser(self):
        self.driver.quit()

if __name__ == "__main__":
    bot = FlexipleBot(EMAIL, PASSWORD)
    try:
        bot.login()
        time.sleep(2)
        bot.apply_to_jobs()
    except KeyboardInterrupt:
        print("\nStopping the bot...")
    finally:
        bot.close_browser()