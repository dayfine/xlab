use technical_indicator::{HistoricalTechnicalIndicatorProvider, TechnicalIndicatorType};
use time::Duration;
use trading_system::{TechnicalTradingSystem, TradingSignal};

pub struct MovingAverageCrossoverTradingSystem<'a> {
    faster_num_periods: i32,
    slower_num_periods: i32,
    ti_provider: &'a dyn HistoricalTechnicalIndicatorProvider,
}

fn ma_type(num_periods: i32) -> Result<TechnicalIndicatorType> {
    match num_periods {
        5 => TechnicalIndicatorType::ExponentialMovingAverage5d,
        20 => TechnicalIndicatorType::ExponentialMovingAverage20d,
        _ => None,
    };
}

impl<'a> TechnicalTradingSystem for MovingAverageCrossoverTradingSystem<'a> {
    fn generate_trading_signal(
        &self,
        security_id: &security_id_lib::SecurityId,
        date: chrono::NaiveDate,
    ) -> Result<Option<TradingSignal>> {
        let faster_ma_type = ma_type(self.faster_num_periods)?;
        let slower_ma_type = ma_type(self.slower_num_periods)?;

        let current_faster_ma: f64 =
            self.ti_provider
                .get_technical_indicator(security_id, date, faster_ma_type)?;
        let current_slower_ma: f64 =
            self.ti_provider
                .get_technical_indicator(security_id, date, slower_ma_type)?;

        let previous_date = date.checked_sub_signed(Duration::days(1)).unwrap();
        let previous_faster_ma: f64 =
            self.ti_provider
                .get_technical_indicator(security_id, previous_date, faster_ma_type)?;
        let previous_slower_ma: f64 =
            self.ti_provider
                .get_technical_indicator(security_id, previous_date, slower_ma_type)?;

        if ((current_faster_ma > current_slower_ma) && (previous_faster_ma < previous_slower_ma)) {
            return Some(TradingSignal {
                side: order::TradeSide::Long,
            });
        }

        if ((current_faster_ma < current_slower_ma) && (previous_faster_ma > previous_slower_ma)) {
            return Some(TradingSignal {
                side: order::TradeSide::Short,
            });
        }

        return None;
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_no_crossover_generates_no_trading_signal() {}

    #[test]
    fn test_crossover_generates_long_signal() {}

    #[test]
    fn test_crossunder_generates_short_signal() {}
}
