# 목차
[0. 개요](https://github.com/malgumi/Stopnow?tab=readme-ov-file#0-%EA%B0%9C%EC%9A%94)

[1. 사용 기술 및 운영체제]()

[2. 자율주행 기술 사전 조사]()

[3. 개발 과정]()

[4. 시연 영상 및 최종 보고서]()
<br><br>

## 0. 개요
2023 컴퓨터신기술 과목 수강을 위해 진행한 프로젝트<br>
jetson nano가 설치된 미니카를 이용한 신호등 객체 인식 자율주행 미니카 프로젝트<br><br>

## 1. 사용 기술 및 운영체제
Jetson Nano OS<br>
ROS2<br>
LABELME<br>
YOLACT -> YOLOv8<br><br>

## 2. 자율주행 기술 사전 조사
- 적합하다고 생각한 기술
  - 카메라: 영상 인식이 중점인 프로젝트이기 때문에 필요.
  - YOLACT: 성능이 우수하며 실시간 객체 인식에 적합함.
  - YOLOv8: 실시간 객체 인식이 빠르고 정확함.
- 적합하지 않다고 생각한 기술
  - 라이다 및 레이더: 영상 인식을 중점으로 둔 프로젝트이고, 시간이 촉박하다고 판단함.
  - R-CNN: 실시간 처리에 적합하지 않은 단점이 존재함.
  - SSD: 작은 객체의 처리가 어려움.<br><br>

## 3. 개발 과정
#### YOLACT vs YOLOv8
  - YOLACT 인식 및 프레임 <br>
    ![image](https://github.com/malgumi/Stopnow/assets/97935451/3633807d-5fed-4d0e-93ce-c00710a1a8f0) <br>
    녹화된 영상 인식 사진. 잘 되는 것을 확인할 수 있다.<br>
    ![image](https://github.com/malgumi/Stopnow/assets/97935451/aade2d1e-f153-488a-86fe-65a97a3ecb70) <br>
    그러나 실시간 프레임을 보면, 0.38프레임으로 매우 느린 것을 확인할 수 있다.
<br>

  - YOLOv8 인식 및 프레임 <br>
    ![image](https://github.com/malgumi/Stopnow/assets/97935451/d525b848-ccdb-46b8-ae35-2daea0ef6538) <br>
    반면 YOLOv8은 실시간 프레임이 30 근처로 안정적인 모습을 보였다. 따라서, YOLOv8을 선택했다.
    <br> <br>

#### 노드 전송 과정
![image](https://github.com/malgumi/Stopnow/assets/97935451/6c2409c5-1967-433f-8dcb-6687cc128d0a) <br>
객체 인식을 해주는 패키지가 pub을 해주는 토픽이 sub토픽과 일치하면, 로봇이 on/off를 인식할 수 있게 된다. 예를 들면 전진하다가 'on'이 인식되면 멈춘다. 
<br><br>

#### 인식 결과 프롬프트
![image](https://github.com/malgumi/Stopnow/assets/97935451/73e2858d-8f20-49a5-98b2-cfb0786af50f)
![image](https://github.com/malgumi/Stopnow/assets/97935451/3319787e-3a14-4e68-9506-a4e14172855f) <br>
stopnow_pub와 stopnow_sub 노드를 실행하면 pub노드에서 토픽이 발행될때마다 로그에 어떤 객체가 인식되는지를 출력한다.
<br><br>


## 4. 시연 영상 및 최종 보고서

[PPT 링크](https://www.canva.com/design/DAF3JXm8TmQ/4kXb5J3sVHR0Bdv5UV3LaQ/edit?utm_content=DAF3JXm8TmQ&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)
