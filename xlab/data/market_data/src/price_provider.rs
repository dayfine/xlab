pub struct HistoricalPrice {
    open: f64,
    close: f64,
    high: f64,
    low: f64,
}

pub trait HistoricalPriceProvider {
    fn get_price(id: &security_id_lib::SecurityId, date: chrono::NaiveDate) -> HistoricalPrice;
}
