# 写
from datetime import datetime
import json
# #
# with open("todos.json", "w", encoding="utf-8") as f:
#     f.write("你好")
# # 读
# with open("todos.json", "r", encoding="utf-8") as f:
#     content = f.read()
#     print(content)

# json序列化
# todos = [{"task":"买牛奶","done":False}]
# with open("todos.json", "w", encoding="utf-8") as f:
#     json.dump(todos, f, ensure_ascii=False, indent=2)
#
# with open("todos.json", "r", encoding="utf-8") as f:
#     todos = json.load(f)
#     print(todos)
#     print(type(todos))


# 异常处理
# def load_todos():
#     try:
#         with open("todos.json", "r", encoding="utf-8") as f:
#             return json.load(f)
#     except FileNotFoundError:
#         return []
#     except json.decoder.JSONDecodeError:
#         print("文件损坏,重置")
#         return []
#     except Exception as e:
#         print(f"未知错误:{e}")
#         return []
#
# todos = load_todos()
# print(todos)



################ 可保存读取的备忘录###########################
todos = []


def add(task):
    todos.append({"task": task, "done": False, "created_at": datetime.now().isoformat()})
    # save()
    print(f"已添加:{task}")


def list_all():
    for i, todo in enumerate(todos):
        status = "√" if todo["done"] else ""
        print(f"{i + 1}.[{status}]{todo['task']}")


def done(index):
    todos[index]["done"] = True
    print(f"已完成:{todos[index]['task']}")
    save()


def save():
    with open("todos.json", "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)


def load():
    try:
        with open("todos.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.decoder.JSONDecodeError:
        return []

todos = load()
add("睡觉")
add("打游戏")
done(3)
done(4)
list_all()
print(todos)