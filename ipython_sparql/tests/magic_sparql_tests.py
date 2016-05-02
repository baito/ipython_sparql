# -*- coding: utf-8 -*-

import unittest
from ipython_sparql.sparql import SparqlWrapperClient


class TestSparqlWrapperClient(unittest.TestCase):

    def setUp(self):
        self.sparql_client = SparqlWrapperClient()
        self.endpoint = 'http://pt.dbpedia.org/sparql'

    def test_sparql_query_ref(self):
        query = \
        '''
        PREFIX onto: <http://dbpedia.org/ontology/>
        PREFIX dbpedia: <http://pt.dbpedia.org/resource/>

        SELECT ?currency WHERE {
            dbpedia:Brasil onto:currency ?currency
        }
        '''
        ref = self.sparql_client.query(self.endpoint, query)

        self.assertIs(self.sparql_client, ref)

    def test_sparql_query_result_ask(self):
        query = \
        '''
        PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
        PREFIX dbpedia: <http://pt.dbpedia.org/resource/>

        ASK {
            dbpedia:Blumenau dbpedia-owl:populationTotal 309214 .
        }
        '''

        result = self.sparql_client.query(self.endpoint, query).results()
        #result['boolean'] = True

        expected = { "head": {"link": []}, "boolean": True}

        self.assertEquals(result, expected)

    def test_sparql_query_result_select(self):
        query = \
        '''
        PREFIX onto: <http://dbpedia.org/ontology/>
        PREFIX dbpedia: <http://pt.dbpedia.org/resource/>

        SELECT ?currency WHERE {
            dbpedia:Brasil onto:currency ?currency
        }
        '''

        expected = { "head": { "link": [], "vars": ["currency"] },
                     "results": { "distinct": False, "ordered": True,
                     "bindings":
                    [{ "currency": { "type": "uri", "value": "http://pt.dbpedia.org/resource/Real_(moeda)" }} ] } }

        result = self.sparql_client.query(self.endpoint, query).results()

        self.assertEquals(result, expected)


"""
def suite():
    suite = unittest.TestSuite()

    suite.addTest(TestSparqlWrapperClient())

    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
"""