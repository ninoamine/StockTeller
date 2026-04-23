def format_mad(amount: float) -> str:
    """Format an amount in Moroccan Dirham."""
    return f"{amount:,.2f} MAD"


def calc_price_change_pct(old: float, new: float) -> float:
    """Calculate the percentage change between two prices.

    Args:
        old: the old price
        new: the new price

    Returns:
        the percentage change from the old price to the new price

    Raises:
        ValueError: if old is zero
    """
    if old == 0:
        raise ValueError("old price cannot be zero")
    return (new - old) / old * 100