import unittest
from unittest import mock
from dqc_us_rules import dqc_us_0018


class TestCompareFacts(unittest.TestCase):
    def test_fact_checkable(self):
        """
        Tests that fact is checkable
        """
        good_fact = mock.Mock()

        bad_fact = mock.Mock()
        bad_fact.concept = None
        bad_fact.context = None

        good_concept = good_fact.concept
        good_context = good_fact.context
        bad_concept = bad_fact.concept
        bad_context = bad_fact.context

        self.assertTrue(
            dqc_us_0018._fact_checkable(good_concept, good_context)
        )

        self.assertFalse(
            dqc_us_0018._fact_checkable(good_concept, bad_context)
        )

        self.assertFalse(
            dqc_us_0018._fact_checkable(bad_concept, good_context)
        )

        self.assertFalse(
            dqc_us_0018._fact_checkable(bad_concept, bad_context)
        )

    def test_deprecated_concept(self):
        """
        Tests that fact errors if it contains a deprecated concept
        """
        val = mock.Mock()
        val.usgaapDeprecations = {}
        val.usgaapDeprecations['HealthCareOrganizationChangeInWriteOffs'] = (
            "Element was deprecated because it was inappropriately modeled. "
            "Possible replacement is "
            "AllowanceForDoubtfulAccountsReceivableWriteOffs."
        )
        bad_fact = mock.Mock()
        bad_fact.concept = mock.Mock()
        bad_fact.concept.name = 'HealthCareOrganizationChangeInWriteOffs'

        good_fact = mock.Mock()
        good_fact.concept = mock.Mock()
        good_fact.concept.name = (
            'AllowanceForDoubtfulAccountsReceivableWriteOffs'
        )

        self.assertTrue(
            dqc_us_0018._deprecated_concept(val, bad_fact.concept)
        )

        self.assertFalse(
            dqc_us_0018._deprecated_concept(val, good_fact.concept)
        )

    def test_deprecated_dimension(self):
        """
        Tests that fact errors if it contains a deprecated dimension
        """
        val = mock.Mock()
        gaapDeps = {}
        gaapDeps['ComponentOfOtherExpenseNonoperatingAxis'] = (
            "Element was deprecated because the financial reporting concept "
            "is no longer conveyed dimensionally."
        )
        val.usgaapDeprecations = gaapDeps
        bad_dim = mock.Mock()
        bad_dim.name = 'ComponentOfOtherExpenseNonoperatingAxis'
        good_dim = mock.Mock()
        good_dim.name = 'LegalEntityAxis'

        self.assertTrue(
            dqc_us_0018._deprecated_dimension(
                val,
                bad_dim
            )
        )

        self.assertFalse(
           dqc_us_0018._deprecated_dimension(
               val,
               good_dim
           )
        )

    def test_deprecated_member(self):
        """
        Tests to make sure that fact errors it it contains a deprecated member
        """
        val = mock.Mock()
        gaapDeps = {}
        gaapDeps['OtherMember'] = (
             "Element was deprecated. Possible replacement is "
             "OtherCreditDerivativesMember."
        )
        val.usgaapDeprecations = gaapDeps
        bad_mem = mock.Mock()
        bad_mem.name = 'OtherMember'
        good_mem = mock.Mock()
        good_mem.name = 'OtherCreditDerivativesMember'

        self.assertTrue(
            dqc_us_0018._deprecated_dimension(
                val,
                bad_mem
            )
        )

        self.assertFalse(
           dqc_us_0018._deprecated_dimension(
               val,
               good_mem
           )
        )
