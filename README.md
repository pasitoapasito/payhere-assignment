## Intro

> **페이히어(payhere) 과제 레포지토리입니다.**

- 본 프로젝트에서 요구하는 서비스는 가계부(Account Book)입니다.
- 사용자는 본 서비스에 로그인하여, 본인의 소비내역을 기록하고 관리할 수 있습니다.
- 단, 로그인하지 않은 사용자는 가계부 내역에 대한 접근제한 처리가 되어야 합니다.

<br>

> **Index**
- [Environments](#environments)
- [Project](#project)
- [Etc](#etc)

<br>
<hr>

## Environments

<br>
<div align="center">
<img src="https://img.shields.io/badge/Python-blue?style=plastic&logo=Python&logoColor=white"/>
<img src="https://img.shields.io/badge/Django-092E20?style=plastic&logo=Django&logoColor=white"/>
<img src="https://img.shields.io/badge/Django Rest Framework-EE350F?style=plastic&logo=Django&logoColor=white"/>
<img src="https://img.shields.io/badge/MySQL-00979D?style=plastic&logo=MySQL&logoColor=white"/>
</div>

<br>
<div align="center">
<img src="https://img.shields.io/badge/AWS EC2-FF9900?style=plastic&logo=Amazon AWS&logoColor=white"/>
<img src="https://img.shields.io/badge/AWS RDS-527FFF?style=plastic&logo=Amazon RDS&logoColor=white"/>
<img src="https://img.shields.io/badge/Docker-%230db7ed.svg?style=plastic&logo=Docker&logoColor=white"/>
<img src="https://img.shields.io/badge/nginx-%23009639.svg?style=plastic&logo=NGINX&logoColor=white"/>
<img src="https://img.shields.io/badge/gunicorn-EF2D5E?style=plastic&logo=Gunicorn&logoColor=white"/>
</div>

<br>
<div align="center">
<img src="https://img.shields.io/badge/Swagger-%23Clojure?style=plastic&logo=swagger&logoColor=white"/>
<img src="https://img.shields.io/badge/Postman-FF6C37?style=plastic&logo=Postman&logoColor=white"/>
<img src="https://img.shields.io/badge/Git-F05032?style=plastic&logo=Git&logoColor=white"/>
<img src="https://img.shields.io/badge/GitHub-181717?style=plastic&logo=GitHub&logoColor=white"/>
</div>

<br>
<hr>

## Project

> **Period**
- #### ⚡️ 22.08.17 ~ 22.08.23

<br>

> **Development**
- #### 🔥 프로젝트 구현기능
  - 사용자 관리:
    - 회원가입
      ```
      > 사용자 회원가입 기능입니다.
      
      * 이메일, 닉네임, 패스워드는 필수 입력값입니다.
      * 이메일, 닉네임은 중복이 허용되지 않습니다.
      * 패스워드는 최소 1개의 소문자/대문자/숫자/(숫자키)특수문자가 포함된 8~20자리로 구성되어야 합니다.
      * 패스워드는 해싱 후 DB에 저장됩니다.
      ```
    - 로그인
      ```
      > 사용자 로그인 기능입니다.
      
      * DRF-SimpleJwt 라이브리러를 활용했습니다.
      * 이메일, 패스워드는 필수 입력값입니다.
      * 입력받은 이메일과 패스워드가 유저 정보와 일치하는지 확인합니다.
      * 모든 유효성 검사에 통과하면 액세스토큰과 리프레시 토큰을 발급합니다.
      ```
    - 로그아웃
      ```
      > 사용자 로그아웃 기능입니다.
      
      * DRF-SimpleJwt 라이브리러를 활용했습니다.
      * 리프레시 토큰은 필수 입력값입니다.
      * 토큰의 타입이 유효한지 확인합니다.(리프레시 토큰만 허용)
      * 토큰의 기한이 만료되었는지 확인합니다.
      * 토큰의 유저정보와 API 요청자의 유저정보가 일치하는지 확인합니다.
      * 모든 유효성 검사에 통과하면, 요청받은 리프레시 토큰을 토큰 블랙리스트에 등록합니다.(사용 제한)
      * 또한, 기존에 발급받은 모든 리프레시 토큰도 함께 토큰 블랙리스트에 등록합니다.
      ```
    - 토큰 재발급
      ```
      > 사용자 토큰 재발급 기능입니다.
      
      * DRF-SimpleJwt의 TokenRefreshView 기능을 활용했습니다.
      * 리프레시 토큰은 필수 입력값입니다.
      * 유효한 토큰인지를 확인합니다.
      * 만료된 토큰인지를 확인합니다.
      * 토큰의 타입을 확인합니다.(오직 리프레시 토큰만 사용 가능)
      * 모든 유효성 검사에 통과하면, 요청받은 리프레시 토큰을 사용하여 액세스토큰을 발급합니다.
      * 단, 리프레시 토큰은 추가로 발급하지 않습니다.
      ```
  - 가계부:
    - 가계부 목록
      ```
      > 인증/인가에 통과한 사용자는 본인 가계부의 리스트 정보를 조회할 수 있습니다.
      
      * 키워드 검색기능(가계부 이름을 기준으로 검색 키워드 적용)
      * 정렬기능(가계부 생성일자/목표 예산을 기준으로 오름차순/내림차순 정렬)
      * 필터링 기능(현재 사용중인/삭제된 가계부를 기준으로 필터링 조회)
      * 페이지네이션 기능(사용자가 원하는 만큼의 가계부 데이터를 요청할 수 있음 >> default: 최신순 10개)
      ```
    - 가계부 생성
      ```
      > 인증/인가에 통과한 사용자는 본인의 가계부를 생성할 수 있습니다.
      
      * 사용자는 목표예산을 지정해서 가계부를 생성할 수 있습니다.
      * 단, 가계부의 이름과 목표예산은 필수 입력값입니다.
      ```
    - 가계부 수정/삭제/복구
      ```
      > 인증/인가에 통과한 사용자는 본인의 가계부를 수정/삭제/복구할 수 있습니다.
      
      - 가계부 수정:
        * 해당 가계부가 존재하는지, 본인의 가계부인지를 확인합니다.
        * 사용자는 가계부의 이름과 목표예산만을 수정할 수 있습니다.
        * 가계부의 내용을 부분적으로 수정할 수 있습니다.
        
      - 가계부 삭제(soft delete):
        * 해당 가계부가 존재하는지, 본인의 가계부인지를 확인합니다.
        * 이미 삭제된 가계부는 다시 삭제할 수 없습니다.
        
      - 가계부 복구:
        * 해당 가계부가 존재하는지, 본인의 가계부인지를 확인합니다.
        * 이미 복구된 가계부는 다시 복구할 수 없습니다.
      ```
  - 가계부 카테고리
    - 가계부 카테고리 목록
      ```
      > 인증/인가에 통과한 사용자는 본인 가계부 카테고리의 리스트 정보를 조회할 수 있습니다.
      
      * 키워드 검색기능(가계부 카테고리 이름을 기준으로 검색 키워드 적용)
      * 정렬기능(가계부 카테고리 생성일자를 기준으로 오름차순/내림차순 정렬)
      * 필터링 기능(현재 사용중인/삭제된 카테고리를 기준으로 필터링 조회)
      * 페이지네이션 기능(사용자가 원하는 만큼의 카테고리 데이터를 요청할 수 있음 >> default: 최신순 10개)
      ```
    - 가계부 카테고리 생성
      ```
      > 인증/인가에 통과한 사용자는 본인의 카테고리를 생성할 수 있습니다.
      
      * 사용자가 원하는 이름의 가계부 카테고리를 생성할 수 있습니다.
      * 단, 카테고리의 이름은 필수 입력값입니다.
      ```
    - 가계부 카테고리 수정/삭제/복구
      ```
      > 인증/인가에 통과한 사용자는 본인의 카테고리를 수정/삭제/복구할 수 있습니다.
      
      - 가계부 카테고리 수정:
        * 해당 카테고리가 존재하는지, 본인의 카테고리인지를 확인합니다.
        * 사용자는 카테고리의 이름만을 수정할 수 있습니다.
        
      - 가계부 카테고리 삭제(soft delete):
        * 해당 카테고리가 존재하는지, 본인의 카테고리인지를 확인합니다.
        * 이미 삭제된 카테고리는 다시 삭제할 수 없습니다.
        
      - 가계부 카테고리 복구:
        * 해당 카테고리가 존재하는지, 본인의 카테고리인지를 확인합니다.
        * 이미 복구된 카테고리는 다시 복구할 수 없습니다.
      ```
  - 가계부 기록
    - 가계부 기록 목록
      ```
      > 인증/인가에 통과한 사용자는 본인 가계부 기록의 리스트 정보를 조회할 수 있습니다.
      
      * 가계부가 존재하는지, 본인의 가계부인지 확인합니다.
      * 사용자 본인의 가계부 기록만을 리스트 조회합니다.
      * 가계부 기록의 총지출/총수입 데이터를 함께 반환합니다.
      * 가계부의 목표예산을 함께 반환합니다.
      * 사용자의 닉네임을 함께 반환합니다.
      
      - 부가기능:
        * 키워드 검색기능(가계부 기록의 제목/설명/가계부 카테고리 이름을 기준으로 검색 키워드 적용)
        * 정렬기능(가계부 기록 생성일자/가격을 기준으로 오름차순/내림차순 정렬)
        * 상태 필터링 기능(현재 사용중인/삭제된 가계부 기록을 기준으로 필터링 조회)
        * 카테고리 필터링 기능(카테고리 id를 기준으로 필터링 조회: 복수의 카테고리 적용가능)
        * 타입 필터링(가계부의 타입[expenditure/income]을 기준으로 필터링 조회)
        * 페이지네이션 기능(사용자가 원하는 만큼의 가계부 기록 데이터를 요청할 수 있음 >> default: 최신순 10개)
      ```
    - 가계부 기록 생성
      ```
      > 인증/인가에 통과한 사용자는 본인의 기록을 생성할 수 있습니다.
      
      * 가계부 id는 필수 입력값입니다.(path param)
      * 가계부 카테고리 id는 필수 입력값입니다.(query string)
      * 가계부가 존재하는지, 본인의 가계부인지를 확인합니다.
      * 카테고리가 존재하는지, 본인의 카테고리인지를 확인합니다.
      * 사용자는 제목/설명/가격/타입/카테고리를 지정하여 가계부 기록을 생성할 수 있습니다.
      * 단, 가계부 기록의 제목과 가격은 필수 입력값입니다.
      ```
    - 가계부 기록 수정/삭제
      ```
      > 인증/인가에 통과한 사용자는 본인의 기록을 수정/삭제/복구할 수 있습니다.
      
      - 가계부 기록 수정:
        * 가계부 id는 필수 입력값입니다.(path param)
        * 가계부 기록 id는 필수 입력값입니다.(path param)
        * 가계부 카테고리 id는 선택 입력값입니다.(query string)
        * 가계부가 존재하는지, 본인의 가계부인지를 확인합니다.
        * 가계부 기록이 존재하는지, 본인의 기록인지, 해당 가계부의 기록인지를 확인합니다.
        * 카테고리가 존재하는지, 본인의 카테고리인지를 확인합니다.(카테고리의 입력값이 존재할 경우)
        * 사용자는 가계부 기록의 제목/설명/가격/타입/카테고리만을 수정할 수 있습니다.
        
      - 가계부 기록 삭제(soft delete):
        * 가계부 id는 필수 입력값입니다.(path param)
        * 가계부 기록 id는 필수 입력값입니다.(path param)
        * 가계부가 존재하는지, 본인의 가계부인지를 확인합니다.
        * 가계부 기록이 존재하는지, 본인의 기록인지, 해당 가계부의 기록인지를 확인합니다.
        * 이미 삭제된 기록은 다시 삭제할 수 없습니다.

      - 가계부 기록 복구:
        * 가계부 id는 필수 입력값입니다.(path param)
        * 가계부 기록 id는 필수 입력값입니다.(path param)
        * 가계부가 존재하는지, 본인의 가계부인지를 확인합니다.
        * 가계부 기록이 존재하는지, 본인의 기록인지, 해당 가계부의 기록인지를 확인합니다.
        * 이미 복구된 기록은 다시 복구할 수 없습니다.
      ```
       
<br>

> **Modeling**
- #### 🚀 ERD 구조
  <img width="1000px" alt="스크린샷 2022-08-23 08 09 47" src="https://user-images.githubusercontent.com/89829943/186034893-74811ef5-67d2-47c9-8514-5544b18179de.png">

<br> 

> **API Docs**
- #### 🌈 API 명세서
  <img width="1000px" alt="스크린샷 2022-08-23 08 47 49" src="https://user-images.githubusercontent.com/89829943/186038988-633d74bc-faab-4624-b333-aefb971d2ef0.png">

<br> 

> **Deploy**
- #### 🏖 프로젝트 배포
  #### Docker, Nginx, Gunicorn을 사용하여 AWS EC2 서버에 프로젝트를 배포했습니다.  👉 [배포 링크(Swagger)](http://3.38.14.143/swagger)
  <img width="1000px" alt="스크린샷 2022-07-27 08 47 14" src="https://user-images.githubusercontent.com/89829943/181131164-f9bd2137-1f08-4263-9a31-035cd0435af8.png">

<br> 

> **Test**
- #### 🚦 테스트코드 작성
  #### 전체 테스트코드: 138 cases
  <img width="1000px" alt="스크린샷 2022-08-23 09 12 33" src="https://user-images.githubusercontent.com/89829943/186041202-39b01448-1ae4-4463-99ce-8bcd2babd129.png">
  <img width="1000px" alt="스크린샷 2022-08-23 09 18 56" src="https://user-images.githubusercontent.com/89829943/186041838-824eed99-9d8f-4e2b-b9f9-390c33322d10.png">
  <img width="1000px" alt="스크린샷 2022-08-22 14 23 23" src="https://user-images.githubusercontent.com/89829943/186041849-08ededd5-e183-470d-9997-7b46a2ab5749.png">
  
  #### 테스트 커버리지: 99%
  <img width="1000px" alt="스크린샷 2022-08-23 09 23 34" src="https://user-images.githubusercontent.com/89829943/186042173-f4357e95-7ba5-49b4-9f80-73c4549d1655.png">

<br> 

> **Issue**
- #### ⏰ 프로젝트 일정관리
  #### 프로젝트 진행사항을 칸반보드와 이슈티켓으로 관리했습니다.
  <img width="1000px" alt="스크린샷 2022-08-21 08 33 05" src="https://user-images.githubusercontent.com/89829943/186043007-3bf11c62-f952-485b-a6ff-4722b3785005.png">

<br>
<hr>

## Etc

> **Guides**
- #### ⚙️ 프로젝트 설치방법
  #### ```✔️ 로컬 개발 및 테스트용```
  
  1. 해당 프로젝트를 clone하고, 프로젝트 폴더로 이동합니다.
  <br>
  
   ```
   git clone https://github.com/pasitoapasito/payhere-assignment.git
   cd project directory
   ```
  
  2. 가상환경을 만들고, 프로젝트에 필요한 python package를 다운받습니다.
  <br>
  
  ```
  conda create --name project-name python=3.9
  conda activate project-name
  pip install -r requirements.txt
  ```
  
  3. manage.py 파일과 동일한 위치에서 환경설정 파일을 만듭니다.
  <br>
  
  ```
  ex) .env file 
  
  ## GENERAL ##
  DEBUG         = True
  ALLOWED_HOSTS = ALLOWED_HOSTS
  SECRET_KEY    = SECRET_KEY

  ## DOCKER DB ##
  MYSQL_TCP_PORT      = '3306'
  MYSQL_DATABASE      = MYSQL_DATABASE
  MYSQL_ROOT_PASSWORD = MYSQL_ROOT_PASSWORD
  MYSQL_USER          = MYSQL_USER
  MYSQL_PASSWORD      = MYSQL_PASSWORD

  ## AWS RDS ##
  RDS_HOSTNAME = RDS_HOSTNAME
  RDS_DB_NAME  = RDS_DB_NAME
  RDS_USERNAME = RDS_USERNAME
  RDS_PASSWORD = RDS_PASSWORD
  RDS_PORT     = '3306'
  ```
  
  4. project-name/settings.py에서 DB 설정을 적절하게 변경합니다.
  <br>
  
  ```
  Docker로 DB를 구축하는 경우 or AWS RDS로 DB를 구축하는 경우 등
  DB를 구축하는 방법에 맞게 DB 설정을 변경합니다.
  
  
  ## DOCKER DB FOR LOCAL-DEV ##
  '''
  DATABASES = {
      'default': {
          'ENGINE'  : 'django.db.backends.mysql',
          'NAME'    : get_env_variable('MYSQL_DATABASE'),
          'USER'    : 'root',
          'PASSWORD': get_env_variable('MYSQL_ROOT_PASSWORD'),
          'HOST'    : 'localhost',
          'PORT'    : get_env_variable('MYSQL_TCP_PORT'),
      }
  }
  '''
  
  ## AWS RDS FOR LOCAL-DEV ##
  DATABASES = {
      'default': {
          'ENGINE'  : 'django.db.backends.mysql',
          'NAME'    : get_env_variable('RDS_DB_NAME'),
          'USER'    : get_env_variable('RDS_USERNAME'),
          'PASSWORD': get_env_variable('RDS_PASSWORD'),
          'HOST'    : get_env_variable('RDS_HOSTNAME'),
          'PORT'    : get_env_variable('RDS_PORT'),
          'OPTIONS' : {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"},
      }
  }
  ```
  
  5. DB의 스키마(schema)를 최신 modeling에 맞게 동기화합니다.
  <br>
  
  ```
  python manage.py migrate
  ```
  
  6. 개발용 서버를 실행합니다.
  <br>
  
  ```
  python manage.py runserver 0:8000
  ```

  #### ```✔️ 배포용```
  1. 배포용 서버에서 해당 프로젝트를 clone하고, 프로젝트 폴더로 이동합니다.
  <br>
  
  ```
  git clone https://github.com/pasitoapasito/payhere-assignment.git
  cd project directory
  ```
  
  2. manage.py 파일과 동일한 위치에서 도커 환경설정 파일을 만듭니다.
  <br>
  
  ```
  ex) .env file 
  
  ## GENERAL ##
  DEBUG         = True
  ALLOWED_HOSTS = ALLOWED_HOSTS
  SECRET_KEY    = SECRET_KEY

  ## DOCKER DB ##
  MYSQL_TCP_PORT      = '3306'
  MYSQL_DATABASE      = MYSQL_DATABASE
  MYSQL_ROOT_PASSWORD = MYSQL_ROOT_PASSWORD
  MYSQL_USER          = MYSQL_USER
  MYSQL_PASSWORD      = MYSQL_PASSWORD

  ## AWS RDS ##
  RDS_HOSTNAME = RDS_HOSTNAME
  RDS_DB_NAME  = RDS_DB_NAME
  RDS_USERNAME = RDS_USERNAME
  RDS_PASSWORD = RDS_PASSWORD
  RDS_PORT     = '3306'
  ```
  
  3. project-name/settings.py에서 DB 설정을 적절하게 변경합니다.
  <br>
  
  ```
  Docker로 DB를 구축하는 경우 or AWS RDS로 DB를 구축하는 경우 등
  DB를 구축하는 방법에 맞게 DB 설정을 변경합니다.
  
  
  ## DOCKER DB FOR DEPLOY ##
  DATABASES = {
      'default': {
          'ENGINE'  : 'django.db.backends.mysql',
          'NAME'    : get_env_variable('MYSQL_DATABASE'),
          'USER'    : 'root',
          'PASSWORD': get_env_variable('MYSQL_ROOT_PASSWORD'),
          'HOST'    : 'db',
          'PORT'    : get_env_variable('MYSQL_TCP_PORT'),
      }
  }
  
  ## AWS RDS FOR DEPLOY ##
  '''
  DATABASES = {
      'default': {
          'ENGINE'  : 'django.db.backends.mysql',
          'NAME'    : get_env_variable('RDS_DB_NAME'),
          'USER'    : get_env_variable('RDS_USERNAME'),
          'PASSWORD': get_env_variable('RDS_PASSWORD'),
          'HOST'    : get_env_variable('RDS_HOSTNAME'),
          'PORT'    : get_env_variable('RDS_PORT'),
          'OPTIONS' : {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"},
      }
  }
  '''
  ```
  
  4. docker-compose 명령을 사용하여, DB/Nginx/Django 서버 컨테이너를 실행시킵니다.
  <br>
  
  ```
  docker-compose -f ./docker-compose.yml up (-d)
  ```

<br>

> **Structure**
- #### 🛠 프로젝트 폴더구조

  ```
   📦account_books
   ┣ 📂migrations
   ┃ ┣ 📜0001_initial.py
   ┃ ┣ 📜0002_alter_accountbooklog_book.py
   ┃ ┗ 📜__init__.py
   ┣ 📂tests
   ┃ ┣ 📂account_book
   ┃ ┃ ┣ 📜__init__.py
   ┃ ┃ ┣ 📜tests_account_book_create.py
   ┃ ┃ ┣ 📜tests_account_book_delete.py
   ┃ ┃ ┣ 📜tests_account_book_list.py
   ┃ ┃ ┣ 📜tests_account_book_restore.py
   ┃ ┃ ┗ 📜tests_account_book_update.py
   ┃ ┣ 📂account_book_category
   ┃ ┃ ┣ 📜__init__.py
   ┃ ┃ ┣ 📜tests_account_book_category_create.py
   ┃ ┃ ┣ 📜tests_account_book_category_delete.py
   ┃ ┃ ┣ 📜tests_account_book_category_list.py
   ┃ ┃ ┣ 📜tests_account_book_category_restore.py
   ┃ ┃ ┗ 📜tests_account_book_category_update.py
   ┃ ┣ 📂account_book_log
   ┃ ┃ ┣ 📜__init__.py
   ┃ ┃ ┣ 📜tests_account_book_log_create.py
   ┃ ┃ ┣ 📜tests_account_book_log_delete.py
   ┃ ┃ ┣ 📜tests_account_book_log_list.py
   ┃ ┃ ┣ 📜tests_account_book_log_restore.py
   ┃ ┃ ┗ 📜tests_account_book_log_update.py
   ┃ ┗ 📜__init__.py
   ┣ 📂views
   ┃ ┣ 📜account_book_categories.py
   ┃ ┣ 📜account_book_logs.py
   ┃ ┗ 📜account_books.py
   ┣ 📜__init__.py
   ┣ 📜admin.py
   ┣ 📜apps.py
   ┣ 📜models.py
   ┣ 📜serializers.py
   ┗ 📜urls.py
   📦config
   ┗ 📂nginx
   ┃ ┗ 📜nginx.conf
   📦core
   ┣ 📂migrations
   ┃ ┗ 📜__init__.py
   ┣ 📂utils
   ┃ ┣ 📜decorator.py
   ┃ ┗ 📜get_obj_n_check_err.py
   ┣ 📜__init__.py
   ┣ 📜admin.py
   ┣ 📜apps.py
   ┣ 📜models.py
   ┣ 📜tests.py
   ┗ 📜views.py
   📦payhere
   ┣ 📜__init__.py
   ┣ 📜asgi.py
   ┣ 📜settings.py
   ┣ 📜urls.py
   ┗ 📜wsgi.py
   📦users
   ┣ 📂migrations
   ┃ ┣ 📜0001_initial.py
   ┃ ┗ 📜__init__.py
   ┣ 📂tests
   ┃ ┣ 📜__init__.py
   ┃ ┣ 📜tests_user_refresh_token.py
   ┃ ┣ 📜tests_user_signin.py
   ┃ ┣ 📜tests_user_signout.py
   ┃ ┗ 📜tests_user_signup.py
   ┣ 📂views
   ┃ ┣ 📜user_signin.py
   ┃ ┣ 📜user_signout.py
   ┃ ┗ 📜user_signup.py
   ┣ 📜__init__.py
   ┣ 📜admin.py
   ┣ 📜apps.py
   ┣ 📜models.py
   ┣ 📜serializers.py
   ┗ 📜urls.py
   ┣ 📜.env
   ┣ 📜.gitignore
   ┣ 📜docker-compose.yml
   ┣ 📜Dockerfile
   ┣ 📜manage.py
   ┣ 📜README.md
   ┗ 📜requirements.txt
  ```



 

