//! Project 002: Temperature Converter
//! Demonstrates enums with methods, traits, and unit conversions.

use std::fmt;

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum TemperatureScale {
    Celsius,
    Fahrenheit,
    Kelvin,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Temperature {
    pub value: f64,
    pub scale: TemperatureScale,
}

impl Temperature {
    pub fn new(value: f64, scale: TemperatureScale) -> Self {
        Self { value, scale }
    }

    pub fn to_celsius(self) -> Self {
        let c = match self.scale {
            TemperatureScale::Celsius => self.value,
            TemperatureScale::Fahrenheit => (self.value - 32.0) * 5.0 / 9.0,
            TemperatureScale::Kelvin => self.value - 273.15,
        };
        Self::new(c, TemperatureScale::Celsius)
    }

    pub fn to_fahrenheit(self) -> Self {
        let f = match self.scale {
            TemperatureScale::Celsius => (self.value * 9.0 / 5.0) + 32.0,
            TemperatureScale::Fahrenheit => self.value,
            TemperatureScale::Kelvin => ((self.value - 273.15) * 9.0 / 5.0) + 32.0,
        };
        Self::new(f, TemperatureScale::Fahrenheit)
    }

    pub fn to_kelvin(self) -> Self {
        let k = match self.scale {
            TemperatureScale::Celsius => self.value + 273.15,
            TemperatureScale::Fahrenheit => ((self.value - 32.0) * 5.0 / 9.0) + 273.15,
            TemperatureScale::Kelvin => self.value,
        };
        Self::new(k, TemperatureScale::Kelvin)
    }
}

impl fmt::Display for Temperature {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let symbol = match self.scale {
            TemperatureScale::Celsius => "°C",
            TemperatureScale::Fahrenheit => "°F",
            TemperatureScale::Kelvin => "K",
        };
        write!(f, "{:.2}{}", self.value, symbol)
    }
}

fn main() {
    println!("=== 🦀 Project 002: Temperature Converter ===");
    let water_boiling = Temperature::new(100.0, TemperatureScale::Celsius);
    println!("Boiling point: {}", water_boiling);
    println!("In Fahrenheit: {}", water_boiling.to_fahrenheit());
    println!("In Kelvin:     {}", water_boiling.to_kelvin());

    let body_temp = Temperature::new(98.6, TemperatureScale::Fahrenheit);
    println!("\nHuman body temp: {}", body_temp);
    println!("In Celsius:     {}", body_temp.to_celsius());
    println!("In Kelvin:      {}", body_temp.to_kelvin());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_celsius_to_fahrenheit() {
        let c = Temperature::new(0.0, TemperatureScale::Celsius);
        let f = c.to_fahrenheit();
        assert!((f.value - 32.0).abs() < 1e-4);
    }

    #[test]
    fn test_round_trip() {
        let k = Temperature::new(300.0, TemperatureScale::Kelvin);
        let round_trip = k.to_celsius().to_fahrenheit().to_kelvin();
        assert!((round_trip.value - 300.0).abs() < 1e-3);
    }
}
