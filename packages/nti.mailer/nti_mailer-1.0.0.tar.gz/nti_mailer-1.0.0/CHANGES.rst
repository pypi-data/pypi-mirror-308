=========
 Changes
=========

1.0.0 (2024-11-12)
==================

- Drop support for Python < 3.10.
- Use native namespace packages.


0.0.1a2 (2021-09-07)
====================

- Translate the *subject* argument given to the default
  ``ITemplatedMailer`` implementation. See `issue 18
  <https://github.com/NextThought/nti.mailer/issues/18>`_.

- Deprecate the *message_factory* argument to
  ``ITemplatedMailer.queue_simple_html_text_email``. If you use this
  argument, please bring up your use-case in the issue tracker.

- Reach 100% test coverage.

0.0.1a1 (2021-08-12)
====================

- Initial PyPI release.

- Add support for Python 3.6 through 3.9. 3.10 is expected when
  zodbpickle supports it.
