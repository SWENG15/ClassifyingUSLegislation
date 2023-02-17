"""This module is used for the python code of the PyScript website homepage"""

from datetime import datetime as dt

def remove_class(element, class_name):
    """remove_class removes a class from an element"""
    element.element.classList.remove(class_name)


def add_class(element, class_name):
    """add_class adds a class to an element"""
    element.element.classList.add(class_name)

tasks = []

# define the task template that will be use to render new templates to the page

# Disable undefined variable as the class is defined at runtime
# pylint: disable=undefined-variable
task_template = Element("task-template").select(".task", from_content=True)
task_list = Element("list-tasks-container")
new_task_content = Element("new-task-content")

# pylint: disable=unused-argument
def add_task(*ags, **kws):
    """add_task adds a task to the page"""
    # ignore empty task
    if not new_task_content.element.value:
        return

    # create task
    task_id = f"task-{len(tasks)}"
    task = {
        "id": task_id,
        "content": new_task_content.element.value,
        "done": False,
        "created_at": dt.now(),
    }

    tasks.append(task)

    # add the task element to the page as new node in the list by cloning from a
    # template
    task_html = task_template.clone(task_id, to=task_list)
    task_html_content = task_html.select("p")
    task_html_content.element.innerText = task["content"]
    task_html_check = task_html.select("input")
    task_list.element.appendChild(task_html.element)

    def check_task(evt=None):
        task["done"] = not task["done"]
        if task["done"]:
            add_class(task_html_content, "line-through")
        else:
            remove_class(task_html_content, "line-through")

    new_task_content.clear()
    task_html_check.element.onclick = check_task


def add_task_event(event):
    """add_task_event deals with if there is an event on the website. 
    Currently just deals with enter key input."""
    if event.key == "Enter":
        add_task()


new_task_content.element.onkeypress = add_task_event
