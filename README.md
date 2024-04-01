![header](https://capsule-render.vercel.app/api?type=waving&color=gradient&height=250&section=header&text=Level3-FinalProject&desc=RecSys-02&fontSize=50&fontColor=FFFFFF&fontAlignY=40)
# 크롤노티 웹사이트 로그를 통한 개인화/세션 기반 추천 시스템 개발

- [발표자료](https://github.com/boostcampaitech6/level2-3-recsys-finalproject-recsys-02/blob/main/docs/Recsys02-level3-%ED%81%AC%EB%A1%A4%EB%85%B8%ED%8B%B0%EC%9B%B9%EC%82%AC%EC%9D%B4%ED%8A%B8%20%EB%A1%9C%EA%B7%B8%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%A5%BC%20%ED%99%9C%EC%9A%A9%ED%95%9C%EA%B0%9C%EC%9D%B8%ED%99%94%EC%B6%94%EC%B2%9C%EC%8B%9C%EC%8A%A4%ED%85%9C%EA%B0%9C%EB%B0%9C.pdf)
- [발표영상](https://www.youtube.com/watch?v=nWuolij8pCE)
- [렙업리포트](https://github.com/boostcampaitech6/level2-3-recsys-finalproject-recsys-02/blob/main/docs/Final%20Wrap%20Up%20Report.pdf)

## 1. 프로젝트 개요
### 프로젝트 소개
![image](https://github.com/boostcampaitech6/level2-3-recsys-finalproject-recsys-02/assets/97018869/2d961787-866c-4a88-af8f-938da515e0e3)

- 크롤노티는 쿠팡 전자기기 특가 알림 사이트입니다. (일 로그 건 수 : 평균 10만 건 이상)
- 크롤노티로부터 제공받은 웹사이트 로그를 통한 개인화/세션 기반 추천 시스템 개발을 주제로 선정했습니다.

###  프로젝트 Task1 - 키워드 알림 개인화
- 크롤노티의 키워드 알림 서비스
   - 핫딜 지수 : 가격 추이, 브랜드, 상품 가격 등을 종합해 계산된 크롤노티 자체 지수

#### AS IS
![image](https://github.com/boostcampaitech6/level2-3-recsys-finalproject-recsys-02/assets/97018869/0bf2ebac-b815-4626-a1a6-9a11dd7a0d3a)

#### TO BE
- 키워드 알림 개인화
   - 키워드를 등록한 유저의 조회 이력과 핫딜 후보로 뜬 상품의 유사도/ 좋아할 확률 → 상품에 대한 유저 별 개인 점수
   - 붉은 색 = 상품에 대한 유저 별 개인 점수, 노란 색 = 알림 발송(0.5 이상)

![image](https://github.com/boostcampaitech6/level2-3-recsys-finalproject-recsys-02/assets/97018869/3d21761d-5210-4a19-839b-3594fd3321bc)


### 프로젝트 Task2 - 세션 기반 Top K 추천
- 세션 기반 Top K 추천
   - 회원가입 없이 사용 가능한 웹사이트로, 키워드를 등록한 유저가 아닌 이상, 유저 특정 불가
   - user-free, 세션 기반, 유저가 클릭할 때마다 추천 아이템들을 갱신하여 보여줄 수 있는 모델을 구현

![image](https://github.com/boostcampaitech6/level2-3-recsys-finalproject-recsys-02/assets/97018869/169ad036-5b7a-4296-a1b9-cb0cc20d7dd3)


## 2. 서비스 아키텍처
![서비스아키텍처](https://github.com/boostcampaitech6/level2-3-recsys-finalproject-recsys-02/assets/97018869/e9ff4ed4-3615-4c6c-9c2b-74214f61804a)

## 3. 추천 모델 아키텍쳐
### 키워드 알림 개인화
![image](https://github.com/boostcampaitech6/level2-3-recsys-finalproject-recsys-02/assets/97018869/63bc45c7-fa47-4192-a72c-c63a495c5401)

### 세션 기반 Top K 추천
![image](https://github.com/boostcampaitech6/level2-3-recsys-finalproject-recsys-02/assets/97018869/42b0d3e8-d9f4-46da-bb2a-a0750de08e75)

## 4. 팀소개

네이버 부스트캠프 AI Tech 6기 Level 2 Recsys 2조 **R_AI_SE** 입니다.

<aside>
    
💡 **R_AI_SE의 의미**

Recsys AI Seeker(추천시스템 인공지능 탐구자)를 줄여서 R_AI_SE입니다~
</aside>

### 👋 R_AI_SE의 멤버를 소개합니다 👋

#### 🦹‍팀원소개
| 팀원   | 역할 및 담당                      |
|--------|----------------------------------|
| [김수진](https://github.com/guridon) |  데이터 분석 및 정제, TopicModeling, EASE, TM2LGCN, FastAPI |
| [김창영](https://github.com/ChangZero) | 데이터 수집 및 정제, Airflow를 활용한 ELT 파이프라인 설계, Serving API 개발 |
| [박승아](https://github.com/SeungahP) | 데이터 정제, 콘텐츠 기반 추천, (TF-IDF, Word2Vec), IBCF(Item2Vec), Looker Studio |
| [전민서](https://github.com/Minseojeonn) | SASRec, EDA, 파이프라인 설계, 클라우드 기반 인프라 구축, 데이터 정제 |
| [한대희](https://github.com/DAEHEE97) | 데이터 분석 및 정제, 데이터 클리닝, 메모리 기반 협업 필터링(UBCF, IBCF)  |
| [한예본](https://github.com/Yebonn-Han) | 데이터 분석 및 정제, EDA(Looker Studio), Sequential Recommentation(SASRec) |

### 👨‍👧‍👦 Team 협업
### 📝 Ground Rule
#### 팀 규칙
- 모더레이터 역할
  - 순서 : 매일 돌아 가면서
  - 역할 : 피어세션 시 소개하고 싶은 곡 선정
- 데일리 스크럼
    - 오늘 학습 계획 정하기
    - Github PR 올린 것 코드리뷰 진행
- 피어세션
    - 모더레이터가 가져 온 노래 나올 때 각자 스트레칭 하기
    - Github PR 올린 것 코드리뷰 진행
- 노션과 깃허브 칸반보드 활용한 일정관리
    - 실험 일지 작성을 통한 원활한 결과 공유 도모

#### Git Ground Rule
<details>
<summary>ISSUE, PR, Commit 컨벤션 규칙</summary>
<div markdown="1">

### 태그 종류 

`Feat` : 새로운 기능 추가<br>
`Fix` : 버그 수정<br>
`Docs` : 문서 수정<br>
`Style` : 코드 포맷팅, 세미콜론 누락, 코드 변경이 없는 경우<br>
`Refactor` : 코드 리펙토링<br>
`Test` : 테스트 코드, 리펙토링 테스트 코드 추가<br>
`Chore` : 빌드 업무 수정, 패키지 매니저 수정<br>
`Rename` : 파일명(or 폴더명) 을 수정한 경우<br>
`Remove` : 코드(파일) 의 삭제가 있을 때. "Clean", "Eliminate" 를 사용하기도 함<br>
`Add` : 코드나 테스트, 예제, 문서등의 추가 생성이 있는경우- Improve : 향상이 있는 경우. 호환성, 검증 기능, 접근성 등이 될수 있습니다.<br>
`Implement` : 코드가 추가된 정도보다 더 주목할만한 구현체를 완성시켰을 때<br>
`EDA` : 데이터 분석<br>
`Data`: 데이터 전처리 및 데이터 가공<br>

## GitHub ISSUE 컨벤션
[태그] 이슈제목

## Git Branch 생성 규칙
태그/이슈번호 브랜치명

## GitHub PR 컨벤션
As Is 
- [태그] 발행 이슈 제목 혹은 PR 제목 #이슈번호

To be
- 태그: 발행 이슈 제목 혹은 PR 제목 #이슈번호

## Git Commit 컨벤션
태그 : 제목의 형태이며, :뒤에만 space가 있음에 유의한다.


더 자세한 커밋 메세지 구조는 해당 [링크](https://velog.io/@msung99/Git-Commit-Message-Convension) 참고

</div>
</details>



## 5. 프로젝트 개발 환경 및 기술 스택
### ⚙️ 개발 환경
- OS: Ubuntu20.04
- GPU: Tesla V100-32GB * 6
- CPU cores: 8

### 🔧 기술 스택
![](https://img.shields.io/badge/Pytorch-EE4C2C?style=flat-square&logo=Pytorch&logoColor=white)
![](https://img.shields.io/badge/jupyter-F37626?style=flat-square&logo=Jupyter&logoColor=white)
![](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=black)
![](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=Pandas&logoColor=white)
![](https://img.shields.io/badge/Numpy-013243?style=flat-square&logo=Numpy&logoColor=white)

![](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=FastAPI&logoColor=white)
![](https://img.shields.io/badge/MLflow-0194E2?style=flat-square&logo=MLflow&logoColor=white)
![](https://img.shields.io/badge/apacheairflow-017CEE?style=flat-square&logo=apacheairflow&logoColor=white)
![](https://img.shields.io/badge/postgresql-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![](https://img.shields.io/badge/minio-C72E49?style=flat-square&logo=minio&logoColor=white)
![](https://img.shields.io/badge/celery-37814A?style=flat-square&logo=celery&logoColor=black)

![](https://img.shields.io/badge/googlecloudstorage-AECBFA?style=flat-square&logo=googlecloudstorage&logoColor=black)
![](https://img.shields.io/badge/googlebigquery-669DF6?style=flat-square&logo=googlebigquery&logoColor=black)
![](https://img.shields.io/badge/googledatastudio-669DF6?style=flat-square&logo=googledatastudio&logoColor=black)
![](https://img.shields.io/badge/googlecloudcomposer-4285F4?style=flat-square&logo=googlecloudcomposer&logoColor=white)


![](https://img.shields.io/badge/slack-4A154B?style=flat-square&logo=slack&logoColor=white)
![](https://img.shields.io/badge/notion-000000?style=flat-square&logo=notion&logoColor=white)


## 6. 프로젝트 디렉토리 구조
```
level2-3-recsys-finalproject-recsys-02
├─ .github
│  ├─ .keep
│  ├─ ISSUE_TEMPLATE
│  │  ├─ bug_report.md
│  │  └─ feature_request.md
│  └─ PULL_REQUEST_TEMPLATE.md
├─ .gitignore
├─ Dockerfile
├─ MLflow
│  ├─ Dockerfile
│  └─ run.sh
├─ README.md
├─ model
│  ├─ IBCF
│  │  ├─ inference.py
│  │  └─ train.py
│  ├─ README.md
│  ├─ SASRec
│  │  ├─ args.py
│  │  ├─ inference.py
│  │  ├─ main.py
│  │  ├─ model.py
│  │  └─ trainer.py
│  ├─ TFIDF
│  │  ├─ inference.py
│  │  ├─ requirements.txt
│  │  └─ train.py
│  └─ UBCF
│     ├─ inference.py
│     └─ train.py
├─ notebooks
├─ run_for_worker_node.sh
└─ servingAPI
   ├─ Dockerfile
   ├─ api.py
   ├─ main.py
   ├─ requirements.txt
   ├─ schemas.py
   ├─ storage
   │  ├─ README.md
   └─ utils
      ├─ __init__.py
      ├─ dependencies.py
      └─ inference.py

```

![footer](https://capsule-render.vercel.app/api?type=waving&color=gradient&height=200&section=footer&)
