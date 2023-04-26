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

def get_difficulty_level():
    print("1. Rare (Easiest)")
    print("2. Medium Rare")
    print("3. Medium Well")
    print("4. Well Done (Hardest)")

    choice = int(input("Enter the number corresponding to your choice: "))
    
    difficulty_multipliers = {
        1: 1,
        2: 0.75,
        3: 0.5,
        4: 0.25
    }

    if 0 < choice <= 4:
        return difficulty_multipliers[choice]
    else:
        print("Invalid input. Please try again.")
        return get_difficulty_level()
    
def get_player_name():
    player_name = input("Please enter your name: ")
    return player_name

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
            monthly_profit = monthly_revenue * company['profit_margin']
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
    business_choice = int(input("Choose a business type by entering the corresponding number: "))

    if 0 < business_choice <= len(business_types):
        business = business_types[business_choice - 1]
        company_name = input("Enter a name for your new company: ")
        capital = int(input("Enter the initial capital for your company (in dollars): "))
        if capital >= business['startup_capital']:
            if player_cash_balance >= capital:
                player_cash_balance -= capital
                return {'name': company_name, 'industry': business['name'], 'capital': capital, 'offshore': False, 'revenue': business['revenue'], 'profit_margin': business['profit_margin']}, player_cash_balance
            else:
                print("You don't have enough cash to start this business. Please try again.")
                return None, player_cash_balance
        else:
            print("You don't have enough capital to start this business. Please try again.")
            return None, player_cash_balance
    else:
        print("Invalid business type. Please try again.")
        return None, player_cash_balance

def hire_management(companies, management_personnel):
    if len(companies) > 0:
        display_companies_list(companies)
        company_choice = int(input("Enter the number of the company you want to hire management for: "))
        if 0 < company_choice <= len(companies):
            company = companies[company_choice - 1]
            if 'management' in company:
                print(f"{company['name']} already has a manager: {company['management']['name']}. Please fire the current manager before hiring a new one.")
                return
        else:
            print("Invalid company number. Please try again.")
            return None

    print("Available managers:")
    for i, manager in enumerate(management_personnel, 1):
        print(f"{i}. {manager['name']} (Salary: ${manager['salary']}/month, Revenue Boost: {manager['revenue_boost'] * 100}%, Profit Margin Boost: {manager['profit_margin_boost'] * 100}%)")
    manager_choice = int(input("Choose a manager to hire by entering the corresponding number: "))

    if 0 < manager_choice <= len(management_personnel):
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
    else:
        print("Invalid manager choice. Please try again.")
        return None

def fire_management(companies):
    if len(companies) > 0:
        display_companies_list(companies)
        company_choice = int(input("Enter the number of the company you want to fire management for: "))
        if 0 < company_choice <= len(companies):
            company = companies[company_choice - 1]
            if 'management' in company:
                print(f"{company['management']['name']} has been fired from {company['name']}.")
                company['revenue'] /= (1 + company['management']['revenue_boost'])
                company['profit_margin'] -= company['management']['profit_margin_boost']
                del company['management']
            else:
                print(f"{company['name']} does not have a manager to fire.")
        else:
            print("Invalid company number. Please try again.")
            return None

def display_companies_list(companies):
    print("Companies:")
    for i, comp in enumerate(companies, 1):
        print(f"{i}. {comp['name']} ({comp['industry']})")

def company_action(companies, cash_balance):
    if len(companies) == 0:
        print("You have no companies to perform an action on. Create a company first.")
    else:
        display_companies_list(companies)
        company_index = int(input("Enter the number of the company you want to perform an action on: "))
        if 0 < company_index <= len(companies):
            company = companies[company_index - 1]
            if company['industry'] == "Dropshipping":
                product_cost = int(input("Enter the cost of the product you want to launch (in dollars): "))
                if cash_balance >= product_cost:
                    cash_balance -= product_cost
                    company['revenue'] += product_cost * 0.5
                    print(f"You have successfully launched a new product in your Dropshipping company. Your company's revenue has increased.")
                else:
                    print("You don't have enough cash to launch this product. Please try again.")
            elif company['industry'] == "Construction":
                project_cost = int(input("Enter the cost of the building project you want to start (in dollars): "))
                if cash_balance >= project_cost:
                    cash_balance -= project_cost
                    company['revenue'] += project_cost * 0.6
                    print(f"You have successfully started a new building project in your Construction company. Your company's revenue has increased.")
                else:
                    print("You don't have enough cash to start this project. Please try again.")
        else:
            print("Invalid company number. Please try again.")
    return companies, cash_balance

def create_offshore_company(cash_balance, offshore_locations):
    print("Offshore locations:")
    for i, location in enumerate(offshore_locations, 1):
        print(f"{i}. {location['name']} (Setup Cost: ${location['setup_cost']}, Tax Rate: {location['tax_rate'] * 100}%)")
    location_choice = int(input("Choose an offshore location by entering the corresponding number: "))

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
        offshore_choice = int(input("Enter the number of the offshore company you want to add a company to: "))
        if 0 < offshore_choice <= len(offshore_companies):
            offshore_company = offshore_companies[offshore_choice - 1]
        else:
            print("Invalid offshore company number. Please try again.")
            return offshore_companies, companies

        display_companies_list(companies)
        company_choice = int(input("Enter the number of the company you want to add to the offshore company: "))
        if 0 < company_choice <= len(companies):
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
            print("Invalid company number. Please try again.")
            return offshore_companies, companies
    else:
        print("You don't have any offshore companies or regular companies. Create them first.")
        return offshore_companies, companies

def remove_company_from_offshore(offshore_companies, companies):
    if len(offshore_companies) > 0 and len(companies) > 0:
        print("Offshore Companies:")
        for i, offshore_company in enumerate(offshore_companies, 1):
            print(f"{i}. {offshore_company['name']} ({offshore_company['location']})")
        offshore_choice = int(input("Enter the number of the offshore company you want to remove a company from: "))
        if 0 < offshore_choice <= len(offshore_companies):
            offshore_company = offshore_companies[offshore_choice - 1]
        else:
            print("Invalid offshore company number. Please try again.")
            return offshore_companies, companies

        print("Companies in the offshore company:")
        for i, comp in enumerate(offshore_company['companies'], 1):
            print(f"{i}. {comp['name']} ({comp['industry']})")
        company_choice = int(input("Enter the number of the company you want to remove from the offshore company: "))
        if 0 < company_choice <= len(offshore_company['companies']):
            company = offshore_company['companies'][company_choice - 1]
            offshore_company['companies'].remove(company)
            company['offshore'] = False
            print(f"{company['name']} has been removed from {offshore_company['name']}.")
            return offshore_companies, companies
        else:
            print("Invalid company number. Please try again.")
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
        taxed_profit = (profit - operating_cost) * (1 - tax_rate)  # Deduct operating_cost before taxes
        cash_balance += taxed_profit * difficulty_level
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
        print("4. Perform a company action")
        print("5. Create an offshore company")
        print("6. Add a company to an offshore company")
        print("7. Remove a company from an offshore company")
        print("8. Advance month")
        print("9. Quit game")
        
        try:
            choice = int(input("Enter the number corresponding to your choice: "))
        except ValueError:
            print("Invalid input. Please try again.")
            continue
                
        if choice == 1:
            new_company, cash_balance = create_company(cash_balance, business_types)
            if new_company is not None:
                companies.append(new_company)
        elif choice == 2:
            company = hire_management(companies, management_personnel)
        elif choice == 3:
            fire_management(companies)
        elif choice == 4:
            if len(companies) == 0:
                print("You have no companies to perform an action on. Create a company first.")
            else:
                companies, cash_balance = company_action(companies, cash_balance)
        elif choice == 5:
            new_offshore_company, cash_balance = create_offshore_company(cash_balance, offshore_locations)
            if new_offshore_company is not None:
                offshore_companies.append(new_offshore_company)
        elif choice == 6:
            offshore_companies, companies = add_company_to_offshore(offshore_companies, companies)
        elif choice == 7:
            offshore_companies, companies = remove_company_from_offshore(offshore_companies, companies)
        elif choice == 8:
            cash_balance = advance_month(cash_balance, companies, offshore_companies, difficulty_level)
            months_passed += 1
        elif choice == 9:
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