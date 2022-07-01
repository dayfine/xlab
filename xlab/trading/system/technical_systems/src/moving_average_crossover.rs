use security_id_lib::SecurityId;
use technical_indicator::{HistoricalTechnicalIndicatorProvider, TechnicalIndicatorType};
use trading_system::{TechnicalTradingSystem, TradingSignal};

pub struct MovingAverageCrossoverTradingSystem<'a> {
    fast_num_periods: i32,
    slow_num_periods: i32,
    ti_provider: &'a dyn HistoricalTechnicalIndicatorProvider,
}

fn ma_type(num_periods: i32) -> Result<TechnicalIndicatorType, status::Status> {
    match num_periods {
        5 => Ok(TechnicalIndicatorType::ExponentialMovingAverage5d),
        20 => Ok(TechnicalIndicatorType::ExponentialMovingAverage20d),
        _ => Err(status::not_found_error(&format!(
            "No indicator available for {}d",
            num_periods
        ))),
    }
}

impl<'a> TechnicalTradingSystem for MovingAverageCrossoverTradingSystem<'a> {
    fn generate_trading_signal(
        &self,
        security_id: &SecurityId,
        date: chrono::NaiveDate,
    ) -> Result<Option<TradingSignal>, status::Status> {
        let fast_ma_type = ma_type(self.fast_num_periods)?;
        let slow_ma_type = ma_type(self.slow_num_periods)?;

        let current_fast_ma: f64 =
            self.ti_provider
                .get_technical_indicator(security_id, date, fast_ma_type)?;
        let current_slow_ma: f64 =
            self.ti_provider
                .get_technical_indicator(security_id, date, slow_ma_type)?;

        let previous_date = date.checked_sub_signed(chrono::Duration::days(1)).unwrap();
        let previous_fast_ma: f64 =
            self.ti_provider
                .get_technical_indicator(security_id, previous_date, fast_ma_type)?;
        let previous_slow_ma: f64 =
            self.ti_provider
                .get_technical_indicator(security_id, previous_date, slow_ma_type)?;

        if (current_fast_ma > current_slow_ma) && (previous_fast_ma < previous_slow_ma) {
            return Ok(Some(TradingSignal {
                side: order::TradeSide::Long,
            }));
        }

        if (current_fast_ma < current_slow_ma) && (previous_fast_ma > previous_slow_ma) {
            return Ok(Some(TradingSignal {
                side: order::TradeSide::Short,
            }));
        }

        return Ok(None);
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use mockall::{automock, mock, predicate::*};

    #[test]
    fn test_no_crossover_generates_no_trading_signal() {
        let mut mock_ti_provider = MockHistoricalTechnicalIndicatorProvider::new();

        let security_id = SecurityId { symbol: "GOOG" };
        let date = chrono::NaiveDate::from_ymd(2022, 2, 5);
        let prev_date = chrono::NaiveDate::from_ymd(2022, 2, 4);

        let system = MovingAverageCrossoverTradingSystem {
            fast_num_periods: 5,
            slow_num_periods: 20,
            ti_provider: &mock_ti_provider,
        };

        mock_ti_provider
            .expect_get_technical_indicator()
            .with(
                eq(security_id),
                eq(date),
                eq(TechnicalIndicatorType::ExponentialMovingAverage5d),
            )
            .times(1)
            .returning(1.0);

        mock_ti_provider
            .expect_get_technical_indicator()
            .with(
                eq(security_id),
                eq(date),
                eq(TechnicalIndicatorType::ExponentialMovingAverage20d),
            )
            .times(1)
            .returning(2.0);

        mock_ti_provider
            .expect_get_technical_indicator()
            .with(
                eq(security_id),
                eq(prev_date),
                eq(TechnicalIndicatorType::ExponentialMovingAverage20d),
            )
            .times(1)
            .returning(1.0);

        mock_ti_provider
            .expect_get_technical_indicator()
            .with(
                eq(security_id),
                eq(prev_date),
                eq(TechnicalIndicatorType::ExponentialMovingAverage20d),
            )
            .times(1)
            .returning(2.0);

        assert_eq!(system.generate_trading_signal(security_id, date), Ok(None));
    }

    #[test]
    fn test_crossover_generates_long_signal() {}

    #[test]
    fn test_crossunder_generates_short_signal() {}
}
