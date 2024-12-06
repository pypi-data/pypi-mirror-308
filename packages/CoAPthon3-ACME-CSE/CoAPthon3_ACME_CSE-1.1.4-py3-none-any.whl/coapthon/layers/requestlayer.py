from __future__ import annotations
from typing import cast, TYPE_CHECKING

from coapthon.messages.response import Response
from coapthon import defines

if TYPE_CHECKING:
	from coapthon.messages.request import Request
	from coapthon.resources.resource import Resource
	from coapthon.transaction import Transaction
	from coapthon.server.coap import CoAP
	from coapthon.client.coap import CoAP as CoAPClient

__author__ = 'Giacomo Tanganelli'


class RequestLayer(object):
    """
    Class to handle the Request/Response layer
    """
    def __init__(self, server:CoAP|CoAPClient):
        self._server = server

    def receive_request(self, transaction:Transaction) -> Transaction:
        """
        Handle request and execute the requested method

        :type transaction: Transaction
        :param transaction: the transaction that owns the request
        :rtype : Transaction
        :return: the edited transaction with the response to the request
        """
        method = transaction.request.code
        if method == defines.Codes.GET.number:
            transaction = self._handle_get(transaction)
        elif method == defines.Codes.POST.number:
            transaction = self._handle_post(transaction)
        elif method == defines.Codes.PUT.number:
            transaction = self._handle_put(transaction)
        elif method == defines.Codes.DELETE.number:
            transaction = self._handle_delete(transaction)
        else:
            transaction.response = None
        return transaction

    def send_request(self, request:Request)	-> Request:
        """
         Dummy function. Used to do not broke the layered architecture.

        :type request: Request
        :param request: the request
        :return: the request unmodified
        """
        return request

    def _handle_get(self, transaction:Transaction) -> Transaction:
        """
        Handle GET requests

        :type transaction: Transaction
        :param transaction: the transaction that owns the request
        :rtype : Transaction
        :return: the edited transaction with the response to the request
        """
        wkc_resource_is_defined = defines.DISCOVERY_URL in self._server.root # type:ignore[union-attr]
        path = str("/" + transaction.request.uri_path)
        transaction.response = Response()
        transaction.response.destination = transaction.request.source
        transaction.response.token = transaction.request.token
        if path == defines.DISCOVERY_URL and not wkc_resource_is_defined:
            transaction = self._server.resourceLayer.discover(transaction) # type:ignore[union-attr]
        else:
            try:
                resource = cast(Resource, self._server.root[path]) # type:ignore[union-attr]
            except KeyError:
                resource = None
            if resource is None or path == '/':
                # Not Found
                transaction.response.code = defines.Codes.NOT_FOUND.number
            else:
                transaction.resource = resource
                transaction = self._server.resourceLayer.get_resource(transaction) # type:ignore[union-attr]
        return transaction

    def _handle_put(self, transaction:Transaction) -> Transaction:
        """
        Handle PUT requests

        :type transaction: Transaction
        :param transaction: the transaction that owns the request
        :rtype : Transaction
        :return: the edited transaction with the response to the request
        """
        path = str("/" + transaction.request.uri_path)
        transaction.response = Response()
        transaction.response.destination = transaction.request.source
        transaction.response.token = transaction.request.token
        try:
            resource = cast(Resource, self._server.root[path]) # type:ignore[union-attr]
        except KeyError:
            resource = None
        if resource is None:
            transaction.response.code = defines.Codes.NOT_FOUND.number
        else:
            transaction.resource = resource
            # Update request
            transaction = self._server.resourceLayer.update_resource(transaction) # type:ignore[union-attr]
        return transaction

    def _handle_post(self, transaction:Transaction) -> Transaction:
        """
        Handle POST requests

        :type transaction: Transaction
        :param transaction: the transaction that owns the request
        :rtype : Transaction
        :return: the edited transaction with the response to the request
        """
        path = str("/" + transaction.request.uri_path)
        transaction.response = Response()
        transaction.response.destination = transaction.request.source
        transaction.response.token = transaction.request.token

        # Create request
        transaction = self._server.resourceLayer.create_resource(path, transaction) # type:ignore[union-attr]
        return transaction

    def _handle_delete(self, transaction:Transaction) -> Transaction:
        """
        Handle DELETE requests

        :type transaction: Transaction
        :param transaction: the transaction that owns the request
        :rtype : Transaction
        :return: the edited transaction with the response to the request
        """
        path = str("/" + transaction.request.uri_path)
        transaction.response = Response()
        transaction.response.destination = transaction.request.source
        transaction.response.token = transaction.request.token
        try:
            resource = cast(Resource, self._server.root[path]) # type:ignore[union-attr]
        except KeyError:
            resource = None

        if resource is None:
            transaction.response.code = defines.Codes.NOT_FOUND.number
        else:
            # Delete
            transaction.resource = resource
            transaction = self._server.resourceLayer.delete_resource(transaction, path) # type:ignore[union-attr]
        return transaction

