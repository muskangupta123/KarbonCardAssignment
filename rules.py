import datetime

class FLAGS:
    GREEN = 1
    AMBER = 2
    RED = 0
    MEDIUM_RISK = 3  # display purpose only
    WHITE = 4  # data is missing for this field

# Constant for revenue threshold
REVENUE_THRESHOLD = 50_000_000

def latest_financial_index(data: dict):
    """
    Determine the index of the latest standalone financial entry in the data.
    """
    for index, financial in enumerate(data.get("financials", [])):
        if financial.get("nature") == "STANDALONE":
            return index
    return 0

def total_revenue(data: dict, financial_index):
    """
    Calculate the total revenue from the financial data at the given index.
    """
    try:
        financials = data["financials"][financial_index]
        pnl = financials.get("pnl", {})
        line_items = pnl.get("lineItems", {})
        net_revenue = line_items.get("Net Revenue", 0)
        return net_revenue
    except (IndexError, KeyError) as e:
        print(f"Error in total_revenue: {e}")
        return 0

def total_borrowing(data: dict, financial_index):
    """
    Calculate the ratio of total borrowings to total revenue for the financial data at the given index.
    """
    try:
        financials = data["financials"][financial_index]
        bs = financials.get("bs", {})
        line_items = bs.get("lineItems", {})
        long_term_borrowings = line_items.get("Long Term Borrowings", 0)
        short_term_borrowings = line_items.get("Short Term Borrowings", 0)
        total_borrowings = long_term_borrowings + short_term_borrowings

        revenue = total_revenue(data, financial_index)
        if revenue == 0:
            return 0
        return total_borrowings / revenue
    except (IndexError, KeyError) as e:
        print(f"Error in total_borrowing: {e}")
        return 0

def iscr_flag(data: dict, financial_index):
    """
    Determine the flag color based on the Interest Service Coverage Ratio (ISCR) value.
    """
    iscr_value = iscr(data, financial_index)
    return FLAGS.GREEN if iscr_value >= 2 else FLAGS.RED

def total_revenue_5cr_flag(data: dict, financial_index):
    """
    Determine the flag color based on whether the total revenue exceeds the defined threshold.
    """
    revenue = total_revenue(data, financial_index)
    return FLAGS.GREEN if revenue >= REVENUE_THRESHOLD else FLAGS.RED

def iscr(data: dict, financial_index):
    """
    Calculate the Interest Service Coverage Ratio (ISCR) for the financial data at the given index.
    """
    try:
        financials = data["financials"][financial_index]
        pnl = financials.get("pnl", {})
        line_items = pnl.get("lineItems", {})
        ebitda = line_items.get("Profit Before Interest and Tax", 0)
        depreciation = line_items.get("Depreciation", 0)
        interest_expense = line_items.get("Interest Expenses", 1)  # Default to 1 to avoid division by zero

        # Calculate ISCR value
        iscr_value = (ebitda + depreciation + 1) / (interest_expense + 1)
        return iscr_value
    except (IndexError, KeyError) as e:
        print(f"Error in iscr: {e}")
        return 0

def borrowing_to_revenue_flag(data: dict, financial_index):
    """
    Determine the flag color based on the ratio of total borrowings to total revenue.
    """
    borrowing_ratio = total_borrowing(data, financial_index)
    return FLAGS.GREEN if borrowing_ratio <= 0.25 else FLAGS.AMBER
