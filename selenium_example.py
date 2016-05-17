from selenium import webdriver

# set up
d = webdriver.PhantomJS()
d.set_window_size(1280, 1024)

# navigate
d.get(
    'https://scholar.google.com/scholar?hl=en&as_sdt=0,6&q=nolen-hoeksema+2000'
)

# find cite buttons
cite_buttons = d.find_elements_by_link_text('Cite')
cite_buttons[0].click()
# add wait

# find APA row
apa = d.find_elements_by_id('gs_cit1')
print apa[0].text

d.quit()
