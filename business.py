import json
import random

def load_data(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def display_intro():
    print("Welcome to the Business Tycoon game!")
    print("In this game, you will start and manage various companies, set up offshore entities, and hire management.")
    print("Your goal is to become the ultimate business tycoon!")

def get_valid_input(min_value, max_value, prompt_message):
    while True:
        try:
            user_input = int(input(prompt_message))
            if min_value <= user_input <= max_value:
                return user_input
            else:
                print(f"Please enter a number between {min_value} and {max_value}.")
        except ValueError:
            print("Invalid input. Please try again.")

def get_difficulty_level():
    print("1. Rare (Easiest)")
    print("2. Medium Rare")
    print("3. Medium Well")
    print("4. Well Done (Hardest)")

    choice = get_valid_input(1, 4, "Enter the number corresponding to your choice: ")
    
    difficulty_multipliers = {
        1: 1,
        2: 0.75,
        3: 0.5,
        4: 0.25
    }

    return difficulty_multipliers[choice]
    
def get_player_name():
    player_name = input("Please enter your name: ")
    return player_name

def display_company_products(companies):
    if len(companies) > 0:
        display_companies_list(companies)
        company_choice = get_valid_input(1, len(companies), "Enter the number of the company you want to view Product(s) for: ")
        company = companies[company_choice - 1]
        if len(company['products']) == 0:
            print(f"{company['name']} has no Product(s).")
        else:
            print("\nProduct(s):")
            for i, product in enumerate(company['products'], 1):
                print(f"{i}. {product['name']} - Investment: ${product['investment']}")
    else:
        print("You don't have any companies to view Product(s) for. Create a company first.")
        
def add_new_product_to_company(companies, cash_balance):
    if len(companies) > 0:
        display_companies_list(companies)
        company_choice = get_valid_input(1, len(companies), "Enter the number of the company you want to add a product to: ")
        company = companies[company_choice - 1]

        product_name = input("Enter a name for your new product: ")
        investment = get_valid_input(0, float('inf'), "Enter the amount of money you want to invest in this product: ")

        if cash_balance >= investment:
            cash_balance -= investment
            profit_margin = 0.1
            added_revenue = investment * profit_margin
            added_profit = added_revenue * company['profit_margin']
            company['revenue'] += added_revenue
            company['profit_margin'] += (company['profit_margin'] * added_profit) / company['revenue']
            company['products'].append({'name': product_name, 'investment': investment, 'revenue': added_revenue})
            print(f"You have successfully added {product_name} to {company['name']} with an investment of ${investment}.")
            print(f"Company's revenue increased by ${added_revenue} and profit increased by ${added_profit}.")
        else:
            print("You don't have enough cash to invest in this Product(s). Please try again.")
    else:
        print("You don't have any companies to add a Product(s) to. Create a company first.")
    return companies, cash_balance

def remove_product_from_company(companies):
    if len(companies) > 0:
        display_companies_list(companies)
        company_choice = get_valid_input(1, len(companies), "Enter the number of the company you want to remove a Product(s) from: ")
        company = companies[company_choice - 1]

        if len(company['products']) == 0:
            print(f"{company['name']} has no Product(s) to remove.")
        else:
            print("Product(s):")
            for i, product in enumerate(company['products'], 1):
                print(f"{i}. {product['name']} - Investment: ${product['investment']}")
            product_choice = get_valid_input(1, len(company['products']), "Enter the number of the Product(s) you want to remove: ")

            removed_product = company['products'].pop(product_choice - 1)
            print(f"{removed_product['name']} has been removed from {company['name']}.")
    else:
        print("You don't have any companies to remove a Product(s) from. Create a company first.")
    return companies

def display_player_info(player_name, cash_balance, companies, offshore_companies, months_passed):
    print(f"\nMonths passed: {months_passed}")
    print("\nPlayer Information:")
    print(f"Name: {player_name}")
    print(f"Cash Balance: ${cash_balance}")
    print("Companies:")
    if len(companies) == 0:
        print("None")
    else:
        for i, company in enumerate(companies, 1):
            monthly_revenue = company['revenue'] * company['capital']
            monthly_profit = monthly_revenue * company['profit_margin'] * difficulty_level
            print(f"{i}. {company['name']} ({company['industry']}) - Management: {company['management']['name'] if 'management' in company else 'None'}, Monthly Revenue: ${monthly_revenue}, Monthly Profit: ${monthly_profit}")

    print("Offshore Companies:")
    if len(offshore_companies) == 0:
        print("None")
    else:
        for i, offshore_company in enumerate(offshore_companies, 1):
            print(f"{i}. {offshore_company['name']} ({offshore_company['location']})")

def create_company(player_cash_balance, business_types):
    print("Available business types:")
    for i, business in enumerate(business_types, 1):
        print(f"{i}. {business['name']} (Startup Capital: ${business['startup_capital']})")
    business_choice = get_valid_input(1, len(business_types), "Choose a business type by entering the corresponding number: ")

    business = business_types[business_choice - 1]
    company_name = input("Enter a name for your new company: ")
    capital = get_valid_input(0, float('inf'), "Enter the initial capital for your company (in dollars): ")

    if capital >= business['startup_capital']:
        if player_cash_balance >= capital:
            player_cash_balance -= capital
            return {'name': company_name, 'industry': business['name'], 'capital': capital, 'offshore': False, 'revenue': business['revenue'], 'profit_margin': business['profit_margin'], 'products': []}, player_cash_balance
        else:
            print("You don't have enough cash to start this business. Please try again.")
            return None, player_cash_balance
    else:
        print("You don't have enough capital to start this business. Please try again.")
        return None, player_cash_balance
        
def hire_management(companies, management_personnel):
    if len(companies) > 0:
        display_companies_list(companies)
        company_choice = get_valid_input(1, len(companies), "Enter the number of the company you want to hire management for: ")
        company = companies[company_choice - 1]
        if 'management' in company:
            print(f"{company['name']} already has a manager: {company['management']['name']}. Please fire the current manager before hiring a new one.")
            return
    else:
        print("You don't have any companies to hire management for. Create a company first.")
        return None

    print("Available managers:")
    for i, manager in enumerate(management_personnel, 1):
        print(f"{i}. {manager['name']} (Salary: ${manager['salary']}/month, Revenue Boost: {manager['revenue_boost'] * 100}%, Profit Margin Boost: {manager['profit_margin_boost'] * 100}%)")
    manager_choice = get_valid_input(1, len(management_personnel), "Choose a manager to hire by entering the corresponding number: ")

    manager = management_personnel[manager_choice - 1]
    monthly_revenue = company['revenue'] * company['capital']
    monthly_profit = monthly_revenue * company['profit_margin']
    if manager['salary'] <= monthly_profit:
        company['revenue'] *= (1 + manager['revenue_boost'])
        company['profit_margin'] += manager['profit_margin_boost']
        company['management'] = manager
        print(f"{manager['name']} has been hired as a manager for {company['name']} at a salary of ${manager['salary']}/month.")
        return company
    else:
        print("You don't have enough monthly profit to hire this manager. Please try again.")
        return None

def fire_management(companies):
    if len(companies) > 0:
        display_companies_list(companies)
        company_choice = get_valid_input(1, len(companies), "Enter the number of the company you want to fire management for: ")
        company = companies[company_choice - 1]
        if 'management' in company:
            print(f"{company['management']['name']} has been fired from {company['name']}.")
            company['revenue'] /= (1 + company['management']['revenue_boost'])
            company['profit_margin'] -= company['management']['profit_margin_boost']
            del company['management']
        else:
            print(f"{company['name']} does not have a manager to fire.")
    else:
        print("You don't have any companies to fire management for. Create a company first.")

def display_companies_list(companies):
    print("Companies:")
    for i, comp in enumerate(companies, 1):
        print(f"{i}. {comp['name']} ({comp['industry']})")

def company_action(companies, cash_balance, business_types):
    if len(companies) == 0:
        print("You have no companies to perform an action on. Create a company first.")
    else:
        display_companies_list(companies)
        company_index = int(input("Enter the number of the company you want to perform an action on: "))
        if 0 < company_index <= len(companies):
            company = companies[company_index - 1]
            business_type = next((biz_type for biz_type in business_types if biz_type['name'] == company['industry']), None)
            
            if business_type is not None:
                if company['industry'] == "Dropshipping":
                    product_cost = get_valid_input(0, float('inf'), "Enter the cost of the product you want to launch (in dollars): ")
                    if cash_balance >= product_cost:
                        cash_balance -= product_cost
                        company['revenue'] += product_cost * business_type['profit_margin']
                        print(f"You have successfully launched a new product in your Dropshipping company. Your company's revenue has increased.")
                    else:
                        print("You don't have enough cash to launch this product. Please try again.")
                elif company['industry'] == "Construction":
                    project_cost = get_valid_input(0, float('inf'), "Enter the cost of the building project you want to start (in dollars): ")
                    if cash_balance >= project_cost:
                        cash_balance -= project_cost
                        company['revenue'] += project_cost * business_type['profit_margin']
                        print(f"You have successfully started a new building project in your Construction company. Your company's revenue has increased.")
                    else:
                        print("You don't have enough cash to start this project. Please try again.")
            else:
                print("Error: Business type not found.")
        else:
            print("Invalid company number. Please try again.")
    return companies, cash_balance

def create_offshore_company(cash_balance, offshore_locations):
    print("Offshore locations:")
    for i, location in enumerate(offshore_locations, 1):
        print(f"{i}. {location['name']} (Setup Cost: ${location['setup_cost']},Tax Rate: {location['tax_rate'] * 100}%)")
    location_choice = get_valid_input(1, len(offshore_locations), "Choose an offshore location by entering the corresponding number: ")

    if 0 < location_choice <= len(offshore_locations):
        location = offshore_locations[location_choice - 1]
        if cash_balance >= location['setup_cost']:
            cash_balance -= location['setup_cost']
            offshore_name = input("Enter a name for your new offshore company: ")
            return {'name': offshore_name, 'location': location['name'], 'tax_rate': location['tax_rate'], 'companies': []}, cash_balance
        else:
            print("You don't have enough cash to set up an offshore company in this location. Please try again.")
            return None, cash_balance
    else:
        print("Invalid offshore location. Please try again.")
        return None, cash_balance

def add_company_to_offshore(offshore_companies, companies):
    if len(offshore_companies) > 0 and len(companies) > 0:
        print("Offshore Companies:")
        for i, offshore_company in enumerate(offshore_companies, 1):
            print(f"{i}. {offshore_company['name']} ({offshore_company['location']})")
        offshore_choice = get_valid_input(1, len(offshore_companies), "Enter the number of the offshore company you want to add a company to: ")
        offshore_company = offshore_companies[offshore_choice - 1]

        display_companies_list(companies)
        company_choice = get_valid_input(1, len(companies), "Enter the number of the company you want to add to the offshore company: ")
        company = companies[company_choice - 1]
        if company['offshore']:
            print(f"{company['name']} is already part of an offshore company. Please remove it from the current offshore company before adding it to a new one.")
            return offshore_companies, companies
        else:
            offshore_company['companies'].append(company)
            company['offshore'] = True
            print(f"{company['name']} has been added to {offshore_company['name']}.")
            return offshore_companies, companies
    else:
        print("You don't have any offshore companies or regular companies. Create them first.")
        return offshore_companies, companies

def remove_company_from_offshore(offshore_companies, companies):
    if len(offshore_companies) > 0 and len(companies) > 0:
        print("Offshore Companies:")
        for i, offshore_company in enumerate(offshore_companies, 1):
            print(f"{i}. {offshore_company['name']} ({offshore_company['location']})")
        offshore_choice = get_valid_input(1, len(offshore_companies), "Enter the number of the offshore company you want to remove a company from: ")
        offshore_company = offshore_companies[offshore_choice - 1]

        print("Companies in the offshore company:")
        for i, comp in enumerate(offshore_company['companies'], 1):
            print(f"{i}. {comp['name']} ({comp['industry']})")
        company_choice = get_valid_input(1, len(offshore_company['companies']), "Enter the number of the company you want to remove from the offshore company: ")
        company = offshore_company['companies'][company_choice - 1]
        offshore_company['companies'].remove(company)
        company['offshore'] = False
        print(f"{company['name']} has been removed from {offshore_company['name']}.")
        return offshore_companies, companies
    else:
        print("You don't have any offshore companies or regular companies. Create them first.")
        return offshore_companies, companies

def advance_month(cash_balance, companies, offshore_companies, difficulty_level):
    cash_balance = update_cash_balance(cash_balance, companies, offshore_companies, difficulty_level)
    return cash_balance

def update_cash_balance(cash_balance, companies, offshore_companies, difficulty_level):
    for company in companies:
        profit = company['revenue'] * company['capital'] * company['profit_margin']
        operating_cost = company['capital'] * 0.05  # Added operating_cost (5% of capital)
        tax_rate = 0.15  # Updated default tax rate
        if company['offshore']:
            for offshore_company in offshore_companies:
                if company in offshore_company['companies']:
                    tax_rate = offshore_company['tax_rate']
                    break
        taxed_profit = ((profit * difficulty_level) - operating_cost) * (1 - tax_rate)  # Deduct operating_cost before taxes
        cash_balance += taxed_profit
    return cash_balance

def main_game_loop(player_name, cash_balance, companies, business_types, management_personnel, offshore_locations, difficulty_level):
    months_passed = 0
    offshore_companies = []

    cash_balance *= 0.5  # Reduce the starting cash balance
    for business_type in business_types:
        business_type['revenue'] *= 0.5  # Reduce the revenue
        business_type['profit_margin'] *= 0.5  # Reduce the profit margin
                
    while True:
        display_player_info(player_name, cash_balance, companies, offshore_companies, months_passed)
        
        print("\n1. Start a new business")
        print("2. Hire management")
        print("3. Fire management")
        print("4. Create an offshore company")
        print("5. Add a company to an offshore company")
        print("6. Remove a company from an offshore company")
        print("7. Advance month")
        print("8. View Product(s)")
        print("9. Add a Product(s) to a company")
        print("10. Remove a Product(s) from a company")
        print("11. Quit game")
        
        choice = get_valid_input(1, 11, "Enter the number corresponding to your choice: ")
                        
        if choice == 1:
            new_company, cash_balance = create_company(cash_balance, business_types)
            if new_company is not None:
                companies.append(new_company)
        elif choice == 2:
            company = hire_management(companies, management_personnel)
        elif choice == 3:
            fire_management(companies)
        elif choice == 4:
            new_offshore_company, cash_balance = create_offshore_company(cash_balance, offshore_locations)
            if new_offshore_company is not None:
                offshore_companies.append(new_offshore_company)
        elif choice == 5:
            offshore_companies, companies = add_company_to_offshore(offshore_companies, companies)
        elif choice == 6:
            offshore_companies, companies = remove_company_from_offshore(offshore_companies, companies)
        elif choice == 7:
            cash_balance = advance_month(cash_balance, companies, offshore_companies, difficulty_level)
            months_passed += 1
        elif choice == 8:
            display_company_products(companies)
        elif choice == 9:
            companies, cash_balance = add_new_product_to_company(companies, cash_balance)
        elif choice == 10:
            companies = remove_product_from_company(companies)
        elif choice == 11:
            print("Thank you for playing Business Tycoon! Goodbye.")
            break
        else:
            print("Invalid input. Please try again.")
        
display_intro()
player_name = get_player_name()
cash_balance = 10000  # Starting cash balance
companies = []
business_types = load_data('business_types.json')
management_personnel = load_data('management.json')
offshore_locations = load_data('offshore_locations.json')
difficulty_level = get_difficulty_level()

main_game_loop(player_name, cash_balance, companies, business_types, management_personnel, offshore_locations, difficulty_level)