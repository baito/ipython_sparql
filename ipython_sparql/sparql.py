# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

from IPython.core.magic import Magics, magics_class, cell_magic, line_magic
from IPython.core.display import display, display_javascript, Javascript, HTML
from SPARQLWrapper import SPARQLWrapper, JSON
from tabulate import tabulate


class SparqlClient(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def query(self, endpoint, query):
        pass

    @abstractmethod
    def results(self):
        '''

        :return: query result formated as https://www.w3.org/TR/sparql11-results-json/
        '''
        pass


class SparqlWrapperClient(SparqlClient):

    def __init__(self):
        self._results = None

    def query(self, endpoint, query):
        client = SPARQLWrapper(endpoint)

        client.setReturnFormat(JSON)
        client.setQuery(query)

        self._results = client.query()

        return self

    def results(self):
        return self._results.convert()


class SparqlResultView(object):

    __metaclass__ = ABCMeta

    def __init__(self, results):
        self._results = results

    @abstractmethod
    def view(self):
        pass


class SparqlTabularResult(SparqlResultView):

    def __init__(self, results, tabular_result):
        super(SparqlTabularResult, self).__init__(results)

        assert isinstance(tabular_result, TabularResult)

        self._tabular_result = tabular_result

    def view(self):
        tabular_data = prepare_json_to_tabular(self._results)

        if len(tabular_data) == 1:
            return self._tabular_result.create(tabular_data)

        return self._tabular_result.create(tabular_data[1:], tabular_data[0])


class TabularResult(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def create(self, headers, body, format=None):
        pass


class TabularResultTabulate(TabularResult):

    def create(self, body,  headers=None, format=None):
        assert isinstance(body, list)

        if format is None:
            format = 'html'

        if len(body) == 1:
            return tabulate([body], tablefmt=format)

        return tabulate(body, headers=headers, tablefmt=format)


@magics_class
class SparqlMagic(Magics):

    def __init__(self, shell, sparql_client):
        super(SparqlMagic, self).__init__(shell)

        self._sparql_endpoint = None
        self._last_result = None

        if sparql_client:
            self._sparql_client = sparql_client
        else:
            raise ValueError('You have to define a Sparql Client!')

    @cell_magic('sparql')
    def sparql(self, line, cell):
        results = self._query(self._sparql_endpoint, cell)

        self._last_result = results

        return self._view_results(results)

    def _view_results(self, result, format=None):
        # TODO: plain text view, python objs view ....
        tabular_result = SparqlTabularResult(result, TabularResultTabulate())

        return display(HTML(tabular_result.view()))

    def _query(self, endpoint, query):
        return self._sparql_client.query(endpoint, query).results()

    @line_magic('sparql_endpoint')
    def sparql_endpoint(self, line):
        if validate_sparql_endpoint(line):
            self._sparql_endpoint = line
        else:
            raise ValueError('Invalid Sparql Endpoint')

    @line_magic('sparql_last_result')
    def sparql_last_result(self, line):
        return self._last_result


def prepare_json_to_tabular(result):

    if 'boolean' in result:
        return [str(result['boolean'])]

    vars = result['head']['vars']
    table = []

    table.append(vars)

    for data in result['results']['bindings']:
        row = []
        for var in vars:
            d = data[var]['value']
            row.append(d)
        table.append(row)

    return table


def validate_sparql_endpoint(url):
    if url == '' or url is None:
        return False

    fragments = url.split('/')

    if fragments[-1] == '':
        if fragments[-2] == 'sparql':
            return True
        return False

    if fragments[-1] == 'sparql':
        return True

    return False


def load_ipython_extension(ipython):
    sparql_client = SparqlWrapperClient()
    ipython.register_magics(SparqlMagic(ipython, sparql_client))

    #lib_sparql_highlight = 'https://raw.githubusercontent.com/codemirror/CodeMirror/master/mode/sparql/sparql.js'
    #sparql_highlight = ("Jupyter.config.cell_magic_highlight['magic_application/sparql-query'] = {'reg': [/^%%sparql/]};")
    #js_highlight = Javascript(data=sparql_highlight, lib=[lib_sparql_highlight])

    #display_javascript(js_highlight)
    #from notebook.services.config.manager import ConfigManager

    #config = ConfigManager()

    #config.update('notebook', {'CodeCell': {'highlight_modes':{'magic_application/sparql-query': {'reg': ['/^%%sparql/']}}}})


def unload_ipython_extension(ipython):
    pass
