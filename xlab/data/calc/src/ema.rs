#[macro_use]
extern crate approx;

const SMOOTHING_FACTOR: f64 = 2.0;

// https://www.investopedia.com/terms/e/ema.asp
pub fn compute_ema(last_ema: f64, price: f64, num_periods: i32) -> f64 {
    let alpha = SMOOTHING_FACTOR / f64::from(num_periods + 1);
    return alpha * price + last_ema * (1.0 - alpha);
}

pub fn compute_ema_initial(prices: impl IntoIterator<Item = f64>, num_periods: i32) -> f64 {
    let mut price_iter = prices.into_iter();
    let mut ema: f64 = price_iter.nth(0).unwrap_or(0.0);
    for price in price_iter {
        ema = compute_ema(ema, price, num_periods);
    }
    return ema;
}

#[cfg(test)]
mod tests {
    use super::*;

    const ALLOWED_ERR: f64 = 1e-8;

    #[test]
    fn test_calculate_initial_ema_20() {
        let price_data: [f64; 20] = [
            56.07, 56.02, 56.08, 56.81, 56.53, 56.59, 57.07, 57.55, 57.79, 57.70, 57.23, 57.17,
            57.96, 58.95, 59.23, 59.41, 59.82, 60.08, 59.62, 59.85,
        ];
        assert_abs_diff_eq!(
            compute_ema_initial(price_data, 20),
            58.255796513052346,
            epsilon = ALLOWED_ERR
        );
    }

    #[test]
    fn test_calculate_incremental_ema_20() {
        assert_abs_diff_eq!(
            compute_ema(/*last_ema=*/ 58.46, /*price=*/ 60.84, /*num_periods=*/ 20),
            58.68666666666667,
            epsilon = ALLOWED_ERR
        );
    }
}
