/*============ Day 1: Calorie Counting ============*/
    
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::collections::BinaryHeap;
use std::cmp::Reverse;


// https://stackoverflow.com/questions/31192956/whats-the-de-facto-way-of-reading-and-writing-files-in-rust-1-x
// BufReader for line by line
fn read_input(path: &str) -> Vec<String> {
    let mut input: Vec<String> = Vec::new();

    let f = File::open(path).expect("Unable to open file");
    let f = BufReader::new(f);
    
    for line in f.lines() {
        let line = line.expect("Unable to read line");
        input.push(line);
    }

    input
}


// find the highest total calorie count 
fn task_one(input: &Vec<String>) -> i32 {
    
    let mut max: i32 = 0;
    let mut curr_elf_val: i32 = 0;

    for line in input.iter() {
        if !line.eq("") {
            // if line is not empty, add calorie val to current elf
            let curr_val: i32 =  line.parse().unwrap();
            curr_elf_val += curr_val;
        } else {
            // if empty line, check previous curr_elf_val and prepare for new elf
            if curr_elf_val > max {
                max = curr_elf_val;
            }
            curr_elf_val = 0;
        }
    }

    max
}


// work smart, not hard 

// find sum of top k calorie counts
fn task_two(input: &Vec<String>) -> i32 {
    
    let k: usize = 3;
    let mut curr_elf_val: i32 = 0;
    let mut all_calorie_values: Vec<i32> = Vec::new();

    for line in input.iter() {
        if !line.eq("") {
            // if line is not empty, add calorie val to current elf
            let curr_val: i32 =  line.parse().unwrap();
            curr_elf_val += curr_val;
        } else {
            // if empty line, check previous curr_elf_val and prepare for new elf
            all_calorie_values.push(curr_elf_val);
            curr_elf_val = 0;
        }
    }

    // sort all elves in ascending order by calorie count
    all_calorie_values.sort();

    // access final k values in sorted list 
    let mut top_k_calories: i32 = 0;
    let len = all_calorie_values.len()-1;

    for i in 0..k {
        top_k_calories += all_calorie_values[len-i]
    }

    top_k_calories
}


fn main() {
    let input: Vec<String> = read_input("input.txt");

    let task1: i32 = task_one(&input);
    println!("task 1: {}", task1);
    
    let task2: i32 = task_two(&input);
    println!("task 2: {}", task2);
}






// min-heap annoying to work with... how to unwrap Reverse(i32)?
// fn task_two(input: Vec<String>) -> i32 {
    
//     let k: usize = 3;
//     let mut curr_elf_val: i32 = 0;

//     // create a min-heap to easily check 3rd smallest value
//     let mut top_k_elves = BinaryHeap::new();

//     for line in input.iter() {

//         if !line.eq("") {
//             // if line is not empty, add calorie val to current elf
//             let curr_val: i32 =  line.parse().unwrap();
//             curr_elf_val += curr_val;
//         } else {
//             // if the k vals are stored and elf calorie count is smaller than the 
//             // smallest value in the min-heap, then continue
//             let lowest_calorie_count: i32 = 0;

//             if top_k_elves.len() == k && curr_elf_val < top_k_elves.peek() {
//                 continue;
//             }

//             // otherwise push to the min-heap
//             top_k_elves.push(Reverse(curr_elf_val));

//             // remove the smallest element if the size is greater than k
//             if top_k_elves.len() > k {
//                 top_k_elves.pop();
//             }

//             // prepare for new elf
//             curr_elf_val = 0;
//         }
//     }

//     // sum up the top k calorie counts
//     let mut total_calories: i32 = 0;
//     for elf_calorie_val in top_k_elves.iter() {
//         total_calories += *elf_calorie_val;
//     }

//     total_calories
// }
