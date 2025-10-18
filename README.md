## 1. ROS Humble 설치 (Source)
### ROS Humble 설치 가이드 링크
[https://docs.ros.org/en/humble/Installation/Alternatives/Ubuntu-Development-Setup.html](https://docs.ros.org/en/humble/Installation/Alternatives/Ubuntu-Development-Setup.html)

### 1.  Set locale
```bash
locale  # check for UTF-8

sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

locale  # verify settings
```

### 2. Add the ROS2 apt repository
```bash
sudo apt install software-properties-common
sudo add-apt-repository universe

sudo apt update && sudo apt install curl -y

export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F\" '{print $4}')

curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"

sudo dpkg -i /tmp/ros2-apt-source.deb
```

### 3. Install development tools and ROS tools
```bash
sudo apt update && sudo apt install -y \
  python3-flake8-docstrings \
  python3-pip \
  python3-pytest-cov \
  ros-dev-tools
```

- 만약 아래 명령어 실행 시 이미 설치되어 있다는 메세지가 출력되는 경우에는 ```sudo apt upgrade -y``` 입력 후 다음 단계로 진행
  ```

```bash
sudo apt install -y \
   python3-flake8-blind-except \
   python3-flake8-builtins \
   python3-flake8-class-newline \
   python3-flake8-comprehensions \
   python3-flake8-deprecated \
   python3-flake8-import-order \
   python3-flake8-quotes \
   python3-pytest-repeat \
   python3-pytest-rerunfailures
```

### 4. Get ROS2 Code
```bash
mkdir -p ~/ros2_humble/src
cd ~/ros2_humble

vcs import --input https://raw.githubusercontent.com/ros2/ros2/humble/ros2.repos src
```

### 5. Install dependencied using rosdep
```bash
sudo apt upgrade

sudo rosdep init
rosdep update

rosdep install --from-paths src --ignore-src -y --skip-keys "fastcdr rti-connext-dds-6.0.1 urdfdom_headers"
```
#### 에러 해결 방법
##### 1. sudo rosdep init 명령어 실행 시 에러 발생한 경우
- 에러 출력 예시
```bash
  ERROR: default sources list files already exists:
	  /etc/ros.rosdep/sources.list.d/20-default.list
  Please delete if you wish to re-initialize
  ```

- 에러 해결 방법  
	- 출력창에 나온 경로를 복붙하여 실행 후 ```sudo rosdep init``` 명령어 재실행
	  ```
```bash
# 입력 예시
sudo rm -rf /etc/ros.rosdep/sources.list.d/20-default.list

# 실제 입력 방법
sudo rm -rf "출력창에 나온 경로를 복붙"

# 제거 완료됐으면 에러 발생한 명령어부터 다시 진행
sudo rosdep init
rosdep update
```

##### 2. rosdep update 명령어 실행 시 에러 발생한 경우
- 에러 해결 방법
	- 아래의 명령어 입력한 뒤 ```rosdep update``` 명령어 재실행
	  ```
```bash
sudo apt install python3-rosdep2
```

### 6. Build the code in the workspace
```bash
cd ~/ros2_humble/
colcon build --symlink-install
```

### 7.  Source the setup script

```bash
. ~/ros2_humble/install/local_setup.bash
```
### 8. 설치 확인
- 터미널 1
```bash
. ~/ros2_humble/install/local_setup.bash
ros2 run demo_nodes_cpp talker
```
- 터미널 2
```bash
. ~/ros2_humble/install/local_setup.bash
ros2 run demo_nodes_py listener
```

---

## 2. ROS Noetic 설치 (Source)
### ROS Noetic 설치 가이드 원본 링크
[https://gist.github.com/Meltwin/fe2c15a5d7e6a8795911907f627255e0](https://gist.github.com/Meltwin/fe2c15a5d7e6a8795911907f627255e0)

### 1. Installing bootstrap dependencies
```bash
sudo apt-get install python3-rosdep python3-rosinstall-generator python3-vcstools python3-vcstool build-essential
```

### 2. Changing rosdep repository adress
1. 
```bash
# 에러 발생 시 ROS Humble 설치에서의 sudo rosdep init 에러 해결 방법과 동일하게 진행한 후 sudo rosdep init 명령어 재실행

sudo rosdep init
```

2. 
```bash
sudo gedit /etc/ros/rosdep/sources.list.d/20-default.list
```

3. 마지막이 base.ymal로 끝나는줄을 아래의 내용으로 수정
**base.yaml 파일 Raw 링크:** [https://raw.githubusercontent.com/mvng6/Noetic-Humble-bridge-setting/main/base.yaml](https://raw.githubusercontent.com/mvng6/Noetic-Humble-bridge-setting/main/base.yaml)
```bash
# 수정할 부분
yaml <enter base.yaml address>

# 수정할 명령어
yaml https://gist.githubusercontent.com/Meltwin/0317ae7481c94da7fd66c3eea8d40740/raw/04f6404249b0430523671410891815e63eadb2fe/base.yaml
```

4. 
```bash
   rosdep update
   
   # 만약 rosdep update 명령어 실행 시 상단에 에러가 출력된 경우
   sudo apt install python3-rosdep2
   rosdep update
```
#### 에러 해결 방법
##### 1. HDDTemp can't be found 와 같은 에러 발생 시
- 에러 출력 예시
```bash
diagnostic_common_diagnostics: [hddtemp] defined as "not available" for OS version [*]
```

- 에러 해결 방법
```bash
sudo add-apt-repository ppa:malcscott/ppa
sudo apt update 
sudo apt install hddtemp
```

### 3.  Create a catkin Workspace
```bash
mkdir -./noetic_ws
cd ./noetic_Ws

rosinstall_generator desktop --rosdistro noetic --deps --tar > noetic-desktop.rosinstall

mkdir ./src

vcs import --input noetic-desktop.rosinstall ./src
```

### 4. Resolving Dependencies
```bash
rosdep install --from-paths ./src --ignore-packages-from-source --rosdistro noetic -y
```

### 5. Building the catkin Workspace
```bash
./src/catkin/bin/catkin_make_isolated -DCMAKE_BUILD_TYPE=Release

# 위 명령어 시 에러가 발생할 가능성 높음
# 만약 에러 발생 시 아래의 rosconsonle error 해결 단계를 진행
# base.ymal 파일로 연결하는 하이퍼링크 설정해줘
```

#### 5.1 Fixing rosconsole error
1. vscode를 열어 noetic_ws 폴더 열기
2. **src/rosconsole/src/rosconsole/impl/rosconsole_log4cxx.cpp** 파일 열고 내용 수정
3. **src/rosconsole/test/thread_test.cpp** 파일 열고 내용 수정
4. **src/rosconsole/test/utest.cpp** 파일 열고 내용 수정
5. noetic_ws에 **change_cpp.py** 파일 생성 및 내용 복붙
6. ```python3 change_cpp.py``` 실행

### 6. Installing noetic
```bash
./src/catkin/bin/catkin_make_isolated --install -DCMAKE_BUILD_TYPE=Release
```

### 7. 설치 확인
```bash
# roscore가 실행되면 정상 설치 완료
source noetic_ws/install_isolated/setup.bash
roscore
```


## 3. ros1-bridge 설치
### ros1-bridge 설치 링크
	https://docs.ros.org/en/humble/How-To-Guides/Using-ros1_bridge-Jammy-upstream.html

### 1. Install development tools and ROS tools
```bash
sudo apt update && sudo apt install -y \
  build-essential \
  cmake \
  git \
  python3-flake8 \
  python3-flake8-blind-except \
  python3-flake8-builtins \
  python3-flake8-class-newline \
  python3-flake8-comprehensions \
  python3-flake8-deprecated \
  python3-flake8-docstrings \
  python3-flake8-import-order \
  python3-flake8-quotes \
  python3-pip \
  python3-pytest \
  python3-pytest-cov \
  python3-pytest-repeat \
  python3-pytest-rerunfailures \
  python3-rosdep \
  python3-setuptools \
  wget

# Install colcon from PyPI, rather than apt packages
python3 -m pip install -U colcon-common-extensions vcstool
```

### 2. Build ros1_bridge
```bash
mkdir -p ~/ros1_bridge/src # Create a workspace for the ros1_bridge
cd ~/ros1_bridge/src

git clone https://github.com/ros2/ros1_bridge

cd ~/ros1_bridge

# Source the ROS 2 workspace
source ~/noetic_ws/install_isolated/setup.bash

# 아래 명령어 실행 시 noetic이 이전에 소스 되었다고 출력이 발생할 수 있음 그럴 경우 아래 명령어를 한번 더 실행해주기
source ~/ros2_humble/install/setup.bash
source ~/ros2_humble/install/setup.bash

# Build
colcon build
```


## 최종 통신 테스트
### 테스트 1 (Humble -> Noetic)
- Talker : Humble
- Listener : Noetic
#### 터미널 1 (Noetic 환경 설정 및 roscore 실행)
```bash
source noetic_ws/install_isolated/setup.bash
roscore
```

#### 터미널 2 (ros1_bridge 환경 설정 맟 ros1_bridge 실행)
```bash
cd ~/ros1_bridge
source install/setup.bash

export ROS_MASTER_URI=http://localhost:11311
ros2 run ros1_bridge dynamic_bridge
```

#### 터미널 3 (Noetic 환경 설정 및 listner 코드 실행)
```bash
source noetic_ws/install_isolated/setup.bash
rosrun roscpp_tutorials listener
```

#### 터미널 4 (Humble 환경 설정 및 talker 코드 실행)
```bash
source ros2_humble/install/setup.bash
ros2 run demo_nodes_py talker
```

### 테스트 2 (Noetic -> Humble)
- Talker : Noetic
- Listener : Humble
#### 터미널 1 (Noetic 환경 설정 및 roscore 실행)
```bash
source noetic_ws/install_isolated/setup.bash
roscore
```

#### 터미널 2 (ros1_bridge 환경 설정 맟 ros1_bridge 실행)
```bash
cd ~/ros1_bridge
source install/setup.bash

export ROS_MASTER_URI=http://localhost:11311
ros2 run ros1_bridge dynamic_bridge
```

#### 터미널 3 (Humble 환경 설정 및 listener 코드 실행)
```bash
source ros2_humble/install/setup.bash
ros2 run demo_nodes_cpp listener
```

#### 터미널 4 (Noetic 환경 설정 및 talker 코드 실행)
```bash
source noetic_ws/install_isolated/setup.bash
rosrun roscpp_tutorials talker
```