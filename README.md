# 백엔드 프리온보딩 선발 과제

### 유저 생성, 인가, 인증 구현

### 게시물 C.R.U.D 구현하기

---

## 구현한 방법과 이유에 대한 간략한 내용

### 사용자

- 사용자 생성 시 정규 표현식과 패스워드 확인으로 오류를 한 번 더 잡았습니다.
- 사용자 인증과 인가를 위한 로그인 시 jwt 토큰을 발행하고 사용합니다.
- jwt 토큰에 담고 있는 정보는 토큰 값과 user의 pk입니다.

### 게시물

- 게시물은 익명의 사용자가 생성, 삭제, 수정을 막기 위해 로그인을 해야 실행할 수 있습니다.
- 게시물 확인은 로그인을 하지 않아도 모두 불러올 수 있게끔 만들었습니다.
- 게시물을 작성한 사용자는 자신이 작성한 게시물을 확인하는 방법으로 로그인이 되었을 때 발급되는 jwt 토큰을 활용해 토큰의 id 값과 user의 pk를 비교하여 게시물을 작성한 본인만이 게시물을 수정 또는 삭제할 수 있습니다.

---

## 자세한 실행 방법(endpoint 호출방법)

### 구현 방법

- 가상환경 생성(conda사용을 가정) conda create -n (가상환경 이름)
- git clone https://github.com/shinwooju/Wanted.git
- pip install -r requirements.txt를 입력하여 package install 진행
- python manage.py runserver 입력
- endpoint 호출 및 실행

### ENDPOINT

| Method | EndpointURL                | Request Body                          | Remark           |
| :----: | -------------------------- | ------------------------------------- | ---------------- |
|  POST  | /users/sign-up             | name, email, password, check_password | 회원가입         |
|  POST  | /users/sign-in             | email, password                       | 로그인           |
|  POST  | /posts                     | title, content                        | 게시물 작성      |
|  GET   | /posts/id                  |                                       | 게시물 조회      |
| DELETE | /posts/id                  |                                       | 게시물 삭제      |
|  PUT   | /posts/id                  | title, content                        | 게시물 수정      |
|  GET   | /posts/list?offset=&limit= |                                       | 게시물 목록 조회 |

---

## API 명세(request/response 서술 필요)

### 1. 회원가입

- Method : POST
- EndpointURL : /users/sign-up
- Remark : (email : @와 .이 들어간 이메일 형식 아닐시 오류반환), (password : 숫자,문자,특수문자가 포함이 된 8자 이상)
- Request

```
POST "http://127.0.0.1:8000/users/sign-up HTTP/1.1" \
--data-raw '{
    "name" : "우주",
    "email" : "shinwj5534@naver.com",
    "password" : "wooju123!@",
    "check_password" : "wooju123!@"
}'
```

- Response

```
{
    "MESSAGE": "SUCCESS"
}
```

### 2. 로그인

- Method : POST
- EndpointURL : /users/sign-in
- Remark : (email : @와 .이 들어간 이메일 형식 아닐시 오류반환), (password : 숫자,문자,특수문자가 포함이 된 8자 이상)
- Request

```
POST "http://127.0.0.1:8000/users/sign-in HTTP/1.1" \
--data-raw '{
    "email" : "shinwj5534@naver.com",
    "password" : "wooju123!@",
}'
```

- Response

```
{
    "MESSAGE": "SUCCESS",
    "TOKEN": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NX0.kuOePN0Q2H6fQnbZeEXp0gu-LHivgBu56qXkrlykjzE"
}
```

### 3. 게시물

- Method : POST
- EndpointURL : /posts
- Remark : header에 "Authorization" : token을 담아야 작성가능
- Request

```
POST "http://127.0.0.1:8000/posts HTTP/1.1" \
--data-raw '{
    "title"   : "도전",
    "content" : "코딩은 재밌다."
}'
```

- Response

```
{
    "MESSAGE": "SUCCESS",
    "RESULT": {
        "author": "신우주",
        "title": "도전",
        "content": "코딩은 재밌다.",
        "created_at": "2021-10-24 16:36:23"
    }
}
```

### 4. 게시물 조회

- Method : GET
- EndpointURL : /posts/id
- Request

```
GET "http://127.0.0.1:8000/posts/12 HTTP/1.1"
```

- Response

```
{
    "RESULT": {
        "author": "신우주",
        "title": "도전",
        "content": "코딩은 재밌다.",
        "created_at": "2021-10-24 16:36:23"
    }
}
```

### 5. 게시물 수정

- Method : PUT
- EndpointURL : /posts/id
- Remark : header에 "Authorization" : token을 담아야 작성가능
- Request

```
PUT "http://127.0.0.1:8000/posts/12 HTTP/1.1" \
--data-raw '{
    "title" : "화이자",
    "content" : "아자아자 화이자"
}'
```

- Response

```
{
    "MESSAGE": "SUCCESS"
}
```

### 6. 게시물 삭제

- Method : DELETE
- EndpointURL : /posts/id
- Remark : header에 "Authorization" : token을 담아야 작성가능
- Request

```
DELETE "http://127.0.0.1:8000/posts/12 HTTP/1.1"
```

- Response

```
{
    "MESSAGE": "DELETED"
}
```

### 7. 게시물 목록 조회

- Method : GET
- EndpointURL : /posts/list?offset=0&limit=5
- Remark : QueryParams (offset/limit)로 페이지네이션 가능
- Request

```
GET "http://127.0.0.1:8000/posts/list?offset=0&limit=5 HTTP/1.1"
```

- Response

```
{
    "count": 5,
    "RESULT": [
        {
            "author": "신우주",
            "title": "우주가 최고야!",
            "content": "",
            "created_at": "2021-10-23 08:35:57"
        },
        {
            "author": "신우주",
            "title": "test1",
            "content": "test1",
            "created_at": "2021-10-23 08:36:09"
        },
        {
            "author": "신우주",
            "title": "test2",
            "content": "test2",
            "created_at": "2021-10-23 08:36:12"
        },
        {
            "author": "신우주",
            "title": "우주가 최고야!",
            "content": "맞아",
            "created_at": "2021-10-23 08:36:19"
        },
        {
            "author": "신우주",
            "title": "test4",
            "content": "test4",
            "created_at": "2021-10-23 08:36:23"
        }
    ]
}
```
