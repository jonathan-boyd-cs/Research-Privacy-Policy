'''
    Webscrapper -> Collecting websites for research study from ahref.com
    Using : playwright (sync)

'''

from playwright.sync_api import sync_playwright

target_site = "https://ahrefs.com/websites/"
with sync_playwright() as playwright:
    # Launch a browser
    browser = playwright.chromium.launch(headless=False)
    # Create a new page/tab
    page = browser.new_page()
    page.set_default_timeout(20000)
   
    page.goto(url=target_site)
    
    industry_btn =  page.locator(
        "button.css-ygijhp.css-x4dmss.css-c5keqc.css-1nns36c.css-115l1wb").\
                    nth(1)
    industry_btn.click()
    
    industries = page.locator("div.css-1mp21er-selectItem")
    top_trending_websites =  "section.css-1x5msv2-section.css-pho8nb-sectionColor.css-0.css-19v4hey.css-huer0q.css-19msw4o"
    website_links = "a.css-1eydlj5"
    
    industry_list = []
    #done = ["All categories","Beauty and Fitness","Books and Literature","Business",
    #        "Computers and Electronics","Entertainment","Finance"]
    for industry in industries.all():
        indust = industry.text_content().strip("\n")
        if indust != "Food and Drink": continue
        
        industry_list.append(indust)

    with open("website-scrape.txt",'a') as f:
        
        for industry in industry_list:
            f.write("* {}\n".format(industry.upper()))
            try:
                i_btn = industries.filter(
                    has_text=industry
                )
                i_btn.click()
                 
                link_segment = page.locator(top_trending_websites).\
                    locator(website_links) 
                
                return_page = str(page.url)
                
                for link in link_segment.all():
                    url = "+ https://" + link.text_content().strip("\n")
                    f.write(url + "\n")
                    link.click()
                    try:
                        traffic_count =  page.locator("div.css-hx0iv3").nth(0).locator("span") # 2
                        traffic_value =  page.locator("div.css-rxkbvu").nth(0).locator("span") # 1
                        domain_rating = page.locator("div.css-hx0iv3").nth(2).locator("span") # 1
                        linking =  page.locator("div.css-rxkbvu").nth(0).locator("span") # 1
                        
                        val = None
                        sym = None
                        # traffic count
                        i = 0
                        for item in traffic_count.all():
                            if i >= 2: continue
                            if i == 0 :
                                val = item.text_content()
                            if i == 1:
                                sym = item.text_content()
                            i += 1
                        
                        f.write("- traffic-count_{}_{}\n".format(val,sym))
                    
                        # traffic value
                        val = None
                        i = 0
                        for item in traffic_value.all():
                            if i >= 1: continue
                            if i == 0 :
                                val = item.text_content()
                            i += 1
                        f.write("- traffic-value_{}\n".format(val))
                        
                        # domain rating
                        i = 0
                        for item in domain_rating.all():
                            if i >= 1: continue
                            if i == 0 :
                                val = item.text_content()
                            i += 1
                        f.write("- domain-rating_{}\n".format(val))
                    
                        # linking webstes
                        i = 0
                        for item in linking.all():
                            if i >= 1: continue
                            if i == 0 :
                                val = item.text_content()
                            i += 1
                        f.write("- (linking-websites)_{}\n".format(val))
                    except:
                        print("FAIL")
                        pass
                    
                    # return to industry page
                    page.goto(return_page)
                    
                industry_btn.click()
                
            except:
                print("FAIL")
                f.write("~")
    
    # Close browser
    browser.close()
    
