# name = "AI助手"
# version = 1.0
# is_ready = True
# tasks = [1, 2, 3, 3, 1, 34, 4]  # 空列表
#
#
# text1 = "   Helloworld     "
# text = "    Helloworld ".strip()  # 去开头以及末尾的空格
# words = "a,b,c".split(",")  # 切割
# result = "-".join(["a", "b", "c"])

# print(text1)
# print(text)
# print(name)
# print(version)
# print(tasks)
# print(words)
# print(result)

# if len(tasks) > 0:
#   print("数组不为空")
# else:
#   print("数组为空")
#
# for task in tasks:
#   print(task)

# while True:
#   user_input = input("请输入:")
#   if user_input == "quit":
#     break

# 列表嵌套字典
messages = []  # list列表
messages.append({"role": "user", "content": "你好"})  # 里面添加的字典
messages.append({"role": "assistant", "content": "你好!"})

print(messages[0]["content"])
print(messages[-1])

# 字典操作
config = {"api-key": "sk-XXX", "model": "deepseek-chat", "temperature": 0.7}

print(config["model"])  # 读
config["timeout"] = 30  # 增

# 字典嵌套列表
request = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "system", "content": "你是助手"},
        {"role": "user", "content": "你好"},
    ],
}
print(request["messages"][0]["content"])

# 元组(函数返回多值时使用)
status, data = (200, {"result": "ok"})
print(status, data["result"])

# 集合(去重时使用)
unique_tags = {"aaa", "bbb", "aaa"}
print(unique_tags)



todos = []
def add(task):
    todos.append({"task": task,"done":False})
    print(f"已添加:{task}")

def list_all():
    for i, todo in enumerate(todos):
        status = "√" if todo["done"] else ""
        print(f"{i + 1}.[{status}]{todo['task']}")

def done(index):
    todos[index]["done"] = True
    print(f"已完成:{todos[index]["task"]}")


add("买牛奶")
add("敲代码")
add("健身")
done(0)
done(1)
list_all()
