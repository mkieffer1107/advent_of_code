/*

        --- Day 6: Tuning Trouble ---
*/
#include <iostream>
#include <fstream>
#include <queue>
#include <unordered_set>
using namespace std;

string read_input(string path)
{
    // single line input
    string content;
    ifstream file(path);
    getline(file,content);  
    file.close();
    return content;
}

// given a running input of characters, determine how many characters
// need to be processed before the first start-of-packet marker is detected
// (when the first unique four-digit sequenece appears)
int task_one(string input)
{
    const char MAX_VAL = 4;
    unsigned int count = 0;
    queue<char> q;

    for (char c : input)
    {   
        // increment count and add char to queue
        count++;
        q.push(c);

        // only keep the 4 most recent characters
        if (q.size() > MAX_VAL)
            q.pop();

        // check if 4 most recent values are unique
        queue<char> copy = q;
        unordered_set<char> check;

        while (!copy.empty())
        {
            check.insert(copy.front());
            copy.pop();
        }

        if (check.size() == MAX_VAL)
            return count;
    }

    return count;
}

// now find the first 14-character unique sequence
int task_two(string input)
{
    const char MAX_VAL = 14;
    unsigned int count = 0;
    queue<char> q;

    for (char c : input)
    {   
        // increment count and add char to queue
        count++;
        q.push(c);

        // only keep the 4 most recent characters
        if (q.size() > MAX_VAL)
            q.pop();

        // check if 4 most recent values are unique
        queue<char> copy = q;
        unordered_set<char> check;

        while (!copy.empty())
        {
            check.insert(copy.front());
            copy.pop();
        }

        if (check.size() == MAX_VAL)
            return count;
    }

    return count;
}

int main()
{
    string input = read_input("input.txt");
    cout << "task 1: " << task_one(input) << endl;
    cout << "task 2: " << task_two(input) << endl;
    return 0;
}