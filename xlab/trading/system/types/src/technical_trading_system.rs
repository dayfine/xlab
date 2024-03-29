use super::trading_signal::TradingSignal;

pub trait TechnicalTradingSystem {
    fn generate_trading_signal(
        &self,
        security_id: &security_id_lib::SecurityId,
        date: chrono::NaiveDate,
    ) -> Result<Option<TradingSignal>, status::Status>;
}
