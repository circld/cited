from unittest import main, TestCase
from cited.cited import *
from re import search


FAIL_MSG = "Not Implemented Yet."


class TestCitationPatterns(TestCase):

    """ Test different citation patterns to match using regex """

    def test_single_author(self):
        """ Lastname, YYYY """
        text = 'Blah blah blah (e.g., Hankin, 2002), blah blah blah'
        found = search(CITATION, text).group()
        self.assertEquals(found, 'Hankin, 2002')

    def test_double_authors(self):
        """ Lastname & Lastname, YYYY """
        text = 'Blah blah blah (see Hankin & Abella, 2002), blah blah blah'
        found = search(CITATION, text).group()
        self.assertEquals(found, 'Hankin & Abella, 2002')

    def test_triple_authors(self):
        """ Lastname, Lastname & Lastname, YYYY """
        text = 'Blah blah blah (see Hankin, Bum & Abella, 2002), blah blah blah'
        found = search(CITATION, text).group()
        self.assertEquals(found, 'Hankin, Bum & Abella, 2002')

    def test_multiple_authors(self):
        """ Lastname et. al, YYYY """
        text = 'Blah blah blah (see Hankin et al., 2002), blah blah blah'
        found = search(CITATION, text).group()
        self.assertEquals(found, 'Hankin et al., 2002')

    def test_list_of_pubs(self):
        """ e.g., lastname, YYYY; lastname et. al, YYYY; ... """
        text = 'Blah blah blah (see Hankin et al., 2002; Bob, Bob & Bob, 2016)'
        found = search(CITATION, text).group()
        self.assertEquals(found,
                          'Hankin et al., 2002')

class TestCitationRetrieval(TestCase):

    def setUp(self):
        self.citations = set([
            'Beck, 1976',
            'Beck & Haigh, 2014',
            'Beck, 1976',
            'Abramson et al., 1989',
            'Blatt & Luyten, 2000',
            'Blatt & Zuroff, 1992',
            'Nolen-Hoeksema et al., 2008',
            'Abela & Hankin, 2008',
            'Gibb & Coles, 2005',
            'Riskind & Alloy, 2006',
            'Hankin, et al., 2016',
            'Hankin, Snyder, et al., 2016',
            'Nolen-Hoeksema & Watkins, 2011',
            'Hankin, et al., 2016',
            'Hong & Cheung, 2014',
            'Alloy, Abramson, Metalsky, & Hartlage, 1988',
            'Hankin et al., 2007',
            'Alloy et al., 2000',
            'Hankin et al., 2007',
            'Hankin et al., 2007',
            'Joiner & Rudd, 1996',
            'Gotlib, Lewinsohn, Seeley, & Rhode, 1991',
            'Reno & Halaris, 1989',
            'Hankin et al., 2007',
            'Possel & Knopf, 2011',
            'Hong & Cheung, 2014',
            'Gotlib, Lewinsohn, Seeley, Rhode & Redner, 1993',
            'Garber, Weiss, & Shanley, 1993',
            'Adams et al. (2007)',
            'Hankin et al., 2007',
            'Possel & Knopf, 2011'
        ])

    def test_find_citations(self):
        self.assertSetEqual(find_citations('test_doc.txt'), self.citations)

    def test_apa_biblio_entry(self):
        d = webdriver.PhantomJS()
        d.set_window_size(1280, 1024)
        d.get(
            'https://scholar.google.com/scholar?hl=en&as_sdt=0,6&q=nolen-hoeksema+2000'
        )
        biblio = get_apa_biblio_entry(d, 1)

        expected = ' '.join([
            'Nolen-Hoeksema, S. (2000).',
            'The role of rumination in depressive disorders and',
            'mixed anxiety/depressive symptoms.',
            'Journal of abnormal psychology, 109(3), 504.'
        ])
        try:
            self.assertEquals(biblio.pop(), expected)
        finally:
            d.quit()

    # TODO: get this test passing
    def test_retrieve_biblio(self):
        two_citations = set([c for i, c in enumerate(self.citations) if i < 2])
        biblio = retrieve_biblio(two_citations, 1)
        self.assertSetEqual(biblio, set(['stuff', 'stuff2']))


if __name__ == '__main__':
    main()
