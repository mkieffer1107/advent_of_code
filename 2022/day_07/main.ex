'''
      --- Day 7: No Space Left On Device ---

  - this might be easy to do with python using nested Dictionaries or maps in other languages
'''

# defmodule Navigator do
#   def navigate(dir) do
#     expanded_dir = Path.expand(dir)
#     go_through([expanded_dir])
#   end

#   defp go_through([]), do: nil
#   defp go_through([content | rest]) do
#     print_and_navigate(content, File.dir?(content))
#     go_through(rest)
#   end

#   defp print_and_navigate(_dir, false), do: nil defp print_and_navigate(dir, true) do
#     IO.puts dir
#     children_dirs = File.ls!(dir)
#     go_through(expand_dirs(children_dirs, dir))
#   end

#   defp expand_dirs([], _relative_to), do:
#     [] defp expand_dirs([dir | dirs], relative_to) do expanded_dir = Path.expand(dir, relative_to)
#     [expanded_dir | expand_dirs(dirs, relative_to)]
#   end
# end

defmodule MyFile do
  defstruct name: "", size: 0

  def new(name, size) do
    %MyFile{name: name, size: size}
  end

  def print(file, spaces) do
    IO.puts "#{spaces}- #{file.name} (file, size=#{file.size})"
  end
end


defmodule Directory do
  defstruct name: "", contents: [], size: 0

  def new(name) do
    %Directory{name: name}
  end

  def ls(dir) do
    ls_helper(dir, 1)
  end

  def ls_helper(dir, depth) do
    spaces = Enum.reduce(0..depth, "", fn(_,acc) -> acc <> " " end)
    IO.puts "#{spaces}- #{dir.name} (dir)"
    Enum.each(dir.contents, fn(content) ->
      if is_struct(content, Directory) do
        Directory.ls_helper(content, depth + 2)
      else
        MyFile.print(content, spaces <> " " <> " ")
      end
    end)
  end

  def cd() do

  end

  def mkdir(dir, dir_to_add) do
    %Directory{name: dir.name, contents: [dir_to_add|dir.contents], size: dir.size + dir_to_add.size}
  end

  def touch(dir, file) do
    %Directory{name: dir.name, contents: [file|dir.contents], size: dir.size + file.size}
  end

  def size(dir) do
    Enum.reduce(dir.contents, 0, fn(item, curr_size) ->
      if is_struct(item, MyFile) do
        curr_size + item.size
      else
        # we are dealing with a directory, traverse down it to get its size
        curr_size + Directory.size(item)
      end
    end)
  end
end


defmodule Solution do
  defp read_input(path) do
    path
    |>File.read!()
    |>String.split("\n")
  end

  defp build_tree(input) do
    # build out the file structure
    root = Directory.new("/")

    # build tree downwards, then propagate sizes back up
    tree = Enum.reduce(input, root, fn(line, root) ->
      parsed = String.split(line, " ")
      type = Enum.at(parsed, 0)

      if type == "$" do
        # command input
        IO.write "command "

        command = Enum.at(parsed, 1)
        IO.puts command

        if command == "cd" do
          IO.puts command

        end

        # new_dir = Directory.mkdir();
      else
        # listing contents
        IO.write "content: "
        if type == "dir" do
          IO.write "dir\n"
        else
          IO.write "file\n"
        end

      end

    end)
    10
  end

  defp task_one(input) do
    tree = build_tree(input)
  end


  defp task_two(input) do

  end

  def run() do
    input = read_input("input.txt")
    # IO.puts "task 1: #{task_one(input)}"
    # IO.puts "task 2: #{task_two(input)}"
    task_one(input)
  end

  def test() do
    root = Directory.new("/")

    file1 = MyFile.new("wow.txt", 21)
    file2 = MyFile.new("abc.json", 32)
    file3 = MyFile.new("pro.rs", 58)

    dir1 = Directory.new("dir1")
    dir1 = Directory.touch(dir1, file1)

    dir2 = Directory.new("dir2")
    file = MyFile.new("something.test", 234)
    dir2 = Directory.touch(dir2, file)

    dir3 = Directory.new("dir3")
    dir3 = Directory.touch(dir3, MyFile.new("ye.r", 094))
    dir3 = Directory.touch(dir3, MyFile.new("hel.lo", 204))
    file = MyFile.new("ye.r", 094)
    file = MyFile.new("scam.sol", 204)

    dir2 = Directory.mkdir(dir2, dir3)

    root = Directory.touch(root, file1)
    root = Directory.touch(root, file2)
    root = Directory.mkdir(root, dir2)
    root = Directory.touch(root, file3)
    root = Directory.mkdir(root, dir1)

    IO.puts "File Structure:"
    Directory.ls(root)

    IO.puts "dir \"/\" size: #{Directory.size(root)}"
    IO.puts "dir \"1\" size: #{Directory.size(dir1)}"
    IO.puts "dir \"2\" size: #{Directory.size(dir2)}"
    IO.puts "dir \"3\" size: #{Directory.size(dir3)}"
  end
end
