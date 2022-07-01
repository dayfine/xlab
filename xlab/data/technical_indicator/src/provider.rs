use super::types::TechnicalIndicatorType;

#[cfg(test)]
use mockall::{automock, mock, predicate::*};
#[cfg_attr(test, automock)]
pub trait HistoricalTechnicalIndicatorProvider {
    fn get_technical_indicator(
        &self,
        id: &security_id_lib::SecurityId,
        date: chrono::NaiveDate,
        indicator_type: TechnicalIndicatorType,
    ) -> Result<f64, status::Status>;
}
