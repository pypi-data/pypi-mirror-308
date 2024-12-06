from urllib.parse import urljoin, urlparse
from .webscraper import WebScraper, sleep_rnd
from .util import print_err
from .names import simpleMatchScore, parseName
import sys
import random

from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

class LinkedInNotFound(Exception):
    pass

class LinkedInPageNotRecognized(Exception):
    pass

def guess_linkedin_profile_ddg(scraper, name, extra):
    search_string = f"site%3Alinkedin.com/in {name} {extra}"
    search_string_escaped = search_string.replace(" ", "%20")
    search_url_ddg = f"http://duckduckgo.com/?q={search_string_escaped}"
    search_url_qw = f"http://qwant.com/?q={search_string_escaped}"
    # Use qwant, seems like less rate limiting lol
    search_url = search_url_qw
    scraper.nav(search_url)
    if search_url_ddg == search_url:
        links = scraper.find_elements('//a[@data-testid="result-title-a"]')
    else:
        links = scraper.find_elements('//a[@data-testid="serTitle"]')
    
    name_obj = parseName(name)
    print_err(name_obj)
    url = None
    for li in links:
        if 'linkedin.com' not in  li.get_attribute('href'):
            continue
        text = li.text.lower()
        print_err(text)
        if name_obj and name_obj['firstname'] in text and name_obj['lastname'] in text:
            url = li.get_attribute('href')
            break
        if name_obj is None:
            url = li.get_attribute('href')
            break
    if url and 'linkedin.com/in' in url:
        return url
    if url and 'linkedin.com/pub' in url:
        scraper.nav(url)
        return scraper.driver.current_url
    return None

def guess_linkedin_profile(scraper, name, extra):
    search_string = f"{name} {extra}"
    search_string_escaped = search_string.replace(" ", "%20")
    search_url = f"https://www.linkedin.com/search/results/people/?keywords={search_string_escaped}&origin=GLOBAL_SEARCH_HEADER"
    scraper.nav(search_url)
    url = check_profile(scraper, name)
    if url:
        return url
   
    search_string = f"site%3Alinkedin.com/in {name} {extra}"
    search_string_escaped = search_string.replace(" ", "%20")
    search_url = f"http://duckduckgo.com/?q=!ducky+{search_string_escaped}"
    scraper.nav(search_url)
    url = scraper.driver.current_url
    if 'linkedin.com/in' not in url:
        return None
    return f"http://www.linkedin.com/in/" + urlparse(url).path.split('/')[2]


def check_profile(scraper, name):
    # First try to see if there is an exact name match
    result_nodes = scraper.find_elements(
        f"//div[contains(@class,'entity-result')]//a"
    )
    if len(result_nodes) == 0:
        # No results
        return None
    name_nodes = [(n, simpleMatchScore(name, n.get_attribute('innerText'))) for n in result_nodes]
    best = max(name_nodes, key= lambda x: x[1])
    if best[1] < 0.5:
        return None

    url = best[0].get_attribute('href') 
    return urljoin(url, urlparse(url).path)


def scrape_linkedin_details(scraper, detail_url, detail_name, detail_name_id):

    def expand_all(scraper):
        expand_about = scraper.driver.find_elements(By.CLASS_NAME, "inline-show-more-text__button")
        for ele in expand_about:
            if "see more" in ele.text:
                ele.click()

    section = scraper.find_element(f'//section[div[@id="{detail_name}"]]')
    if section is None:
        return None

    see_more = section.find_elements(By.XPATH, f'//a[@id="navigation-index-see-all-{detail_name_id}"]')

    if len(see_more) > 0:
        scraper.nav(detail_url)
        expand_all(scraper)
        html = scraper.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        div = soup.find("main")
    else:
        expand_all(scraper)
        html = section.get_attribute('outerHTML')
        soup = BeautifulSoup(html, "html.parser")
        div = soup

    details = []
    if div and "Nothing to see" not in div.text and div.find('ul'):
        ul = div.find("ul")
        detail_lis = ul.findChildren("li", recursive=False)
        for li in detail_lis:
            header = li.select_one('div.flex-row')
            if header is None:
                continue
            title = getText(header.select_one('.t-bold > span'))
            subtitle = getText(header.select_one('.t-normal > span'))
            time = getText(header.select_one('.t-black--light > span'))

            extra_details_parent = li.select_one('div.pvs-list__container')
            extra_detail_text = None
            if extra_details_parent:
                extra_details = extra_details_parent.select('ul.pvs-list > li')
                if len(extra_details) > 1:
                    # Weird linked in nested thing
                    titles = [getText(e.select_one('.t-bold > span')) for e in extra_details]
                    times = [getText(e.select_one('.t-black--light > span')) for e in extra_details]
                    main_title = titles[0]
                    titles_texts = ','.join((t for t in titles if t))
                    time_texts = ','.join((t for t in times if t))
                    time = subtitle
                    subtitle = title
                    title = main_title
                    extra_detail_text = {
                        'titles': titles_texts,
                        'times': time_texts,
                    }
                else:
                    extra_detail_text = '\n'.join((getText(e.select_one('span')) for e in extra_details if e.select_one('span')))

            details.append({
                'title': title,
                'subtitle': subtitle,
                'time': time,
                'extra_details': extra_detail_text
            })

    return details

def getText(node):
    if node:
        return node.getText(separator=" ", strip=True)
    return None


def scrape_linkedin_profile(scraper, name, url):
    scraper.nav(url)
    if 'authwall' in scraper.driver.current_url:
        print_err("Rate limited!")
        sys.exit()
    expand_about = scraper.driver.find_elements(By.CLASS_NAME, "inline-show-more-text__button")
    for ele in expand_about:
        if "see more" in ele.text:
            ele.click()
    html = scraper.driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find("main")
    header = main.find("section")
    if header is None:
        raise LinkedInPageNotRecognized

    li_name = getText(header.find("h1"))
    current_spans = header.select("span.text-body-small.hoverable-link-text")
    pronoun_span = header.select_one("span.text-body-small.v-align-middle:not(.distance-badge)")
    location_span = header.select_one("div.mt2 > span.text-body-small")
    pronouns = getText(pronoun_span)
    location = getText(location_span)
    title = getText(header.find('div', class_="text-body-medium"))
    about = getText(main.find('div', id='about'))
    current = ','.join([getText(cs) for cs in current_spans])


    url = urljoin(scraper.driver.current_url, urlparse(scraper.driver.current_url).path)
    educations = scrape_linkedin_details(scraper, url + "/details/education", 'education', 'education')
    experiences = scrape_linkedin_details(scraper, url + "/details/experience", 'experience', 'experiences')

    return {
        "url": url,
        "li_name": li_name,
        "pronouns": pronouns,
        'title': title,
        "about": about,
        "location": location,
        'current': current,
        "experience": experiences,
        "education": educations,
        "name_match": simpleMatchScore(name, li_name)
    }

class LinkedInScraper(WebScraper):

    def __init__(self, username, password, delay=4):
        WebScraper.__init__(self, delay)

        # manual log in
        AUTH_URL = "https://www.linkedin.com/"
        self.nav(AUTH_URL)
        username_el = self.find_element(
            f"//input[@autocomplete='username']"
        )
        if username_el:
            username_el.send_keys(username)
        else:
            print_err(f"Could not autofill username: {username}")
        pw = self.find_element(
            f"//input[@autocomplete='current-password']"
        )
        if pw:
            pw.send_keys(password)
        else:
            print_err(f"Could not autofill username: {password}")
        print_err("Press enter once login is complete...")
        input("")
    
    def scrape(self, name, desc, url=None):
        if url is None:
            url = guess_linkedin_profile(self, name, desc)
        if url is None:
            raise LinkedInNotFound
        results = scrape_linkedin_profile(self, name, url)
        return results