use super::types::TechnicalIndicatorType;

pub trait HistoricalTechnicalIndicatorProvider {
    fn get_price(
        &self,
        id: &security_id_lib::SecurityId,
        date: chrono::NaiveDate,
        indicator_type: TechnicalIndicatorType,
    ) -> f64;
}
