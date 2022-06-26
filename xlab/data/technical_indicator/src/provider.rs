use super::types::TechnicalIndicatorType;

extern crate chrono;
extern crate security_id_lib;

pub trait HistoricalTechnicalIndicatorProvider {
    fn get_price(
        id: &security_id_lib::SecurityId,
        date: chrono::NaiveDate,
        indicator_type: TechnicalIndicatorType,
    ) -> f64;
}
