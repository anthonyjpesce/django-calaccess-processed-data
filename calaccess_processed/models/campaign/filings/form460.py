#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing data from Campaign Disclosure Statements (Form 460).
"""
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.managers import ProcessedDataManager
from calaccess_processed.models.campaign.filings import (
    CampaignFinanceFilingBase,
    CampaignContributionBase,
    CampaignExpenditureItemBase,
    CampaignExpenditureSubItemBase,
)


class Form460FilingBase(CampaignFinanceFilingBase):
    """
    Base and abstract model for Form 460 filings.
    """
    from_date = models.DateField(
        verbose_name='from date',
        db_index=True,
        null=False,
        help_text="The first date of the filing period covered by the statement "
                  "(from CVR_CAMPAIGN_DISCLOSURE.FROM_DATE)",
    )
    thru_date = models.DateField(
        verbose_name='thru date',
        db_index=True,
        null=False,
        help_text="The last date of the filing period covered by the statement "
                  "(from CVR_CAMPAIGN_DISCLOSURE.THRU_DATE)",
    )
    monetary_contributions = models.IntegerField(
        verbose_name='monetary contributions',
        null=True,
        help_text="Total monetary contributions (from line 1, column A)",
    )
    loans_received = models.IntegerField(
        verbose_name='loans received',
        null=True,
        help_text="Total loans received (from line 2, column A)",
    )
    subtotal_cash_contributions = models.IntegerField(
        verbose_name='subtotal cash contributions',
        null=True,
        help_text="Monetary contributions and loans received combined (from "
                  "line 3, column A)",
    )
    nonmonetary_contributions = models.IntegerField(
        verbose_name='nonmonetary contributions',
        null=True,
        help_text="Non-monetary contributions (from line 4, column A)",
    )
    total_contributions = models.IntegerField(
        verbose_name='total contributions',
        null=True,
        help_text="Total contributions (from line 5, column A)",
    )
    payments_made = models.IntegerField(
        verbose_name='payments made',
        null=True,
        help_text="Payments made (from line 6, column A)",
    )
    loans_made = models.IntegerField(
        verbose_name='loans made',
        null=True,
        help_text="Loans made (from line 7, column A)",
    )
    subtotal_cash_payments = models.IntegerField(
        verbose_name='subtotal cash payments',
        null=True,
        help_text="Sub-total of cash payments (from line 8, column A)",
    )
    unpaid_bills = models.IntegerField(
        verbose_name='unpaid bills',
        null=True,
        help_text="Unpaid bills / accrued expenses (from line 9, column A)",
    )
    nonmonetary_adjustment = models.IntegerField(
        verbose_name='nonmonetary adjustment',
        null=True,
        help_text="Non-monetary adjustment (from line 10, column A), which is "
                  "equal to the total of non-monetary contributions",
    )
    total_expenditures_made = models.IntegerField(
        verbose_name='total expenditures made',
        null=True,
        help_text="Total expenditures made (from line 11, column A)",
    )
    begin_cash_balance = models.IntegerField(
        verbose_name='begin cash balance',
        null=True,
        help_text="Beginning cash balance (from line 12), which is equal to "
                  "the Ending Cash Balance (line 16) reported on the summary "
                  "page of the previous Form 460 filing"
    )
    cash_receipts = models.IntegerField(
        verbose_name='cash receipts',
        null=True,
        help_text="Cash receipts (from line 13)",
    )
    miscellaneous_cash_increases = models.IntegerField(
        verbose_name='miscellaneous cash increases',
        null=True,
        help_text="Miscellaneous cash increases (from line 14)",
    )
    cash_payments = models.IntegerField(
        verbose_name='cash payments',
        null=True,
        help_text="Cash payments (from line 15)",
    )
    ending_cash_balance = models.IntegerField(
        verbose_name='ending cash balance',
        null=True,
        help_text="Ending cash balance (from line 16)",
    )
    loan_guarantees_received = models.IntegerField(
        verbose_name='loan guarantees received',
        null=True,
        help_text="Loan guarantees received (from line 17)",
    )
    cash_equivalents = models.IntegerField(
        verbose_name='cash equivalents',
        null=True,
        help_text="Cash equivalents (from line 18), which includes investments "
                  "that can't be readily converted to cash, such as outstanding "
                  "loans the committee has made to others"
    )
    outstanding_debts = models.IntegerField(
        verbose_name='outstanding debts',
        null=True,
        help_text="Outstanding debts on loans owed by the committee (from line "
                  "19)",
    )

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Form460Filing(Form460FilingBase):
    """
    The most recent version of each Form 460 (Campaign Disclosure Statement) 
    filing by recipient committees.

    Includes information from the cover sheet and summary page of the most 
    recent amendment to each filing. All versions of Form 460 filings can be
    found in form460version.
    """
    filing_id = models.IntegerField(
        verbose_name='filing id',
        primary_key=True,
        null=False,
        help_text='Unique identification number for the Form 460 filing ('
                  'from CVR_CAMPAIGN_DISCLOSURE_CD.FILING_ID)',
    )
    amendment_count = models.IntegerField(
        verbose_name='Count amendments',
        db_index=True,
        null=False,
        help_text='Number of amendments to the Form 460 filing (from '
                  'maximum value of CVR_CAMPAIGN_DISCLOSURE_CD.AMEND_ID)',
    )

    objects = ProcessedDataManager()

    class Meta:
        index_together = ((
            'filing_id',
            'amendment_count',
        ),)

    def __str__(self):
        return str(self.filing_id)


@python_2_unicode_compatible
class Form460FilingVersion(Form460FilingBase):
    """
    Every version of each Form 460 (Campaign Disclosure Statement) filing by
    recipient committees.

    Includes information found on the cover sheet and summary page of each
    amendment. For the most recent version of each filing, see form460.
    """
    filing = models.ForeignKey(
        'Form460Filing',
        related_name='versions',
        db_constraint=False,
        null=True,
        on_delete=models.SET_NULL,
        help_text='Unique identification number for the Form 460 filing ('
                  'from CVR_CAMPAIGN_DISCLOSURE_CD.FILING_ID)',
    )
    amend_id = models.IntegerField(
        verbose_name='amendment id',
        null=False,
        help_text='Identifies the version of the Form 497 filing, with 0 '
                  'representing the initial filing (from CVR_CAMPAIGN_'
                  'DISCLOSURE_CD.AMEND_ID)',
    )

    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing',
            'amend_id',
        ),)
        index_together = ((
            'filing',
            'amend_id',
        ),)

    def __str__(self):
        return '%s-%s' % (self.filing, self.amend_id)


class Form460ScheduleAItemBase(CampaignContributionBase):
    """
    Abstract base model for monetary contributions received by campaign filers.

    These transactions are itemized on Schedule A of Form 460 filings and 
    stored in the RCPT_CD table with a FORM_TYPE value of 'A'.
    """
    amount = models.DecimalField(
        verbose_name='amount',
        decimal_places=2,
        max_digits=14,
        help_text="Amount received from the contributor in the period covered "
                  "by the filing (from RCPT_CD.AMOUNT)"
    )

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Form460ScheduleAItem(Form460ScheduleAItemBase):
    """
    Monetary contributions received by campaign filers.

    These transactions are itemized on Schedule A of the most recent amendment
    to each Form 460 filing. For monetary contributions itemized on any version
    of any Form 460 filing, see Form460ScheduleAItemVersion.

    Also includes contributions transferred to special election commitees,
    formerly itemized on Schedule A-1. 

    Derived from RCPT_CD records where FORM_TYPE is 'A' or 'A-1'.
    """
    filing = models.ForeignKey(
        'Form460Filing',
        related_name='itemized_monetary_contributions',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the Form 460 on which the monetary'
                  ' contribution was reported (from RCPT_CD.FILING_ID)',
    )

    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing',
            'line_item',
        ),)

    def __str__(self):
        return '%s-%s' % (self.filing, self.line_item)


@python_2_unicode_compatible
class Form460ScheduleAItemVersion(Form460ScheduleAItemBase):
    """
    Every version of the monetary contributions received by campaign filers.

    For monetary contributions itemized on Schedule A of the most recent
    version of each Form 460 filing, see Form460ScheduleAItem.

    Derived from RCPT_CD records where FORM_TYPE is 'A' or 'A-1'.
    """
    filing_version = models.ForeignKey(
        'Form460FilingVersion',
        related_name='itemized_monetary_contributions',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the version of the Form 460 that '
                  'includes the received contribution'
    )

    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing_version',
            'line_item',
        ),)
        index_together = ((
            'filing_version',
            'line_item',
        ),)

    def __str__(self):
        return '%s-%s-%s' % (
            self.filing_version.filing_id,
            self.filing_version.amend_id,
            self.line_item
        )


class Form460ScheduleCItemBase(CampaignContributionBase):
    """
    Abstract base model for nonmonetary contributions received by campaign filers.

    These transactions are itemized on Schedule C of Form 460 filings and 
    stored in the RCPT_CD table with a FORM_TYPE value of 'C'.
    """
    fair_market_value = models.DecimalField(
        verbose_name='fair market value',
        decimal_places=2,
        max_digits=14,
        help_text="Amount it would cost to purchase the donated goods or "
                  "services on the open market (from RCPT_CD.AMOUNT)"
    )
    contribution_description = models.CharField(
        max_length=90,
        blank=True,
        help_text="Description of the contributed goods or services (from "
                  "RCPT_CD.CTRIB_DSCR)"
    )
    
    class Meta:
        abstract = True


@python_2_unicode_compatible
class Form460ScheduleCItem(Form460ScheduleCItemBase):
    """
    Nonmonetary contributions received by campaign filers.

    These transactions are itemized on Schedule C of the most recent amendment
    to each Form 460 filing. For nonmonetary contributions itemized on any 
    version of any Form 460 filing, see nonmonetarycontributionversion.

    Derived from RCPT_CD records where FORM_TYPE is 'C'.
    """
    filing = models.ForeignKey(
        'Form460Filing',
        related_name='itemized_nonmonetary_contributions',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the Form 460 on which the monetary'
                  ' contribution was reported (from RCPT_CD.FILING_ID)',
    )

    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing',
            'line_item',
        ),)

    def __str__(self):
        return '%s-%s' % (self.filing, self.line_item)


@python_2_unicode_compatible
class Form460ScheduleCItemVersion(Form460ScheduleCItemBase):
    """
    Every version of the nonmonetary contributions received by campaign filers.

    For nonmonetary contributions itemized on Schedule C of the most recent
    version of each Form 460 filing, see nonmonetarycontribution.

    Derived from RCPT_CD records where FORM_TYPE is 'C'.
    """
    filing_version = models.ForeignKey(
        'Form460FilingVersion',
        related_name='itemized_nonmonetary_contributions',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the version of the Form 460 that '
                  'includes the received contribution'
    )

    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing_version',
            'line_item',
        ),)
        index_together = ((
            'filing_version',
            'line_item',
        ),)

    def __str__(self):
        return '%s-%s-%s' % (
            self.filing_version.filing_id,
            self.filing_version.amend_id,
            self.line_item
        )


class Form460ScheduleDItemBase(CampaignExpenditureItemBase):
    """
    Abstract base model for items reported on Schedule D of Form 460.

    On Schedule D, campaign filers are required to summarize contributions
    and independent expenditures in support or opposition to other candidates
    and ballot measures
    """
    cumulative_election_amount = models.DecimalField(
        decimal_places=2,
        max_digits=14,
        null=True,
        help_text="If the candidate is subject to contribution limits, the "
                  "cumulative amount given by the filer during the election "
                  "cycle as of the Form 460's filing date (from EXPN_CD."
                  "CUM_OTH)"
    )

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Form460ScheduleDItem(Form460ScheduleDItemBase):
    """
    Contribution and expenditures in support or opposition to other candidates
    and ballot measures.

    These transactions are itemized on Schedule D of the most recent version
    to each Form 460 filing. For payments itemized on any version of any Form
    460 filing, see Form460scheduleditemversion.

    Derived from EXPN_CD records where FORM_TYPE is 'D'.
    """
    filing = models.ForeignKey(
        'Form460Filing',
        related_name='schedule_d_items',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the Form 460 on which the '
                  'payment was reported (from RCPT_CD.FILING_ID)',
    )

    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing',
            'line_item',
        ),)

    def __str__(self):
        return '%s-%s' % (self.filing, self.line_item)


@python_2_unicode_compatible
class Form460ScheduleDItemVersion(Form460ScheduleDItemBase):
    """
    Every version of the payments made on behalf of campaign filers.

    For payments itemized on Schedule D of the most recent version of each Form
    460 filing, see Form460scheduleditem.

    Derived from EXPN_CD records where FORM_TYPE is 'D'.
    """
    filing_version = models.ForeignKey(
        'Form460FilingVersion',
        related_name='schedule_d_items',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the version of the Form 460 that '
                  'includes the payment made'
    )

    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing_version',
            'line_item',
        ),)
        index_together = ((
            'filing_version',
            'line_item',
        ),)

    def __str__(self):
        return '%s-%s-%s' % (
            self.filing_version.filing_id,
            self.filing_version.amend_id,
            self.line_item
        )


@python_2_unicode_compatible
class Form460ScheduleEItem(CampaignExpenditureItemBase):
    """
    Payments made by campaign filers, itemized on Schedule E of Form 460.

    These transactions are itemized on the most recent version of each Form 460
    filing. For payments itemized on any version of any Form 460 filing, see
    Form460scheduleeitemversion.

    Does not include:
    * Interest paid on loans received
    * Loans made to others
    * Transfers of campaign funds into savings accounts
    * Payments made by agents or contractors on behalf of the filer
    * Certificates of deposit
    * Money market accounts
    * Purchases of other assets that can readily be converted to cash

    Derived from EXPN_CD records where FORM_TYPE is 'E'.
    """
    filing = models.ForeignKey(
        'Form460Filing',
        related_name='schedule_e_items',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the Form 460 on which the '
                  'payment was reported (from RCPT_CD.FILING_ID)',
    )

    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing',
            'line_item',
        ),)

    def __str__(self):
        return '%s-%s' % (self.filing, self.line_item)


@python_2_unicode_compatible
class Form460ScheduleEItemVersion(CampaignExpenditureItemBase):
    """
    Every version of the payments made, itemized on Form 460 Schedule E.

    For payments itemized on the most recent version of each Form 460 filing,
    see Form460scheduleeitem.

    Does not include:
    * Interest paid on loans received
    * Loans made to others
    * Transfers of campaign funds into savings accounts
    * Payments made by agents or contractors on behalf of the filer
    * Certificates of deposit
    * Money market accounts
    * Purchases of other assets that can readily be converted to cash

    Derived from EXPN_CD records where FORM_TYPE is 'E'.
    """
    filing_version = models.ForeignKey(
        'Form460FilingVersion',
        related_name='schedule_e_items',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the version of the Form 460 that '
                  'includes the payment made'
    )

    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing_version',
            'line_item',
        ),)
        index_together = ((
            'filing_version',
            'line_item',
        ),)

    def __str__(self):
        return '%s-%s-%s' % (
            self.filing_version.filing_id,
            self.filing_version.amend_id,
            self.line_item
        )


@python_2_unicode_compatible
class Form460ScheduleESubItem(CampaignExpenditureSubItemBase):
    """
    Sub-items of payments made by campaign filers.

    These transactions are itemized on Schedule E of the most recent version
    of each Form 460 filing. For payments sub-itemitemized on any version of
    any Form 460 filing, see Form460scheduleesubitemversion.

    A sub-item is a transaction where the amount is lumped into another 
    "parent" payment reported elsewhere on the filing.

    Includes:
    * Payments supporting or opposing other candidates, ballot measures 
    or committees, which are summarized on Schedule D
    * Payments made to vendors over $100 included in credit card payments
    * Payments made by agents or independent contractors on behalf of the 
    campaign filer which were reported on Schedule E instead of G
    * Payments made on the accrued expenses reported on Schedule F

    Derived from EXPN_CD records where FORM_TYPE is 'E' and MEMO_CODE is not
    blank.
    """
    filing = models.ForeignKey(
        'Form460Filing',
        related_name='schedule_e_subitems',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the Form 460 on which the '
                  'payment was reported (from RCPT_CD.FILING_ID)',
    )

    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing',
            'line_item',
        ),)

    def __str__(self):
        return '%s-%s' % (self.filing, self.line_item)


@python_2_unicode_compatible
class Form460ScheduleESubItemVersion(CampaignExpenditureSubItemBase):
    """
    Every version of the sub-items of payments by campaign filers.

    For payments sub-itemized on Schedule E of the most recent version of each
    Form 460 filing, see Form460scheduleesubitem.

    A sub-item is a transaction where the amount is lumped into another
    "parent" payment reported elsewhere on the filing.

    Includes:
    * Payments supporting or opposing other candidates, ballot measures 
    or committees, which are summarized on Schedule D
    * Payments made to vendors over $100 included in credit card payments
    * Payments made by agents or independent contractors on behalf of the 
    campaign filer which were reported on Schedule E instead of G
    * Payments made on the accrued expenses reported on Schedule F

    Derived from EXPN_CD records where FORM_TYPE is 'E' and MEMO_CODE is not
    blank.
    """
    filing_version = models.ForeignKey(
        'Form460FilingVersion',
        related_name='schedule_e_subitems',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the version of the Form 460 that '
                  'includes the payment made'
    )

    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing_version',
            'line_item',
        ),)
        index_together = ((
            'filing_version',
            'line_item',
        ),)

    def __str__(self):
        return '%s-%s-%s' % (
            self.filing_version.filing_id,
            self.filing_version.amend_id,
            self.line_item
        )


class Form460ScheduleGItemBase(CampaignExpenditureSubItemBase):
    """
    Abstract base model for items reported on Schedule G of Form 460.
    """
    agent_title = models.CharField(
        verbose_name='agent title',
        max_length=10,
        blank=True,
        help_text='Name title of the agent (from EXPN_CD.AGENT_NAMT)',
    )
    agent_lastname = models.CharField(
        verbose_name='agent lastname',
        max_length=200,
        blank=True,
        help_text='Last name of the agent or business name (from '
                  'EXPN_CD.AGENT_NAML)',
    )
    agent_firstname = models.CharField(
        verbose_name='agent firstname',
        max_length=45,
        help_text='First name of the agent (from EXPN_CD.AGENT_NAMF)',
    )
    agent_name_suffix = models.CharField(
        verbose_name='agent name suffix',
        max_length=10,
        blank=True,
        help_text='Name suffix of the agent (from EXPN_CD.AGENT_NAMS)',
    )
    PARENT_SCHEDULE_CHOICES = (
        ('E', 'Schedule E: Payments Made'),
        ('F', 'Schedule F: Accrued Expenses (Unpaid Bills)')
    )
    parent_schedule = models.CharField(
        max_length=1,
        blank=True,
        help_text="Indicates which schedule (E or F) includes the parent item "
                  "(from EXPN_CD.G_FROM_E_F)",
    )

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Form460ScheduleGItem(Form460ScheduleGItemBase):
    """
    Payments made by on behalf of campaign filers.

    These transactions are itemized on Schedule G of the most recent version
    to each Form 460 filing. For payments itemized on any version of any Form
    460 filing, see Form460schedulegitemversion.

    Derived from EXPN_CD records where FORM_TYPE is 'G'.
    """
    filing = models.ForeignKey(
        'Form460Filing',
        related_name='schedule_g_items',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the Form 460 on which the '
                  'payment was reported (from RCPT_CD.FILING_ID)',
    )

    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing',
            'line_item',
        ),)

    def __str__(self):
        return '%s-%s' % (self.filing, self.line_item)


@python_2_unicode_compatible
class Form460ScheduleGItemVersion(Form460ScheduleGItemBase):
    """
    Every version of the payments made on behalf of campaign filers.

    For payments itemized on Schedule G of the most recent version of each Form
    460 filing, see Form460schedulegitem.

    Derived from EXPN_CD records where FORM_TYPE is 'G'.
    """
    filing_version = models.ForeignKey(
        'Form460FilingVersion',
        related_name='schedule_g_items',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the version of the Form 460 that '
                  'includes the payment made'
    )

    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing_version',
            'line_item',
        ),)
        index_together = ((
            'filing_version',
            'line_item',
        ),)

    def __str__(self):
        return '%s-%s-%s' % (
            self.filing_version.filing_id,
            self.filing_version.amend_id,
            self.line_item
        )


class Form460ScheduleIItemBase(CampaignContributionBase):
    """
    Abstract base model for miscellaneous cash increases for campaign filers.

    Includes any transaction that increases the cash position of the filer, but
    is not a monetary contribution, loan, or loan repayment.

    These transactions are itemized on Schedule I of Form 460 filings and 
    stored in the RCPT_CD table with a FORM_TYPE value of 'I'.
    """
    amount = models.DecimalField(
        verbose_name='amount',
        decimal_places=2,
        max_digits=14,
        help_text="Amount of cash increase from the contributor in the period "
                  "covered by the filing (from RCPT_CD.AMOUNT)"
    )
    receipt_description = models.CharField(
        verbose_name='receipt description',
        max_length=90,
        blank=True,
        help_text="Description of the cash increase (from RCPT_CD.CTRIB_DSCR)"
    )

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Form460ScheduleIItem(Form460ScheduleIItemBase):
    """
    Miscellaneous cash increases to the coffers of campaign filers.

    Includes any transaction that increases the cash position of the filer, but
    is not a monetary contribution, loan, or loan repayment.

    These transactions are itemized on Schedule C of the most recent amendment
    to each Form 460 filing. For miscellaneous cash increases itemized on any
    version of any Form 460 filing, see misccashincreaseversion.

    Derived from RCPT_CD records where FORM_TYPE is 'I'.
    """
    filing = models.ForeignKey(
        'Form460Filing',
        related_name='misc_cash_increases',
        null=True,
        on_delete=models.SET_NULL,
        db_constraint=False,
        help_text='Foreign key referring to the Form 460 on which the '
                  'miscellaneous cash increase was report (from RCPT_CD.'
                  'FILING_ID)',
    )

    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing',
            'line_item',
        ),)

    def __str__(self):
        return '%s-%s' % (self.filing, self.line_item)


@python_2_unicode_compatible
class Form460ScheduleIItemVersion(Form460ScheduleIItemBase):
    """
    Every version of the miscellaneous cash increases for campaign filers.

    Includes any transaction that increases the cash position of the filer, but
    is not a monetary contribution, loan, or loan repayment.

    For miscellaneous cash increases itemized on Schedule I of the most recent
    version of each Form 460 filing, see misccashincreaseversion.

    Derived from RCPT_CD records where FORM_TYPE is 'I'.
    """
    filing_version = models.ForeignKey(
        'Form460FilingVersion',
        related_name='misc_cash_increases',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the version of the Form 460 that '
                  'includes the miscellaneous cash increase'
    )

    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing_version',
            'line_item',
        ),)
        index_together = ((
            'filing_version',
            'line_item',
        ),)

    def __str__(self):
        return '%s-%s-%s' % (
            self.filing_version.filing_id,
            self.filing_version.amend_id,
            self.line_item
        )