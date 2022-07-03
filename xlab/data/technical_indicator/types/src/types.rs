#[derive(Hash, Copy, Clone, Debug, Eq, PartialEq)]
pub enum TechnicalIndicatorType {
    ExponentialMovingAverage5d = 1,
    ExponentialMovingAverage20d = 2,
}

impl std::fmt::Display for TechnicalIndicatorType {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "{:?}", self)
    }
}
