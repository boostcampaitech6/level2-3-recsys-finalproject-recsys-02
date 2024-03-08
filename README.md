# Final Project

### 태그 종류 
Issue, Branch, PR, Commit 태그 모두 아래로 통일하면 좋을 것 같습니다.
기존 방식들은 각각 규칙이 달라서 다들 혼동이 있었을 것 같음 ㅎ 

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

원래 방법대로 하면 PR제목을 바꿔줘야해서 불편함... To be로 바꾸면 제목을 바꾸지 않아도 됨 ㅎㅎ

## Git Commit 컨벤션
태그 : 제목의 형태이며, :뒤에만 space가 있음에 유의한다.



더 자세한 커밋 메세지 구조는 해당 [링크](https://velog.io/@msung99/Git-Commit-Message-Convension) 참고

## 베이스라인 디렉토리 구조
```
level2-3-recsys-finalproject-recsys-02
├─ .gitignore
├─ README.md
├─ config
│  ├─ GCP_Account_Key.json
│  └─ BigQuery_Account_Key.json
├─ data
│  ├─ data.zip
│  └─ raw_data
├─ data_collection
│  ├─ README.md
│  └─ notiAPI
│     ├─ api.py
│     ├─ auth.py
│     └─ parse_log.py
├─ model
│  └─ README.md
└─ servingAPI
   └─ README.md

```
