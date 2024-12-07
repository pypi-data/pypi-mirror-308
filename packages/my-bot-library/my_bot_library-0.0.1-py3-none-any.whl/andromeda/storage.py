"""
This code defines a `Storage` class for storing conversation IDs and associated activity IDs.

Improvements:

- Clear comments explain the purpose and functionality.
- Uses a dictionary structure for `request_data` to handle nested data.
- Handles potential data type inconsistencies gracefully using `get` methods.
- Added checks for invalid input types to prevent runtime errors.

**Type hints are optional but recommended for better readability and static type checking.**
"""


class Storage:
    def __init__(self):
        """
        Initializes an empty dictionary to store request and activity IDs.
        """
        # self.request_data = {}  # Nested dictionary for request-specific activity IDs
        # self.data = {}
        # Nested dictionary for request-specific activity IDs
        self.request_data: dict[str, dict[str, str]] = {}
        self.data: dict[str, str] = {}  # Dictionary for general activity IDs

    def store_rqst_ts(self, user_id: str, request_id: str, ts: str, channel_id) -> None:
        """
        Stores the activity ID associated with a conversation and request ID.

        Args:
            user_id (str): The unique conversation ID.
            request_id (str): The unique request ID within the conversation.
            ts (str): The activity ID to be stored.

        Raises:
            TypeError: If any of the input arguments are not strings.
        """

        # Validate input types to prevent potential errors
        if (
            not isinstance(user_id, str)
            or not isinstance(request_id, str)
            or not isinstance(ts, str)
        ):
            raise TypeError("All arguments must be strings.")

        self.request_data.setdefault(user_id, {})[request_id] = {
            "ts": ts,
            "channel_id": channel_id,
        }

    def store_rqst_activity_id(
        self, conversation_id: str, request_id: str, activity_id: str
    ) -> None:
        """
        Stores the activity ID associated with a conversation and request ID.

        Args:
            conversation_id (str): The unique conversation ID.
            request_id (str): The unique request ID within the conversation.
            activity_id (str): The activity ID to be stored.

        Raises:
            TypeError: If any of the input arguments are not strings.
        """

        # Validate input types to prevent potential errors
        if (
            not isinstance(conversation_id, str)
            or not isinstance(request_id, str)
            or not isinstance(activity_id, str)
        ):
            raise TypeError("All arguments must be strings.")

        self.request_data.setdefault(conversation_id, {})[request_id] = activity_id

    def store_activity_id(self, conversation_id: str, activity_id: str) -> None:
        """
        Stores the general activity ID associated with a conversation.

        Args:
            conversation_id (str): The unique conversation ID.
            activity_id (str): The activity ID to be stored.

        Raises:
            TypeError: If any of the input arguments are not strings.
        """

        # Validate input types
        if not isinstance(conversation_id, str) or not isinstance(activity_id, str):
            raise TypeError("All arguments must be strings.")

        self.data[conversation_id] = activity_id  # Use a separate dictionary

    def get_rqst_activity_id(self, conversation_id: str, request_id: str) -> str:
        """
        Retrieves the activity ID associated with a specific conversation and request.

        Args:
            conversation_id (str): The unique conversation ID.
            request_id (str): The unique request ID within the conversation.

        Returns:
            str: The activity ID if found, None otherwise.
        """

        # conversation_data = self.request_data.get(conversation_id)
        # if conversation_data:
        #     return conversation_data.get(request_id)
        # return None
        # Use get to safely retrieve nested data, returns None if not found
        return self.request_data.get(conversation_id, {}).get(request_id, None)

    def get_activity_id(self, conversation_id: str) -> str | None:
        """
        Retrieves the general activity ID associated with a conversation.

        Args:
            conversation_id (str): The unique conversation ID.

        Returns:
            str | None: The activity ID if found, None otherwise.
        """

        # Use get to safely retrieve data, returns None if not found
        return self.data.get(conversation_id, None)

    def delete_activity_id(self, conversation_id: str) -> None:
        """
        Deletes the activity ID associated with a conversation (both general and request-specific).

        Args:
            conversation_id (str): The unique conversation ID.
        """

        # Delete the general activity ID if it exists
        if conversation_id in self.data:
            del self.data[conversation_id]

        # Delete the request-specific activity IDs if they exist
        if conversation_id in self.request_data:
            del self.request_data[conversation_id]
