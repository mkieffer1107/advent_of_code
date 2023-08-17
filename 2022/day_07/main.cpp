/*
        --- Day 7: No Space Left On Device ---

    the file structure is basically a tree where dirs are nodes and files are data

*/
#include <iostream>
#include <fstream>
#include <vector>
#include <map>
using namespace std;

struct File
{
    string name;
    int size;
    File(string name, int size) 
    {
        this->name = name;
        this->size = size;
    }

    void print() {cout <<  name << " (file, size=" << to_string(size) << ")" << endl; }
    string string() {return name + " (file, size=" + to_string(size) + ")"; }

};

struct Directory 
{
    string name;
    int size;
    vector<File> files;
    vector<Directory> dirs;
    
    Directory(string name) 
    {
        this->name = name;
        this->size = 0;
    }

    string print()
    {
        print_helper(1);
    }

    string print_helper(int depth)
    {
        // get the number of spaces based on the file depth
        string spaces = "";
        for (int i = 0; i < depth; i++)
            spaces + " ";

        // print out all files in current directory first
        for (File file : files)
        {

        }

        // then print out all directories
        for (Directory dir : dirs) 
        {

        }

    }
    
};




vector<string> read_input(string path)
{
    vector<string> lines;
    ifstream file(path);
    
    string line;
    while(getline(file, line))
        lines.push_back(line);

    file.close();
    return lines;
}

// return max value of two ints
int max(int a, int b)
{
    return (a >= b) ? a : b;
}

int task_one(vector<string> input)
{
    int sum = 0;
    for (string line : input)
    {   
        cout << line << endl;
    }
    return sum;
}

int task_two(vector<string> input)
{

}

int main()
{
    vector<string> input = read_input("input.txt");
    // int test = task_one(input);
    // cout << "task 1: " << task_one(input) << endl;
    // cout << "task 2: " << task_two(input) << endl;


    File test = File("test", 21);

    cout << endl << endl;
    cout << "testing: " << endl;
    cout << endl;
    test.print();
    cout << test.string() << endl;



    return 0;
}