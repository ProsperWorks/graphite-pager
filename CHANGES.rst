Changelog
=========

0.1.3 (2016-10-31)
------------------

- Fix support for git 2.0 in release script. [Jose Diaz-Gonzalez]

- Add editorconfig. [Jose Diaz-Gonzalez]

- Allow no data patch. [Jacob Greenleaf]

- Pull down all keys when updating local copy. [Jose Diaz-Gonzalez]

0.1.2 (2016-01-25)
------------------

- Minor release changes. [Jose Diaz-Gonzalez]

0.1.1 (2015-11-28)
------------------

- Remove readme from manifest. [Jose Diaz-Gonzalez]

0.1.0 (2015-11-28)
------------------

- Pip freeze > requirements.txt. [Jose Diaz-Gonzalez]

- Add a release script. [Jose Diaz-Gonzalez]

- Change readme format to RST. [Jose Diaz-Gonzalez]

v0.0.10 (2015-06-30)
--------------------

- V0.0.10. [Jose Diaz-Gonzalez]

- Include txt and rst files. [Jose Diaz-Gonzalez]

v0.0.9 (2015-06-30)
-------------------

- V0.0.9. [Jose Diaz-Gonzalez]

v0.1.0 (2015-06-30)
-------------------

- V0.1.0. [Jose Diaz-Gonzalez]

- Allow specifying multiple slack urls for a given alert/level. [Jose
  Diaz-Gonzalez]

- Set proper formatting of slack notifications. [Jose Diaz-Gonzalez]

  Slack uses a not-quite markdown format, which means we need to add yet another format to the description object. Rather than passing around another output, we'll just use the description object directly.


- Fix quoting in templates. [Jose Diaz-Gonzalez]

- Fix testcase for http verification. [Jose Diaz-Gonzalez]

- PEP8. [Jose Diaz-Gonzalez]

- Move missing record notification into it's own method. [Jose Diaz-
  Gonzalez]

- Switch to a command map for running graphite-pager commands. [Jose
  Diaz-Gonzalez]

- Remove commented out code. [Jose Diaz-Gonzalez]

- Add a slack notifier. [Jose Diaz-Gonzalez]

- Comment out print statements. [Jose Diaz-Gonzalez]

  We'll need to refactor this to use a logger


- Add libmagic requirement for pushbullet. [Jose Diaz-Gonzalez]

- Add StdoutNotifier. [Jose Diaz-Gonzalez]

- Verify http requests. [Jose Diaz-Gonzalez]

- Remove extra line printing. [Jose Diaz-Gonzalez]

- Add pushbullet support, update docs. [Jaka Hudoklin]

- Clarify BSD 2-Clause License usage. [Jose Diaz-Gonzalez]

- Simplify some alerts retrieval. [Jose Diaz-Gonzalez]

- Simplify argument parsing and move to a separate module. [Jose Diaz-
  Gonzalez]

- Add pep8 and pyflakes. [Jose Diaz-Gonzalez]

- PEP8 for all tests. [Jose Diaz-Gonzalez]

- Add mock requirement to travis.yml. [Jose Diaz-Gonzalez]

- Refactor alerts.py to use Alert.get method for data. [Jose Diaz-
  Gonzalez]

  Also move description-related classes/functions into new module


- Remove unused import. [Jose Diaz-Gonzalez]

- Allow overriding service_key on a per-alert type basis. [Jose Diaz-
  Gonzalez]

- Remove missing notifiers. [Jose Diaz-Gonzalez]

- Use self.data() to retrieve yaml configuration data. [Jose Diaz-
  Gonzalez]

- Remove unnecessary argument. [Jose Diaz-Gonzalez]

- Reimplement config key checking to use 'in' operator internally. [Jose
  Diaz-Gonzalez]

- Simplify config.get() logic. [Jose Diaz-Gonzalez]

- Allow the specification of environment variables in yaml. Closes #17.
  [Jose Diaz-Gonzalez]

- Reorganize notifiers. [Jose Diaz-Gonzalez]

  This commit moves around the notifiers into a subpackage - graphitepager.notifiers - and simplifies the notifier attachment code. All notifiers now initialize themselves with their own client and also have an `enabled` flag that can be used to tell whether or not a notifier should be in use.

  This commit makes all notifiers optional - though you really should use at least one notifier!


- Allow overriding the pagerduty service_key for a given alert. [Jose
  Diaz-Gonzalez]

  This commit also adds the alert_data to each alert object, as well as an accessor method for said data


- Move global function into RedisStorage scope. [Jose Diaz-Gonzalez]

  The function is unused elsewhere in the codebase. This commit is to cleanup a function that is ostensibly a private function call and remove it from the global scope where it is unused.


- Document redis requirement and add fallback for REDISTOGO_URL env var.
  [Jose Diaz-Gonzalez]

  Closes #19


- Fix all pyflakes warnings for graphitepager package. [Jose Diaz-
  Gonzalez]

- Don't include distribute in requirements.txt. [Jose Diaz-Gonzalez]

  Causes errors in Python 2.7.4

v0.0.8 (2013-07-31)
-------------------

- V0.0.8. [Philip Cristiano]

- Remove printing. [Philip Cristiano]

- Add verify command. [Philip Cristiano]

- Example alerts: Fix typo. [Philip Cristiano]

v0.0.7 (2013-05-10)
-------------------

- Version 0.0.7. [Philip Cristiano]

- Notifier_proxy: Remove unneeded pass statement. [Philip Cristiano]

- Hipchat: Notify on NO DATA errors. [Philip Cristiano]

  A useful error to be aware of. This will include NO DATA errors in HipChat notifications.

- Spell Check. [Yuvaraj]

  Corrected PagerDuty Spelling Mistake

v0.0.6 (2013-03-10)
-------------------

- V0.0.6: Add documentation url. [Philip Cristiano]

v0.0.5 (2013-02-12)
-------------------

- V0.0.5: Alert for failing checks. [Philip Cristiano]

  Closes #4

v0.0.4 (2013-02-03)
-------------------

- V0.0.4. [Philip Cristiano]

- Alerting: Use last value instead of average. [Philip Cristiano]

  The average value makes it hard to reason about when an alert will trigger or has triggered when looking at the graph. The averaging done previously could easily be done in graphite if it was required.

  closes #10

- Log: Output alert if not nominal. [Philip Cristiano]

  Closes #9

- Descriptions: Delay rendering of description till it's needed. [Philip
  Cristiano]

  No reason to call the template object if it will never be used. This should speed up the time to check all alerts

- Only run every 60 seconds. [Philip Cristiano]

- Version info. [Philip Cristiano]

- Worker: Order imports. [Philip Cristiano]

- Config: Allow specifying the alerts file. [Philip Cristiano]

v0.0.3 (2012-12-07)
-------------------

- Parsing: Allow targets with commas closes #8. [Philip Cristiano]

- Storage: Set redis expiry to 1 hour. [Philip Cristiano]

  5 minutes is short enough that it could forget the pager duty key if it stopped for some reason

- Alerts: Remove whitespace. [Philip Cristiano]

- Requirements: Fix syntax. [Philip Cristiano]

- Set different values for subset of metrics. [Philip Cristiano]

- Missed one. [Philip Cristiano]

- Return level from alert. [Philip Cristiano]

  This was breaking if the excluded target didn't have data


- Add ability to exclude certain targets. [Philip Cristiano]

- Add hipchat to setup.py. [Philip Cristiano]

- Customize time to query for metrics. [Philip Cristiano]

- README: notifiers. [Philip Cristiano]

- Cleanup hipchat notifier. [Philip Cristiano]

- Hipchat: Notify change with colors! [Philip Cristiano]

- Add HipChat notifier. [Philip Cristiano]

- Rename and possible py2.6 fix. [Philip Cristiano]

- Notifiers: Support multiple notifier classes. [Philip Cristiano]

- Properly encode url for emails. [Philip Cristiano]

- Send the actual value in graph, not the level… again. [Philip
  Cristiano]

- Improve description. [Philip Cristiano]

- Add something to read. [Philip Cristiano]

- Alert for data of `None`s. [Philip Cristiano]

- Test averages from graphite. [Philip Cristiano]

- Resolve incidents that are no longer alerting in graphite. [Philip
  Cristiano]

- Include travis. [Philip Cristiano]

- Tests: Add forgotten test. [Philip Cristiano]

- Alerts: Alert for high or low values determined by level. [Philip
  Cristiano]

- Alerts: Send critical alerts. [Philip Cristiano]

- Parsing: Handle metrics that are missing data. [Philip Cristiano]

- Handle more than 1 metric returned per target. [Philip Cristiano]

- Req: Add requirements to setup.py. [Philip Cristiano]

- Setup: Have a process to run. [Philip Cristiano]

- Alert: Make more sense. [Philip Cristiano]

- Prototype: alert via pagerduty. [Philip Cristiano]

- Test reading file. [Philip Cristiano]

- Add some README. [Philip Cristiano]

- Can hit graphite server. [Philip Cristiano]

- First heroku setup. [Philip Cristiano]

- Make: Add upload target. [Philip Cristiano]

- Make: Fix path to Python. [Philip Cristiano]

- Basic project layout. [Philip Cristiano]

- Initial commit. [philipcristiano]


