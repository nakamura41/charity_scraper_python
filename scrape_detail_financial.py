from splinter import Browser
from config import config, links
import math
import copy
import pandas
import time


def calculate_page_count(record_number):
    return math.ceil(record_number / config.CHARITIES_PER_PAGE)


def get_target_link(pageNo):
    # charities.gov.sg has a very weird pagination system (1 => 16 => 26 => ...) ???
    return "#a${pageNo}" if pageNo != 1 else ''


hidden_link = 'https://www.charities.gov.sg/_layouts/MCYSCPSearch/MCYSCPSearchOrgProfile.aspx?AccountId=ZTk3MzY2MTktN2I2NS1lMzExLTgyZGItMDA1MDU2YjMwNDg0'


def scrape_charity_financial(browser, primary_sector, sub_sector, link_id, subsector_link, page_no, item_no):
    retry = True
    attempt_no = 1
    result = []

    turn_page = "javascript:turnPage(%d);" % page_no

    while retry and attempt_no < config.MAX_RETRY_ATTEMPTS:
        try:
            print("================================================")
            print("Processing financial information")
            print("Primary sector %s, sub sector %s" % (primary_sector, sub_sector))
            print("Page %s, item no %s" % (page_no, item_no))
            print("Attempt No: %s" % attempt_no)
            print("================================================")

            browser.visit(config.START_URL)

            # link to christian section
            browser.execute_script(subsector_link)

            # open page
            browser.execute_script(turn_page)

            # pick item
            hidden_element = browser.find_by_css(
                '#ctl00_PlaceHolderMain_lstSearchResults_ctrl{}_hfViewDetails'.format(item_no)).first

            hidden_link = hidden_element.value

            # visit charity profile page
            browser.visit(hidden_link)

            charity_name = browser.find_by_css('#ctl00_PlaceHolderMain_LabelOrgName').first.value
            print('Name: {}'.format(charity_name))
            print("------------------------------------------------")

            main_data = {
                'primary_sector': primary_sector,
                'sub_sector': sub_sector
            }

            # capturing main information
            for element in config.LAYOUT_PROFILE_MAPPING:
                main_data[element] = browser.find_by_css(config.LAYOUT_PROFILE_MAPPING[element]).html

            # visit financial information section
            print('Click Financial Information link')
            browser.click_link_by_href("javascript:__doPostBack('ctl00$PlaceHolderMain$Menu1','1')")

            try:
                # click SingPass alert message
                alert = browser.get_alert()
                alert.accept()

                singpass_input_id = browser.find_by_css('#loginID').first
                if singpass_input_id:
                    print('SingPass is required, fill in your login and password')

                    browser.find_by_css('#loginID').fill('ryan7san')
                    browser.find_by_css('#password').fill('1234qwer')
                    browser.execute_script("doSubmit('login')")
            except Exception as e:
                print("No SingPass alert message or you have logged-in to SingPass before")
                print(e)

            # visit financial information section again
            if browser.is_element_present_by_xpath(
                    xpath='//*[@id="ctl00_PlaceHolderMain_Menu1n1"]/table/tbody/tr/td/a',
                    wait_time=180
            ):
                print('Re-click Financial Information link')
                browser.click_link_by_href("javascript:__doPostBack('ctl00$PlaceHolderMain$Menu1','1')")

                # capturing financial information
                print("Checking whether 'Financial Summary of past three (3) financial periods' exists or not")
                if browser.is_element_present_by_xpath(
                        '//*[@id="ctl00_PlaceHolderMain_ucFSDetails_tbFSDetails"]',
                        wait_time=10
                ):
                    print("------------------------------------------------")
                    print("Yes, that information does exists")
                    for key in config.LAYOUT_FINANCIAL_MAPPING:
                        temp_data = copy.deepcopy(main_data)
                        for sub_key in config.LAYOUT_FINANCIAL_MAPPING[key]:
                            try:
                                temp_data[sub_key] = browser.find_by_css(
                                    config.LAYOUT_FINANCIAL_MAPPING[key][sub_key]).first.html
                            except Exception as e:
                                temp_data[sub_key] = 0

                        result.append(temp_data)

                    if result:
                        csvfile = "data/output/financial_%s_%s_%s.csv" % (link_id, page_no, item_no)
                        dataframe = pandas.DataFrame(result)
                        dataframe.to_csv(csvfile, index=False, header=True)
                        print("Finish writing charity financial information")
                        print("File: %s" % csvfile)
                    else:
                        print("Can not write empty financial information to file!!!")
                else:
                    print("------------------------------------------------")
                    print("No financial information to be captured")

            else:
                print('Financial Information link can not be found, retry scraping!')

            retry = False

        except Exception as e:
            print(e)

        attempt_no += 1

    return result


def main():
    print("Start Scraping")
    browser = Browser("chrome", headless=True)

    jobs = []
    for link in links.LINKS:
        page_no = 1

        for i in range(1, link['record_count']):
            jobs.append({
                'primary_sector': link['primary_sector'],
                'sub_sector': link['sub_sector'],
                'link_id': link['id'],
                'href': link['href'],
                'page_no': page_no,
                'item_no': (i - 1) % 5
            })
            if i % 5 == 0:
                page_no += 1

    for job in jobs:
        scrape_charity_financial(
            browser, job["primary_sector"], job["sub_sector"], job["link_id"], job["href"], job["page_no"],
            job["item_no"])

        time.sleep(8)

    print("Scraping Done")


main()
