from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
import time
from dotenv import load_dotenv
import os
import random
load_dotenv()
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')

def scroll_to_element(driver, element):
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    time.sleep(1)

def click_element(driver, element):
    try:
        scroll_to_element(driver, element)
        element.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", element)
    time.sleep(1)

def apply_instahyre_jobs():
    brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
    options = webdriver.ChromeOptions()
    options.binary_location = brave_path
    
    # Add these options to handle SSL errors
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--disable-web-security')
    options.add_argument('--allow-running-insecure-content')
    
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()  # Maximize window to avoid element visibility issues

    try:
        # First navigate to login page
        driver.get("https://www.instahyre.com/login/")
        
        # Wait for email and password fields
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        time.sleep(1)
        password_field = driver.find_element(By.ID, "password")

        # Enter credentials
        email_field.send_keys(EMAIL)
        time.sleep(1)
        password_field.send_keys(PASSWORD)

        # Click login button 
        login_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-lg.btn-success")
        login_button.click()

        # Wait longer for page load after login
        time.sleep(10)

        # Navigate to opportunities page and wait
        driver.get("https://www.instahyre.com/candidate/opportunities/?matching=true")
        time.sleep(8)

        # Updated job functions selection logic
        try:
            # First find and click the job functions input to open dropdown
            job_functions_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "job-functions-selectized"))
            )
            driver.execute_script("arguments[0].click();", job_functions_input)
            time.sleep(2)

            # Now find and click the Full-Stack Development option
            software_eng_option = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, 
                    "//div[contains(@class, 'option') and contains(text(), 'All - Software Engineering')]"))
            )
            driver.execute_script("arguments[0].click();", software_eng_option)
            time.sleep(2)

        except Exception as e:
            print(f"Error selecting job function: {e}")

        # Set experience and trigger change
        driver.execute_script("""
            var el = document.getElementById('years');
            el.value = '1';
            var event = new Event('input', { bubbles: true });
            el.dispatchEvent(event);
        """)
        time.sleep(3)

        # Click show results with retry
        show_results = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "show-results"))
        )
        click_element(driver, show_results)
        time.sleep(8)  # Wait for results to load

        try:
            # Use a more specific selector for the first View button
            view_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 
                    "div.employer-block:first-child div.opportunity-action-links button.button-interested.btn.btn-success"))
            )
            
            # Ensure the button is in view and clickable
            driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", view_button)
            time.sleep(2)

            # Try multiple click methods
            try:
                # Try regular click
                view_button.click()
            except:
                try:
                    # Try JavaScript click
                    driver.execute_script("arguments[0].click();", view_button)
                except:
                    # Try Actions chain
                    actions = webdriver.ActionChains(driver)
                    actions.move_to_element(view_button).click().perform()
            
            time.sleep(3)

            # Modified continuous application loop
            applications_count = 0
            
            while True:  # Infinite loop
                try:
                    # Try to find Apply button
                    apply_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "button.btn.btn-lg.btn-primary.new-btn"))
                    )

                    # Check if we can apply
                    if apply_button.text == "Apply":
                        # Random delay between 1-3 seconds
                        delay = random.uniform(1, 3)
                        time.sleep(delay)
                        
                        scroll_to_element(driver, apply_button)
                        try:
                            apply_button.click()
                        except:
                            driver.execute_script("arguments[0].click();", apply_button)
                        
                        time.sleep(1)  # Short delay after clicking

                        # Handle modal apply button
                        try:
                            modal = WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located((By.CLASS_NAME, "modal-dialog"))
                            )
                            modal_apply_button = modal.find_element(By.CSS_SELECTOR, "button.btn.btn-lg.btn-primary.new-btn")
                            click_element(driver, modal_apply_button)
                            applications_count += 1
                            print(f"Successfully applied to job #{applications_count}")
                            
                            # Random delay before next application
                            # delay = random.uniform(1, 3)
                            time.sleep(delay)
                            
                        except Exception as e:
                            print(f"Modal handling error: {e}")
                            # Don't break, continue trying
                            continue
                    else:
                        print(f"Button text changed to: {apply_button.text}, retrying...")
                        time.sleep(2)
                        continue

                except TimeoutException:
                    print("Apply button not found, retrying...")
                    time.sleep(2)
                    continue
                    
                except Exception as e:
                    print(f"Error in application loop: {e}, retrying...")
                    time.sleep(2)
                    continue

        except Exception as e:
            print(f"Error clicking initial View button: {e}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    apply_instahyre_jobs()