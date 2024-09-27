from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import os

# Path to ChromeDriver
CHROMEDRIVER_PATH = "./chromedriver.exe"

# JavaScript code with logging
javascript_code = """
console.log("Script started");
document.querySelectorAll('.content > a')[0].click();
console.log("Clicked on the first anchor in .content");

setTimeout(() => {
  const secondAccordion = document.querySelectorAll('.accordion.closed')[1];
  const teamLogo = secondAccordion ? secondAccordion.querySelector('.team-logo.svelte-b0nj1o') : null;

  if (teamLogo) {
    teamLogo.click();
    console.log("Team logo clicked");
  } else {
    console.error("Team logo not found");
  }

  const observer = new MutationObserver((mutations, observerInstance) => {
    const players = secondAccordion.querySelectorAll('.player-card');

    if (players.length > 0) {
      console.log("Player cards found");

      players.forEach(player => {
        const playerName = player.querySelector('.player-data p').textContent.trim();

        if (playerName === 'PlayerName') {
          console.log(`Player found: ${playerName}`);
          const checkbox = player.querySelector('input[type="checkbox"]');
          if (checkbox) {
            checkbox.checked = true;
            console.log("Checkbox checked");

            setTimeout(() => {
              const event = new Event('change', { bubbles: true });
              checkbox.dispatchEvent(event);
              console.log("Checkbox change event triggered");
            }, 2000);
          }
        }
      });

      observerInstance.disconnect();
      console.log("Stopped observing");

      setTimeout(() => {
        const submitButton = secondAccordion.querySelector('.btn.vote-btn');
        if (submitButton) {
          submitButton.click();
          console.log("Submit button clicked");
        } else {
          console.error("Submit button not found");
        }
      }, 5000);
    } else {
      console.error("Player cards not found");
    }
  });

  observer.observe(secondAccordion, { childList: true, subtree: true });
  console.log("Started observing DOM changes");

}, 2000);
"""

# Function to open Chrome in incognito, run JavaScript, and capture logs
def open_incognito_and_run_js(iteration):
    chrome_options = Options()
    chrome_options.add_argument("--incognito")

    # Enable browser logging
    capabilities = DesiredCapabilities.CHROME
    capabilities['goog:loggingPrefs'] = {'browser': 'ALL'}

    # Initialize ChromeDriver
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=chrome_options, desired_capabilities=capabilities)

    try:
        # Open the desired URL
        driver.get("https://esports.battlegroundsmobileindia.com/")  # Replace with your URL

        # Wait for the page to load
        time.sleep(5)

        # Inject the JavaScript into the page
        driver.execute_script(javascript_code)

        # Allow time for the script to execute
        time.sleep(10)

        # Retrieve and store browser logs
        logs = driver.get_log('browser')
        log_filename = f"iteration_{iteration}_log.txt"
        with open(log_filename, "w") as log_file:
            for entry in logs:
                log_file.write(f"{entry['level']}: {entry['message']}\n")
        
        print(f"Logs saved for iteration {iteration} in {log_filename}")

    finally:
        # Close the browser
        driver.quit()

# Run the process 10 times
for i in range(10):
    print(f"Starting iteration {i+1}")
    open_incognito_and_run_js(i+1)
    time.sleep(2)  # Optional delay between iterations
