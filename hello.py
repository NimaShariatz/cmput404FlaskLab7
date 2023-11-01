#!/usr/bin/env python3


#do 'chmod +x hello.py' to make it executable and do ./hello.py to run. alternatively just do python3 hell.py to run it as well

#to run, do python3 hello.py in one terminal while in virtual enviroment
#then say http localhost:5000/todos in another while in virtual enviroment


#to see our to do list
#http localhost:5000/todos
#http :5000/todos
#http HEAD :5000/todos
#http POST :5000/todos task="Try httpie!"#to add a task to our todolist



#to manipulate our to do list, you can do the following commands as well


#curl localhost:5000/todos
#curl localhost:5000/todos/3
#curl -v -X DELETE localhost:5000/todos/2
#curl -v -X POST localhost:5000/todos -d "task=make sure to do lab 7 questions"
#curl -v -X PUT localhost:5000/todos/3 -d "task=profit more"



from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()#for user input by using request
parser.add_argument("task")

TODOs = {
    1: {"task": "build an API"},
    2: {"task": "?????"},
    3: {"task": "profit"},
}


def abort_if_todo_not_found(todo_id):
    if todo_id not in TODOs:
        abort(404, message="TODO {} does not exist".format(todo_id))


def add_todo(todo_id):#adds more todo by user input
    args = parser.parse_args()#for user input
    todo = {"task": args["task"]}
    TODOs[todo_id] = todo
    return todo


class Todo(Resource):
    """
    Shows a single TODO item and lets you delete a TODO item.
    """

    def get(self, todo_id):
        abort_if_todo_not_found(todo_id)
        return TODOs[todo_id]

    def delete(self, todo_id):
        abort_if_todo_not_found(todo_id)
        del TODOs[todo_id]
        return "", 204

    def put(self, todo_id):
        return add_todo(todo_id), 201


class TodoList(Resource):
    """
    Shows a list of all TODOs and lets you POST to add new tasks.
    """

    def get(self):#return ALL todos
        return TODOs

    def post(self):#add one more todo
        todo_id = max(TODOs.keys()) + 1#initializes new todo ID
        return add_todo(todo_id), 201#adds new todo by calling it


api.add_resource(Todo, "/todos/<int:todo_id>")
api.add_resource(TodoList, "/todos")

if __name__ == "__main__":
    app.run(debug=True)