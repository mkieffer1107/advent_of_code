/*============ Day 3:Rucksack Reorganization ============*/
/*
    Each line of input represents a rucksack

    Each rucksack has two compartments of the same size
        - first half of input is first compartment, second ...
        - each char represents a different item (case-sensitive)
        - each item in these halves are globally unique, except for one shared item
    
    We assign a priority to each item
        - lowercase item types 'a' through 'z' have priorities 1 through 26
        - uppercase item types 'A' through 'Z' have priorities 27 through 52

    Sources:
        - https://www.educative.io/answers/what-is-stringchars-in-rust
*/

use std::fs::File;
use std::io::{BufRead, BufReader};
use std::collections::HashSet;


// for every rucksack, store each container's items in a HashSet 
fn read_input(path: &str) -> Vec<(HashSet::<i8>, HashSet::<i8>)> {

    // each rucksack contains two containers, represented as sets
    // let rucksacks: Vec<(HashSet::<i8>, HashSet::<i8>)> = Vec::new();

    // read the file
    let f = File::open(path).expect("Unable to open file");
    let f = BufReader::new(f);

    // read each line in file and collect into vector
    let lines: Vec<String> = f.lines().map(|line| line.expect("Unable to read line")).collect();
    
    // anonynous function to add each item in compartment to a HashSet
    let create_comp = |contents: &str| {

        // create a single compartment
        let mut compartment: HashSet::<i8> = HashSet::<i8>::new();

        // ascii for 'A' is 65: 65 - 38 = 27
        // ascii for 'a' is 97: 97 - 96 = 1

        // contents.chars().map(|c| compartment.insert(c as i8 - if c.is_uppercase() {'A' as i8 - 27} else {'a' as i8 - 1});
        
        // for each item in string (.char() is char iter), convert the char to a number and add to compartment set 
        for c in contents.chars() {
            // compartment.insert(c as i8 - if c.is_uppercase() {38} else {96});
            
            // map 'A' -> 27 and 'a'-> 1 by subtracting their ascii value to get to 0 and adding desired value back on (-(-a) = +a)
            compartment.insert(c as i8 - if c.is_uppercase() {'A' as i8 - 27} else {'a' as i8 - 1});
        }
 
        // return single compartment
        compartment
    };

    // return all rucksacks as a tuple of HashSets: rucksack = ({compartment_1}, {compartment_2})
    lines.iter()
        .map(|line| line.split_at(line.len()/2)) // split each line into two equally-size vectors (rucksack has two compartments)
        .map(|(comp_1, comp_2)| (create_comp(comp_1), create_comp(comp_2))) // create two compartments for each rucksack
        .collect() // add all (HashSet::<i8>, HashSet::<i8>) tuples to vector (each tuple is a rucksack with its compartments)
}


/*
    Find the item type that appears in both compartments of each rucksack. 
    What is the sum of the priorities of those item types?
*/
fn task_one(input: &Vec<(HashSet::<i8>, HashSet::<i8>)>) -> i32 {
    // let mut sum_of_priorities: i32 = 0;

    // iterate over each rucksack and sum the intersection of each compartment
    // for rucksack in input.iter() {

    //     let comp_1: &HashSet::<i8> = &rucksack.0;
    //     let comp_2: &HashSet::<i8> = &rucksack.1;

    //     let intersections: HashSet<_> = comp_1.intersection(&comp_2).collect();

    //     for intersection in intersections.iter() {
    //         sum_of_priorities += **intersection as i32;
    //     }
    // }

    // sum_of_priorities

    // condensed version
    input.iter()
        .map(|(comp_1, comp_2)| comp_1.intersection(comp_2).sum::<i8>()) // sum the intersection of each compartment
        .map(|sum| sum as i32) // convert to i32
        .sum() // sum all rucksack intersections
}


/*
    Find the item type that corresponds to the badges of each three-Elf group. 
    What is the sum of the priorities of those item types?
*/
fn task_two(input: &Vec<(HashSet::<i8>, HashSet::<i8>)>) -> i32 {

    // let mut sum_of_priorities: i32 = 0;

    // // get every group of three in list
    // for i in (0..input.len()).step_by(3) {

    //     // rucksacks: Vec<(HashSet::<i8>, HashSet::<i8>)>
    //     let rucksack_1: &(HashSet::<i8>, HashSet::<i8>) = &input[i]; 
    //     let rucksack_2: &(HashSet::<i8>, HashSet::<i8>) = &input[i+1]; 
    //     let rucksack_3: &(HashSet::<i8>, HashSet::<i8>) = &input[i+2]; 

    //     // combine all items in each rucksack
    //     // let items_in_1: HashSet::<i8> = rucksack_1.0.extend(&rucksack_1.1);
    //     let items_in_1: HashSet::<i8> = rucksack_1.0.union(&rucksack_1.1).copied().collect();
    //     let items_in_2: HashSet::<i8> = rucksack_2.0.union(&rucksack_2.1).copied().collect();
    //     let items_in_3: HashSet::<i8> = rucksack_3.0.union(&rucksack_3.1).copied().collect();

    //     // take the intersection of these items
    //     let intersection1: HashSet::<i8> = items_in_1.intersection(&items_in_2).copied().collect();
    //     let intersection2: Vec<&i8> = intersection1.intersection(&items_in_3).collect();

    //     // there will be only one intersection between each group of three elves
    //     let id: i32 = *intersection2[0] as i32;

    //     sum_of_priorities += id;

    //     let intersection: HashSet::<i8> = items_in_1.intersection(&items_in_2).intersection(&items_in_3).copied().collect();
    // }

    // sum_of_priorities

    
    // slighty more condensed version
    (0..input.len()).step_by(3)
    .map(|i| {
        // rucksacks: Vec<(HashSet::<i8>, HashSet::<i8>)>
        let rucksack_1: &(HashSet::<i8>, HashSet::<i8>) = &input[i]; 
        let rucksack_2: &(HashSet::<i8>, HashSet::<i8>) = &input[i+1]; 
        let rucksack_3: &(HashSet::<i8>, HashSet::<i8>) = &input[i+2]; 

        // combine all items in each rucksack
        let items_in_1: HashSet::<i8> = rucksack_1.0.union(&rucksack_1.1).copied().collect();
        let items_in_2: HashSet::<i8> = rucksack_2.0.union(&rucksack_2.1).copied().collect();
        let items_in_3: HashSet::<i8> = rucksack_3.0.union(&rucksack_3.1).copied().collect();

        // take the intersection of these items
        let intersection1: HashSet::<i8> = items_in_1.intersection(&items_in_2).copied().collect();
        let intersection2: Vec<&i8> = intersection1.intersection(&items_in_3).collect();

        // there will be only one intersection between each group of three elves
        *intersection2[0] as i32
    })
    .sum()


    // (0..input.len()).step_by(3)
    // .map(|i| {
    //     (i..i+3).step_by(1)
    //     .map(|j| {
    //         // combine all items in each rucksack
    //         &input[j].0.union(&input[j].1).copied().collect::<HashSet<i8>>();
    //     })
    // });
}



fn main() {
    let input: Vec<(HashSet::<i8>, HashSet::<i8>)> = read_input("input.txt");

    let task1: i32 = task_one(&input);
    println!("task 1: {task1}");
    
    let task2: i32 = task_two(&input);
    println!("task 2: {task2}");
}