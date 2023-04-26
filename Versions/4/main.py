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

def get_player_name():
    player_name = input("Please enter your name: ")
    return player_name

def display_player_info(player_name, cash_balance, companies, months_passed):
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

def hire_management(company, management_personnel):
    if len(companies) > 0:
        print("Companies:")
        for i, comp in enumerate(companies, 1):
            print(f"{i}. {comp['name']} ({comp['industry']})")
        company_choice = int(input("Enter the number of the company you want to hire management for: "))
        if 0 < company_choice <= len(companies):
            company = companies[company_choice - 1]
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
            company['capital'] -= manager['salary']
            company['revenue'] += manager['revenue_boost']
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

def company_action(company, cash_balance):
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
    return company, cash_balance

def advance_month(cash_balance, companies):
    cash_balance = update_cash_balance(cash_balance, companies)
    return cash_balance

def update_cash_balance(cash_balance, companies):
    for company in companies:
        profit = company['revenue'] * company['capital'] * company['profit_margin']
        cash_balance += profit
    return cash_balance

def main_game_loop(player_name, cash_balance, companies, business_types, management_personnel):
    months_passed = 0

    while True:
        display_player_info(player_name, cash_balance, companies, months_passed)

        print("\n1. Start a new business")
        print("2. Hire management")
        print("3. Perform a company action")
        print("4. Advance month")
        print("5. Quit game")
        
        choice = int(input("Enter the number corresponding to your choice: "))
        
        if choice == 1:
            new_company, cash_balance = create_company(cash_balance, business_types)
            if new_company is not None:
                companies.append(new_company)
        elif choice == 2:
            company = hire_management(companies, management_personnel)
        elif choice == 3:
            if len(companies) == 0:
                print("You have no companies to perform an action on. Create a company first.")
            else:
                company_index = int(input("Enter the number of the company you want to perform an action on: "))
                if 0 < company_index <= len(companies):
                    company = companies[company_index - 1]
                    company, cash_balance = company_action(company, cash_balance)
                else:
                    print("Invalid company number. Please try again.")
        elif choice == 4:
            cash_balance = advance_month(cash_balance, companies)
            months_passed += 1
        elif choice == 5:
            print("Thank you for playing Business Tycoon! Goodbye.")
            break
        else:
            print("Invalid input. Please try again.")

display_intro()
player_name = get_player_name()
cash_balance = 1000000000  # Starting cash balance
companies = []
business_types = load_data('business_types.json')
management_personnel = load_data('management.json')

main_game_loop(player_name, cash_balance, companies, business_types, management_personnel)