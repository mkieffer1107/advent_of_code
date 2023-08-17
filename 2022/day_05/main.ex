'''
                              --- Day 5: Supply Stacks ---

  resources:
    structs: https://elixir-lang.org/getting-started/structs.html
    maps: https://hexdocs.pm/elixir/1.12/Map.html

  notes:
    - Structs are a special type of Map
    - hell
    - less is more


  The Stack data structure has O(1) time complexity for all functions except print(), which is O(n)

'''

defmodule Stack do
  # store Stack as List, where first value represents the top of the Stack
  defstruct elements: [], size: 0

  def new(items_to_add \\ []) do
    # pass in optional parameter to iteratively build Stack from a List of items
    # if no arg passed in, use default value [], then just return empty Stack becuase nothing to iterate over
    # items will be added to Stack in the order they are listed,
    # e.g., items_ = [1,2,3] -> Stack = {3,2,1}, where 3 is the top of the Stack
    Enum.reduce(
      items_to_add,  # List of items to add [addFirst, addSecond, ...]
      %Stack{},      # initial value of accumulator is empty Stack
      fn item, curr_stack -> push(curr_stack, item) end  # add each element to the running Stack
    )
  end

  def push(stack, element) do
    # return new Stack with element appended to front of List
    # O(1) time complexity for adding to front of linked list
    %Stack{elements: [element|stack.elements], size: stack.size + 1}
  end

  def pop(stack) do
    # return new Stack without top value
    if stack.size > 0 do
      [_|others] = stack.elements
      %Stack{elements: others, size: stack.size - 1}
    else
      # return stack if empty
      stack
    end
  end

  def top(stack) do
    # return top of stack: first element in List
    if stack.size > 0 do
      [top|_] = stack.elements
      top
    else
      # return stack if empty
      nil
    end
  end

  def print(stack) do
    # print values of stack in order last in --> first in
    print_helper(stack.elements)
  end

  defp print_helper([]), do: IO.puts ""
  defp print_helper([top|other]) do
    IO.write "#{top} "
    print_helper(other)
  end
end



defmodule Solution do

  defp read_input(path) do
    path
    |> File.read!()           # split file at double newline character to
    |> String.split("\n\n")   # separate the initial stacks from the commands
  end


  defp move(curr_set) do
    # move single items from stack to stack at a time

    # unpack stacks from current set
    [from_stack, to_stack] = curr_set

    # pop off item from top of from_stack
    to_move = Stack.top(from_stack)
    from_stack = Stack.pop(from_stack)

    # push this item to the to_stack
    to_stack = Stack.push(to_stack, to_move)

    # repackage stacks into set
    [from_stack, to_stack]
  end


  defp move_v2(curr_set, num_to_move) do
    # move multiple items as a single unit from stack to stack at a time

    # unpack stacks from current set
    [from_stack, to_stack] = curr_set

    # pop off all values and add them to a list -- accumulator stores lists of states of vals to move and from_stack
    from_packed = Enum.reduce(1..num_to_move, [[], from_stack], fn(_, acc) ->

      # pop off item from top of from_stack
      from_stack = Enum.at(acc, 1)
      to_move = Stack.top(from_stack)
      from_stack = Stack.pop(from_stack)

      # insert next val into move list
      # [most_recent|_] = acc
      to_move_list = Enum.at(acc, 0)
      to_move_list = [to_move|to_move_list]

      # package current state and add to front of accumulator list
      curr = List.replace_at(acc, 0, to_move_list)
      curr = List.replace_at(curr, 1, from_stack)
      curr
    end)

    # unpack
    to_move = Enum.at(from_packed, 0)
    from_stack = Enum.at(from_packed, 1)

    # push this item to the to_stack
    to_stack = Enum.reduce(to_move, to_stack, fn(val, acc) ->
      Stack.push(acc, val)
    end)

    # repackage stacks into set
    [from_stack,to_stack]
  end


  defp execute_command(command, stacks, version) do
    # parse command
    [_, num_to_move, _, from_index, _, to_index] = String.split(command, " ")

    # IO.puts "move #{num_to_move} from #{from_index} to #{to_index}"

    # convert values to integers
    num_to_move = String.to_integer(num_to_move)
    from_index = String.to_integer(from_index)
    to_index =  String.to_integer(to_index)

    # convert to zero-based indexing
    from_index = from_index - 1
    to_index = to_index - 1

    # get stacks to move from List
    from_stack = Enum.at(stacks, from_index)
    to_stack = Enum.at(stacks, to_index)

    # if we are doing move_v2, then we call the move function once per command
    # otherwise, we call it num_to_move times per command
    num_to_iterate = if version == :v1, do: num_to_move, else: 1

    # move history is a List of every move from from_stack to to_stack where the first
    # element in the List is the most recent move
    # [[from_stack_n, to_stack_n], ...,[from_stack1, to_stack1,[from_stack0, to_stack0]]
    move_history = Enum.reduce(1..num_to_iterate, [[from_stack, to_stack]], fn(_, acc) ->
      # get the most recent move from the front of the List in the accumulator
      # to_move = [from_stack, to_stack]
      [to_move|_] = acc

      # append the current move to the front of the accumulator List O(1)

      if version == :v1 do
        curr_move = move(to_move)
        [curr_move|acc]
      else
        curr_move = move_v2(to_move, num_to_move)
        [curr_move|acc]
      end
    end)

    # get the most recent (final) move from front of the list
    [[from_stack, to_stack]|_] = move_history

    # swap in new stacks
    stacks = List.replace_at(stacks, from_index, from_stack)
    stacks = List.replace_at(stacks, to_index, to_stack)

    # return updated list of Stacks
    stacks
  end


  defp parse_stacks(initial_stacks) do
    # parse the initial stacks from the input and return a List of Lists, where
    # each nested List represents elements to add to each stack

    # split each line in a vector
    lines = String.split(initial_stacks, "\n")

    #  then reverse order of vector so that the bottom of the stack is first line in vector
    lines = Enum.reverse(lines)

    # get rid of first item
    [first_line|lines] = lines

    # get number of stacks
    num_stacks = String.at(first_line, String.length(first_line)-2)
    num_stacks = String.to_integer(num_stacks)

    # add num stacks to list
    initial_stacks = Enum.reduce(0..num_stacks-1, [], fn(_, acc) -> [[]|acc] end)

    # read the columns from input
    Enum.reduce(lines, initial_stacks, fn(line, acc) ->
      # initial_stacks contains an empty list for each stack / column

      # use accumulate to keep track of the columns after reading each line
      # pass in the current accumulate value (previous columns loaded)
      # return the updated accumulated value (new columns loaded) (this Enum returns a value which becomes acc)
      Enum.reduce(0..num_stacks-1, acc, fn(i, acc1) ->

        # get the index of the current column in the string (pass first char and then skip 4 each time)
        index_in_string = 4*i + 1
        val_to_add = String.at(line, index_in_string)

        # don't add blank chars to stack
        if val_to_add != " " and val_to_add != "" do

          # IO.puts "add #{val_to_add} to stack #{i+1}"

          # update list to be inserted into stack
          stack_to_update = Enum.at(acc1, i)
          stack_to_update = [val_to_add | stack_to_update]

          # swap the stack back into the list of stacks (return this value to be acc1)
          List.replace_at(acc1, i, stack_to_update)
        else
          # return acc regardless of whether it is updated
          acc1
        end
      end)
    end)
  end


  defp load_initial_stacks(to_load) do
    # create Stack structs from inital configurations list
    Enum.map(to_load, fn(load) ->
      # oops, need to reverse the order to load
      load = Enum.reverse(load)
      Stack.new(load)
    end)
  end


  # after executing each move, what are the crates on top
  defp task_one(input) do
    # split the input commands fro the input stacks
    [stacks_from_input | commands] = input

    # get the initial stacks as list of lists
    initial_stacks = parse_stacks(stacks_from_input)
    initial_stacks = load_initial_stacks(initial_stacks)

    # IO.puts "\ninitial configuration"
    # IO.inspect(initial_stacks)
    # IO.puts "\n"

    # break apart commands
    commands = Enum.at(commands, 0)  # commands are the tail of the input list, but just one element, so ["commands"]
    commands = String.split(commands, "\n")

    # execute every command
    final_stacks = Enum.reduce(commands, initial_stacks, fn(command, acc) ->
      execute_command(command, acc, :v1)
    end)

    # IO.puts "\nfinal configuration"
    # IO.inspect(final_stacks)
    # IO.puts "\n"

    # return a string containing the items on top of each stack
    Enum.reduce(final_stacks, "", fn(stack, acc) ->
      acc <> Stack.top(stack)
    end)
  end


  # same as task one, except now when we move 2 or 3 crates at once, they remain in the same stack
  defp task_two(input) do
    # split the input commands fro the input stacks
    [stacks_from_input | commands] = input

    # get the initial stacks as list of lists
    initial_stacks = parse_stacks(stacks_from_input)
    initial_stacks = load_initial_stacks(initial_stacks)

    # IO.puts "\ninitial configuration"
    # IO.inspect(initial_stacks)
    # IO.puts "\n"

    # break apart commands
    commands = Enum.at(commands, 0)  # commands are the tail of the input list, but just one element, so ["commands"]
    commands = String.split(commands, "\n")

    # execute every command
    final_stacks = Enum.reduce(commands, initial_stacks, fn(command, acc) ->
      execute_command(command, acc, :v2)
    end)

    # IO.puts "\nfinal configuration"
    # IO.inspect(final_stacks)
    # IO.puts "\n"

    # return a string containing the items on top of each stack
    Enum.reduce(final_stacks, "", fn(stack, acc) ->
      acc <> Stack.top(stack)
    end)
  end

  def run() do
    input = read_input("input.txt")
    IO.puts "task 1: #{task_one(input)}"
    IO.puts "task 2: #{task_two(input)}"

  end
end

# elixir main.elixir
# Solution.run
