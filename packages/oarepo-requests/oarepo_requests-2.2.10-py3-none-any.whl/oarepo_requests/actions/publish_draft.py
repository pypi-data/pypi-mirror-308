from invenio_access.permissions import system_identity
from invenio_records_resources.services.uow import RecordCommitOp
from marshmallow import ValidationError
from oarepo_runtime.datastreams.utils import get_record_service_for_record
from oarepo_runtime.i18n import lazy_gettext as _

from .cascade_events import update_topic
from .generic import (
    AddTopicLinksOnPayloadMixin,
    OARepoAcceptAction,
    OARepoDeclineAction,
    OARepoSubmitAction,
)


class PublishDraftSubmitAction(OARepoSubmitAction):
    def can_execute(self):
        if not super().can_execute():
            return False
        try:
            topic = self.request.topic.resolve()
        except:  # noqa: used for links, so ignore errors here
            return False
        topic_service = get_record_service_for_record(topic)
        try:
            topic_service.validate_draft(system_identity, topic["id"])
            return True
        except ValidationError:
            return False


class PublishDraftAcceptAction(AddTopicLinksOnPayloadMixin, OARepoAcceptAction):
    self_link = "published_record:links:self"
    self_html_link = "published_record:links:self_html"

    name = _("Publish")

    def apply(self, identity, request_type, topic, uow, *args, **kwargs):
        topic_service = get_record_service_for_record(topic)
        if not topic_service:
            raise KeyError(f"topic {topic} service not found")
        id_ = topic["id"]

        if "payload" in self.request and "version" in self.request["payload"]:
            topic.metadata["version"] = self.request["payload"]["version"]
            uow.register(RecordCommitOp(topic, indexer=topic_service.indexer))

        published_topic = topic_service.publish(
            identity, id_, uow=uow, expand=False, *args, **kwargs
        )
        update_topic(self.request, topic, published_topic._record, uow)
        return super().apply(
            identity, request_type, published_topic, uow, *args, **kwargs
        )


class PublishDraftDeclineAction(OARepoDeclineAction):
    name = _("Return for correction")
