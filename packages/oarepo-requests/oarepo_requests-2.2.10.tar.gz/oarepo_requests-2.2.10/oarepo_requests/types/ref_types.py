from invenio_records_resources.references import RecordResolver
from invenio_requests.proxies import current_requests

from oarepo_requests.proxies import current_oarepo_requests


class ModelRefTypes:
    """
    This class is used to define the allowed reference types for the topic reference.
    The list of ref types is taken from the configuration (configuration key REQUESTS_ALLOWED_TOPICS).
    """

    def __init__(self, published=False, draft=False):
        self.published = published
        self.draft = draft

    def __get__(self, obj, owner):
        """Property getter, returns the list of allowed reference types."""
        ret = []
        for ref_type in current_requests.entity_resolvers_registry:
            if not isinstance(ref_type, RecordResolver):
                continue
            is_draft = getattr(ref_type.record_cls, "is_draft", False)
            if self.published and not is_draft:
                ret.append(ref_type.type_key)
            elif self.draft and is_draft:
                ret.append(ref_type.type_key)
        return ret


class ReceiverRefTypes:
    """
    This class is used to define the allowed reference types for the receiver reference.
    The list of ref types is taken from the configuration (configuration key REQUESTS_ALLOWED_RECEIVERS).
    """

    def __get__(self, obj, owner):
        """Property getter, returns the list of allowed reference types."""
        return current_oarepo_requests.allowed_receiver_ref_types
