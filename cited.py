from os.path import basename, splitext
from re import compile, finditer
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from sys import argv


CITATION = compile(
    '([A-Za-z]+ ){0,2}[A-Z][A-Za-z-]+(,?( &| and)? '
    '([A-Za-z]+ ){0,2}[A-Z][A-Za-z-]*?|,? et al.)*'
    '(,? \d{4}[a-z]?| \(\d{4}[a-z]?\))'
)
SCHOLAR_QUERY = 'https://scholar.google.com/scholar?hl=en&as_sdt=0,6&q={}'


def find_citations(filename):
    """ Searches the plaintext file for citation patterns

    :filename: file location (string).
    :returns: set of citations

    """
    with open(filename, 'r') as f:
        raw_text = f.readlines()

    text = ' '.join(raw_text)
    m = finditer(CITATION, text)
    return set(s.replace('e.g., ', '').replace('see ', '').strip()
               for c in m for s in c.group().split(';'))


def retrieve_biblio(citations, limit=3):
    """ Retrieve bibliographic information from Google Schola

    :citations: iterable of citations
    :limit: number (int) of Google Scholar results to return per citation
    :returns: set of bibliographic entries (string)

    """
    d = webdriver.PhantomJS(executable_path='/Users/pgaraud/cited/phantomjs')
    d.set_window_size(1280, 1024)
    d.implicitly_wait(3)

    bib = set()
    for c in citations:

        # entering terms directly via search bar
        d.get('https://scholar.google.com')
        search = d.find_element_by_id('gs_hp_tsi')
        search.send_keys(c)
        search.send_keys(Keys.ENTER)
        bib |= get_apa_biblio_entry(d, limit)

    return bib


def get_apa_biblio_entry(driver, limit):
    """ Takes webdriver, clicks on 'Cite' for first `limit` records and
    retrieves the APA style entry for each

    :driver: selenium.webdriver object
    :limit: number (int) of Google Scholar results to return per citation
    :returns: set of citations

    """
    if 'robot' in driver.page_source.lower():
        raise AttributeError('Google Scholar requiring ReCaptcha.')

    biblios = []
    cite = driver.find_elements_by_link_text('Cite')
    for i in xrange(limit):
        cite[i].click()
        biblios.append(driver.find_element_by_id('gs_cit1').text)
    return set(biblios)


if __name__ == '__main__':
    paper = argv[1]
    paper_name, _ = splitext(basename(paper))

    # extract citations
    citations = find_citations(paper)
    with open('{}_citations.txt'.format(paper_name), 'w') as f:
        f.write('\n'.join(c for c in sorted(citations)))

    # look up APA bibliographical entry
    # refs = retrieve_biblio(citations, limit=1)
    # with open('{}_references.txt'.format(paper_name), 'w') as f:
    #     f.write('\n'.join(r.encode('ascii', 'ignore') for r in refs))
