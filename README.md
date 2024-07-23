# 빵집 탐방 : 리뷰와 지도로 만나는 빵 맛집
사용자들이 지도에서 빵집을 추가하고 선택한 후 리뷰를 작성하여 공유할 수 있는 웹 서비스
<br>
- 팀원
    - Frontend : [iamgyu](https://github.com/iamgyu)
    - Backend : [sunni546](https://github.com/sunni546)

## 기술 스택
### Front
- HTML/CSS
- JavaScript
- React
- Next.js
- TypeScript
- kakaomap API
### Back
- Python 3.9
- Flask
- SQLAlchemy
- JWT
- REST API

## 핵심 기능
- 카카오맵을 연동하여 빵집의 위치와 정보를 지도에 표시합니다.
- 전체 및 카테고리 별 빵집 검색 및 랭킹을 제공합니다.
- 빵집 별 개인 페이지를 통해 빵집의 상세 정보와 해당 빵집의 리뷰 작성 및 확인이 가능합니다.
- 리뷰 작성 시 사용자에게 포인트를 부여하여, 포인트에 따른 레벨 제도가 있습니다.
- 모든 리뷰 내용에 작성자의 레벨이 표시되고, 각 빵집 리뷰에서 레벨 별로 리뷰를 따로 정렬할 수 있습니다.
- 마이페이지에서 사용자 정보 및 사용자가 추가한 관심 빵집과 작성한 리뷰를 확인 및 삭제가 가능합니다.

## Database
### ERD
![Bakery-Map](</bakery-map-back/Bakery-Map.png>)

## API (Endpoints)

### levels

| Method | Url          | Decription |
| ------ | ------------ | ---------- |
| GET    | /levels/     | 전체 '레벨' 목록 조회 |
| POST   | /levels      | '레벨' 추가 |
| GET    | /levels/{id} | 특정 '레벨' 조회 |
| PATCH  | /levels/{id} | '레벨' 수정 |
| DELETE | /levels/{id} | '레벨' 삭제 |

### users

| Method | Url          | Decription |
| ------ | ------------ | ---------- |
| GET    | /users       | jwt를 통한 특정 '사용자' 조회 |
| POST   | /users/login | '사용자' 회원가입(추가) |
| POST   | /users/join  | '사용자' 로그인 |

### interests

| Method | Url                      | Decription |
| ------ | ------------------------ | ---------- |
| GET    | /interests               | 전체 '관심' 목록 조회 |
| POST   | /interests               | '관심' 추가 |
| DELETE | /interests/{id}          | '관심' 삭제 |
| DELETE | /interests/bakery/{id}   | 특정 '빵집'의 '관심' 삭제 |

### reviews

| Method | Url                  | Decription |
| ------ | -------------------- | ---------- |
| GET    | /reviews             | 전체 '리뷰' 목록 조회 |
| POST   | /reviews             | '리뷰' 추가 |
| GET    | /reviews/{id}        | 특정 '리뷰' 조회 |
| PATCH  | /reviews/{id}        | '리뷰' 수정 |
| DELETE | /reviews/{id}        | '리뷰' 삭제 |
| GET    | /reviews/bakery/{id} | 특정 '빵집'의 '리뷰' 목록 조회 |
| POST   | /reviews/bakery/{id} | 특정 '빵집'의, 특정 '레벨'의 '리뷰' 목록 조회 |

### reviewed_breads

| Method | Url                  | Decription |
| ------ | -------------------- | ---------- |
| GET    | /reviewed_breads     | 전체 '리뷰한 빵들' 목록 조회 |

### bakeries

| Method | Url                      | Decription |
| ------ | ------------------------ | ---------- |
| GET    | /bakeries                | 전체 '빵집' 목록 조회 |
| POST   | /bakeries                | '빵집' 추가 |
| GET    | /bakeries/{id}           | 특정 '빵집' 조회 |
| PATCH  | /bakeries/{id}           | '빵집' 수정 |
| DELETE | /bakeries/{id}           | '빵집' 삭제 |
| POST   | /bakeries/location       | 특정 위치(위도, 경도)의 '빵집' 조회 |
| POST   | /bakeries/search         | 특정 이름이 포함된 '빵집' 목록 조회 |
| GET    | /bakeries/category/{id}  | 특정 '카테고리'의 '빵집' 목록 조회 |
| GET    | /bakeries/ranking        | (평점 순) '빵집' 목록 조회 |
| GET    | /bakeries/ranking/{id}   | (평점 순) 특정 '카테고리'의 '빵집' 목록 조회 |

### breads

| Method | Url      | Decription |
| ------ | -------- | ---------- |
| GET    | /breads  | 전체 '빵집의 빵들' 목록 조회 |

### categories

| Method | Url              | Decription |
| ------ | ---------------- | ---------- |
| GET    | /categories/     | 전체 '카테고리' 목록 조회 |
| POST   | /categories      | '카테고리' 추가 |
| GET    | /categories/{id} | 특정 '카테고리' 조회 |
| PATCH  | /categories/{id} | '카테고리' 수정 |
| DELETE | /categories/{id} | '카테고리' 삭제 |

## 화면별 실행결과
