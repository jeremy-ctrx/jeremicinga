from src.risk.risk_manager import (
    DailyLossTracker,
    RiskLimitExceeded,
    compute_position_size,
    enforce_min_risk_reward,
)


def test_compute_position_size_basic():
    result = compute_position_size(
        equity=100, risk_per_trade_pct=1.0,
        entry_price=2000, stop_loss_price=1990, take_profit_price=2020,
    )
    assert result.risk_amount == 1.0
    assert result.position_size_units == 0.1
    assert result.risk_reward == 2.0


def test_compute_position_size_rejects_excessive_risk():
    try:
        compute_position_size(
            equity=100, risk_per_trade_pct=5.0,
            entry_price=2000, stop_loss_price=1990, take_profit_price=2020,
        )
        assert False, "devrait lever RiskLimitExceeded"
    except RiskLimitExceeded:
        pass


def test_enforce_min_risk_reward():
    try:
        enforce_min_risk_reward(1.5, min_risk_reward=2.0)
        assert False, "devrait lever RiskLimitExceeded"
    except RiskLimitExceeded:
        pass

    enforce_min_risk_reward(2.5, min_risk_reward=2.0)  # ne doit pas lever


def test_daily_loss_tracker_blocks_after_limit():
    tracker = DailyLossTracker(starting_equity=100, max_daily_loss_pct=3.0)
    assert tracker.trading_allowed() is True

    tracker.record_trade_result(-3.5)
    assert tracker.trading_allowed() is False
