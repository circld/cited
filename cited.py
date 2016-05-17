from cgi import escape
from re import compile, finditer
from selenium import webdriver
from sys import argv


CITATION = compile(
    '[A-Z][A-Za-z-]+(,? ?&? [A-Z][A-Za-z-]*?|,? et al.)*(, \d{4}| \(\d{4}\))'
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
    d = webdriver.PhantomJS()
    d.set_window_size(1280, 1024)

    bib = set()
    for c in citations:
        encoded = escape(c).encode('ascii', 'xmlcharrefreplace')
        d.get(SCHOLAR_QUERY.format(encoded))
        bib |= get_apa_biblio_entry(d, limit)

    return bib


def get_apa_biblio_entry(driver, limit):
    """ Takes webdriver, clicks on 'Cite' for first `limit` records and
    retrieves the APA style entry for each

    :driver: selenium.webdriver object
    :limit: number (int) of Google Scholar results to return per citation
    :returns: set of citations

    """
    biblios = []
    cite = driver.find_elements_by_link_text('Cite')
    for i in xrange(limit):
        cite[i].click()
        biblios.append(driver.find_element_by_id('gs_cit1').text)
    return set(biblios)


if __name__ == '__main__':
    paper = argv[1]
    citations = find_citations(paper)
    refs = retrieve_biblio(citations, limit=1)
    refs = set(['ex1', 'ex2', 'ex3'])
    with open('{}_references.txt'.format(paper), 'w') as f:
        f.write('\n'.join(c for c in refs))
