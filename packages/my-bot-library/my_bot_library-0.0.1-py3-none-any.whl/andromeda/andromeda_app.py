import time
import json
import logger
import requests
from config import DefaultConfig
from datetime import datetime, timezone
from graphql import (
    _get_request_provider_graphql_query,
    _get_provider_account_policy,
    _get_user_origins_resource_graphql_query,
    _get_request_details_graphql_query,
    _get_requested_graphql_query,
    _get_reviewrs_details_graphql_query,
    _get_user_origins_graphql_query,
    _get_provider_account_query,
    _get_all_eligibility_query,
    _get_all_provider_query,
)


default_config_instance = DefaultConfig()


class AndromedaSecurity:
    def __init__(self):
        self.api_url = default_config_instance.API_URL
        self.graphql_url = default_config_instance.GRAPHQL_URL
        self._cookies_token = ""

    async def _get_cookie_token_api(self, api_token):
        """Async function to get the cookie token for Andromeda login.

        Args:
            api_token (str): The API token to be used for login.

        Returns:
            dict: A dictionary with keys 'err' and 'cookie', representing the
                    error message and the obtained cookie token, respectively.
        """
        logger.info("Started retrieving cookie token API.")
        cookie_data = {}

        payload = json.dumps({"code": api_token})

        try:
            start_time = time.time()
            login_response = requests.post(
                f"{self.api_url}/login/access-key",
                data=payload,
                headers={"Content-Type": "application/json"},
            )
            end_time = time.time()
            elapsed_time = end_time - start_time
            logger.info(f"Request took: {elapsed_time:.2f} seconds.")

            # Check HTTP status and handle response accordingly
            if login_response.status_code == 200:
                logger.info(
                    f"Get cookie token executed successfully with status code: {login_response.status_code}"
                )
                # Extract and clean the cookie value
                cookie_header = login_response.headers.get("Set-Cookie")
                if cookie_header:
                    cookie_data["cookie"] = cookie_header.split(";")[0]
                else:
                    cookie_data["err"] = "No Set-Cookie header found"
            else:
                # Handle errors based on status code
                if login_response.status_code == 401:
                    cookie_data["err"] = "401"
                else:
                    error_message = login_response.json().get(
                        "message", "Unknown error"
                    )
                    cookie_data["err"] = (
                        f"Error {login_response.status_code}: {error_message}"
                    )

        except requests.RequestException as e:
            cookie_data["err"] = f"Request error occurred: {str(e)}"
            logger.error(f"Request error occurred: {cookie_data['err']}")
        except Exception as e:
            cookie_data["err"] = f"An unexpected error occurred: {str(e)}"
            logger.error(f"An unexpected error occurred: {cookie_data['err']}")

        return cookie_data

    async def _get_eligibility_api(self, andro_token, andro_user_id):
        """Get the access request details from andromeda to access a request.

        Args:
            andro_user_id: andromeda user identity or slack user id

        Returns:
            results of all the access requests available for the requesting user identity id

        """
        eligibility_result = {}
        logger.info(
            f"Started getting access request REQUESTOR ANDRO USER: {andro_user_id}"
        )
        payload = json.dumps(
            {
                "query": await _get_request_provider_graphql_query(
                    user_identity_id=andro_user_id
                )
            }
        )
        eligibility_headers = await self._get_header(token=andro_token)
        if "err" not in eligibility_headers:
            try:
                access_response = requests.request(
                    "POST",
                    f"{self.graphql_url}/graphql",
                    headers=eligibility_headers.get("header"),
                    data=payload,
                )
                # access_response.raise_for_status()
                data = access_response.json()
                if access_response.status_code == 200:
                    logger.info(
                        f"Get Eligibility executed in andromeda API with:> {access_response.status_code}"
                    )
                    if "errors" not in data:
                        provider_name = []
                        account_name = []
                        scope = []
                        policy_name = []
                        reviewers = []
                        for provider in data["data"]["Identity"]["providersData"][
                            "edges"
                        ]:
                            provider_detail = {
                                "name": provider["node"]["providerName"],
                                "id": provider["node"]["providerId"],
                            }

                            if provider_detail not in provider_name:
                                provider_name.append(provider_detail)
                            accountsData = provider["node"]["accountsData"]["edges"]
                            if accountsData:
                                for account in accountsData:
                                    account_nme = account["node"]["eligiblePolicies"][
                                        "edges"
                                    ][0]["node"]["accountName"]
                                    account_id = account["node"]["eligiblePolicies"][
                                        "edges"
                                    ][0]["node"]["accountId"]
                                    account_details = {
                                        "name": account_nme,
                                        "id": account_id,
                                    }
                                    if account_details not in account_name:
                                        account_name.append(account_details)
                                    for policy in account["node"]["eligiblePolicies"][
                                        "edges"
                                    ]:
                                        policy_details = {
                                            "name": policy["node"]["policyName"],
                                            "id": policy["node"]["policyId"],
                                        }
                                        if policy_details not in policy_name:
                                            policy_name.append(policy_details)
                                        reviewers = policy["node"][
                                            "policyAccessRequestProfile"
                                        ]["policyRequestReviewers"]
                                        for resource_scope in policy["node"][
                                            "eligibleResourceGroups"
                                        ]["edges"]:
                                            if resource_scope.get("node") not in scope:
                                                scope.append(
                                                    resource_scope.get("node"))
                            else:
                                err_m = f"Sorry, you do not meet the eligibility criteria at this time"
                                logger.error(err_m)
                                eligibility_result["err"] = err_m
                                return eligibility_result
                        eligibility_result["result"] = {
                            "provider": provider_name,
                            "account": account_name,
                            "resource_scope": scope,
                            "policy": policy_name,
                            "approvers": reviewers,
                        }
                    else:
                        eligibility_result["err"] = data.get("errors")[
                            0]["message"]
                else:
                    eligibility_result["err"] = data.get("message")
                    logger.error(
                        f" Get Eligibility andro api thrown error: {eligibility_result['err']}"
                    )
                return eligibility_result
            except Exception as err:
                eligibility_result["err"] = str(err)
                logger.error(
                    f" Get Eligibility andro api thrown error: {eligibility_result['err']}"
                )
                return eligibility_result
        else:
            eligibility_result["err"] = eligibility_headers.get("err")
            return eligibility_result

    async def _create_access_request_api(
        self, origin_user_id, incoming_values, token_key
    ):
        """Create access request for andromeda security api.

        Args:
            - requestor_id : who is requesting the access request
            - incoming_values : submitted request values

        Returns:
            - request submitted response or if any error
        """
        logger.info("Started creating access request API")
        request_response = {"result": {}}
        cret_header = await self._get_header(token_key)
        if "err" not in cret_header:
            provider_id = incoming_values.get("provider_id")
            account_id = incoming_values.get("account_id")
            policy_id = incoming_values.get("policy_id")
            justification = incoming_values.get("justification")
            duration = incoming_values.get("duration")
            int_duration = int(duration) * 60
            scope_id = incoming_values.get("scope_id")
            url = f"{self.api_url}/providers/{provider_id}/accounts/{account_id}/accessrequests"
            current_time = (
                datetime.now(timezone.utc)
                .isoformat(timespec="milliseconds")
                .replace("+00:00", "Z")
            )
            payload = {
                "requesterUserId": origin_user_id,
                "type": "JIT",
                "policyId": policy_id,
                "startTime": current_time,
                "description": justification,
                "duration": str(int_duration),
            }
            if scope_id:
                payload.update(
                    {
                        "requestScope": {
                            "scopeType": "RESOURCE_GROUP",
                            "scopeId": scope_id,
                        }
                    }
                )
            else:
                payload.update(
                    {"requestScope": {"scopeType": "ACCOUNT", "scopeId": account_id}}
                )
            try:
                response = requests.request(
                    "POST",
                    url,
                    headers=cret_header.get("header"),
                    data=json.dumps(payload),
                )
                resp = response.json()
                if response.status_code == 200:
                    logger.info(
                        f"Created access request API: {response.status_code}")
                    request_response["result"]["request_id"] = resp.get("id")
                    request_response["result"]["provider_id"] = resp.get(
                        "providerId")
                    request_response["result"]["account_id"] = resp.get(
                        "accountId")
                else:
                    request_response["err"] = resp["details"][0]["message"]
                    logger.error(
                        f"Error found while creating the access request to andromeda api: {resp}"
                    )
                return request_response
            except Exception as err:
                request_response["err"] = str(err)
                logger.error(
                    f"Error found while creating the access request to andromeda api: {request_response['err']}"
                )
                return request_response

        else:
            request_response["err"] = cret_header.get("err")
            return request_response

    async def _get_origins_user_api(
        self, user_identity, provider_id, account_id, policy_id, resource_id, token_key
    ):
        """Get Andromeda user origin ID.

        Args:
            user_identity (str): Andromeda user identity.
            token_key (str): Andromeda user access key.

        Returns:
            dict: Contains 'err' for errors and 'result' with the origin user ID.
        """
        origin_results = {"result": {}}
        if resource_id:
            payload = json.dumps(
                {
                    "query": await _get_user_origins_resource_graphql_query(
                        user_identity, provider_id, account_id, policy_id, resource_id
                    )
                }
            )
        else:
            payload = json.dumps(
                {
                    "query": await _get_user_origins_graphql_query(
                        user_identity, provider_id, account_id, policy_id
                    )
                }
            )

        origin_headers = await self._get_header(token=token_key)

        if "err" in origin_headers:
            origin_results["err"] = origin_headers.get("err")
            return origin_results

        try:
            start_time = time.time()
            origin_response = requests.post(
                f"{self.graphql_url}/graphql",
                headers=origin_headers.get("header"),
                data=payload,
            )
            end_time = time.time()
            elapsed_time = end_time - start_time
            logger.info(f"Request took: {elapsed_time:.2f} seconds.")

            origin_response.raise_for_status()  # Raise an error for bad HTTP status codes
            json_response = origin_response.json()

            if "errors" in json_response:
                origin_results["err"] = json_response.get("errors")[0].get(
                    "message", "Unknown error"
                )
                logger.error(f"GraphQL errors: {origin_results['err']}")
                return origin_results

            origin_identity = json_response.get("data", {}).get("Identity", {})
            if not origin_identity:
                origin_results["err"] = "Origin identity is empty"
                logger.error(f"Origin identity is empty")
                return origin_results
            origin_users = []
            origin_results["result"]["requestor_name"] = origin_identity.get(
                "name", None
            )
            provider_edges = origin_identity.get("providersData")["edges"]
            if not provider_edges:
                origin_results["err"] = "Origin identity is empty"
                return origin_results
            for accounts in provider_edges:
                account_node = accounts["node"]["accountsData"]["edges"]
                if not account_node:
                    origin_results["err"] = "Origin identity account is empty"
                    return origin_results
                for policy in account_node:
                    policy_node = policy["node"]["eligiblePolicies"]["edges"]
                    if not policy_node:
                        origin_results["err"] = "Origin identity policy is empty"
                        return origin_results

                    for user in policy_node:
                        origin_users_data = user["node"]["eligibleUsers"]["edges"]
                        if not origin_users_data:
                            origin_results["err"] = "Origin identity user is empty"
                            return origin_results
                        for origin_node in origin_users_data:
                            origin_users_node = origin_node.get("node")
                            origin_users.append(
                                {
                                    "id": origin_users_node.get("userId"),
                                    "name": origin_users_node.get("name"),
                                }
                            )

            origin_results["result"]["origin_lst"] = origin_users

        except requests.HTTPError as e:
            origin_results["err"] = f"HTTP error occurred: {e}"
            logger.error(f"HTTP error occurred: {origin_results['err']}")
        except requests.RequestException as e:
            origin_results["err"] = f"Request error occurred: {e}"
            logger.error(f"Request error occurred: {origin_results['err']}")
        except Exception as e:
            origin_results["err"] = str(e)
            logger.error(
                f"An unexpected error occurred: {origin_results['err']}")

        return origin_results

    async def _get_request_id_summary_api(
        self, identity_id, provider_id, request_id, api_token
    ):
        """After creating access request or any other action
        [Approve or deny or cancel ] new request id will be generated
        and get the details of the request id

        Args:
            identity_id (str): Andromeda user identity id.
            provider_id (str): user was selected provider id
            request_id (str): request id for all andromeda action from teams

        Return:
            result with all details of the request id.
        """
        requested_data = {"result": {"data": {}}}
        logger.info(
            "Started retrieving the requested id to get details from Andromeda API."
        )

        request_headers = await self._get_header(api_token)
        if "err" in request_headers:
            requested_data["err"] = request_headers.get("err")
            return requested_data

        request_info = await _get_requested_graphql_query(
            identity_id, provider_id, request_id
        )

        try:
            response = requests.post(
                f"{self.graphql_url}/graphql",
                headers=request_headers.get("header"),
                data=json.dumps({"query": request_info}),
            )
            response.raise_for_status()

            request_id_details = response.json()
            logger.info(
                "Successfully retrieved the requested id details from Andromeda API."
            )

            data = (
                request_id_details.get("data", {})
                .get("Identity", {})
                .get("providersData", {})
                .get("edges", [])
            )
            if data:
                provider = data[0].get("node", {})
                requested_data["result"]["data"]["provider"] = {
                    "name": provider.get("providerName"),
                    "id": provider.get("providerId"),
                }
                access_request_edges = provider.get("accessRequestData", {}).get(
                    "edges", []
                )
                if access_request_edges:
                    for access_request in access_request_edges:
                        access_request_node = access_request.get("node", {})
                        requested_data["result"]["data"]["account"] = {
                            "name": access_request_node.get("accountName"),
                            "id": access_request_node.get("accountId"),
                        }
                        requested_data["result"]["data"]["policy"] = {
                            "name": access_request_node.get("policyName"),
                            "id": access_request_node.get("policyId"),
                        }
                        scope_data = access_request_node.get(
                            "requestScope", {})
                        requested_data["result"]["data"]["ScopeName"] = {
                            "name": scope_data.get("scopeName"),
                            "id": scope_data.get("scopeId"),
                        }
                        requested_data["result"][
                            "duration"
                        ] = f"{int(access_request_node.get('duration')) / 60} minutes"
                        requested_data["result"]["createdAt"] = access_request_node.get(
                            "createdAt"
                        )
                        requested_data["result"]["description"] = (
                            access_request_node.get("description")
                        )
                        requested_data["result"]["status"] = access_request_node.get(
                            "status", {}
                        ).get("status")
                        requested_data["result"]["requestor_name"] = (
                            access_request_node.get(
                                "requester", {}).get("name")
                        )
                        requested_data["result"]["approvers"] = access_request_node.get(
                            "reviews", []
                        )
                else:
                    requested_data["err"] = (
                        f"Found request id: {request_id} got empty access request response from Andromeda API."
                    )
            else:
                requested_data["err"] = (
                    f"Found request id: {request_id} got empty providers data from Andromeda API."
                )

        except requests.HTTPError as e:
            requested_data["err"] = str(e)
            logger.error(
                f"HTTP error occurred while retrieving the access requested details: {requested_data['err']}."
            )
        except requests.RequestException as e:
            requested_data["err"] = str(e)
            logger.error(
                f"Request error occurred while retrieving the access requested details: {requested_data['err']}."
            )
        except Exception as e:
            requested_data["err"] = str(e)
            logger.error(
                f"An error occurred while retrieving the access requested details: {requested_data['err']}."
            )

        return requested_data

    async def _end_session(self, provider_id, account_id, request_id, api_key):
        logger.info("Started ending the session for the access request in API")

        # Get the header for the request
        endsession_header = await self._get_header(api_key)
        if "err" in endsession_header:
            # If there's an error in the header, return it immediately
            return {"err": endsession_header.get("err")}

        # Prepare the URL and headers
        url = f"{self.api_url}/providers/{provider_id}/accounts/{account_id}/accessrequests/{request_id}/action"
        headers = endsession_header.get("header")
        payload = json.dumps({"action": "CLOSE"})

        try:
            # Make the PUT request
            response = requests.put(url, headers=headers, data=payload)
            response_data = response.json()

            # Return response data based on the status code
            if response.status_code == 200:
                return {"id": response_data.get("id")}
            else:
                return {"err": response_data}
        except Exception as err:
            # Return any exceptions that occur as errors
            return {"err": str(err)}

    async def _cancel_request(self, provider_id, account_id, request_id, access_key):
        """Cancel requested access.

        Args:
            provider_id (str): Access requested provider id.
            account_id (str): Requested account id.
            request_id (str): Previous request submitted request id.

        Returns:
            dict: Contains the cancelled request id or error message.
        """
        logger.info(
            f"Started cancelling the access request with Request ID: {request_id}"
        )
        cancel_response = {}

        try:
            # Get the headers for the API request
            cancel_header = await self._get_header(access_key)
            if "err" in cancel_header:
                return {"err": cancel_header.get("err")}

            # Construct the request URL and payload
            url = f"{self.api_url}/providers/{provider_id}/accounts/{account_id}/accessrequests/{request_id}/action"
            payload = json.dumps({"action": "CLOSE"})

            # Make the API request to cancel the access
            response = requests.put(
                url, headers=cancel_header.get("header"), data=payload, timeout=10
            )

            # Check for successful response
            if response.status_code == 200:
                cancel_result = response.json()
                cancel_response["request_id"] = cancel_result.get("id")
                logger.info(
                    f"Successfully cancelled access request: {cancel_response['request_id']}"
                )
            else:
                # Handle errors in response
                cancel_result = response.json()
                logger.error(
                    f"Error while cancelling the access request: {cancel_result}"
                )
                cancel_response["err"] = cancel_result.get(
                    "details", [{"message": "Unknown error"}]
                )[0]["message"]
                logger.error(
                    f"Error while cancelling the access request: {cancel_response['err']}"
                )

        except requests.RequestException as req_err:
            logger.error(
                f"Request error while cancelling access request: {str(req_err)}"
            )
            cancel_response["err"] = "Failed to connect to the API"

        except Exception as err:
            logger.error(
                f"Unexpected error while cancelling access request: {str(err)}"
            )
            cancel_response["err"] = str(err)

        return cancel_response

    async def _approve_request(self, account_id, request_id, review_id, api_token):
        """Approve the requested access.

        Args:
            account_id (str): Requested account id.
            request_id (str): Access requested submitted Request id.
            review_id (str): Reviewer id for whom it is being reviewed.

        Returns:
            dict: Contains the approved request id or error message.
        """
        logger.info(
            f"Started approving the access request for Request ID: {request_id}"
        )
        approved = {}

        try:
            # Get the headers for the API request
            approved_header = await self._get_header(api_token)
            if "err" in approved_header:
                return {"err": approved_header.get("err")}

            # Construct the request URL and payload
            url = f"{self.api_url}/accounts/{account_id}/accessrequests/{request_id}/reviews/{review_id}"
            payload = json.dumps(
                {
                    "status": "APPROVED",
                    "reason": "Requested access approved for the account",
                }
            )

            # Make the API request to approve the access
            response = requests.put(
                url, headers=approved_header.get("header"), data=payload, timeout=10
            )

            # Check for successful response
            if response.status_code == 200:
                approved_result = response.json()
                approved["approved_request_id"] = approved_result.get(
                    "accessRequestId")
                logger.info(
                    f"Successfully approved access request: {approved['approved_request_id']}"
                )
            else:
                # Handle errors in response
                approved_result = response.json()
                approved["err"] = approved_result.get(
                    "error", [{"message": "Unknown error"}]
                )[0]["message"]
                logger.error(
                    f"Error while approving the access request: {approved['err']}"
                )

        except requests.RequestException as req_err:
            logger.error(
                f"Request error while approving access request: {str(req_err)}"
            )
            approved["err"] = "Failed to connect to the API"

        except Exception as err:
            logger.error(
                f"Unexpected error while approving access request: {str(err)}")
            approved["err"] = str(err)

        return approved

    async def _get_reviewers_details(self, review_ident_id, request_id, api_token):
        """Get the reviewer details and reviewer ID with review identity id.

        Args:
            review_ident_id (str): Reviewer Identity ID for getting review id (each time review id will change).
            request_id (str): The request ID for the access request.
            api_token (str): API access token.

        Returns:
            dict: Contains the review ID or an error message if applicable.
        """
        logger.info("Started getting andromeda reviewer details")
        reviewr_err = {}

        try:
            # Get headers for the API request
            reviewr_header = await self._get_header(api_token)
            if "err" in reviewr_header:
                return {"err": reviewr_header.get("err")}

            # Prepare the GraphQL query
            review_query = await _get_reviewrs_details_graphql_query(
                review_identity_id=review_ident_id, request_id=request_id
            )

            # Make the API request
            response = requests.post(
                f"{self.graphql_url}/graphql",
                headers=reviewr_header.get("header"),
                data=json.dumps({"query": review_query}),
                timeout=10,  # Adding a timeout for better request control
            )

            # Check if the response is successful
            if response.status_code != 200:
                return {
                    "err": response.json().get("error", [{"message": "Unknown error"}])[
                        0
                    ]["message"]
                }

            reviewr_result = response.json()
            edges = reviewr_result["data"]["Identity"]["providersData"]["edges"][0][
                "node"
            ]
            review_request_edges = edges["reviewRequestData"]["edges"]

            # Process the review request edges to find the review ID
            if review_request_edges:
                for request_edge in review_request_edges:
                    request_node = request_edge["node"]
                    status = request_node["request"]["status"]["status"]
                    if status == "REVIEW_IN_PROGRESS":
                        reviewr_err["review_id"] = request_node.get("reviewId")
                        logger.info(
                            f"Found Reviewer ID: {reviewr_err['review_id']}")
                        return reviewr_err
                reviewr_err["err"] = "ReviewID not found for in-progress reviews"
            else:
                reviewr_err["err"] = "No review request data found"

        except requests.RequestException as req_err:
            logger.error(
                f"Request error while getting reviewer details: {str(req_err)}"
            )
            return {"err": "Failed to connect to the API"}

        except Exception as err:
            logger.error(f"Unexpected error: {str(err)}")
            return {"err": str(err)}

        return reviewr_err

    async def _deny_request(self, account_id, request_id, review_id, api_key):
        """Reject/Deny requested access from Teams user.

        Args:
            account_id (str): Requested account id.
            request_id (str): Access request submitted Request id.
            review_id (str): Reviewer id for the review.

        Returns:
            dict: Result containing the rejected request id or error.
        """
        logger.info("Started denying the access request in API")
        reject = {}

        try:
            reject_header = await self._get_header(api_key)
            if "err" in reject_header:
                return {"err": reject_header.get("err")}

            url = f"{self.api_url}/accounts/{account_id}/accessrequests/{request_id}/reviews/{review_id}"

            # Prepare the payload
            payload = json.dumps(
                {
                    "status": "REJECTED",
                    "reason": "Requested access REJECTED for the access account",
                }
            )

            # Send the PUT request
            response = requests.put(
                url, headers=reject_header.get("header"), data=payload, timeout=10
            )

            # Check the status code and process response
            if response.status_code == 200:
                approved_result = response.json()
                reject["deny_request_id"] = approved_result.get(
                    "accessRequestId")
            else:
                response_data = response.json()
                reject["err"] = response_data.get("error", [{}])[0].get(
                    "message", "Unknown error from Andromeda API"
                )

        except requests.RequestException as req_err:
            logger.error(
                f"Request error while denying the access request: {str(req_err)}"
            )
            reject["err"] = "Failed to deny access request due to network issue"

        except Exception as err:
            logger.error(
                f"Unexpected error while denying access request: {str(err)}")
            reject["err"] = str(err)

        return reject

    async def _get_access_request_details(self, identity_id, token_key=None):
        """Get the access requester details.

        Args:
            identity_id (str): Identity ID for the Andromeda user.
            token_key (str, optional): Token key for authentication.

        Returns:
            dict: Details of the access requests that are currently open.
        """
        logger.info("Started getting access request details")
        requestor_summary = {}

        try:
            access_request_header = await self._get_header(token_key)

            if "err" in access_request_header:
                return {"err": access_request_header.get("err")}

            # Prepare the payload for the GraphQL query
            payload = json.dumps(
                {
                    "query": await _get_request_details_graphql_query(
                        andro_user_identity_id=identity_id
                    )
                }
            )

            # Send the POST request to fetch the access request details
            response = requests.post(
                f"{self.graphql_url}/graphql",
                headers=access_request_header.get("header"),
                data=payload,
                timeout=10,  # Added timeout to avoid long-hanging requests
            )

            # Check if the request was successful
            if response.status_code != 200:
                return {
                    "err": f"Failed to fetch details, status code: {response.status_code}"
                }

            # Parse the response JSON
            summary_results = response.json()

            if "errors" in summary_results:
                return {"err": summary_results["errors"][0]["message"]}

            # Extract and process nodes
            nodes_list = []
            edges = (
                summary_results.get("data", {})
                .get("Identity", {})
                .get("providersData", {})
                .get("edges", [])
            )

            for edge in edges:
                provider_name = edge["node"]["providerName"]
                provider_id = edge["node"]["providerId"]
                access_request_data_edges = edge["node"]["accessRequestData"]["edges"]

                for request_edge in access_request_data_edges:
                    node = request_edge["node"]

                    # Collect relevant fields into a dictionary
                    extracted_data = {
                        "request_id": node.get("requestId"),
                        "providerName": provider_name,
                        "provider_id": provider_id,
                        "accountName": node.get("accountName"),
                        "account_id": node.get("accountId"),
                        "policyName": node.get("policyName"),
                        "reviewers": [
                            review.get("name") for review in node.get("reviews", [])
                        ],
                        "status": node.get("status", {}).get("status"),
                        "duration": node.get("duration"),
                        "description": node.get("description"),
                        "type": node.get("type"),
                        "createdAt": node.get("createdAt"),
                        "startTime": node.get("startTime"),
                    }
                    # Append extracted data to nodes list
                    nodes_list.append(extracted_data)

            requestor_summary["result"] = nodes_list

        except requests.RequestException as e:
            logger.error(
                f"Request error while fetching access request details: {str(e)}"
            )
            requestor_summary["err"] = "Failed to connect to access request API"

        except Exception as err:
            logger.error(f"Unexpected error: {str(err)}")
            requestor_summary["err"] = str(err)

        return requestor_summary

    async def _get_header(self, token):
        """Get the header with cookie auth."""
        header_property = {}
        if not token:
            logger.error("Andromeda API key is not found or expired")
            header_property["err"] = "Andromeda API key is not found"
            return header_property
        cookie_key = await self._get_cookie_token_api(api_token=token)
        if "err" not in cookie_key.keys():
            logger.info("Returning header and cookie token")
            header_property["header"] = {
                "Content-Type": "application/json",
                "Cookie": cookie_key.get("cookie"),
            }
        else:
            header_property["err"] = cookie_key.get("err")
        return header_property

    async def _get_provider_api(self, andro_token, andro_user_id):
        """Get the access request details from Andromeda for a specific user.

        Args:
            andro_user_id: Andromeda user identity or Teams user ID

        Returns:
            Results of all access requests available for the requesting user identity ID.
        """
        provider_result = {}
        logger.info(f"Started getting provider ANDRO USER: {andro_user_id}")

        try:
            payload = json.dumps(
                {"query": await _get_all_provider_query(identity_uuid=andro_user_id)}
            )
            provider_headers = await self._get_header(token=andro_token)

            if "err" in provider_headers:
                return {"err": provider_headers.get("err")}

            response = requests.post(
                f"{self.graphql_url}/graphql",
                headers=provider_headers.get("header"),
                data=payload,
                timeout=10,  # Adding a timeout to avoid hanging
            )

            if response.status_code != 200:
                return {"err": response.json().get("message", "Unknown error occurred")}

            provider_data = response.json()

            if "errors" in provider_data:
                return {"err": provider_data["errors"][0]["message"]}
            providers_lst = (
                provider_data.get("data", {})
                .get("Identity", {})
                .get("providersData", {})
                .get("edges", [])
            )

            if not providers_lst:
                return {"err": "User does not have eligibility to select"}

            providers = [
                {"name": edge["node"]["providerName"],
                    "id": edge["node"]["providerId"]}
                for edge in providers_lst
            ]

            provider_result["result"] = providers

        except requests.RequestException as e:
            logger.error(f"Error in provider API request: {str(e)}")
            return {"err": "Failed to connect to provider API"}

        except Exception as err:
            logger.error(f"Unexpected error: {str(err)}")
            return {"err": str(err)}

        return provider_result

    async def _get_provider_account_api(self, provider_id, andro_token, andro_user_id):
        """Get the access request details from Andromeda for a specific provider.

        Args:
            andro_user_id: Andromeda user identity or Teams user ID

        Returns:
            Results of all access requests available for the requesting user identity ID.
        """
        provider_acc_result = {}
        multiple_accounts = []
        logger.info(f"Started getting provider ANDRO USER: {andro_user_id}")

        try:
            payload = json.dumps(
                {
                    "query": await _get_provider_account_query(
                        provider_uuid=provider_id, identity_uuid=andro_user_id
                    )
                }
            )
            provider_acc_headers = await self._get_header(token=andro_token)

            if "err" in provider_acc_headers:
                return {"err": provider_acc_headers.get("err")}

            response = requests.post(
                f"{self.graphql_url}/graphql",
                headers=provider_acc_headers.get("header"),
                data=payload,
                timeout=10,  # Adding a timeout to avoid hanging
            )

            if response.status_code != 200:
                return {"err": response.json().get("message", "Unknown error occurred")}

            provider_acc_data = response.json()

            if "errors" in provider_acc_data:
                return {"err": provider_acc_data["errors"][0]["message"]}

            # Extract provider details
            provider_edges = (
                provider_acc_data.get("data", {})
                .get("Identity", {})
                .get("providersData", {})
                .get("edges", [])
            )

            if not provider_edges:
                return {"err": "No provider data available"}

            # Process provider and accounts data
            for provider_node in provider_edges:
                provider_name = provider_node["node"]["providerName"]
                provider_id = provider_node["node"]["providerId"]
                provider_acc_result["result"] = {
                    "provider_name": provider_name,
                    "id": provider_id,
                }
                account_data = provider_node["node"]["accountsData"]["edges"]
                if account_data:
                    for account_node in account_data:
                        multiple_accounts.append(account_node["node"])
                else:
                    return {"err": "Failed to connect to provider account API"}

            provider_acc_result["result"]["accounts"] = multiple_accounts

        except requests.RequestException as e:
            logger.error(f"Error in provider account API request: {str(e)}")
            return {"err": "Failed to connect to provider account API"}

        except Exception as err:
            logger.error(f"Unexpected error: {str(err)}")
            return {"err": str(err)}

        return provider_acc_result

    async def _get_provider_account_policy_api(
        self, provider_id, account_id, andro_user_id, andro_token
    ):
        """Get the access request details from Andromeda for a specific provider account and its policies.

        Args:
            andro_user_id: Andromeda user identity.
            provider_id: User-selected provider ID.
            account_id: User-selected account ID.
            andro_token: Andromeda access token.

        Returns:
            Results of all access requests available for the requesting user identity ID.
        """
        pder_acc_plcy_result = {}
        multiple_policy = []
        logger.info(f"Started getting provider ANDRO USER: {andro_user_id}")

        try:
            payload = json.dumps(
                {
                    "query": await _get_provider_account_policy(
                        identity_uuid=andro_user_id,
                        provider_uuid=provider_id,
                        account_uuid=account_id,
                    )
                }
            )
            provider_acc_headers = await self._get_header(token=andro_token)

            if "err" in provider_acc_headers:
                return {"err": provider_acc_headers.get("err")}

            response = requests.post(
                f"{self.graphql_url}/graphql",
                headers=provider_acc_headers.get("header"),
                data=payload,
                timeout=10,  # Adding a timeout to prevent indefinite hanging
            )

            if response.status_code != 200:
                return {"err": response.json().get("message", "Unknown error occurred")}

            provider_acc_data = response.json()

            if "errors" in provider_acc_data:
                return {"err": provider_acc_data["errors"][0]["message"]}

            # Process the provider, account, and policy details
            provider_edges = (
                provider_acc_data.get("data", {})
                .get("Identity", {})
                .get("providersData", {})
                .get("edges", [])
            )

            if not provider_edges:
                return {"err": "No provider data available"}

            for provider_node in provider_edges:
                provider_name = provider_node["node"]["providerName"]
                provider_id = provider_node["node"]["providerId"]

                account_edges = provider_node["node"]["accountsData"]["edges"]
                if not account_edges:
                    return {"err": "No account data available"}

                for account_node in account_edges:
                    account_name = account_node["node"]["accountName"]
                    account_id = account_node["node"]["accountId"]

                    pder_acc_plcy_result["result"] = {
                        "provider_name": provider_name,
                        "provider_id": provider_id,
                        "account": {
                            "account_name": account_name,
                            "account_id": account_id,
                        },
                    }
                    policy_edges = account_node["node"]["eligiblePolicies"]["edges"]
                    if not policy_edges:
                        return {"err": "No policy data available"}
                    for policy_node in policy_edges:
                        multiple_policy.append(
                            {
                                "policy_name": policy_node["node"]["policyName"],
                                "policy_id": policy_node["node"]["policyId"],
                            }
                        )

            pder_acc_plcy_result["result"]["policy"] = multiple_policy

        except requests.RequestException as e:
            logger.error(
                f"Error in provider account policy API request: {str(e)}")
            return {"err": "Failed to connect to provider account policy API"}

        except Exception as err:
            logger.error(f"Unexpected error: {str(err)}")
            return {"err": str(err)}
        return pder_acc_plcy_result

    async def _get_all_eligibility_api(
        self, andro_token, user_id_uuid, provider_id, account_id, policy_id
    ):
        """Get access request details from Andromeda for a specific 
        provider, account, and policy.

        Args:
            andro_token: Andromeda API Access token.
            user_id_uuid: Andromeda user identity or Teams user ID.
            provider_id: User-selected provider ID.
            account_id: User-selected account ID.
            policy_id: User-selected policy ID.

        Returns:
            Results of all the access requests available for the requesting user identity ID.
        """
        eligibility_result = {}
        logger.info(
            f"Started getting all access requests for ANDRO USER: {user_id_uuid}"
        )

        try:
            # Prepare the payload and headers
            payload = json.dumps(
                {
                    "query": await _get_all_eligibility_query(
                        identity_id=user_id_uuid,
                        provider_id=provider_id,
                        account_id=account_id,
                        policy_id=policy_id,
                    )
                }
            )
            eligibility_headers = await self._get_header(token=andro_token)

            if "err" in eligibility_headers:
                return {"err": eligibility_headers.get("err")}

            # Send the POST request
            response = requests.post(
                f"{self.graphql_url}/graphql",
                headers=eligibility_headers.get("header"),
                data=payload,
                timeout=10,  # Adding a timeout to prevent hanging
            )

            # Handle non-200 status codes
            if response.status_code != 200:
                return {"err": response.json().get("message", "Unknown error occurred")}

            # Parse the response data
            data = response.json()

            if "errors" in data:
                return {"err": data["errors"][0]["message"]}

            # Process the provider, account, policy, reviewer, and resource details
            provider_edges = (
                data.get("data", {})
                .get("Identity", {})
                .get("providersData", {})
                .get("edges", [])
            )

            if not provider_edges:
                return {"err": "No provider data available"}

            provider, multiple_accounts, multiple_policy, reviewers, resources = (
                [],
                [],
                [],
                [],
                [],
            )

            for provider_node in provider_edges:
                provider.append(
                    {
                        "provider_name": provider_node["node"]["providerName"],
                        "provider_id": provider_node["node"]["providerId"],
                    }
                )

                for account_node in provider_node["node"]["accountsData"]["edges"]:
                    multiple_accounts.append(
                        {
                            "account_name": account_node["node"]["accountName"],
                            "account_id": account_node["node"]["accountId"],
                        }
                    )

                    for policy_node in account_node["node"]["eligiblePolicies"][
                        "edges"
                    ]:
                        multiple_policy.append(
                            {
                                "policy_name": policy_node["node"]["policyName"],
                                "policy_id": policy_node["node"]["policyId"],
                            }
                        )

                        reviewers.append(
                            {
                                "reviewers": policy_node["node"][
                                    "policyAccessRequestProfile"
                                ]["policyRequestReviewers"]
                            }
                        )

                        for scope_type in policy_node["node"]["eligibilityConstraints"]:
                            if scope_type.get("scopeType") == "RESOURCE_GROUP":
                                for resource_node in policy_node["node"][
                                    "eligibleResourceGroups"
                                ]["edges"]:
                                    resources.append(
                                        {
                                            "resource_name": resource_node["node"][
                                                "name"
                                            ],
                                            "resource_id": resource_node["node"]["id"],
                                        }
                                    )

            eligibility_result["result"] = {
                "provider": provider,
                "account": multiple_accounts,
                "policy": multiple_policy,
                "approvers": reviewers,
                "resource": resources,
            }

        except requests.RequestException as e:
            logger.error(f"Error in eligibility API request: {str(e)}")
            return {"err": "Failed to connect to eligibility API"}

        except Exception as err:
            logger.error(f"Unexpected error: {str(err)}")
            return {"err": str(err)}

        return eligibility_result
