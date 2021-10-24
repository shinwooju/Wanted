import datetime
import json
import jwt

from django.test import TestCase, Client

from wanted.settings import SECRET_KEY
from users.models    import User
from .models         import Post


class PostViewTest(TestCase):
    def setUp(self):
        User.objects.bulk_create(
            [
                User(
                    id       = 1,
                    name     = "wooju0",
                    email    = "zkzkxls@naver.com",
                    password = "wooju123!@",
                ),
                User(
                    id       = 2,
                    name     = "wooju1",
                    email    = "zkzkxls@gmail.com",
                    password = "wooju12!@"
                ),
                User(
                    id       = 3,
                    name     = "wooju2",
                    email    = "zkzkxls@hanmail.com",
                    password = "wooju12!@#$!"
                )
            ]
        )
        self.time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        Post.objects.bulk_create(
            [
                Post(
                    id      = 1,
                    author  = User.objects.get(id = 1).name,
                    user    = User.objects.get(id = 1),
                    title   = "테스트 1번", 
                    content = "테스트 1번 내용"
                ),
                Post(
                    id      = 2,
                    author  = User.objects.get(id = 1).name,
                    user    = User.objects.get(id = 1),
                    title   = "테스트 2번", 
                    content = "테스트 2번 내용"
                ),
                Post(
                    id      = 3,
                    author  = User.objects.get(id = 2).name,
                    user    = User.objects.get(id = 2),
                    title   = "테스트 3번", 
                    content = "테스트 3번 내용"
                ),
                Post(
                    id      = 4,
                    author  = User.objects.get(id = 2).name,
                    user    = User.objects.get(id = 2),
                    title   = "테스트 4번", 
                    content = "테스트 4번 내용"
                ),
                Post(
                    id      = 5,
                    author  = User.objects.get(id = 2).name,
                    user    = User.objects.get(id = 2),
                    title   = "테스트 5번", 
                    content = "테스트 5번 내용"
                ),
                Post(
                    id      = 6,
                    author  = User.objects.get(id = 3).name,
                    user    = User.objects.get(id = 3),
                    title   = "테스트 6번", 
                    content = "테스트 6번 내용"
                ),
                Post(
                    id      = 7,
                    author  = User.objects.get(id = 3).name,
                    user    = User.objects.get(id = 3),
                    title   = "테스트 7번", 
                    content = "테스트 7번 내용"
                )
            ]
        )

    def tearDown(self):
        Post.objects.all().delete()
        User.objects.all().delete()

    def test_Post_View_Create_Success(self):
        token = jwt.encode({'id' : 3}, SECRET_KEY, algorithm = "HS256")
        header = {"HTTP_AUTHORIZATION" : token}

        post = {
            "author"     : User.objects.get(id = 3).name,
            "title"      : "테스트 8번",
            "content"    : "테스트 8번 내용",
            "created_at" : self.time
        }

        client   = Client()
        response = client.post(
            "/posts", json.dumps(post), content_type = "application/json", **header
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"MESSAGE": "SUCCESS",
        "data": {
            "author"     : "wooju2",
            "title"      : "테스트 8번",
            "content"    : "테스트 8번 내용",
            "created_at" : self.time
                }
            }
        )

    def test_Post_View_Key_Error(self):
        token = jwt.encode({'id' : 3}, SECRET_KEY, algorithm = "HS256")
        header = {"HTTP_AUTHORIZATION": token}

        post = {
            "author"     : User.objects.get(id = 3).name,
            "title"      : "테스트 8번",
        }

        client   = Client()
        response = client.post(
            "/posts", json.dumps(post), content_type = "application/json", **header
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE' : 'KEY_ERROR'})

    def test_Post_View_Get_Success(self):
        client   = Client()
        response = client.get("/posts/1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "RESULT": {
                    "author"     : "wooju0",
                    "title"      : "테스트 1번", 
                    "content"    : "테스트 1번 내용",
                    "created_at" : Post.objects.get(id = 1).created_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            }
        )
    
    def test_Post_View_Get_Does_Not_Post(self):
        client   = Client()
        response = client.get("/posts/15")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"MESSAGE" : "DOSE_NOT_EXIST_POST"})

    def test_Post_View_Delete_Success(self):
        token  = jwt.encode({'id' : 1}, SECRET_KEY, algorithm = "HS256")
        header = {"HTTP_AUTHORIZATION": token}

        client   = Client()
        response = client.delete("/posts/1", **header)

        self.assertEqual(response.status_code, 200)

    def test_Post_View_Delete_Dose_Not_Post(self):
        token  = jwt.encode({'id' : 1}, SECRET_KEY, algorithm = "HS256")
        header = {"HTTP_AUTHORIZATION": token}

        client   = Client()
        response = client.delete("/posts/77", **header)

        self.assertEqual(response.status_code, 404)

    def test_Post_View_Delete_No_Permission(self):
        token  = jwt.encode({'id' : 1}, SECRET_KEY, algorithm = "HS256")
        header = {"HTTP_AUTHORIZATION": token}

        client   = Client()
        response = client.delete("/posts/5", **header)

        self.assertEqual(response.status_code, 403)

    def test_Post_View_Put_Success(self):
        token = jwt.encode({'id' : 1}, SECRET_KEY, algorithm = "HS256")
        header = {"HTTP_AUTHORIZATION" : token}

        post = {
            "title"   : "수정 1번",
            "content" : "수정 1번 내용"
        }

        client   = Client()
        response = client.put(
            "/posts/1", json.dumps(post), content_type = "application/json", **header
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"MESSAGE": "SUCCESS"})

    def test_Post_View_Put_Dose_Not_Exist_Post(self):
        token = jwt.encode({'id' : 1}, SECRET_KEY, algorithm = "HS256")
        header = {"HTTP_AUTHORIZATION" : token}

        post = {
            "title"   : "수정 1번",
            "content" : "수정 1번 내용"
        }

        client   = Client()
        response = client.put(
            "/posts/25", json.dumps(post), content_type = "application/json", **header
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"MESSAGE" : "DOSE_NOT_EXIST_POST"})

    def test_Post_View_Put_No_Permission(self):
        token = jwt.encode({'id' : 1}, SECRET_KEY, algorithm = "HS256")
        header = {"HTTP_AUTHORIZATION" : token}

        post = {
            "title"   : "수정 1번",
            "content" : "수정 1번 내용"
        }

        client   = Client()
        response = client.put(
            "/posts/5", json.dumps(post), content_type = "application/json", **header
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"MESSAGE" : "NO_PERMISSION"})

    def test_Post_View_Put_Key_Error(self):
        token = jwt.encode({'id' : 1}, SECRET_KEY, algorithm = "HS256")
        header = {"HTTP_AUTHORIZATION" : token}

        post = {
            "ti"      : "수정 1번",
            "content" : "수정 1번 내용"
        }

        client   = Client()
        response = client.put(
            "/posts/1", json.dumps(post), content_type = "application/json", **header
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE" : "KEY_ERROR"})

    def test_PostList_View_Get_List_Success(self):
        client = Client()
        response = client.get("/posts/list?offset=0&limit=5")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "count": 5,
                "RESULT": [
                    {
                        "author"     : "wooju0",
                        "title"      : "테스트 1번",
                        "content"    : "테스트 1번 내용",
                        "created_at" : Post.objects.get(id = 1).created_at.strftime('%Y-%m-%d %H:%M:%S')
                    },
                    {
                        "author"     : "wooju0",
                        "title"      : "테스트 2번",
                        "content"    : "테스트 2번 내용",
                        "created_at" : Post.objects.get(id = 2).created_at.strftime('%Y-%m-%d %H:%M:%S')
                    },
                    {
                        "author"     : "wooju1",
                        "title"      : "테스트 3번",
                        "content"    : "테스트 3번 내용",
                        "created_at" : Post.objects.get(id = 3).created_at.strftime('%Y-%m-%d %H:%M:%S')
                    },
                    {
                        "author"     : "wooju1",
                        "title"      : "테스트 4번",
                        "content"    : "테스트 4번 내용",
                        "created_at" : Post.objects.get(id = 4).created_at.strftime('%Y-%m-%d %H:%M:%S')
                    },
                    {
                        "author"     : "wooju1",
                        "title"      : "테스트 5번",
                        "content"    : "테스트 5번 내용",
                        "created_at" : Post.objects.get(id = 5).created_at.strftime('%Y-%m-%d %H:%M:%S')
                    }
                ]
            }
        )
