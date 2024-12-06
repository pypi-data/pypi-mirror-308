# spark-dash

### Pypi
- [spark-dash](https://pypi.org/project/spark-dash/)

### usage
1. Run streamlit 
```
$ run-dashboard
 
  Local URL: http://localhost:8501
  Network URL: http://172.31.41.91:8501
```

2. Explore dashboard <br/>
   1. main dashboard <br/>
      <img src="https://github.com/user-attachments/assets/2f96e14b-1f77-4353-a511-0b1b2d8f00c4" width=50% /> <br/>

      > a. 현재 spark 관련 container의 CPU 및 MEM 사용량을 보여줍니다.
      > 
      > b. 자동 Scale in/out까지 시간 진행률(60초 중에 얼마나 왔는지)
      > 
      > c. 수동 Scale in/out 버튼
   2. Scale log dashboard <br/>
      <img src="https://github.com/user-attachments/assets/cdad97b4-deee-4b43-a523-cdca3c1d9402" width=50% /> <br/>
      > a. 데이터를 나타낼 log file 선택
      > 
      > b. 선택된 log file을 DataFrame으로 표출
      > 
      > c. 선택된 log file에서 시간별 Worker의 수를 line plot으로 표출
      > 
      > d. 선택된 log file에서 Scale In/Out이 일어난 횟수를 bar plot으로 표출
  
   3. Usage log dashboard <br/>
      <!--img src="https://github.com/user-attachments/assets/5d1a44be-ed1a-4e91-8dcd-034ea91913e4" width=50% /-->
      <img src="https://github.com/user-attachments/assets/1dd382dd-c291-482b-9813-93b254e9cecd" width=50% /> <br/>

      > a. 데이터를 나타낼 log file 선택
      > 
      > b. 선택된 log file을 DataFrame으로 표출
      > 
      > c. 선택된 log file에서 CPU 사용량을 line plot으로 표출
      > 
      > d. 선택된 log file에서 현재 CPU 사용상태를 bar plot으로 표출

### Configure
```bash
$ cat config.ini
[limit]
max_cpu_use=1   # 10%
min_cpu_use=1   # 10%

[scale]
min_cnt=1
max_cnt=10
```
> scale in/out이 일어나는 cpu %와 최대/최소 worker의 갯수를 `config.ini` 파일에 지정 

### dependency
![streamlit>=1.40.1](https://img.shields.io/badge/streamlit>=1.40.1-FF4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=FFFFFF) <br/>
![matplotlib>=3.9.2](https://img.shields.io/badge/matplotlib>=3.9.2-3776AB.svg?style=for-the-badge&logo=python&logoColor=FFFFFF) <br/>
![schedule>=1.2.2](https://img.shields.io/badge/schedule>=1.2.2-3776AB.svg?style=for-the-badge&logo=python&logoColor=FFFFFF) <br/>
![tz-kst>=0.5.3](https://img.shields.io/badge/tz--kst>=0.5.3-3776AB.svg?style=for-the-badge&logo=python&logoColor=FFFFFF)