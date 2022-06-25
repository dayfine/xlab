use trading_system::{TechnicalTradingSystem, TradingSignal};

pub struct MovingAverageCrossoverTradingSystem<'a> {
    price_provider: &'a dyn price_provider_lib::HistoricalPriceProvider,
    technical_indicator_provider: &'a dyn technical_indicator::HistoricalTechnicalIndicatorProvider,
}

impl<'a> TechnicalTradingSystem for MovingAverageCrossoverTradingSystem<'a> {
    fn generate_trading_signal(
        &self,
        security_id: &security_id_lib::SecurityId,
        date: chrono::NaiveDate,
    ) -> Option<TradingSignal> {
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
