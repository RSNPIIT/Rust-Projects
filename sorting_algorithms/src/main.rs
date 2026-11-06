//! Project 022: Classic Sorting Suite
//! Demonstrates Bubble, Selection, Insertion, Merge, and Quick Sort on generic slices.

pub fn bubble_sort<T: Ord>(arr: &mut [T]) {
    let n = arr.len();
    for i in 0..n {
        for j in 0..n.saturating_sub(i + 1) {
            if arr[j] > arr[j + 1] {
                arr.swap(j, j + 1);
            }
        }
    }
}

pub fn insertion_sort<T: Ord + Copy>(arr: &mut [T]) {
    for i in 1..arr.len() {
        let key = arr[i];
        let mut j = i;
        while j > 0 && arr[j - 1] > key {
            arr[j] = arr[j - 1];
            j -= 1;
        }
        arr[j] = key;
    }
}

pub fn quick_sort<T: Ord + Copy>(arr: &mut [T]) {
    if arr.len() <= 1 { return; }
    let pivot = arr[arr.len() / 2];
    let mut left = 0;
    let mut right = arr.len() - 1;

    while left <= right {
        while arr[left] < pivot { left += 1; }
        while arr[right] > pivot {
            if right == 0 { break; }
            right -= 1;
        }
        if left <= right {
            arr.swap(left, right);
            left += 1;
            if right > 0 { right -= 1; }
        }
    }

    if right > 0 { quick_sort(&mut arr[0..=right]); }
    if left < arr.len() { quick_sort(&mut arr[left..]); }
}

fn main() {
    println!("=== 🦀 Project 022: Classic Sorting Suite ===");
    let mut data1 = [64, 34, 25, 12, 22, 11, 90];
    bubble_sort(&mut data1);
    println!("Bubble sorted:    {:?}", data1);

    let mut data2 = [64, 34, 25, 12, 22, 11, 90];
    insertion_sort(&mut data2);
    println!("Insertion sorted: {:?}", data2);

    let mut data3 = [64, 34, 25, 12, 22, 11, 90];
    quick_sort(&mut data3);
    println!("Quick sorted:     {:?}", data3);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sorts() {
        let mut v = vec![5, 2, 8, 1, 9];
        quick_sort(&mut v);
        assert_eq!(v, vec![1, 2, 5, 8, 9]);
    }
}
