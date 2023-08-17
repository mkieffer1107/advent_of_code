'''
                              --- Day 4: Camp Cleanup ---

  resources:
    pipe operator: https://elixirschool.com/en/lessons/basics/pipe_operator
    reading files: https://elixir-lang.org/getting-started/io-and-the-file-system.html
    lists vs tuples: https://www.tutorialspoint.com/elixir/elixir_lists_and_tuples.htm

  notes:
    - File.read() returns {:ok, "content"} (a tuple)
    - File.read!() returns "content" (function raises an error if error reading file)
    - Lists are linked lists,
    - Tuples are arrays
    - Enum.each(list, lambda_fn) -> iterate over each item in list and apply function (return :ok, not a list)
    - Enum.map(list, lambda_fn) -> one-to-one mapping of each element in list to a new list via lambda_fn
'''

defmodule Solution do
  # read a file and return nested lists for each line "lowA-highA,lowB-highB" -> [[lowA, highA],[lowB, highB]]
  defp read_input(path) do
    path
    |> File.read!()                                 # read file
    |> String.split("\n", trim: true)               # add each line to a List [lowA-highA,lowB-highB]
    |> Enum.map(fn(line) -> parse_line(line) end)   # format each line as [[lowA, highA],[lowB, highB]]
  end


  # parse a line into nested lists: [[lowA-highA],[lowB-highB]] -> [[lowA, highA],[lowB, highB]]
  defp parse_line(line) do
    line
    |> String.split(",")                            # [lowA-highA,lowB-highB] -> [[lowA-highA],[lowB-highB]]
    |> Enum.map(fn(intervals) ->                    # iterate over the two intervals in the line
        intervals
        |> String.split("-")                        # [[lowA-highA],[lowB-highB]] -> [[lowA, highA],[lowB, highB]]
        |> Enum.map(fn (num) -> String.to_integer(num) end)  # convert every string to an integer
        # |> Enum.map(fn x -> IO.write("#{x} ") end)         # print values
    end)
    # IO.puts ""
  end


  # count the number of pairs of intervals where one interval is a subset of the other
  #       lowA-------highA
  #         lowB--highB
  defp task_one(input) do
    Enum.reduce(input, 0, fn(line, acc) ->
      [[lowA, highA], [lowB, highB]] = line
      if (lowA <= lowB and highB <= highA) or (lowB <= lowA and highA <= highB) do
        acc + 1
      else
        acc + 0
      end
    end)
  end



  # count the number of pairs of intervals where A intersection B != null set
  #    lowA---highA
  #         lowB---highB
  defp task_two(input) do
    Enum.reduce(input, 0, fn(line, acc) ->
      [[lowA, highA], [lowB, highB]] = line
      if (lowA <= highB) and (lowB <= highA), do: acc + 1, else: acc
        # acc + 1
      # else
        # acc + 0
      # end
    end)
  end


  def run() do
    input = read_input("input.txt")
    IO.puts "task 1: #{task_one(input)}"
    IO.puts "task 2: #{task_two(input)}"
  end
end
