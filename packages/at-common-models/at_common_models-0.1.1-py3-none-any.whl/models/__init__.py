# Import all models to register them with SQLAlchemy
from models.stock.overview import OverviewModel
from models.stock.daily_candlestick import DailyCandlestickModel
from models.stock.daily_indicator import DailyIndicatorModel
from models.stock.quotation import QuotationModel
from models.stock.financials.annual_balance_sheet_statement import AnnualBalanceSheetStatementModel
from models.stock.financials.quarter_balance_sheet_statement import QuarterBalanceSheetStatementModel
from models.stock.financials.annual_income_statement import AnnualIncomeStatementModel
from models.stock.financials.quarter_income_statement import QuarterlyIncomeStatementModel
from models.stock.financials.annual_cashflow_statement import AnnualCashFlowStatementModel
from models.stock.financials.quarter_cashflow_statement import QuarterCashflowStatementModel
from models.news.article import NewsArticleModel
from models.news.stock import NewsStockModel

# These imports will register all models with the Base.metadata
__all__ = [
    'OverviewModel',
    'DailyCandlestickModel',
    'DailyIndicatorModel',
    'QuotationModel',
    'AnnualBalanceSheetStatementModel',
    'QuarterBalanceSheetStatementModel',
    'AnnualIncomeStatementModel',
    'QuarterlyIncomeStatementModel',
    'AnnualCashFlowStatementModel',
    'QuarterCashflowStatementModel',
    'NewsArticleModel',
    'NewsStockModel'
]
