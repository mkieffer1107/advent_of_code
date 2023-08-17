/*============ Day 2: Rock Paper Scissors ============*/

use std::fs::File;
use std::io::{BufRead, BufReader};
use std::collections::HashMap;


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


/*
             rock paper scissors 
    opponent:   A    B      C
         you:   X    Y      Z

    Calculate your score after playing each match
    from the input file.
*/
fn task_one(input: &Vec<String>) -> i32 {

    let mut points: i32 = 0;

    // your_choice -> (victory, loss, points for choice)
    let outcomes = HashMap::from([
        ('X', ('C', 'B', 1)),
        ('Y', ('A', 'C', 2)),
        ('Z', ('B', 'A', 3)),
    ]);

    // tally points for each match
    for line in input.iter() {
        // split line 
        let chars: Vec<char> = line.chars().collect();
        let opponent_choice = chars[0];
        let your_choice = chars[2];

        // get the various outcomes and # of points for your choice
        let win_condition = outcomes[&your_choice].0;
        let loss_condition = outcomes[&your_choice].1;
        let choice_points = outcomes[&your_choice].2;

        // add up points from match
        if opponent_choice == win_condition {
            points += 6;
        } else if opponent_choice == loss_condition {
            points += 3;
        } else {
            points += 0;
        }

        points += choice_points;
    }

    points
}


/*
    X means you need to lose
    Y means you need to draw
    Z means you need to win

    such a sloppy solution 
*/
fn task_two(input: &Vec<String>) -> i32 {

    let mut points: i32 = 0;

    // your_choice -> (victory, loss, points for choice)
    let outcomes = HashMap::from([
        ('X', ('C', 'B', 1)),
        ('Y', ('A', 'C', 2)),
        ('Z', ('B', 'A', 3)),
    ]);

    // opponent_choice -> (win, loss, draw)
    let complement = HashMap::from([
        ('A', ('Z','Y','X')),
        ('B', ('X','Z','Y')),
        ('C', ('Y','X','Z')),
    ]);

    // tally points for each match
    for line in input.iter() {
        // split line 
        let chars: Vec<char> = line.chars().collect();
        let opponent_choice = chars[0];
        let your_choice = chars[2];


        if your_choice == 'X' {
            // you must lose
            points += 0;
            points += outcomes[&complement[&opponent_choice].0].2
            

        } else if your_choice == 'Y' {
            // you must draw
            points += 3;
            points += outcomes[&complement[&opponent_choice].2].2

        } else {
            // you must win
            points += 6;
            points += outcomes[&complement[&opponent_choice].1].2

        }
    }

    points
}


fn main() {
    let input: Vec<String> = read_input("input.txt");

    let task1: i32 = task_one(&input);
    println!("task 1: {}", task1);
    
    let task2: i32 = task_two(&input);
    println!("task 2: {}", task2);
}