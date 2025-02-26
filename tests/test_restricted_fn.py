import pytest
from brownie import reverts


def test_restricted_fn_user(strategy, user):
    with reverts("!authorized"):
        strategy.setDontClaimComp(False, {"from": user})

    with reverts("!authorized"):
        strategy.setForceMigrate(False, {"from": user})

    with reverts("!authorized"):
        strategy.setMinCompToSell(0, {"from": user})

    with reverts("!authorized"):
        strategy.setMinWant(0, {"from": user})

    with reverts("!authorized"):
        strategy.setCollateralTarget(0, {"from": user})

    with reverts("!authorized"):
        strategy.manualReleaseWant(1, {"from": user})

    with reverts("!authorized"):
        strategy.manualDeleverage(1, {"from": user})

    with reverts("!authorized"):
        strategy.setCollatRatioDAI(1, {"from": user})
    # NO FUNCTIONS THAT CHANGE STRATEGY BEHAVIOR SHOULD BE CALLABLE FROM A USER
    # thus, this may not be used
    # TODO: add all the external functions that should be callably by a user (if any)
    # strategy.setter(arg1, arg2, {'from': user})
    return


def test_restricted_fn_management(strategy, management):
    # ONLY FUNCTIONS THAT DO NOT HAVE RUG POTENTIAL SHOULD BE CALLABLE BY MANAGEMENT
    # (e.g. a change of 3rd party contract => rug potential)
    # (e.g. a change in leverage ratio => no rug potential)
    # TODO: add all the external functions that should not be callable by management (if any)
    with reverts("!authorized"):
        strategy.manualReleaseWant(1, {"from": management})

    with reverts("!authorized"):
        strategy.setForceMigrate(False, {"from": management})

    # Functions that are required to unwind a strategy should go be callable by management
    # TODO: add all the external functions that should be callably by management (if any)
    return


def test_restricted_fn_governance(strategy, gov):
    # OPTIONAL: No functions are required to not be callable from governance so this may not be used
    # TODO: add all the external functions that should not be callable by governance (if any)
    # with reverts("!authorized"):
    #     strategy.setter(arg1, arg2, {'from': gov})

    # All setter functions should be callable by governance
    # TODO: add all the external functions that should be callably by governance (if any)
    # strategy.setter(arg1, arg2, {'from': gov})
    return
