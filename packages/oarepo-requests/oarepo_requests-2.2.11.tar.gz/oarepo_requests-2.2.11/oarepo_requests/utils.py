import copy

from invenio_access.permissions import system_identity
from invenio_pidstore.errors import PersistentIdentifierError
from invenio_records_resources.proxies import current_service_registry
from invenio_requests.proxies import (
    current_request_type_registry,
    current_requests_service,
)
from invenio_requests.resolvers.registry import ResolverRegistry
from invenio_search.engine import dsl

try:
    from oarepo_workflows import AutoApprove, Workflow, WorkflowRequest
    from oarepo_workflows.errors import MissingWorkflowError
    from oarepo_workflows.proxies import current_oarepo_workflows
except ImportError:
    current_oarepo_workflows = None
    Workflow = None
    WorkflowRequest = None
    AutoApprove = None
    MissingWorkflowError = None


def allowed_request_types_for_record(record):
    if current_oarepo_workflows:
        try:
            workflow_requests = current_oarepo_workflows.get_workflow(record).requests()
        except MissingWorkflowError:
            # workflow not defined on the record, probably not a workflow-enabled record
            # so returning all matching request types
            # TODO: is this correct?
            workflow_requests = None
    else:
        workflow_requests = None

    request_types = current_request_type_registry._registered_types
    ret = {}
    try:
        record_ref = list(ResolverRegistry.reference_entity(record).keys())[0]
    except:
        # log?
        return ret
    for request_name, request_type in request_types.items():
        allowed_type_keys = set(
            request_type.allowed_topic_ref_types
        )  # allowed topic types does not work correctly - delete published allows community and documents_file_draft
        if record_ref in allowed_type_keys:
            if not workflow_requests or hasattr(workflow_requests, request_name):
                ret[request_name] = request_type
    return ret


def _reference_query_term(term, reference):
    return dsl.Q(
        "term", **{f"{term}.{list(reference.keys())[0]}": list(reference.values())[0]}
    )


def search_requests_filter(
    type_id,
    topic_reference=None,
    receiver_reference=None,
    creator_reference=None,
    is_open=False,
    add_filter=None,
    or_filter=None,
):
    must = [
        dsl.Q("term", **{"type": type_id}),
        dsl.Q("term", **{"is_open": is_open}),
    ]
    if receiver_reference:
        must.append(_reference_query_term("receiver", receiver_reference))
    if creator_reference:
        must.append(_reference_query_term("creator", creator_reference))
    if topic_reference:
        must.append(_reference_query_term("topic", topic_reference))

    extra_filter = dsl.query.Bool(
        "must",
        must=must,
    )
    if add_filter:
        extra_filter &= add_filter
    if or_filter:
        extra_filter |= or_filter

    return extra_filter


def open_request_exists(topic_or_reference, type_id):
    topic_reference = ResolverRegistry.reference_entity(topic_or_reference, raise_=True)
    base_filter = search_requests_filter(
        type_id=type_id, topic_reference=topic_reference, is_open=True
    )
    results = current_requests_service.search(
        system_identity, extra_filter=base_filter
    ).hits
    return bool(list(results))


# TODO these things are related and possibly could be approached in a less convoluted manner? For example, global model->services map would help
def resolve_reference_dict(reference_dict):
    topic_resolver = None
    for resolver in ResolverRegistry.get_registered_resolvers():
        try:
            if resolver.matches_reference_dict(reference_dict):
                topic_resolver = resolver
                break
        except ValueError:
            # Value error ignored from matches_reference_dict
            pass
    obj = topic_resolver.get_entity_proxy(reference_dict).resolve()
    return obj


def get_matching_service_for_refdict(reference_dict):
    for resolver in ResolverRegistry.get_registered_resolvers():
        if resolver.matches_reference_dict(reference_dict):
            return current_service_registry.get(resolver._service_id)
    return None


def get_type_id_for_record_cls(record_cls):
    for resolver in ResolverRegistry.get_registered_resolvers():
        if hasattr(resolver, "record_cls") and resolver.record_cls == record_cls:
            return resolver.type_id
    return None


def get_requests_service_for_records_service(records_service):
    return current_service_registry.get(f"{records_service.config.service_id}_requests")


def stringify_first_val(dct):
    if isinstance(dct, dict):
        for k, v in dct.items():
            dct[k] = str(v)
    return dct


def reference_to_tuple(reference):
    return (list(reference.keys())[0], list(reference.values())[0])


def get_receiver_for_request_type(request_type, identity, topic):
    if not topic:
        return None

    try:
        workflow: Workflow = current_oarepo_workflows.get_workflow(topic)
    except MissingWorkflowError:
        return None

    try:
        workflow_request: WorkflowRequest = workflow.requests()[request_type.type_id]
    except KeyError:
        return None

    receivers = workflow_request.reference_receivers(
        identity=identity, record=topic, request_type=request_type, creator=identity
    )
    if not receivers:
        return None

    return receivers


def is_auto_approved(request_type, *, identity=None, topic=None, receiver=None):
    if not current_oarepo_workflows:
        return False

    if not receiver:
        receiver = get_receiver_for_request_type(
            request_type=request_type, identity=identity, topic=topic
        )

    return receiver and (
        isinstance(receiver, AutoApprove)
        or isinstance(receiver, dict)
        and receiver.get("auto_approve")
    )


def request_identity_matches(entity_reference, identity):
    if not entity_reference:
        return False

    try:
        entity = ResolverRegistry.resolve_entity_proxy(entity_reference)
        if entity:
            needs = entity.get_needs()
            return bool(identity.provides.intersection(needs))
    except PersistentIdentifierError:
        return False


def merge_resource_configs(config_to_merge_in, original_config):
    actual_config = copy.deepcopy(config_to_merge_in)
    original_keys = {x for x in dir(original_config) if not x.startswith("_")}
    merge_in_keys = {
        x for x in dir(config_to_merge_in) if not x.startswith("_")
    }  # have to do this bc hasattr fails on resolving response_handlers
    for copy_from_original_key in original_keys - merge_in_keys:
        setattr(
            actual_config,
            copy_from_original_key,
            getattr(original_config, copy_from_original_key),
        )
    return actual_config
