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
      
      * 이메일, 닉네임, 패스워드는 필수값입니다.
      * 전화번호, 프로필 이미지는 선택값입니다.
      * 이메일, 닉네임은 중복되지 않습니다.
      * 패스워드는 반드시 8~20자리의 최소 1개의 소문자/대문자/숫자/(숫자키)특수문자로 구성됩니다.
      * 패스워드는 해싱 후 DB에 저장됩니다.
      ```
    - 로그인
      ```
      > 사용자 로그인 기능입니다.
      
      * DRF-SimpleJwt 라이브리러를 활용했습니다.
      * 이메일, 패스워드는 필수값입니다.
      * 입력받은 이메일과 패스워드가 유저 정보와 일치하는지 확인합니다.
      * 모든 유효성 검사에 통과하면 액세스토큰과 리프레시 토큰을 발급합니다.
      ```
    - 로그아웃
      ```
      > 사용자 로그아웃 기능입니다.
      
      * DRF-SimpleJwt 라이브리러를 활용했습니다.
      * 리프레시 토큰은 필수값입니다.
      * 유효한 토큰인지를 확인합니다.
      * 만료된 토큰인지를 확인합니다.
      * 모든 유효성 검사에 통과하면 요청받은 리프레시 토큰을 토큰 블랙리스트에 등록합니다.
      * 단, 기존에 발급된 리프레시 토큰은 모두 사용을 제한합니다.
      ```
    - 토큰 재발급
      ```
      > 사용자의 토큰을 재발급하는 기능입니다.
      
      * DRF-SimpleJwt의 TokenRefreshView 기능을 활용했습니다.
      * 리프레시 토큰은 필수값입니다.
      * 유효한 토큰인지를 확인합니다.
      * 만료된 토큰인지를 확인합니다.
      * 토큰의 타입을 확인합니다.(오직 리프레시 토큰만 사용가능)
      * 모든 유효성 검사에 통과하면 요청받은 리프레시 토큰을 기반으로 액세스토큰을 발급합니다.
      * 단, 리프레시 토큰은 추가로 발급하지 않습니다.
      ```
  - 가계부:
    - 가계부 목록
      ```
      > 인증/인가에 통과한 사용자는 본인 가계부의 리스트 정보를 조회할 수 있습니다.
      
      * 키워드 검색기능(가계부 이름에 해당 키워드가 검색조건으로 사용)
      * 정렬기능(가계부 생성일자/목표 예산을 기준으로 오름차순, 내림차순 정렬)
      * 필터링 기능(현재 사용중인 가계부/삭제된 가계부 필터링 조회)
      * 페이지네이션 기능(사용자가 원하는 가계부 개수를 정할 수 있음 >> default: 최신순 10개)
      ```
    - 가계부 생성
      ```
      > 인증/인가에 통과한 사용자는 본인의 가계부를 생성할 수 있습니다.
      
      * 사용자는 목표예산을 지정해서 가계부를 생성할 수 있습니다.
      ```
    - 가계부 수정/삭제/복구
      ```
      > 인증/인가에 통과한 사용자는 본인의 가계부를 수정/삭제/복구할 수 있습니다.
      
      - 가계부 수정:
        * 해당 가계부가 존재하는지, 본인의 가계부인지를 확인합니다.
        * 사용자는 가계부의 이름과 예산만 수정할 수 있습니다.
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
      
      * 키워드 검색기능(가계부 카테고리 이름에 해당 키워드가 검색조건으로 사용)
      * 정렬기능(가계부 카테고리 생성일자를 기준으로 오름차순, 내림차순 정렬)
      * 필터링 기능(현재 사용중인 카테고리/삭제된 카테고리 필터링 조회)
      * 페이지네이션 기능(사용자가 원하는 카테고리 개수를 정할 수 있음 >> default: 최신순 10개)
      ```
    - 가계부 카테고리 생성
      ```
      > 인증/인가에 통과한 사용자는 본인의 카테고리를 생성할 수 있습니다.
      
      * 사용자는 원하는 이름의 가계부 카테고리를 생성할 수 있습니다.
      ```
    - 가계부 카테고리 수정/삭제/복구
      ```
      > 인증/인가에 통과한 사용자는 본인의 카테고리를 수정/삭제/복구할 수 있습니다.
      
      - 가계부 카테고리 수정:
        * 해당 카테고리가 존재하는지, 본인의 카테고리인지를 확인합니다.
        * 사용자는 카테고리의 이름만 수정할 수 있습니다.
        
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
      * 사용자의 닉네임을 함께 반환합니다.
      
      - 부가기능:
        * 키워드 검색기능(가계부 기록 제목/설명/카테고리에 해당 키워드가 검색조건으로 사용)
        * 정렬기능(가계부 기록 생성일자/가격을 기준으로 오름차순, 내림차순 정렬)
        * 상태 필터링 기능(현재 사용중인 가계부 기록/삭제된 가계부 기록 필터링 조회)
        * 카테고리 필터링 기능(다수의 카테고리 id를 기준으로 이에 해당되는 가계부 기록 필터링 조회)
        * 타입 필터링(가계부의 타입[expenditure/income]을 기준으로 필터링 조회)
        * 페이지네이션 기능(사용자가 원하는 가계부 기록의 개수를 정할 수 있음 >> default: 최신순 10개)
      ```
    - 가계부 기록 생성
      ```
      > 인증/인가에 통과한 사용자는 본인의 기록을 생성할 수 있습니다.
      
      * 가계부 id는 필수 입력값입니다.(path param)
      * 가계부 카테고리 id는 필수 입력값입니다.(query string)
      * 가계부가 존재하는지, 본인의 가계부인지를 확인합니다.
      * 카테고리가 존재하는지, 본인의 카테고리인지를 확인합니다.
      * 사용자는 제목/설명/가격/타입을 지정하여 가계부 기록을 생성할 수 있습니다.
      ```
    - 가계부 기록 수정/삭제
      ```
      > 인증/인가에 통과한 사용자는 본인의 기록을 수정/삭제/복구할 수 있습니다.
      
      - 가계부 기록 수정:
        * 가계부 id는 필수 입력값입니다.(path param)
        * 가계부 기록 id는 필수 입력값입니다.(path param)
        * 가계부가 존재하는지, 본인의 가계부인지를 확인합니다.
        * 가계부 기록이 존재하는지, 본인의 기록인지를 확인합니다.
        * 사용자는 기록의 제목/설명/가격/타입만 수정할 수 있습니다.
        
      - 가계부 기록 삭제(soft delete):
        * 가계부 id는 필수 입력값입니다.(path param)
        * 가계부 기록 id는 필수 입력값입니다.(path param)
        * 가계부가 존재하는지, 본인의 가계부인지를 확인합니다.
        * 가계부 기록이 존재하는지, 본인의 기록인지를 확인합니다.
        * 이미 삭제된 기록은 다시 삭제할 수 없습니다.
      ```
       
<br>

