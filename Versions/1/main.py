import json
import random
import time

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

def display_player_info(player_name, cash_balance, companies):
    print("\nPlayer Information:")
    print(f"Name: {player_name}")
    print(f"Cash Balance: ${cash_balance}")
    print("Companies:")
    if len(companies) == 0:
        print("None")
    else:
        for company in companies:
            print(f"{company['name']} ({company['industry']}) - Management: {company['management']['name'] if 'management' in company else 'None'}")

def create_company(player_cash_balance, business_types):
    print("Available business types:")
    for business in business_types:
        print(f"{business['name']} (Startup Capital: ${business['startup_capital']})")
    business_choice = input("Choose a business type: ")

    for business in business_types:
        if business['name'].lower() == business_choice.lower():
            company_name = input("Enter a name for your new company: ")
            capital = int(input("Enter the initial capital for your company (in dollars): "))
            if capital >= business['startup_capital']:
                if player_cash_balance >= capital:
                    player_cash_balance -= capital
                    return {'name': company_name, 'industry': business['name'], 'capital': capital, 'offshore': False, 'revenue': 0, 'profit_margin': 0}, player_cash_balance
                else:
                    print("You don't have enough cash to start this business. Please try again.")
                    return None, player_cash_balance
            else:
                print("You don't have enough capital to start this business. Please try again.")
                return None, player_cash_balance
    print("Invalid business type. Please try again.")
    return None, player_cash_balance

def hire_management(company, management_personnel):
    print("Available managers:")
    for manager in management_personnel:
        print(f"{manager['name']} (Salary: ${manager['salary']}/month, Revenue Boost: {manager['revenue_boost'] * 100}%, Profit Margin Boost: {manager['profit_margin_boost'] * 100}%)")
    manager_choice = input("Choose a manager to hire: ")

    for manager in management_personnel:
        if manager['name'].lower() == manager_choice.lower():
            if company['capital'] >= manager['salary']:
                company['capital'] -= manager['salary']
                company['revenue'] += manager['revenue_boost']
                company['profit_margin'] += manager['profit_margin_boost']
                company['management'] = manager
                print(f"{manager['name']} has been hired as a manager for {company['name']} at a salary of ${manager['salary']}/month.")
                return company
            else:
                print("You don't have enough capital to hire this manager. Please try again.")
                return None
    print("Invalid manager choice. Please try again.")
    return None

def update_cash_balance(cash_balance, companies):
    for company in companies:
        profit = company['revenue'] * company['capital'] * company['profit_margin']
        cash_balance += profit
    return cash_balance

def main_game_loop(player_name, cash_balance, companies, business_types, management_personnel):
    last_month_update = time.time()

    while True:
        display_player_info(player_name, cash_balance, companies)

        print("\n1. Start a new business")
        print("2. Hire management")
        print("3. Quit game")
        
        choice = int(input("Enter the number corresponding to your choice: "))
        
        if choice == 1:
            new_company, cash_balance = create_company(cash_balance, business_types)
            if new_company is not None:
                companies.append(new_company)
        elif choice == 2:
            if len(companies) == 0:
                print("You have no companies to hire management for. Create a company first.")
            else:
                company_name = input("Enter the name of the company you want to hire management for: ")
                found = False
                for company in companies:
                    if company['name'].lower() == company_name.lower():
                        found = True
                        company = hire_management(company, management_personnel)
                        break
                if not found:
                    print("Company not found. Please try again.")
        elif choice == 3:
            print("Thank you for playing Business Tycoon! Goodbye.")
            break
        else:
            print("Invalid input. Please try again.")

        # Update cash balance every minute (one month in-game time)
        current_time = time.time()
        if current_time - last_month_update >= 60:
            cash_balance = update_cash_balance(cash_balance, companies)
            last_month_update = current_time

display_intro()
player_name = get_player_name()
cash_balance = 1000000000  # Starting cash balance
companies = []
business_types = load_data('business_types.json')
management_personnel = load_data('management.json')

main_game_loop(player_name, cash_balance, companies, business_types, management_personnel)