Feature: Car Valuation

  Scenario: Validate car valuation details for all registrations
    Given the system reads the input file "input/car_input.txt" with mileage range "1000" to "200000"
    And the "confused_page" page is open with title "Confused.com"
    Then for each registration in the input file:
      Given the "confused_page" page is open with title "Confused.com"
      When on page "confused_page" the user clicks the "cookies"
      And on page "confused_page" the user clicks the "hero_product_car_insurance"
      And on page "confused_page" the user enters the registration number into the "registration-number-input" field
      And on page "confused_page" the user clicks the "find-vehicle-btn"
      Then on page "confused_page" verify no errors are displayed for "error-summary__heading"
      And on page "confused_page" waiting for element "registration-lookup-summary-title" text to contain "Make and model"
      When on page "confused_page" the user scrapes the car details in "car_details"
      Then the system should compare fetched details with expected "input/car_output.txt"
