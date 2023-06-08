# AUTO GENERATED BASED ON Kong 3.4.x, DO NOT EDIT
# Original source path: kong/pdk/client/tls.lua

from typing import TypeVar, Any, Union, List, Mapping, Tuple, Optional

number = TypeVar('number', int, float)
table = TypeVar('table', List[Any], Mapping[str, Any])
# XXX
cdata = Any
err = str


class tls():


    @staticmethod
    def disable_session_reuse() -> Tuple[bool, err]:
        """

            Prevents the TLS session for the current connection from being reused
            by disabling the session ticket and session ID for the current TLS connection.

        Phases:
            certificate

        Example:
            res, err = kong.client.tls.disable_session_reuse()

            if not res:

                # do something with err

        :return: Returns `true` if successful, `nil` if it fails.

        :rtype: bool
        :return: Returns `nil` if successful, or an error message if it fails.

        :rtype: err
        """
        pass

    @staticmethod
    def get_full_client_certificate_chain() -> Tuple[str, err]:
        """

            Returns the PEM encoded downstream client certificate chain with the
            client certificate at the top and intermediate certificates
            (if any) at the bottom.

        Phases:
            rewrite, access, balancer, header_filter, body_filter, log

        Example:
            cert, err = kong.client.get_full_client_certificate_chain()

            if err:

                # do something with errif not cert:

                # client did not complete mTLS# do something with cert

        :return: Returns a PEM-encoded client certificate if the mTLS
            handshake was completed, or `nil` if an error occurred or the client did
            not present its certificate.

        :rtype: str
        :return: Returns `nil` if successful, or an error message if it fails.

        :rtype: err
        """
        pass

    @staticmethod
    def request_client_certificate(ca_certs: Optional[cdata]) -> Tuple[bool, err]:
        """

            Requests the client to present its client-side certificate to initiate mutual
            TLS authentication between server and client.
            This function *requests*, but does not *require* the client to start
            the mTLS process. The TLS handshake can still complete even if the client
            doesn't present a client certificate. However, in that case, it becomes a
            TLS connection instead of an mTLS connection, as there is no mutual
            authentication.
            To find out whether the client honored the request, use
            `get_full_client_certificate_chain` in later phases.
            The `ca_certs` argument is the optional CA certificate chain opaque pointer,
            which can be created by the [parse_pem_cert](https://github.com/openresty/lua-resty-core/blob/master/lib/ngx/ssl.md#parse_pem_cert)
            or [resty.opensslx509.chain](https://github.com/fffonion/lua-resty-openssl#restyopensslx509chain)
            The Distinguished Name (DN) list hints of the CA certificates will be sent to clients.
            If omitted, will not send any DN list to clients.

        Phases:
            certificate

        Example:
            x509_lib = require "resty.openssl.x509"

            chain_lib = require "resty.openssl.x509.chain"

            res, err

            chain = chain_lib.new()

            # err check

            x509, err = x509_lib.new(pem_cert, "PEM")

            # err check

            res, err = chain:add(x509)

            # err check

            # `chain.ctx` is the raw data of the chain, i.e. `STACK_OF(X509) *`

            res, err = kong.client.tls.request_client_certificate(chain.ctx)

            if not res:

                # do something with err

        :parameter ca_certs: The CA certificate chain opaque pointer
        :type ca_certs: cdata

        :return: Returns `true` if successful, or `nil` if it fails.

        :rtype: bool
        :return: Returns `nil` if successful, or an error message if it fails.

        :rtype: err
        """
        pass

    @staticmethod
    def set_client_verify() -> None:
        """

            Overrides the client's verification result generated by the log serializer.
            By default, the `request.tls.client_verify` field inside the log
            generated by Kong's log serializer is the same as the
            [$ssl_client_verify](https://nginx.org/en/docs/http/ngx_http_ssl_module.html#var_ssl_client_verify)
            Nginx variable.
            Only `"SUCCESS"`, `"NONE"`, or `"FAILED:<reason>"` are accepted values.
            This function does not return anything on success, and throws a Lua error
            in case of a failure.

        Phases:
            rewrite, access, balancer

        Example:
            kong.client.tls.set_client_verify("FAILED:unknown CA")

        """
        pass

    pass