//! Project 008: Prime Sieve & Factorizer
//! Demonstrates Sieve of Eratosthenes and prime factorization.

pub fn sieve_of_eratosthenes(limit: usize) -> Vec<usize> {
    if limit < 2 {
        return Vec::new();
    }
    let mut is_prime = vec![true; limit + 1];
    is_prime[0] = false;
    is_prime[1] = false;

    let p_limit = (limit as f64).sqrt() as usize;
    for p in 2..=p_limit {
        if is_prime[p] {
            let mut multiple = p * p;
            while multiple <= limit {
                is_prime[multiple] = false;
                multiple += p;
            }
        }
    }

    is_prime
        .iter()
        .enumerate()
        .filter_map(|(idx, &prime)| if prime { Some(idx) } else { None })
        .collect()
}

pub fn prime_factors(mut n: u64) -> Vec<u64> {
    let mut factors = Vec::new();
    while n % 2 == 0 {
        factors.push(2);
        n /= 2;
    }
    let mut d = 3;
    while d * d <= n {
        while n % d == 0 {
            factors.push(d);
            n /= d;
        }
        d += 2;
    }
    if n > 1 {
        factors.push(n);
    }
    factors
}

fn main() {
    println!("=== 🦀 Project 008: Prime Sieve & Factorizer ===");
    let primes_up_to_50 = sieve_of_eratosthenes(50);
    println!("Primes up to 50: {:?}", primes_up_to_50);

    let num = 840;
    println!("Prime factors of {}: {:?}", num, prime_factors(num));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sieve() {
        let primes = sieve_of_eratosthenes(30);
        assert_eq!(primes, vec![2, 3, 5, 7, 11, 13, 17, 19, 23, 29]);
    }

    #[test]
    fn test_factors() {
        assert_eq!(prime_factors(840), vec![2, 2, 2, 3, 5, 7]);
    }
}
