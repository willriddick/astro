import os


def gather_metrics(src_dir="src"):
    total_files = 0
    total_lines = 0
    py_files = 0
    py_lines = 0
    comment_lines = 0
    blank_lines = 0
    function_defs = 0
    class_defs = 0

    for root, _, files in os.walk(src_dir):
        for file in files:
            total_files += 1
            filepath = os.path.join(root, file)

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
            except Exception as e:
                print(f"Skipping {filepath}: {e}")
                continue

            line_count = len(lines)
            total_lines += line_count

            if file.endswith('.py'):
                py_files += 1
                py_lines += line_count

                for line in lines:
                    stripped = line.strip()
                    if stripped.startswith('#'):
                        comment_lines += 1
                    elif stripped == "":
                        blank_lines += 1
                    elif stripped.startswith('def '):
                        function_defs += 1
                    elif stripped.startswith('class '):
                        class_defs += 1

    print(f"📁 Total files: {total_files}")
    print(f"📄 Total lines: {total_lines}")
    print(f"🐍 Python files: {py_files}")
    print(f"📜 Python lines: {py_lines}")
    if py_files:
        print(f"📊 Average lines per Python file: {py_lines // py_files}")
    print(f"💬 Comment lines: {comment_lines}")
    print(f"⬜ Blank lines: {blank_lines}")
    print(f"🔧 Function definitions: {function_defs}")
    print(f"🏛️ Class definitions: {class_defs}")


if __name__ == "__main__":
    gather_metrics("src")
