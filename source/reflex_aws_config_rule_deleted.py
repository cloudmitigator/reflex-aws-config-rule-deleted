""" Module for ConfigRuleDeleted """

import json

from reflex_core import AWSRule, subscription_confirmation


class ConfigRuleDeleted(AWSRule):
    """ A Reflex Rule for detecting when AWS Config Rules are deleted """

    def __init__(self, event):
        super().__init__(event)

    def extract_event_data(self, event):
        """ Extract required event data """
        self.rule_name = event["detail"]["requestParameters"]["configRuleName"]

    def resource_compliant(self):
        """
        Determine if the resource is compliant with your rule.

        Return True if it is compliant, and False if it is not.
        """
        # We simply want to know when this event occurs. Since this rule was
        # triggered we know that happened, and we want to alert. Therefore
        # the resource is never compliant.
        return False

    def get_remediation_message(self):
        """ Returns a message about the remediation action that occurred """
        return f"The Config Rule {self.rule_name} was deleted."


def lambda_handler(event, _):
    """ Handles the incoming event """
    print(event)
    if subscription_confirmation.is_subscription_confirmation(event):
        subscription_confirmation.confirm_subscription(event)
        return
    rule = ConfigRuleDeleted(json.loads(event["Records"][0]["body"]))
    rule.run_compliance_rule()
