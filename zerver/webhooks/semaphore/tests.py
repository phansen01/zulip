# -*- coding: utf-8 -*-
from typing import Text

from zerver.lib.test_classes import WebhookTestCase

class SemaphoreHookTests(WebhookTestCase):
    STREAM_NAME = 'semaphore'
    URL_TEMPLATE = "/api/v1/external/semaphore?stream={stream}&api_key={api_key}"

    # Messages are generated by Semaphore on git push. The subject lines below
    # contain information on the repo and branch, and the message has links and
    # details about the build, deploy, server, author, and commit

    def test_semaphore_build(self) -> None:
        expected_subject = u"knighthood/master"  # repo/branch
        expected_message = u"""[build 314](https://semaphoreci.com/donquixote/knighthood/branches/master/builds/314): passed
!avatar(don@lamancha.com) [`a490b8d`](https://github.com/donquixote/knighthood/commit/a490b8d508ebbdab1d77a5c2aefa35ceb2d62daf): Create user account for Rocinante :horse:."""
        self.send_and_test_stream_message('build', expected_subject, expected_message,
                                          content_type="application/x-www-form-urlencoded")

    def test_semaphore_deploy(self) -> None:
        expected_subject = u"knighthood/master"
        expected_message = u"""[deploy 17](https://semaphoreci.com/donquixote/knighthood/servers/lamancha-271/deploys/17) of [build 314](https://semaphoreci.com/donquixote/knighthood/branches/master/builds/314) on server lamancha-271: passed
!avatar(don@lamancha.com) [`a490b8d`](https://github.com/donquixote/knighthood/commit/a490b8d508ebbdab1d77a5c2aefa35ceb2d62daf): Create user account for Rocinante :horse:."""
        self.send_and_test_stream_message('deploy', expected_subject, expected_message,
                                          content_type="application/x-www-form-urlencoded")

    def get_body(self, fixture_name: Text) -> Text:
        return self.webhook_fixture_data("semaphore", fixture_name, file_type="json")
