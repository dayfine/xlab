extern crate portfolio_rust_proto;

#[macro_use]
extern crate approx;

use self::portfolio_rust_proto::{Position, PositionLot, SettlementType_Enum};

// Updates a position for a position change, e.g. shares / contracts in
// this position being bought / sold, and returns the P&L of the transaction.
pub fn update_position(position: &mut Position, change: &PositionLot) -> f64 {
    // Adding to existing position, no realized profit or loss.
    if !is_offseting(change, position) {
        position.mut_lots().push(change.clone());
        return 0.0;
    }

    // An offset transaction realizes some profit or loss.
    let multiplier = get_multiplier(position);
    let mut lots_to_perseve = 0;
    let mut pnl = 0.0;
    let mut change_size = change.get_size();
    // FIFO. TODO(dayfine): Validate time order.
    for lot in position.mut_lots().iter_mut() {
        if can_offset_lot(change_size, lot) {
            pnl += get_lot_pnl(lot, change.get_cost(), multiplier);
            lots_to_perseve += 1;
            change_size += lot.get_size()
        } else {
            let mut lot_to_partially_offest = PositionLot::new();
            lot_to_partially_offest.set_size(-change_size);
            lot_to_partially_offest.set_cost(lot.get_cost());
            pnl += get_lot_pnl(&lot_to_partially_offest, change.get_cost(), multiplier);
            // Offset the remaining change with this lot.
            lot.size += change_size;
            change_size = 0.0;
            break;
        }
    }
    // TODO: simplify this.
    if change_size != 0.0 {
        let mut remaining_change = change.clone();
        remaining_change.set_size(change_size);
        position.clear_lots();
        position.mut_lots().push(remaining_change);
    } else {
        *position.mut_lots() = position
            .take_lots()
            .into_iter()
            .enumerate()
            .filter(|(i, _)| i >= &lots_to_perseve)
            .map(|(_, lot)| lot)
            .collect();
    }

    position.realized_profit_and_loss += pnl;
    pnl
}

// Marks a position to its mark value given the spot price, and returns the
// realized profit and loss. The cost basis of the position will be updated to
// the spot price. This only applies to securities settled in future type
// settlement.
pub fn mark_to_market(position: &mut Position, price: f64) -> f64 {
    if get_settlement_type(position) != SettlementType_Enum::FUTURE {
        return 0.0;
    }

    let multiplier = get_multiplier(position);
    let mut pnl = 0.0;
    for lot in position.mut_lots().iter_mut() {
        pnl += get_lot_pnl(lot, price, multiplier);
        lot.set_cost(price);
    }
    position.realized_profit_and_loss += pnl;
    pnl
}

pub fn get_unrealized_pnl(position: &Position, price: f64) -> f64 {
    if get_settlement_type(position) != SettlementType_Enum::STOCK {
        return 0.0;
    }

    let multiplier = get_multiplier(position);
    position
        .get_lots()
        .iter()
        .fold(0.0, |pnl, lot| pnl + get_lot_pnl(lot, price, multiplier))
}

fn can_offset_lot(change_size: f64, lot: &PositionLot) -> bool {
    if change_size == 0.0 || lot.get_size() == 0.0 {
        false
    } else if lot.get_size() > 0.0 {
        -change_size >= lot.get_size()
    } else if lot.get_size() < 0.0 {
        -change_size <= lot.get_size()
    } else {
        false
    }
}

fn is_offseting(change: &PositionLot, position: &Position) -> bool {
    let position_size = total_size(position);
    if change.get_size() == 0.0 || position_size == 0.0 {
        return false;
    }
    change.get_size().signum() != position_size.signum()
}

fn get_multiplier(position: &Position) -> f64 {
    position.get_security().get_contract_info().get_multiplier() as f64
}

fn get_settlement_type(position: &Position) -> SettlementType_Enum {
    position
        .get_security()
        .get_contract_info()
        .get_settle_type()
}

fn total_size(position: &Position) -> f64 {
    position
        .get_lots()
        .iter()
        .fold(0.0, |size, lot| size + lot.get_size())
}

fn get_lot_pnl(lot: &PositionLot, txn_price: f64, multiplier: f64) -> f64 {
    // Note the size can be negative, i.e. for calculating the P&L of a short
    // transaction. For example, if price bought back is lower than proceeds
    // received initially, the transaction makes profit.
    lot.get_size() * multiplier * (txn_price - lot.get_cost())
}

#[cfg(test)]
mod test {
    use super::*;

    const ALLOWED_ERR: f64 = 1e-8;

    fn make_position(settle_type: SettlementType_Enum, multiplier: i32) -> Position {
        let mut pos = Position::new();
        {
            let contract = pos.mut_security().mut_contract_info();
            contract.set_multiplier(multiplier);
            contract.set_settle_type(settle_type);
        }
        pos
    }

    fn make_transaction(price: f64, size: f64) -> PositionLot {
        let mut txn = PositionLot::new();
        txn.set_size(size);
        txn.set_cost(price);
        txn
    }

    #[test]
    fn test_computing_pnl_for_closing_long_position() {
        let mut pos = make_position(SettlementType_Enum::STOCK, 1);
        {
            pos.mut_lots().push(make_transaction(6.60, 10.0));
        }
        let sale = make_transaction(6.70, -10.0);
        assert_abs_diff_eq!(
            update_position(&mut pos, &sale),
            1.00,
            epsilon = ALLOWED_ERR
        );
    }

    #[test]
    fn test_computing_pnl_for_closing_short_position() {
        let mut pos = make_position(SettlementType_Enum::STOCK, 1);
        {
            pos.mut_lots().push(make_transaction(9.99, -10.0));
        }
        let buy = make_transaction(9.70, 10.0);
        assert_abs_diff_eq!(update_position(&mut pos, &buy), 2.90, epsilon = ALLOWED_ERR);
    }

    #[test]
    fn test_computing_unrealized_pnl() {
        let mut pos = make_position(SettlementType_Enum::STOCK, 1);
        {
            pos.mut_lots().push(make_transaction(9.99, -10.0));
        }
        assert_abs_diff_eq!(
            get_unrealized_pnl(&pos, 10.12),
            -1.30,
            epsilon = ALLOWED_ERR
        );
    }

    #[test]
    fn test_computing_pnl_for_partial_offset_lot() {
        let mut pos = make_position(SettlementType_Enum::STOCK, 1);
        {
            pos.mut_lots().push(make_transaction(4.99, 10.0));
            pos.mut_lots().push(make_transaction(5.03, 10.0));
        }
        let sale = make_transaction(5.01, -5.0);
        assert_abs_diff_eq!(
            update_position(&mut pos, &sale),
            0.10,
            epsilon = ALLOWED_ERR
        );
    }

    #[test]
    fn test_computing_pnl_for_offseting_multiple_lots() {
        let mut pos = make_position(SettlementType_Enum::STOCK, 1);
        {
            pos.mut_lots().push(make_transaction(4.99, 10.0));
            pos.mut_lots().push(make_transaction(5.03, 10.0));
        }
        let sale = make_transaction(5.01, -15.0);
        assert_abs_diff_eq!(
            update_position(&mut pos, &sale),
            0.10,
            epsilon = ALLOWED_ERR
        );
    }

    #[test]
    fn test_computing_pnl_for_changing_direction() {
        let mut pos = make_position(SettlementType_Enum::STOCK, 1);
        {
            pos.mut_lots().push(make_transaction(4.99, 10.0));
            pos.mut_lots().push(make_transaction(5.03, 10.0));
        }
        let sale = make_transaction(5.01, -25.0);
        assert_abs_diff_eq!(
            update_position(&mut pos, &sale),
            0.00,
            epsilon = ALLOWED_ERR
        );
        assert_eq!(pos.get_lots(), &[make_transaction(5.01, -5.0)]);
    }

    #[test]
    fn test_computing_pnl_for_mark_to_market() {
        let mut pos = make_position(SettlementType_Enum::FUTURE, 1);
        {
            pos.mut_lots().push(make_transaction(2.50, 5.0));
            pos.mut_lots().push(make_transaction(2.00, 15.0));
        }
        assert_abs_diff_eq!(mark_to_market(&mut pos, 2.50), 7.5, epsilon = ALLOWED_ERR);
        assert_abs_diff_eq!(mark_to_market(&mut pos, 2.25), -5.0, epsilon = ALLOWED_ERR);
    }

    struct TestStep {
        transaction: Option<PositionLot>,
        spot_price: f64,
        realized_pnl: f64,
        unrealized_pnl: f64,
    }

    fn test_series_of_transactions(pos: &mut Position, steps: &[TestStep]) {
        for step in steps {
            let mut realized_pnl = 0.0;
            if let Some(ref txn) = step.transaction {
                realized_pnl += update_position(pos, txn);
            }
            realized_pnl += mark_to_market(pos, step.spot_price);
            assert_abs_diff_eq!(realized_pnl, step.realized_pnl, epsilon = ALLOWED_ERR);
            assert_abs_diff_eq!(
                get_unrealized_pnl(&pos, step.spot_price),
                step.unrealized_pnl,
                epsilon = ALLOWED_ERR
            );
        }
        assert!(pos.get_lots().is_empty());
    }

    #[test]
    fn test_series_of_transactions_with_stock_type_settlement() {
        let mut pos = make_position(SettlementType_Enum::STOCK, 1);

        let steps = &[
            TestStep {
                transaction: Some(make_transaction(53.0, 1200.0)),
                spot_price: 53.0,
                realized_pnl: 0.0,
                unrealized_pnl: 0.0,
            },
            TestStep {
                transaction: Some(make_transaction(57.0, -500.0)),
                spot_price: 57.0,
                realized_pnl: 2000.0,
                unrealized_pnl: 2800.0,
            },
            TestStep {
                transaction: None,
                spot_price: 51.0,
                realized_pnl: 0.0,
                unrealized_pnl: -1400.0,
            },
            TestStep {
                transaction: Some(make_transaction(54.0, -700.0)),
                spot_price: 53.0,
                realized_pnl: 700.0,
                unrealized_pnl: 0.0,
            },
        ];

        test_series_of_transactions(&mut pos, steps);
    }

    #[test]
    fn test_series_of_transactions_with_future_type_settlement() {
        let mut pos = make_position(SettlementType_Enum::FUTURE, 100);

        let steps = &[
            TestStep {
                transaction: Some(make_transaction(75.0, -9.0)),
                spot_price: 75.0,
                realized_pnl: 0.0,
                unrealized_pnl: 0.0,
            },
            TestStep {
                transaction: None,
                spot_price: 77.0,
                realized_pnl: -1800.0,
                unrealized_pnl: 0.0,
            },
            TestStep {
                transaction: Some(make_transaction(74.0, 2.0)),
                spot_price: 74.0,
                realized_pnl: 2700.0,
                unrealized_pnl: 0.0,
            },
            TestStep {
                transaction: Some(make_transaction(70.0, 4.0)),
                spot_price: 70.0,
                realized_pnl: 2800.0,
                unrealized_pnl: 0.0,
            },
            TestStep {
                transaction: Some(make_transaction(80.0, 3.0)),
                spot_price: 80.0,
                realized_pnl: -3000.0,
                unrealized_pnl: 0.0,
            },
        ];

        test_series_of_transactions(&mut pos, steps);
    }
}
