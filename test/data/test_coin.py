import os.path
_here = os.path.dirname(__file__)
_herepath = lambda pth: os.path.join(_here, *pth.split('/'))

from rdflib import Graph, URIRef
from court.data.coin import URIMinter


exampledir = "../../../court/resources/examples/coin/"

test_data = [
    (
        u"http://example.org/def/coin#",
        _herepath(exampledir+"blog/urispace.n3"),
        _herepath(exampledir+"blog/data.n3"),
        [
        u'http://example.org/blogs/alice',
        u'http://example.org/blogs/alice/post/12',
        u'http://example.org/blogs/alice/post/12/comment/3']
    ),
    (
        u"http://example.org/def/urispace#",
        _herepath(exampledir+"example_1.n3"),
        None,
        [
        u"http://example.org/publ/c1/the_report",
        u"http://example.org/publ/c1/the_report/rev/2000-01-01",
        u"http://example.org/profiles/earl_ae_aangstroem#person",
        u"http://example.org/profiles/earl_ae_aangstroem"]
    ),
]

def test_minter():
    for coin_uri, space, examples, resources in test_data:
        coingraph = Graph().parse(space, format='n3')
        graph = Graph().parse(examples, format='n3') if examples else coingraph
        def do_test():
            minter = URIMinter(coingraph, URIRef(coin_uri))
            for subject in resources:
                uriref = URIRef(subject)
                results = minter.compute_uris(graph)
                uris = results.get(uriref) or []
                assert subject in uris, graph.serialize(format='n3')
        yield do_test,


