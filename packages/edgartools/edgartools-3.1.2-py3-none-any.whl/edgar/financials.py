from collections import defaultdict
from functools import lru_cache, cached_property
from typing import Optional, List, Dict

import numpy as np
import pandas as pd
from pydantic import BaseModel
from rich import box
from rich.console import Group
from rich.panel import Panel
from rich.table import Table, Column
from rich.text import Text
import asyncio

from edgar.core import run_async_or_sync, datefmt
from edgar.richtools import repr_rich
from edgar.xbrl.presentation import FinancialStatementMapper, XBRLPresentation
from edgar.xbrl.xbrldata import XBRLData, Statement


__all__ = ['Financials', 'MultiFinancials']


class StandardConcept(BaseModel):
    concept: str
    label: str


class StandardStatement(BaseModel):
    statement_name: str
    primary_concept: str
    display_name: str
    concepts: List[StandardConcept]


BalanceSheet = StandardStatement(statement_name="BALANCE_SHEET",
                  primary_concept="us-gaap_StatementOfFinancialPositionAbstract",
                  display_name="Consolidated Balance Sheets",
                  concepts=[
                      StandardConcept(concept="us-gaap_AssetsAbstract", label="Assets"),
                      StandardConcept(concept="us-gaap_AssetsCurrentAbstract", label="Current Assets:"),
                      StandardConcept(concept="us-gaap_CashAndCashEquivalentsAtCarryingValue",
                                      label="Cash & Equivalents"),
                      StandardConcept(concept="us-gaap_AccountsReceivableNetCurrent",
                                      label="Accounts Receivable"),
                      StandardConcept(concept="us-gaap_InventoryNet", label="Inventory"),
                      StandardConcept(concept="us-gaap_AssetsCurrent", label="Total Current Assets"),
                      StandardConcept(concept="us-gaap_PropertyPlantAndEquipmentNet",
                                      label="Property, Plant and Equipment"),
                      StandardConcept(concept="us-gaap_Goodwill", label="Goodwill"),
                      StandardConcept(concept="us-gaap_OtherAssetsNoncurrent", label="Other Assets"),
                      StandardConcept(concept="us-gaap_Assets", label="Total Assets"),
                      StandardConcept(concept="us-gaap_LiabilitiesAndStockholdersEquityAbstract",
                                      label="Liabilities & Equity"),
                      StandardConcept(concept="us-gaap_LiabilitiesCurrentAbstract",
                                      label="Current Liabilities:"),
                      StandardConcept(concept="us-gaap_AccountsPayableCurrent",
                                      label="Accounts Payable"),
                      StandardConcept(concept="us-gaap_LiabilitiesCurrent",
                                      label="Total Current Liabilities"),
                      StandardConcept(concept="us-gaap_OtherLiabilitiesNoncurrent",
                                      label="Long-term Liabilities"),
                      StandardConcept(concept="us-gaap_Liabilities", label="Total Liabilities"),
                      StandardConcept(concept="us-gaap_CommitmentsAndContingencies",
                                      label="Commitments & Contingencies"),
                      StandardConcept(concept="us-gaap_StockholdersEquityAbstract",
                                      label="Stockholders' Equity:"),
                      StandardConcept(concept="us-gaap_CommonStockValue", label="Common Stock"),
                      StandardConcept(concept="us-gaap_RetainedEarningsAccumulatedDeficit",
                                      label="Retained Earnings"),
                      StandardConcept(concept="us-gaap_AccumulatedOtherComprehensiveIncomeLossNetOfTax",
                                      label="Other Comprehensive Income"),
                      StandardConcept(concept="us-gaap_StockholdersEquity",
                                      label="Total Stockholders' Equity"),
                      StandardConcept(concept="us-gaap_LiabilitiesAndStockholdersEquity",
                                      label="Total Liabilities & Equity"),
                  ]
                  )
IncomeStatement = StandardStatement(statement_name="INCOME_STATEMENT",
                  primary_concept="us-gaap_IncomeStatementAbstract",
                  display_name="Income Statements",
                  concepts=[
                      StandardConcept(concept="us-gaap_IncomeStatementAbstract",
                                      label="Income Statement"),
                      StandardConcept(
                          concept="us-gaap_RevenueFromContractWithCustomerExcludingAssessedTax", label="Revenue"),
                      StandardConcept(concept="us-gaap_CostOfGoodsAndServicesSold", label="Cost of Sales"),
                      StandardConcept(concept="us-gaap_OperatingExpensesAbstract", label="Operating Expenses"),
                      StandardConcept(concept="us-gaap_ResearchAndDevelopmentExpense", label="Research & Development"),
                      StandardConcept(concept="us-gaap_SellingGeneralAndAdministrativeExpense", label="Selling, General & Admin"),
                      StandardConcept(concept="us-gaap_OperatingExpenses", label="Total Operating Expenses"),


                      StandardConcept(concept="us-gaap_OperatingIncomeLoss", label="Operating Income"),
                      StandardConcept(
                          concept="us-gaap_IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
                          label="Pre-tax Income"),
                      StandardConcept(concept="us-gaap_IncomeTaxExpenseBenefit",
                                      label="Income Tax"),
                      StandardConcept(concept="us-gaap_NetIncomeLoss",
                                      label="Net Income"),
                      StandardConcept(concept="us-gaap_EarningsPerShareBasic",
                                      label="EPS Basic"),
                      StandardConcept(concept="us-gaap_EarningsPerShareDiluted",
                                      label="EPS Diluted"),
                      StandardConcept(
                          concept="us-gaap_WeightedAverageNumberOfSharesOutstandingBasic",
                          label="Shares Basic"),
                      StandardConcept(
                          concept="us-gaap_WeightedAverageNumberOfDilutedSharesOutstanding",
                          label="Shares Diluted"),
                  ]
                  )
CashFlowStatement = StandardStatement(statement_name="CASH_FLOW",
                  primary_concept="us-gaap_StatementOfCashFlowsAbstract",
                  display_name="Consolidated Statement of Cash Flows",
                  concepts=[
                      StandardConcept(concept="us-gaap_NetCashProvidedByUsedInOperatingActivitiesAbstract",
                                      label="Operating Activities:"),
                      StandardConcept(concept="us-gaap_AdjustmentsToReconcileNetIncomeLossToCashProvidedByUsedInOperatingActivitiesAbstract",
                                      label="Adjustments to Net Income:"),
                      StandardConcept(concept="us-gaap_ShareBasedCompensation",
                                      label="Stock-based Compensation"),
                      StandardConcept(concept="us-gaap_IncreaseDecreaseInOperatingCapitalAbstract",
                                      label="Changes in Working Capital:"),
                      StandardConcept(concept="us-gaap_IncreaseDecreaseInInventories",
                                      label="Inventories"),
                      StandardConcept(concept="us-gaap_NetCashProvidedByUsedInOperatingActivities",
                                      label="Net Cash from Operations"),
                      StandardConcept(concept="us-gaap_NetCashProvidedByUsedInInvestingActivitiesAbstract",
                                      label="Investing Activities:"),
                      StandardConcept(concept="us-gaap_PaymentsToAcquirePropertyPlantAndEquipment",
                                      label="Capital Expenditures"),
                      StandardConcept(concept="us-gaap_NetCashProvidedByUsedInInvestingActivities",
                                      label="Net Cash from Investing"),
                      StandardConcept(concept="us-gaap_NetCashProvidedByUsedInFinancingActivitiesAbstract",
                                      label="Financing Activities:"),
                      StandardConcept(concept="us-gaap_PaymentsForRepurchaseOfCommonStock",
                                      label="Stock Repurchases"),
                      StandardConcept(concept="us-gaap_NetCashProvidedByUsedInFinancingActivities",
                                      label="Net Cash from Financing"),
                      StandardConcept(concept="us-gaap_CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents",
                                      label="Total Cash and Equivalents"),
                      StandardConcept(concept="us-gaap_CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalentsPeriodIncreaseDecreaseIncludingExchangeRateEffect",
                                      label="Net Change in Cash"),
                  ]
)
StatementOfChangesInEquity = StandardStatement(statement_name="EQUITY",
                                               primary_concept="us-gaap_StatementOfStockholdersEquityAbstract",
                                               display_name="Consolidated Statement of Shareholders Equity",
                                               concepts=[
                                                   StandardConcept(concept="us-gaap_CommonStockMember",
                                                                   label="Common Stock"),
                                                   StandardConcept(concept="us-gaap_AdditionalPaidInCapitalMember",
                                                                   label="Additional Paid-in Capital"),
                                                   StandardConcept(
                                                       concept="us-gaap_AccumulatedOtherComprehensiveIncomeMember",
                                                       label="Accumulated Other Comprehensive Income (Loss)"),
                                                   StandardConcept(concept="us-gaap_RetainedEarningsMember",
                                                                   label="Retained Earnings"),
                                                   StandardConcept(concept="us-gaap_StatementLineItems",
                                                                   label="Statement [Line Items]"),
                                                   StandardConcept(
                                                       concept="us-gaap_IncreaseDecreaseInStockholdersEquityRollForward",
                                                       label="Increase (Decrease) in Stockholders' Equity [Roll Forward]"),
                                                   StandardConcept(
                                                       concept="us-gaap_AdjustmentsToAdditionalPaidInCapitalSharebasedCompensationRequisiteServicePeriodRecognitionValue",
                                                       label="Stock-based compensation"),
                                               ]
                                               )
StatementOfComprehensiveIncome = StandardStatement(statement_name="COMPREHENSIVE_INCOME",
                                                   primary_concept="us-gaap_StatementOfIncomeAndComprehensiveIncomeAbstract"
                                                   , display_name="Comprehensive Income Statement",
                                                   concepts=[
                                                       StandardConcept(
                                                           concept="us-gaap_StatementOfIncomeAndComprehensiveIncomeAbstract",
                                                           label="Statement of Comprehensive Income"),
                                                       StandardConcept(concept="us-gaap_ComprehensiveIncomeNetOfTax",
                                                                       label="Comprehensive income"),
                                                   ]
                                                   )
cover_page = StandardStatement(statement_name="COVER_PAGE",
                               primary_concept="dei_CoverAbstract",
                               display_name="Cover Page",
                               concepts=[])


class Financials:

    """
    A convenience class to extract and work with financial statements from an XBRL filing.
    Wraps and XbrlData object and provides methods to extract standard financial statements
    """

    @staticmethod
    def _filter_standard_statement(statement: Statement, standard_statement: StandardStatement) -> Statement:
        if statement is None:
            return None

        standard_concepts = {concept.concept for concept in standard_statement.concepts}
        standard_labels = {concept.concept: concept.label for concept in standard_statement.concepts}

        df = statement.data.reset_index()
        df = df[df['concept'].isin(standard_concepts)]
        df['label'] = df['concept'].map(standard_labels)
        df = df.set_index('label')

        return Statement(
            df=df,
            definition=statement.definition,
            name=statement.name,
            display_name=standard_statement.display_name,
            entity=statement.entity
        )

    @classmethod
    def get_standard_name(cls, role_name: str) -> Optional[str]:
        role_name_normalized = ''.join(char.upper() for char in role_name if char.isalnum())
        for standard_name, variations in FinancialStatementMapper.STANDARD_STATEMENTS.items():
            if any(variation in role_name_normalized for variation in variations):
                return standard_name
        return None

    def __init__(self, xbrl_data: XBRLData):
        self.xbrl_data: XBRLData = xbrl_data
        self.presentation: XBRLPresentation = xbrl_data.presentation

    @classmethod
    def extract(cls, filing) -> Optional['Financials']:
        return run_async_or_sync(cls.extract_async(filing))

    @classmethod
    async def extract_async(cls, filing) -> Optional['Financials']:
        assert filing.form in ['10-K', '10-Q', '10-K/A', '10-Q/A'], "Filing must be a 10-K or 10-Q"
        xbrl_data = await XBRLData.from_filing(filing)
        if not xbrl_data:
            return None
        return cls(xbrl_data)

    def _get_statement_name_for_standard_name(self, standard_statement: StandardStatement) -> Optional[str]:
        role = self.xbrl_data.presentation.get_role_by_standard_name(standard_statement.statement_name)
        if not role:
            role = self.find_role_by_concept(standard_statement.primary_concept)
        if role:
            statement_name = role.split('/')[-1]
            return statement_name

    @cached_property
    def balance_sheet(self):
        return self.get_balance_sheet()

    def get_balance_sheet(self, standard: bool = False) -> Statement:
        """
        Retrieves the Balance Sheet (Statement of Financial Position).

        This statement provides a snapshot of the company's financial position at a specific point in time,
        showing its assets, liabilities, and shareholders' equity.

        Returns:
            Statement: The Balance Sheet data, or None if not found.
        """
        statement_name = self._get_statement_name_for_standard_name(BalanceSheet)
        if statement_name:
            statement = self.xbrl_data.get_statement(statement_name, display_name="Consolidated Balance Sheets")
            if standard and statement:
                return self._filter_standard_statement(statement, BalanceSheet)
            return statement

    @cached_property
    def income(self):
        return self.get_income_statement()

    def get_income_statement(self, standard: bool = False) -> Optional[Statement]:
        """
        Retrieves the Income Statement (Statement of Operations).

        This statement shows the company's revenues, expenses, and resulting profit or loss over a specific period.
        It may also be referred to as the Profit and Loss Statement (P&L) or Statement of Earnings.

        Returns:
            Statement: The Income Statement data, or None if not found.
        """
        statement_name = self._get_statement_name_for_standard_name(IncomeStatement)
        if statement_name:
            statement = self.xbrl_data.get_statement(statement_name,
                                                     display_name="Income Statements") if statement_name else None
            if standard and statement:
                return self._filter_standard_statement(statement, IncomeStatement)
            return statement

    @cached_property
    def cashflow(self):
        return self.get_cash_flow_statement()

    def get_cash_flow_statement(self, standard: bool = False) -> Statement:
        """
        Retrieves the Statement of Cash Flows.

        This statement shows how changes in balance sheet accounts and income affect cash and cash equivalents,
        breaking the analysis down into operating, investing, and financing activities.

        Returns:
            Statement: The Cash Flow Statement data, or None if not found.
        """
        statement_name = self._get_statement_name_for_standard_name(CashFlowStatement)
        if statement_name:
            statement = self.xbrl_data.get_statement(statement_name,
                                                     display_name="Consolidated Statement of Cash Flows")
            if standard and statement:
                return self._filter_standard_statement(statement, CashFlowStatement)
            return statement

    @cached_property
    def equity(self):
        return self.get_statement_of_changes_in_equity()

    def get_statement_of_changes_in_equity(self, standard: bool = False) -> Statement:
        """
        Retrieves the Statement of Changes in Equity (Statement of Stockholders' Equity).

        This statement shows the changes in the company's equity over a period, including items such as
        share capital, retained earnings, and other equity items.

        Returns:
            Statement: The Statement of Changes in Equity data, or None if not found.
        """
        statement_name = self._get_statement_name_for_standard_name(StatementOfChangesInEquity)
        if statement_name:
            statement = self.xbrl_data.get_statement(statement_name,
                                                     display_name="Consolidated Statement of Shareholders Equity")
            if standard and statement:
                return self._filter_standard_statement(statement, StatementOfChangesInEquity)
            return statement

    @cached_property
    def comprehensive_income(self):
        return self.get_statement_of_comprehensive_income()

    def get_statement_of_comprehensive_income(self, standard: bool = False) -> Statement:
        """
        Retrieves the Statement of Comprehensive Income.

        This statement shows all changes in equity during a period, except those resulting from
        investments by owners and distributions to owners. It includes both net income from the
        Income Statement and other comprehensive income items.

        Returns:
            Statement: The Statement of Comprehensive Income data, or None if not found.
        """
        statement_name = self._get_statement_name_for_standard_name(StatementOfComprehensiveIncome)
        if statement_name:
            statement = self.xbrl_data.get_statement(statement_name,
                                                     display_name="Comprehensive Income Statement")
            if standard and statement:
                return self._filter_standard_statement(statement, StatementOfComprehensiveIncome)
            return statement

    @cached_property
    def cover(self):
        return self.get_cover_page()

    def get_cover_page(self) -> Statement:
        """
        Retrieves the Document and Entity Information.

        This is not a financial statement per se, but contains important metadata about the filing entity
        and the document itself, such as company name, filing date, and other regulatory information.

        Returns:
            Statement: The Document and Entity Information data, or None if not found.
        """
        statement_name = self._get_statement_name_for_standard_name(cover_page)
        if statement_name:
            return self.xbrl_data.get_statement(statement_name, display_name="Cover Page")

    def find_role_by_concept(self, concept: str) -> Optional[str]:
        """
        Helper method to find a role containing specific concepts.

        Args:
            primary_concept str: Concept names to search for.

        Returns:
            Optional[str]: The role containing the most matching concepts, or None if no matches found.
        """
        role_matches = defaultdict(int)
        for role in self.xbrl_data.presentation.get_roles_containing_concept(concept):
            role_matches[role] += 1

        return max(role_matches, key=role_matches.get) if role_matches else None

    def list_standard_statements(self) -> List[str]:
        return [
            standard_statement.display_name
            for standard_statement in [cover_page, BalanceSheet, IncomeStatement, CashFlowStatement,
                                       StatementOfChangesInEquity, StatementOfComprehensiveIncome]
            if self._get_statement_name_for_standard_name(standard_statement) is not None
        ]

    def get_dimensioned_statement(self, statement_name: str, dimensions: Dict[str, str]) -> Optional[Statement]:
        return self.xbrl_data.generate_dimensioned_statement(statement_name, dimensions)

    def pivot_statement(self, statement_name: str, dimension: str) -> pd.DataFrame:
        return self.xbrl_data.pivot_on_dimension(statement_name, dimension)

    def compare_statement_dimensions(self, statement_name: str, dimension: str, value1: str,
                                     value2: str) -> pd.DataFrame:
        return self.xbrl_data.compare_dimension_values(statement_name, dimension, value1, value2)

    def __rich__(self):
        title = Text.assemble((self.xbrl_data.company, "bold deep_sky_blue1"),
                              " Financials"
                              )
        subtitle  = Text.assemble(("Period ending ", "grey70"), (f"{datefmt(self.xbrl_data.period_end, '%B %d, %Y')}", "bold"))
        statements_table = Table(Column(""), Column("Standard Financial Statements",
                                                    justify="left"),
                                 box=box.ROUNDED,
                                 show_header=False,
                                 title=title,
                                 caption=subtitle)
        for index, statement in enumerate(self.list_standard_statements()):
            statements_table.add_row(str(index + 1), Text(statement, style="bold"))
        return statements_table

    def __repr__(self):
        return repr_rich(self.__rich__())


class MultiFinancials:
    """
    Merges the financial statements from multiple periods into a single financials.
    """

    def __init__(self, filings):
        self.financials_list = []
        for filing in filings:
            if filing.form not in ['10-K', '10-Q', '10-K/A', '10-Q/A']:
                raise ValueError("Filing must be a 10-K or 10-Q")
            financials = Financials.extract(filing)
            self.financials_list.append(financials)
        self.primary_financials = self.financials_list[0] if self.financials_list else None

    @classmethod
    async def extract_async(cls, filings) -> 'MultiFinancials':
        tasks = []
        for filing in filings:
            if filing.form not in ['10-K', '10-Q', '10-K/A', '10-Q/A']:
                continue
            tasks.append(Financials.extract_async(filing))

        financials_results = await asyncio.gather(*tasks)
        financials_list = [f for f in financials_results if f is not None]

        multi_financials = cls.__new__(cls)
        multi_financials.financials_list = financials_list
        multi_financials.primary_financials = financials_list[0] if financials_list else None
        return multi_financials

    @classmethod
    def extract(cls, filings) -> 'MultiFinancials':
        return run_async_or_sync(cls.extract_async(filings))


    @classmethod
    def stitch(cls, financials_list: List[Financials]) -> 'MultiFinancials':
        return cls(financials_list)

    @staticmethod
    def merge_preserving_order(df0, df1) -> pd.DataFrame:
        # Ensure 'label' is the index and 'concept' is a column
        df0 = df0.reset_index().set_index('label') if df0.index.name != 'label' else df0
        df1 = df1.reset_index().set_index('label') if df1.index.name != 'label' else df1

        # Define metadata columns
        metadata_cols = [col for col in ['segment', 'level', 'decimals', 'style']
                            if col in df0.columns or col in df1.columns]

        # Identify period columns
        period_cols0 = [col for col in df0.columns if col not in metadata_cols and col != 'concept']
        period_cols1 = [col for col in df1.columns if col not in metadata_cols and col != 'concept']

        # Create dictionaries to store the original order of labels in both dataframes
        order_dict0 = {label: i for i, label in enumerate(df0.index)}
        order_dict1 = {label: i for i, label in enumerate(df1.index)}

        # Perform an outer merge
        merged_df = pd.merge(df0, df1, left_index=True, right_index=True, how='outer', suffixes=('_0', '_1'))

        # Custom sorting function
        def custom_sort(label):
            in_df0 = label in order_dict0
            in_df1 = label in order_dict1

            if in_df0:
                return (0, order_dict0[label])  # Prioritize df0 order
            elif in_df1:
                return (1, order_dict1[label])  # Next priority: unique to df1
            else:
                return (2, 0)  # Should not happen with outer merge

        # Sort the merged dataframe using the custom sorting function
        merged_df['sort_key'] = merged_df.index.map(custom_sort)
        merged_df = merged_df.sort_values('sort_key').drop('sort_key', axis=1)

        # Combine all columns (period, concept, and metadata)
        all_columns = sorted(set(period_cols0 + period_cols1), reverse=True) + ['concept'] + metadata_cols

        for col in all_columns:
            if f'{col}_0' in merged_df.columns and f'{col}_1' in merged_df.columns:
                # Use numpy where to prioritize df0 values
                merged_df[col] = np.where(merged_df[f'{col}_0'].notna(), merged_df[f'{col}_0'], merged_df[f'{col}_1'])
                merged_df = merged_df.drop([f'{col}_0', f'{col}_1'], axis=1)
            elif f'{col}_0' in merged_df.columns:
                merged_df = merged_df.rename(columns={f'{col}_0': col})
            elif f'{col}_1' in merged_df.columns:
                merged_df = merged_df.rename(columns={f'{col}_1': col})

        # Handle specific column dtypes
        merged_df['level'] = pd.to_numeric(merged_df['level'], errors='coerce').astype('Int64')

        # Replace NaN with pd.NA in all columns
        for col in merged_df.columns:
            if merged_df[col].dtype == 'object':
                merged_df[col] = merged_df[col].astype('string')
            merged_df[col] = merged_df[col].fillna(pd.NA)

        # Group by concept and aggregate
        def agg_func(x):
            return x.iloc[0] if len(x) > 0 else pd.NA

        merged_df = merged_df.reset_index().groupby('concept').agg({
            'label': 'first',  # Keep the first label for each concept
            **{col: agg_func for col in merged_df.columns if col not in ['concept', 'label']}
        }).reset_index()

        # Restore the original order
        original_order = {label: i for i, label in enumerate(df0.index)}
        original_order.update({label: i + len(df0) for i, label in enumerate(df1.index) if label not in original_order})

        merged_df['sort_key'] = merged_df['label'].map(lambda x: original_order.get(x, len(original_order)))
        merged_df = merged_df.sort_values('sort_key').drop('sort_key', axis=1)

        # Set 'label' as index
        merged_df = merged_df.set_index('label')

        # Select final columns and order them: period columns, concept, metadata columns
        period_columns = sorted(set(period_cols0 + period_cols1), reverse=True)
        final_columns = period_columns + ['concept'] + metadata_cols
        merged_df = merged_df[final_columns]

        return merged_df

    def _stitch_statements(self, statement_getter):
        if not self.financials_list:
            return None

        statements = [statement_getter(f) for f in self.financials_list if statement_getter(f) is not None]
        if not statements:
            return None

        # Use the first (most recent) statement as a base
        base_statement = statements[0]
        result_df = base_statement.data

        for statement in statements[1:]:
            result_df = self.merge_preserving_order(result_df, statement.data)

        # Create a new Statement object
        stitched_statement = Statement(
            df=result_df,
            definition=base_statement.definition,
            name=base_statement.name,
            display_name=base_statement.display_name,
            entity=base_statement.entity
        )

        return stitched_statement

    @cached_property
    def balance_sheet(self, standard: bool = True) -> Optional[Statement]:
        return self.get_balance_sheet(standard=standard)

    @lru_cache(maxsize=1)
    def get_balance_sheet(self, standard: bool = True) -> Optional[Statement]:
        return self._stitch_statements(lambda f: f.get_balance_sheet(standard=standard))

    @cached_property
    def income(self, standard: bool = True) -> Optional[Statement]:
        return self.get_income_statement(standard=standard)

    @lru_cache(maxsize=1)
    def get_income_statement(self, standard: bool = True) -> Optional[Statement]:
        return self._stitch_statements(lambda f: f.get_income_statement(standard=standard))

    @cached_property
    def cashflow(self, standard: bool = True) -> Optional[Statement]:
        return self.get_cash_flow_statement(standard=standard)

    @lru_cache(maxsize=1)
    def get_cash_flow_statement(self, standard: bool = True) -> Optional[Statement]:
        return self._stitch_statements(lambda f: f.get_cash_flow_statement(standard=standard))

    @cached_property
    def comprehensive_income(self, standard: bool = True) -> Optional[Statement]:
        return self.get_statement_of_comprehensive_income(standard=standard)

    @lru_cache(maxsize=1)
    def get_statement_of_comprehensive_income(self, standard: bool = True) -> Optional[Statement]:
        return self._stitch_statements(lambda f: f.get_statement_of_comprehensive_income(standard=standard))

    def list_standard_statements(self) -> List[str]:
        if not self.primary_financials:
            return []
        return self.primary_financials.list_standard_statements()

    def __rich__(self):
        if not self.primary_financials:
            return Panel("No financial data available")

        statements_table = Table(Column(""), Column("Standard Financial Statements", justify="left"),
                                 box=box.ROUNDED, show_header=True)
        for index, statement in enumerate(self.list_standard_statements()):
            statements_table.add_row(str(index + 1), statement)

        contents = [statements_table]

        panel = Panel(
            Group(*contents),
            title=Text.assemble((self.primary_financials.xbrl_data.company, "bold deep_sky_blue1"), " financials",
                                (f" ({len(self.financials_list)} periods)", "bold green")),
        )
        return panel

    def __repr__(self):
        return repr_rich(self.__rich__())
