from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    __name__,
    "assets",
    default="semantic-ui",
    themes={
        "semantic-ui": dict(
            entry={
                "oarepo_requests_ui_record_requests": "./js/oarepo_requests_ui/record-requests/index.js",
                "oarepo_requests_ui_request_detail": "./js/oarepo_requests_ui/request-detail/index.js",
                "oarepo_requests_ui_components": "./js/oarepo_requests_ui/custom-components.js",
            },
            dependencies={},
            devDependencies={},
            aliases={
                "@translations/oarepo_requests_ui": "translations/oarepo_requests_ui",
                "@js/oarepo_requests": "js/oarepo_requests_ui/record-requests",
                "@js/oarepo_requests_detail": "js/oarepo_requests_ui/request-detail",
                "@js/oarepo_requests_common": "js/oarepo_requests_ui/common",
            },
        )
    },
)
