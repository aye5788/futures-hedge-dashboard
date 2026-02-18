def calculate_beta_exposure(portfolio_value, portfolio_beta):
    return portfolio_value * portfolio_beta


def calculate_futures_notional(mes_contracts, mes_multiplier, spx_level, direction):
    notional_per_contract = mes_multiplier * spx_level
    sign = -1 if direction == "SHORT" else 1
    return mes_contracts * notional_per_contract * sign


def calculate_full_hedge_contracts(beta_exposure, mes_multiplier, spx_level):
    notional_per_contract = mes_multiplier * spx_level
    return beta_exposure / notional_per_contract

