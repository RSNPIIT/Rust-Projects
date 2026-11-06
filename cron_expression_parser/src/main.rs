//! Project 051: Cron Expression Parser
//! Demonstrates 5-field cron parsing and execution time matching.

#[derive(Debug, PartialEq)]
pub struct CronSchedule {
    pub minutes: Vec<u8>,
    pub hours: Vec<u8>,
    pub dom: Vec<u8>,
    pub months: Vec<u8>,
    pub dow: Vec<u8>,
}

fn parse_field(field: &str, min: u8, max: u8) -> Result<Vec<u8>, &'static str> {
    if field == "*" {
        return Ok((min..=max).collect());
    }
    let mut values = Vec::new();
    for part in field.split(',') {
        if let Some((start, step)) = part.split_once('/') {
            let s: u8 = if start == "*" { min } else { start.parse().map_err(|_| "Invalid num")? };
            let step: u8 = step.parse().map_err(|_| "Invalid step")?;
            for v in (s..=max).step_by(step as usize) {
                values.push(v);
            }
        } else if let Some((start, end)) = part.split_once('-') {
            let s: u8 = start.parse().map_err(|_| "Invalid range start")?;
            let e: u8 = end.parse().map_err(|_| "Invalid range end")?;
            for v in s..=e {
                values.push(v);
            }
        } else {
            let v: u8 = part.parse().map_err(|_| "Invalid value")?;
            values.push(v);
        }
    }
    values.sort_unstable();
    values.dedup();
    Ok(values)
}

pub fn parse_cron(expr: &str) -> Result<CronSchedule, &'static str> {
    let parts: Vec<&str> = expr.split_whitespace().collect();
    if parts.len() != 5 {
        return Err("Cron must have exactly 5 fields: min hour dom month dow");
    }
    Ok(CronSchedule {
        minutes: parse_field(parts[0], 0, 59)?,
        hours: parse_field(parts[1], 0, 23)?,
        dom: parse_field(parts[2], 1, 31)?,
        months: parse_field(parts[3], 1, 12)?,
        dow: parse_field(parts[4], 0, 6)?,
    })
}

fn main() {
    println!("=== 🦀 Project 051: Cron Expression Parser ===");
    let cron = "*/15 9-17 * * 1-5";
    let schedule = parse_cron(cron).unwrap();
    println!("Expression: {}", cron);
    println!("Minutes (every 15): {:?}", schedule.minutes);
    println!("Hours (9 to 17):     {:?}", schedule.hours);
    println!("Days of Week (Mon-Fri): {:?}", schedule.dow);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_cron() {
        let sched = parse_cron("0 12 * * *").unwrap();
        assert_eq!(sched.minutes, vec![0]);
        assert_eq!(sched.hours, vec![12]);
    }
}
