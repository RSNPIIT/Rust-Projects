//! Project 011: Physical Unit Converter
//! Demonstrates trait-based conversions and dimension unit modeling.

#[derive(Debug, PartialEq, Clone, Copy)]
pub enum LengthUnit {
    Meter,
    Kilometer,
    Mile,
    Foot,
    Inch,
}

impl LengthUnit {
    fn to_meters(self, val: f64) -> f64 {
        match self {
            LengthUnit::Meter => val,
            LengthUnit::Kilometer => val * 1000.0,
            LengthUnit::Mile => val * 1609.344,
            LengthUnit::Foot => val * 0.3048,
            LengthUnit::Inch => val * 0.0254,
        }
    }

    fn from_meters(self, meters: f64) -> f64 {
        match self {
            LengthUnit::Meter => meters,
            LengthUnit::Kilometer => meters / 1000.0,
            LengthUnit::Mile => meters / 1609.344,
            LengthUnit::Foot => meters / 0.3048,
            LengthUnit::Inch => meters / 0.0254,
        }
    }

    pub fn convert(from: Self, to: Self, value: f64) -> f64 {
        let meters = from.to_meters(value);
        to.from_meters(meters)
    }
}

fn main() {
    println!("=== 🦀 Project 011: Physical Unit Converter ===");
    let marathon_miles = 26.21875;
    let km = LengthUnit::convert(LengthUnit::Mile, LengthUnit::Kilometer, marathon_miles);
    let meters = LengthUnit::convert(LengthUnit::Mile, LengthUnit::Meter, marathon_miles);
    println!("{:.2} miles = {:.2} km = {:.0} meters", marathon_miles, km, meters);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_conversions() {
        let m = LengthUnit::convert(LengthUnit::Kilometer, LengthUnit::Meter, 1.0);
        assert!((m - 1000.0).abs() < 1e-4);
        let feet = LengthUnit::convert(LengthUnit::Meter, LengthUnit::Foot, 1.0);
        assert!((feet - 3.28084).abs() < 1e-3);
    }
}
