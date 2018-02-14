from splinter import Browser
import math
import copy

START_URL = 'https://www.charities.gov.sg/_layouts/MCYSCPSearch/MCYSCPSearchCriteriaPage.aspx'
CHARITIES_PER_PAGE = 5
MAX_RETRY_ATTEMPTS = 10

LAYOUT_PROFILE_MAPPING = {
    'name': '#ctl00_PlaceHolderMain_LabelOrgName',
    'uen': '#ctl00_PlaceHolderMain_lblUENNo',
}

LAYOUT_FINANCIAL_MAPPING = {
    'fy1': {
        'financial_period': '#ctl00_PlaceHolderMain_gvFinancialInformation > tbody > tr:nth-child(2) > td:nth-child(1)',
        'receipts_total': '#ctl00_PlaceHolderMain_gvFinancialInformation > tbody > tr:nth-child(2) > td:nth-child(2)',
        'expenses_total': '#ctl00_PlaceHolderMain_gvFinancialInformation > tbody > tr:nth-child(2) > td:nth-child(3)',
        'financial_status': '#ctl00_PlaceHolderMain_gvFinancialInformation > tbody > tr:nth-child(2) > td:nth-child(5)',
        'receipts_donation_cash_tax_deductible': '#ctl00_PlaceHolderMain_ucFSDetails_income_td_cash_2',
        'receipts_donation_cash_non_tax_deductible': '#ctl00_PlaceHolderMain_ucFSDetails_income_ntd_cash_2',
        'receipts_donation_cash_total': '#ctl00_PlaceHolderMain_ucFSDetails_income_total_cash_2',
        'receipts_donation_kind_tax_deductible': '#ctl00_PlaceHolderMain_ucFSDetails_income_td_kind_2',
        'receipts_donation_kind_non_tax_deductible': '#ctl00_PlaceHolderMain_ucFSDetails_income_ntd_kind_2',
        'receipts_donation_kind_total': '#ctl00_PlaceHolderMain_ucFSDetails_income_total_kind_2',
        'receipts_government_grants': '#ctl00_PlaceHolderMain_ucFSDetails_income_gov_grants_2',
        'receipts_investment_income': '#ctl00_PlaceHolderMain_ucFSDetails_income_investment_2',
        'receipts_programme_fees': '#ctl00_PlaceHolderMain_ucFSDetails_income_program_fee_2',
        'receipts_others_income': '#ctl00_PlaceHolderMain_ucFSDetails_income_other_2',
        'capital_in_nature': '#ctl00_PlaceHolderMain_ucFSDetails_capital_in_nature_2',
        'expenses_fund_raising': '#ctl00_PlaceHolderMain_ucFSDetails_expenses_fr_2',
        'expenses_charitable_local': '#ctl00_PlaceHolderMain_ucFSDetails_expenses_cae_local_2',
        'expenses_charitable_overseas': '#ctl00_PlaceHolderMain_ucFSDetails_expenses_cae_overseas_2',
        'expenses_charitable_total': '#ctl00_PlaceHolderMain_ucFSDetails_expenses_total_cape_2',
        'expenses_others_total': '#ctl00_PlaceHolderMain_ucFSDetails_expenses_other_2',
        'other_info_donation_other_charities': '#ctl00_PlaceHolderMain_ucFSDetails_oi_dgs_reg_charity_2',
        'other_info_no_of_employees': '#ctl00_PlaceHolderMain_ucFSDetails_oi_employee_no_2',
        'other_info_total_employee_costs': '#ctl00_PlaceHolderMain_ucFSDetails_oi_total_employee_cost_2',
        'other_info_fund_raising_efficiency_ratio': '#ctl00_PlaceHolderMain_ucFSDetails_oi_fr_efficiency_ratio_2',
        'other_info_total_related_party_transactions': '#ctl00_PlaceHolderMain_ucFSDetails_oi_total_related_party_2',
        'balance_assets_land_building': '#ctl00_PlaceHolderMain_ucFSDetails_bs_assets_land_building_2',
        'balance_assets_other_tangible': '#ctl00_PlaceHolderMain_ucFSDetails_bs_assets_other_tangible_2',
        'balance_assets_investments': '#ctl00_PlaceHolderMain_ucFSDetails_bs_assets_investments_2',
        'balance_assets_inventories': '#ctl00_PlaceHolderMain_ucFSDetails_bs_assets_inventories_2',
        'balance_assets_accounts_receivables': '#ctl00_PlaceHolderMain_ucFSDetails_bs_assets_accounts_receivables_2',
        'balance_assets_cash_deposits': '#ctl00_PlaceHolderMain_ucFSDetails_bs_assets_cash_deposits_2',
        'balance_assets_other_assets': '#ctl00_PlaceHolderMain_ucFSDetails_bs_assets_other_2',
        'balance_assets_total': '#ctl00_PlaceHolderMain_ucFSDetails_bs_assets_total_2',
        'balance_funds_unrestricted': '#ctl00_PlaceHolderMain_ucFSDetails_bs_funds_unrestricted_2',
        'balance_funds_restricted': '#ctl00_PlaceHolderMain_ucFSDetails_bs_funds_restricted_2',
        'balance_funds_endowment': '#ctl00_PlaceHolderMain_ucFSDetails_bs_funds_endowment_2',
        'balance_funds_total': '#ctl00_PlaceHolderMain_ucFSDetails_bs_funds_total_2',
        'balance_liabilities_current': '#ctl00_PlaceHolderMain_ucFSDetails_bs_liabilities_current_2',
        'balance_liabilities_non_current': '#ctl00_PlaceHolderMain_ucFSDetails_bs_liabilities_longterm_2',
        'balance_liabilities_total': '#ctl00_PlaceHolderMain_ucFSDetails_bs_liabilities_total_2',
        'balance_funds_liabilities_total': '#ctl00_PlaceHolderMain_ucFSDetails_bs_funds_liabilities_total_2'
    },
    'fy2': {
        'financial_period': '#ctl00_PlaceHolderMain_gvFinancialInformation > tbody > tr:nth-child(3) > td:nth-child(1)',
        'receipts_total': '#ctl00_PlaceHolderMain_gvFinancialInformation > tbody > tr:nth-child(3) > td:nth-child(2)',
        'expenses_total': '#ctl00_PlaceHolderMain_gvFinancialInformation > tbody > tr:nth-child(3) > td:nth-child(3)',
        'financial_status': '#ctl00_PlaceHolderMain_gvFinancialInformation > tbody > tr:nth-child(3) > td:nth-child(5)',
        'receipts_donation_cash_tax_deductible': '#ctl00_PlaceHolderMain_ucFSDetails_income_td_cash_1',
        'receipts_donation_cash_non_tax_deductible': '#ctl00_PlaceHolderMain_ucFSDetails_income_ntd_cash_1',
        'receipts_donation_cash_total': '#ctl00_PlaceHolderMain_ucFSDetails_income_total_cash_1',
        'receipts_donation_kind_tax_deductible': '#ctl00_PlaceHolderMain_ucFSDetails_income_td_kind_1',
        'receipts_donation_kind_non_tax_deductible': '#ctl00_PlaceHolderMain_ucFSDetails_income_ntd_kind_1',
        'receipts_donation_kind_total': '#ctl00_PlaceHolderMain_ucFSDetails_income_total_kind_1',
        'receipts_government_grants': '#ctl00_PlaceHolderMain_ucFSDetails_income_gov_grants_1',
        'receipts_investment_income': '#ctl00_PlaceHolderMain_ucFSDetails_income_investment_1',
        'receipts_programme_fees': '#ctl00_PlaceHolderMain_ucFSDetails_income_program_fee_1',
        'receipts_others_income': '#ctl00_PlaceHolderMain_ucFSDetails_income_other_1',
        'capital_in_nature': '#ctl00_PlaceHolderMain_ucFSDetails_capital_in_nature_1',
        'expenses_fund_raising': '#ctl00_PlaceHolderMain_ucFSDetails_expenses_fr_1',
        'expenses_charitable_local': '#ctl00_PlaceHolderMain_ucFSDetails_expenses_cae_local_1',
        'expenses_charitable_overseas': '#ctl00_PlaceHolderMain_ucFSDetails_expenses_cae_overseas_1',
        'expenses_charitable_total': '#ctl00_PlaceHolderMain_ucFSDetails_expenses_total_cape_1',
        'expenses_others_total': '#ctl00_PlaceHolderMain_ucFSDetails_expenses_other_1',
        'other_info_donation_other_charities': '#ctl00_PlaceHolderMain_ucFSDetails_oi_dgs_reg_charity_1',
        'other_info_no_of_employees': '#ctl00_PlaceHolderMain_ucFSDetails_oi_employee_no_1',
        'other_info_total_employee_costs': '#ctl00_PlaceHolderMain_ucFSDetails_oi_total_employee_cost_1',
        'other_info_fund_raising_efficiency_ratio': '#ctl00_PlaceHolderMain_ucFSDetails_oi_fr_efficiency_ratio_1',
        'other_info_total_related_party_transactions': '#ctl00_PlaceHolderMain_ucFSDetails_oi_total_related_party_1',
        'balance_assets_land_building': '#ctl00_PlaceHolderMain_ucFSDetails_bs_assets_land_building_1',
        'balance_assets_other_tangible': '#ctl00_PlaceHolderMain_ucFSDetails_bs_assets_other_tangible_1',
        'balance_assets_investments': '#ctl00_PlaceHolderMain_ucFSDetails_bs_assets_investments_1',
        'balance_assets_inventories': '#ctl00_PlaceHolderMain_ucFSDetails_bs_assets_inventories_1',
        'balance_assets_accounts_receivables': '#ctl00_PlaceHolderMain_ucFSDetails_bs_assets_accounts_receivables_1',
        'balance_assets_cash_deposits': '#ctl00_PlaceHolderMain_ucFSDetails_bs_assets_cash_deposits_1',
        'balance_assets_other_assets': '#ctl00_PlaceHolderMain_ucFSDetails_bs_assets_other_1',
        'balance_assets_total': '#ctl00_PlaceHolderMain_ucFSDetails_bs_assets_total_1',
        'balance_funds_unrestricted': '#ctl00_PlaceHolderMain_ucFSDetails_bs_funds_unrestricted_1',
        'balance_funds_restricted': '#ctl00_PlaceHolderMain_ucFSDetails_bs_funds_restricted_1',
        'balance_funds_endowment': '#ctl00_PlaceHolderMain_ucFSDetails_bs_funds_endowment_1',
        'balance_funds_total': '#ctl00_PlaceHolderMain_ucFSDetails_bs_funds_total_1',
        'balance_liabilities_current': '#ctl00_PlaceHolderMain_ucFSDetails_bs_liabilities_current_1',
        'balance_liabilities_non_current': '#ctl00_PlaceHolderMain_ucFSDetails_bs_liabilities_longterm_1',
        'balance_liabilities_total': '#ctl00_PlaceHolderMain_ucFSDetails_bs_liabilities_total_1',
        'balance_funds_liabilities_total': '#ctl00_PlaceHolderMain_ucFSDetails_bs_funds_liabilities_total_1'
    },
    'fy3': {
        'financial_period': '#ctl00_PlaceHolderMain_gvFinancialInformation > tbody > tr:nth-child(4) > td:nth-child(1)',
        'receipts_total': '#ctl00_PlaceHolderMain_gvFinancialInformation > tbody > tr:nth-child(4) > td:nth-child(2)',
        'expenses_total': '#ctl00_PlaceHolderMain_gvFinancialInformation > tbody > tr:nth-child(4) > td:nth-child(3)',
        'financial_status': '#ctl00_PlaceHolderMain_gvFinancialInformation > tbody > tr:nth-child(4) > td:nth-child(5)',
        'receipts_donation_cash_tax_deductible': '#ctl00_PlaceHolderMain_ucFSDetails_income_td_cash_0',
        'receipts_donation_cash_non_tax_deductible': '#ctl00_PlaceHolderMain_ucFSDetails_income_ntd_cash_0',
        'receipts_donation_cash_total': '#ctl00_PlaceHolderMain_ucFSDetails_income_total_cash_0',
        'receipts_donation_kind_tax_deductible': '#ctl00_PlaceHolderMain_ucFSDetails_income_td_kind_0',
        'receipts_donation_kind_non_tax_deductible': '#ctl00_PlaceHolderMain_ucFSDetails_income_ntd_kind_0',
        'receipts_donation_kind_total': '#ctl00_PlaceHolderMain_ucFSDetails_income_total_kind_0',
        'receipts_government_grants': '#ctl00_PlaceHolderMain_ucFSDetails_income_gov_grants_0',
        'receipts_investment_income': '#ctl00_PlaceHolderMain_ucFSDetails_income_investment_0',
        'receipts_programme_fees': '#ctl00_PlaceHolderMain_ucFSDetails_income_program_fee_0',
        'receipts_others_income': '#ctl00_PlaceHolderMain_ucFSDetails_income_other_0',
        'capital_in_nature': '#ctl00_PlaceHolderMain_ucFSDetails_capital_in_nature_0',
        'expenses_fund_raising': '#ctl00_PlaceHolderMain_ucFSDetails_expenses_fr_0',
        'expenses_charitable_local': '#ctl00_PlaceHolderMain_ucFSDetails_expenses_cae_local_0',
        'expenses_charitable_overseas': '#ctl00_PlaceHolderMain_ucFSDetails_expenses_cae_overseas_0',
        'expenses_charitable_total': '#ctl00_PlaceHolderMain_ucFSDetails_expenses_total_cape_0',
        'expenses_others_total': '#ctl00_PlaceHolderMain_ucFSDetails_expenses_other_0',
        'other_info_donation_other_charities': '#ctl00_PlaceHolderMain_ucFSDetails_oi_dgs_reg_charity_0',
        'other_info_no_of_employees': '#ctl00_PlaceHolderMain_ucFSDetails_oi_employee_no_0',
        'other_info_total_employee_costs': '#ctl00_PlaceHolderMain_ucFSDetails_oi_total_employee_cost_0',
        'other_info_fund_raising_efficiency_ratio': '#ctl00_PlaceHolderMain_ucFSDetails_oi_fr_efficiency_ratio_0',
        'other_info_total_related_party_transactions': '#ctl00_PlaceHolderMain_ucFSDetails_oi_total_related_party_0',
        'balance_assets_land_building': '#ctl00_PlaceHolderMain_ucFSDetails_bs_assets_land_building_0',
        'balance_assets_other_tangible': '#ctl00_PlaceHolderMain_ucFSDetails_bs_assets_other_tangible_0',
        'balance_assets_investments': '#ctl00_PlaceHolderMain_ucFSDetails_bs_assets_investments_0',
        'balance_assets_inventories': '#ctl00_PlaceHolderMain_ucFSDetails_bs_assets_inventories_0',
        'balance_assets_accounts_receivables': '#ctl00_PlaceHolderMain_ucFSDetails_bs_assets_accounts_receivables_0',
        'balance_assets_cash_deposits': '#ctl00_PlaceHolderMain_ucFSDetails_bs_assets_cash_deposits_0',
        'balance_assets_other_assets': '#ctl00_PlaceHolderMain_ucFSDetails_bs_assets_other_0',
        'balance_assets_total': '#ctl00_PlaceHolderMain_ucFSDetails_bs_assets_total_0',
        'balance_funds_unrestricted': '#ctl00_PlaceHolderMain_ucFSDetails_bs_funds_unrestricted_0',
        'balance_funds_restricted': '#ctl00_PlaceHolderMain_ucFSDetails_bs_funds_restricted_0',
        'balance_funds_endowment': '#ctl00_PlaceHolderMain_ucFSDetails_bs_funds_endowment_0',
        'balance_funds_total': '#ctl00_PlaceHolderMain_ucFSDetails_bs_funds_total_0',
        'balance_liabilities_current': '#ctl00_PlaceHolderMain_ucFSDetails_bs_liabilities_current_0',
        'balance_liabilities_non_current': '#ctl00_PlaceHolderMain_ucFSDetails_bs_liabilities_longterm_0',
        'balance_liabilities_total': '#ctl00_PlaceHolderMain_ucFSDetails_bs_liabilities_total_0',
        'balance_funds_liabilities_total': '#ctl00_PlaceHolderMain_ucFSDetails_bs_funds_liabilities_total_0'
    }
}


def calculate_page_count(record_number):
    return math.ceil(record_number / CHARITIES_PER_PAGE)


def get_target_link(pageNo):
    # charities.gov.sg has a very weird pagination system (1 => 16 => 26 => ...) ???
    return "#a${pageNo}" if pageNo != 1 else ''


hidden_link = 'https://www.charities.gov.sg/_layouts/MCYSCPSearch/MCYSCPSearchOrgProfile.aspx?AccountId=ZTk3MzY2MTktN2I2NS1lMzExLTgyZGItMDA1MDU2YjMwNDg0'


def scrape_charity_financial(browser, primary_sector, sub_sector, subsector_link, page_no, item_no):
    retry = True
    attempt_no = 1
    result = []

    turn_page = "javascript:turnPage(%d);" % page_no

    while retry and attempt_no < MAX_RETRY_ATTEMPTS:
        try:
            print("================================================")
            print("Processing financial information")
            print("Primary sector %s, sub sector %s" % (primary_sector, sub_sector))
            print("Page %s, item no %s" % (page_no, item_no))
            print("Attempt No: %s" % attempt_no)
            print("================================================")

            browser.visit(START_URL)

            # link to christian section
            browser.execute_script(subsector_link)

            # open page
            browser.execute_script(turn_page)

            # pick item
            hidden_element = browser.find_by_id(
                'ctl00_PlaceHolderMain_lstSearchResults_ctrl{}_hfViewDetails'.format(item_no)).first

            hidden_link = hidden_element.value

            # visit charity profile page
            browser.visit(hidden_link)

            charity_name = browser.find_by_id('ctl00_PlaceHolderMain_LabelOrgName').first.value
            print('Name: {}'.format(charity_name))

            # visit financial information section
            browser.click_link_by_href("javascript:__doPostBack('ctl00$PlaceHolderMain$Menu1','1')")

            alert = browser.get_alert()
            alert.accept()

            singpass_input_id = browser.find_by_xpath('//*[@id="loginID"]').first
            if singpass_input_id:
                print('SingPass is required, fill in SingPass login and password')

                browser.find_by_xpath('//*[@id="loginID"]').fill('ryan7san')
                browser.find_by_xpath('//*[@id="password"]').fill('1234qwer')
                browser.execute_script("doSubmit('login')")

            # visit financial information section again
            if browser.is_element_present_by_xpath(
                    xpath='//*[@id="ctl00_PlaceHolderMain_Menu1n1"]/table/tbody/tr/td/a',
                    wait_time=180):

                main_data = {
                    'primary_sector': primary_sector,
                    'sub_setor': sub_sector
                }

                # capturing main information
                for element in LAYOUT_PROFILE_MAPPING:
                    main_data[element] = browser.find_by_css(LAYOUT_PROFILE_MAPPING[element]).html

                # capturing financial information
                browser.click_link_by_href("javascript:__doPostBack('ctl00$PlaceHolderMain$Menu1','1')")

                last_financial_period = browser.find_by_css(
                    '#ctl00_PlaceHolderMain_gvFinancialInformation > tbody > tr:nth-child(2) > td.textCenter').first.html
                print("Last financial period: %s" % last_financial_period)

                if last_financial_period:
                    for key in LAYOUT_FINANCIAL_MAPPING:
                        temp_data = copy.deepcopy(main_data)
                        for sub_key in LAYOUT_FINANCIAL_MAPPING[key]:
                            try:
                                temp_data[sub_key] = browser.find_by_css(LAYOUT_FINANCIAL_MAPPING[key][sub_key]).first.html
                            except Exception as e:
                                temp_data[sub_key] = 0

                        result.append(temp_data)

                retry = False

            else:
                print('Financial Information link can not be found, retry scraping!')
        except Exception as e:
            print(e)

        attempt_no += 1

    return result


def main():
    print("Start Scraping")
    browser = Browser("chrome", headless=True)

    subsector_link = "javascript:SearchBySectorClass('1ed69f16-87a2-e211-b716-005056b30ba7','f0d42b7b-95a3-e311-93ea-005056b30485');"

    result = scrape_charity_financial(browser, "Religious", "Christianity", subsector_link, 1, 2)
    print(result)

main()
