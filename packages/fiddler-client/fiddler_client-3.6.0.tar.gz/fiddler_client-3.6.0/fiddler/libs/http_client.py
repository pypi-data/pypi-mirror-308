from __future__ import annotations

from copy import deepcopy
from typing import Any
from urllib.parse import urljoin

import requests
import simplejson
from requests.adapters import HTTPAdapter

from fiddler.constants.common import JSON_CONTENT_TYPE
from fiddler.exceptions import (  # pylint: disable=redefined-builtin
    HttpError,
)
from fiddler.libs.json_encoder import RequestClientJSONEncoder
from fiddler.utils.logger import get_logger

logger = get_logger(__name__)


class RequestClient:
    def __init__(
        self,
        base_url: str,
        headers: dict[str, str],
        verify: bool = True,
        proxies: dict | None = None,
    ) -> None:
        """Construct a request instance."""
        self.base_url = base_url
        self.proxies = proxies
        self.headers = headers
        self.headers.update({'Content-Type': JSON_CONTENT_TYPE})
        self.session = requests.Session()
        self.session.verify = verify
        adapter = HTTPAdapter(
            pool_connections=25,
            pool_maxsize=25,
        )
        self.session.mount(self.base_url, adapter)

    def call(
        self,
        *,
        method: str,
        url: str,
        params: dict | None = None,
        headers: dict | None = None,
        data: dict | bytes | None = None,
        timeout: float | tuple[float, float] | None = None,
        **kwargs: Any,
    ) -> requests.Response:
        """
        Emit HTTP request.

        :param method: HTTP method like
        :param url: API endpoint
        :param params: Query parameters
        :param headers: Request headers
        :param data: Dict/binary data
        :param timeout: Request timeout in seconds
        """
        logger.debug('next: HTTP %s %s', method, url)

        full_url = urljoin(self.base_url, url)

        request_headers = self.headers
        # override/update headers coming from the calling method
        if headers:
            request_headers = deepcopy(self.headers)
            request_headers.update(headers)

        content_type = request_headers.get('Content-Type')
        if data is not None and content_type == JSON_CONTENT_TYPE:
            data = simplejson.dumps(data, ignore_nan=True, cls=RequestClientJSONEncoder)  # type: ignore

        kwargs.setdefault('allow_redirects', True)
        # requests is not able to pass the value of self.session.verify to the
        # verify param in kwargs when REQUESTS_CA_BUNDLE is set.
        # So setting that as default here
        kwargs.setdefault('verify', self.session.verify)

        try:
            resp = self.session.request(
                method,
                full_url,
                params=params,
                data=data,
                headers=request_headers,
                timeout=timeout,
                proxies=self.proxies,
                **kwargs,
            )
        except requests.exceptions.RequestException as exc:
            # Note(JP): we did not get a response. An error happened before
            # sending the request, while sending the request, while waiting for
            # response, or while receiving the response. A few examples for
            # common errors handled here:
            # - DNS resolution error
            # - TCP connect() timeout
            # - Timeout while waiting for the other end to start sending the
            #   HTTP response (after having sent the request).
            # - RECV timeout between trying to receive two response bytes.
            #
            # TODO: add centralized default retrying here, at least for GET
            # (conservative, I understand we initially may not want to retry
            # other methods).
            #
            # For now, have centralized logging and re-raise to give callers
            # the opportunity to implement a local error handler, but not
            # having to worry about logging the full error message.
            logger.info("http: %s %s failed: %s", method, full_url, exc)
            raise

        # Raise requests.HTTPError for non-2xx responses, caller can inspect
        # response status code from the exception object via
        # e.g. exc.response.status_code.
        resp.raise_for_status()

        return resp

    def get(
        self,
        *,
        url: str,
        params: dict | None = None,
        headers: dict | None = None,
        timeout: float | tuple[float, float] | None = None,
        **kwargs: dict[str, Any],
    ) -> requests.Response:
        """Construct a get request instance."""
        return self.call(
            method='GET',
            url=url,
            params=params,
            headers=headers,
            timeout=timeout,
            **kwargs,
        )

    def delete(
        self,
        *,
        url: str,
        params: dict | None = None,
        headers: dict | None = None,
        timeout: int | None = None,
        **kwargs: dict[str, Any],
    ) -> requests.Response:
        """Construct a delete request instance."""
        return self.call(
            method='DELETE',
            url=url,
            params=params,
            headers=headers,
            timeout=timeout,
            **kwargs,
        )

    def post(
        self,
        *,
        url: str,
        params: dict | None = None,
        headers: dict | None = None,
        timeout: int | None = None,
        data: dict | bytes | None = None,
        **kwargs: dict[str, Any],
    ) -> requests.Response:
        """Construct a post request instance."""
        return self.call(
            method='POST',
            url=url,
            params=params,
            headers=headers,
            timeout=timeout,
            data=data,
            **kwargs,
        )

    def put(
        self,
        *,
        url: str,
        params: dict | None = None,
        headers: dict | None = None,
        timeout: int | None = None,
        data: dict | None = None,
        **kwargs: dict[str, Any],
    ) -> requests.Response:
        """Construct a put request instance."""
        return self.call(
            method='PUT',
            url=url,
            params=params,
            headers=headers,
            timeout=timeout,
            data=data,
            **kwargs,
        )

    def patch(
        self,
        *,
        url: str,
        params: dict | None = None,
        headers: dict | None = None,
        timeout: int | None = None,
        data: dict | None = None,
        **kwargs: dict[str, Any],
    ) -> requests.Response:
        """Construct a potch request instance."""
        return self.call(
            method='PATCH',
            url=url,
            params=params,
            headers=headers,
            timeout=timeout,
            data=data,
            **kwargs,
        )
