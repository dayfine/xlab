use std::collections::HashMap;

use security_id_lib::SecurityId;
use technical_indicator::{HistoricalTechnicalIndicatorProvider, TechnicalIndicatorType};

#[derive(Hash, Eq, PartialEq, Debug)]
pub struct Key {
    symbol: String,
    date: chrono::NaiveDate,
    indicator_type: TechnicalIndicatorType,
}

impl Key {
    pub fn new(
        security_id: &SecurityId,
        date: chrono::NaiveDate,
        indicator_type: TechnicalIndicatorType,
    ) -> Key {
        Key {
            symbol: security_id.symbol.clone(),
            date,
            indicator_type,
        }
    }
}

pub struct MemHistoricalTechnicalIndicatorProvider {
    data: HashMap<Key, f64>,
}

impl MemHistoricalTechnicalIndicatorProvider {
    pub fn new(data: HashMap<Key, f64>) -> MemHistoricalTechnicalIndicatorProvider {
        MemHistoricalTechnicalIndicatorProvider { data }
    }
}

impl HistoricalTechnicalIndicatorProvider for MemHistoricalTechnicalIndicatorProvider {
    fn get_technical_indicator(
        &self,
        id: &security_id_lib::SecurityId,
        date: chrono::NaiveDate,
        indicator_type: TechnicalIndicatorType,
    ) -> Result<f64, status::Status> {
        match self.data.get(&Key::new(id, date, indicator_type)) {
            Some(&value) => Ok(value),
            _ => Err(status::not_found_error(&format!(
                "Cannot find technical indidactor for {} {} {}",
                id.symbol, date, indicator_type
            ))),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_lookup_known_value() {
        let security_id = SecurityId {
            symbol: "GOOG".to_string(),
        };
        let date = chrono::NaiveDate::from_ymd(2000, 06, 30);
        let ti_type = TechnicalIndicatorType::ExponentialMovingAverage5d;

        let mut data = HashMap::new();

        data.insert(Key::new(&security_id, date, ti_type), 100.10);

        let ti_provider = MemHistoricalTechnicalIndicatorProvider::new(data);

        assert_eq!(
            ti_provider.get_technical_indicator(&security_id, date, ti_type),
            Ok(100.10)
        );

        {
            let result = ti_provider.get_technical_indicator(
                &security_id,
                chrono::NaiveDate::from_ymd(2000, 06, 29),
                ti_type,
            );
            assert!(result.is_err());
            assert_eq!(
                result.err().unwrap().status_code,
                status::StatusCode::NotFound
            );
        }

        {
            let result = ti_provider.get_technical_indicator(
                &security_id,
                date,
                TechnicalIndicatorType::ExponentialMovingAverage20d,
            );
            assert!(result.is_err());
            assert_eq!(
                result.err().unwrap().status_code,
                status::StatusCode::NotFound
            );
        }
    }
}
