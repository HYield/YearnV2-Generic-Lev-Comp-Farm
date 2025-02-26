import pytest
from brownie import chain
from utils import checks, actions, utils

# TODO: Add tests that show proper operation of this strategy through "emergencyExit"
#       Make sure to demonstrate the "worst case losses" as well as the time it takes


def test_shutdown(chain, token, vault, strategy, amount, gov, user, RELATIVE_APPROX):
    # Deposit to the vault and harvest
    actions.user_deposit(user, vault, token, amount)
    chain.sleep(1)
    strategy.harvest({"from": gov})
    utils.sleep(1)
    assert pytest.approx(strategy.estimatedTotalAssets(), rel=RELATIVE_APPROX) == amount

    # Generate profit
    utils.strategy_status(vault, strategy)
    profit_amount = actions.generate_profit(strategy, 200)
    utils.strategy_status(vault, strategy)
    strategy.setMinCompToSell(1e5)
    # Set debtRatio to 0, then harvest, check that accounting worked as expected
    vault.updateStrategyDebtRatio(strategy, 0, {"from": gov})
    strategy.setCollateralTarget(0.1 * 1e18, {"from": gov})
    strategy.harvest({"from": gov})
    utils.sleep(1)
    chain.mine(5)
    strategy.harvest({"from": gov})
    utils.sleep()
    strategy.harvest({"from": gov})

    status = vault.strategies(strategy).dict()
    utils.strategy_status(vault, strategy)
    assert status["totalGain"] >= profit_amount  # underestimating
    assert pytest.approx(status["totalLoss"], abs=strategy.minWant()) == 0
    assert pytest.approx(status["totalDebt"], abs=strategy.minWant()) == 0
