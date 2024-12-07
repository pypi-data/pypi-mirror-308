async def _get_request_provider_graphql_query(self, user_identity_id):
    return f"""
    query Identity {{
    Identity(id: "{user_identity_id}") {{
        providersData {{
            edges {{
                node {{
                    providerId
                    providerName
                    accountsData{{
                        edges {{
                            node {{
                                eligiblePolicies {{
                                    edges {{
                                        node {{
                                            policyId
                                            policyName
                                            policyType
                                            accountId
                                            accountName
                                            blastRisk
                                            policyAccessRequestProfile {{
                                                policyRequestReviewers
                                                requestValidationConfig {{
                                                    minDuration
                                                    maxDuration
                                                }}
                                            }}
                                            eligibleResourceGroups {{
                                                edges {{
                                                    node {{
                                                        id
                                                        name
                                                    }}
                                                }}
                                            }}
                                        }}
                                    }}
                                }}
                            }}
                        }}
                    }}
                }}
            }}
        }}
    }}
}}
"""


async def _get_requested_graphql_query(self, identity_id, provider_id, request_id):
    return f"""
        query Identity {{
            Identity(id: "{identity_id}") {{
                providersData(
                    filters: {{ id: {{ equals: "{provider_id}" }} }}
                ) {{
                    edges {{
                        node {{
                            providerId
                            providerName
                            accessRequestData(
                                filters: {{ requestId: {{ equals: "{request_id}" }} }}
                            ) {{
                                edges {{
                                    node {{
                                        requestId
                                        policyName
                                        policyId
                                        policyType
                                        accountId
                                        accountName
                                        startTime
                                        updatedAt
                                        createdAt
                                        duration
                                        tags
                                        description
                                        type
                                        status {{
                                            status
                                        }}
                                        requester {{
                                            name
                                        }}
                                        reviews {{
                                            name
                                            reviewerId
                                            status
                                        }}
                                        requestScope {{
                                            scopeId
                                            scopeName
                                        }}
                                    }}
                                }}
                            }}
                        }}
                    }}
                }}
            }}
        }}
    """


async def _get_reviewrs_details_graphql_query(self, review_identity_id, request_id):
    return f"""
        query Identity {{
            Identity(id: "{review_identity_id}") {{
                providersData {{
                    edges {{
                        node {{
                            providerId
                            providerName
                            reviewRequestData (filters: {{
                                requestId: {{
                                equals: "{request_id}"
                                }} 
                                }}){{
                                edges {{
                                    node {{
                                        reviewId
                                        status
                                        reason
                                        updatedAt
                                        request {{
                                            requestId
                                            policyId
                                            policyName
                                            policyType
                                            accountId
                                            accountName
                                            startTime
                                            updatedAt
                                            createdAt
                                            duration
                                            tags
                                            description
                                            type
                                            requester {{
                                                name
                                            }}
                                            status {{
                                                status
                                            }}
                                            requestAnalysis {{
                                                checks {{
                                                    category
                                                    status
                                                }}
                                            }}
                                        }}
                                    }}
                                }}
                            }}
                        }}
                    }}
                }}
            }}
        }}
        """


async def _get_user_origins_resource_graphql_query(
    self, identity_id, provider_id, account_id, policy_id, resource_group_id
):
    return f"""
query Identity {{
    Identity(id: "{identity_id}") {{
        id
        name
        username
        state
        type
        providersData(
            filters: {{ id: {{ equals: "{provider_id}" }} }}
        ) {{
            edges {{
                node {{
                    providerId
                    providerName
                    type
                    accountsData(
                        filters: {{ id: {{ equals: "{account_id}" }} }}
                    ) {{
                        edges {{
                            node {{
                                accountId
                                accountName
                                eligiblePolicies(
                                    filters: {{ policyId: {{ equals: "{policy_id}" }} }}
                                ) {{
                                    edges {{
                                        node {{
                                            policyId
                                            policyName
                                            policyType
                                            eligibleUsers(filters: {{ eligibleResourceGroupId: {{ equals: "{resource_group_id}" }} }}) {{
                                                edges {{
                                                    node {{
                                                        userId
                                                        name
                                                        username
                                                        identityOriginType
                                                    }}
                                                }}
                                            }}
                                        }}
                                    }}
                                }}
                            }}
                        }}
                    }}
                }}
            }}
            
        }}
    }}
}}
"""


async def _get_user_origins_graphql_query(
    self, identity_id, provider_id, account_id, policy_id
):
    return f"""
query Identity {{
    Identity(id: "{identity_id}") {{
        id
        name
        username
        state
        type
        providersData(
            filters: {{ id: {{ equals: "{provider_id}" }} }}
        ) {{
            edges {{
                node {{
                    providerId
                    providerName
                    type
                    accountsData(
                        filters: {{ id: {{ equals: "{account_id}" }} }}
                    ) {{
                        edges {{
                            node {{
                                accountId
                                accountName
                                eligiblePolicies(
                                    filters: {{ policyId: {{ equals: "{policy_id}" }} }}
                                ) {{
                                    edges {{
                                        node {{
                                            policyId
                                            policyName
                                            policyType
                                            eligibleUsers {{
                                                edges {{
                                                    node {{
                                                        userId
                                                        name
                                                        username
                                                        identityOriginType
                                                    }}
                                                }}
                                            }}
                                        }}
                                    }}
                                }}
                            }}
                        }}
                    }}
                }}
            }}
        }}
    }}
}}
"""


async def _get_all_provider_query(self, identity_uuid):
    return f"""query Identity {{
                Identity(id: "{identity_uuid}") {{
                    id
                    name
                    username
                    providersData {{
                        edges {{
                            node {{
                                providerName
                                type
                                providerId
                            }}
                        }}
                    }}
                }}
            }}
"""


async def _get_provider_account_query(self, identity_uuid, provider_uuid):
    return f"""
query Identity {{
    Identity(id: "{identity_uuid}") {{
        id
        name
        username
        providersData(
            filters: {{ id: {{ equals: "{provider_uuid}" }} }}
        ) {{
            edges {{
                node {{
                    providerName
                    type
                    providerId
                    accountsData {{
                        edges {{
                            node {{
                                accountId
                                accountName
                            }}
                        }}
                    }}
                }}
            }}
        }}
    }}
}}
"""


async def _get_provider_account_policy(
    self, identity_uuid, provider_uuid, account_uuid
):
    return f"""
    query Identity {{
        Identity(id: "{identity_uuid}") {{
            id
            name
            username
            providersData(
                filters: {{ id: {{ equals: "{provider_uuid}" }} }}
            ) {{
                edges {{
                    node {{
                        providerName
                        type
                        providerId
                        accountsData(
                            filters: {{ id: {{ equals: "{account_uuid}" }} }}
                        ) {{
                            edges {{
                                node {{
                                    accountId
                                    accountName
                                    eligiblePolicies {{
                                        edges {{
                                            node {{
                                                policyId
                                                policyName
                                                eligibleResourceGroups {{
                                                    edges {{
                                                        node {{
                                                            id
                                                            name
                                                        }}
                                                    }}
                                                }}
                                                policyAccessRequestProfile {{
                                                    requestValidationConfig {{
                                                        minDuration
                                                        maxDuration
                                                    }}
                                                    policyRequestReviewers
                                                }}
                                            }}
                                        }}
                                    }}
                                }}
                            }}
                        }}
                    }}
                }}
            }}
        }}
    }}
"""


async def _get_all_eligibility_query(
    self, identity_id, provider_id, account_id, policy_id
):
    return f"""
query Identity {{
    Identity(id: "{identity_id}") {{
        id
        name
        username
        providersData(
            filters: {{ id: {{ equals: "{provider_id}" }} }}
        ) {{
            edges {{
                node {{
                    providerName
                    type
                    providerId
                    accountsData(
                        filters: {{ id: {{ equals: "{account_id}" }} }}
                    ) {{
                        edges {{
                            node {{
                                accountId
                                accountName
                                eligiblePolicies(
                                    filters: {{ policyId: {{ equals: "{policy_id}" }} }}
                                ) {{
                                    edges {{
                                        node {{
                                            policyId
                                            policyName
                                            policyType
                                            eligibleResourceGroups {{
                                                edges {{
                                                    node {{
                                                        id
                                                        name
                                                    }}
                                                }}
                                            }}
                                            policyAccessRequestProfile {{
                                                requestValidationConfig {{
                                                    minDuration
                                                    maxDuration
                                                }}
                                                policyRequestReviewers
                                            }}
                                        }}
                                    }}
                                }}
                            }}
                        }}
                    }}
                }}
            }}
        }}
    }}
}}
"""


async def _get_request_details_graphql_query(self, andro_user_identity_id):
    return f"""
query Identity {{
    Identity(id: "{andro_user_identity_id}") {{
        providersData {{
            edges {{
                node {{
                    providerId
                    providerName
                    accessRequestData(filters: {{ status: {{ equals: "PROVISIONED" }} }}) {{
                        edges {{
                            node {{
                                requestId
                                policyId
                                policyName
                                policyType
                                accountId
                                accountName
                                startTime
                                updatedAt
                                createdAt
                                duration
                                tags
                                description
                                type
                                accountMode
                                reviews {{
                                    status
                                    reason
                                    reviewerId
                                    name
                                }}
                                status {{
                                    status
                                    reason
                                }}
                            }}
                        }}
                    }}
                }}
            }}
        }}
    }}
}}
"""
