from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .serializers import TodoSerializer, UserSerializer
from .models import Todo
from django.contrib.auth.models import User

# Create your views here.

@api_view(['POST', 'GET'])
def create_user(request: Request):
    user = request.user
    if user.id is None:
        serialized = UserSerializer(data=request.data)
        if serialized.is_valid():
            User.objects.create(
                username=serialized.data['username'],
                password=serialized.data['password']
            )
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response('Siz ro\'yhatdan o\'tgansiz.', status=status.HTTP_226_IM_USED)

@api_view(['GET'])
def apiOverview(request: Request):
    api_urls = {
        'List' : '/todo-list/',
        'Detail View' : '/todo-detail/<int:id>/',
        'Create' : '/todo-create/',
        'Update' : '/todo-update/<int:id>/',
        'Delete' : '/todo-delete/<int:id>/',
    }
    return Response(api_urls, status=status.HTTP_200_OK)


@api_view(['GET'])
def todoList(request: Request):
    user = request.user
    if user.id is None:
        return Response('Anonim foydalanuvchi uchun kirish ruxsat etilmagan!', status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        todo = Todo.objects.filter(user=user).order_by('todo_id')
        serializer = TodoSerializer(todo, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def todoDetail(request: Request, id: int):
    user = request.user
    if user.id is None:
        return Response('Anonim foydalanuvchi uchun kirish ruxsat etilmagan!', status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        todo = Todo.objects.get(user=user, todo_id=id)
        serializer = TodoSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST', 'GET'])
def todoCreate(request: Request):
    user = request.user
    if user.id is None:
        return Response('Anonim foydalanuvchi uchun kirish ruxsat etilmagan!', status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        if request.method=='POST':
            data = request.data
            todo_all = Todo.objects.filter(user=user).order_by('todo_id')
            if not todo_all.exists():
                todo_id = 0
            elif 'todo_id' in list(data.keys()):
                if data['todo_id'] <= len(todo_all)-1:
                    todo_id = data['todo_id']
                    todo_next_all = todo_all[todo_id:]
                    for todo_n in todo_next_all:
                        todo_n.todo_id=todo_n.todo_id+1
                        todo_n.save()
                else:
                    todo_id=len(todo_all)
            else:
                todo_id = len(todo_all)

            data['todo_id'] = todo_id
            data['user'] = user.id
            
            serializer = TodoSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response('Nimanidir xato jo\'natdingiz',status=status.HTTP_400_BAD_REQUEST)

        elif request.method=='GET':
            post_method = {
                'json':{
                    'todo_id':'ixtiyoriy, max=len(todos)+1, default=max',
                    'todo':'majburiy',
                    'completed':'ixtiyoriy, default=False',
                    'schedule_date':'ixtiyoriy, default=None'
                }
            }
            return Response(post_method, status=status.HTTP_200_OK)


@api_view(['POST', 'GET'])
def todoUpdate(request: Request, id):
    user = request.user
    if user.id is None:
        return Response('Anonim foydalanuvchi uchun kirish ruxsat etilmagan!', status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        todo = Todo.objects.get(user=user, todo_id=id)
        if request.method=='POST':
            data = request.data
            todos = Todo.objects.filter(user=user).order_by('todo_id')

            if data.get('todo_id') is not None:
                new_id = data['todo_id']
                if new_id<=len(todos)-1:
                    if new_id>id:
                        todo_s = todos[id+1:new_id+1]
                        for todo_n in todo_s:
                            todo_n.todo_id = todo_n.todo_id-1
                            todo_n.save()
                    elif new_id<id:
                        todo_s = todos[new_id:id]
                        for todo_n in todo_s:
                            todo_n.todo_id = todo_n.todo_id+1
                            todo_n.save()
                else:
                    return Response("Ma'lumot yuborishda xato!", status=status.HTTP_400_BAD_REQUEST)
            else:
                data['todo_id']=todo.todo_id

            data['user']=user.id
            serializer = TodoSerializer(instance=todo, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response("Ma'lumot yuborishda xato!", status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = TodoSerializer(todo)
            return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE', 'GET'])
def todoDelete(request: Request, id: int):
    user = request.user
    if user.id is None:
        return Response('Anonim foydalanuvchi uchun kirish ruxsat etilmagan!', status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        todo = Todo.objects.filter(user=user, todo_id = id)
        if request.method=='DELETE':
            todo.delete()
            todos = Todo.objects.filter(user=user)
            todos_next = todos.order_by('todo_id')[id:]
            for todo_n in todos_next:
                todo_n.todo_id=todo_n.todo_id-1
                todo_n.save()
            return Response("Todo muvaffaqiyatli o'chirildi.", status=status.HTTP_200_OK)
        else:
            serializer = TodoSerializer(todo, many=True)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
