# github 가이드

# 0. github 계정 생성

[github.com](http://github.com) 에서 본인 이메일을 사용해서 계정 생성 진행하면 됩니다.

![image1](/resources/github-guide/image1.png)


# 1. organization 가입

## 1-1. 이메일 초대 확인

2025ajou-capstone 프로젝트에 초대 받기 위해서는 허재석, 이운호에게 이야기해주세요.

생성하신 github 계정으로 2025ajou-capstone 프로젝트에 접근할 수 있도록 초대해드리겠습니다.

![image2](/resources/github-guide/image2.png)

## 1-2. github 로그인

이메일에서 join 버튼을 클릭하시면 github 웹 사이트로 연결되며, 이전에 생성하신 github 계정으로 로그인하시면 됩니다.

![image3](/resources/github-guide/image3.png)

## 1-3. organization 가입

2025ajou-capstone 프로젝트에 가입하시면 됩니다.

![image4](/resources/github-guide/image4.png)

## 1-4. organization 내부의 repositories 클릭

2025ajou-capstone 프로젝트에 가입하신 이후에 Repositories를 클릭하시고, 2025ajou-capstone이 있는 것을 확인합니다.
![image5](/resources/github-guide/image5.png)

## 1-5. organization 내부의 repositories 클릭

다음과 같이 화면이 나왔다면 organization에 정상적으로 가입했고, repository에도 접근할 수 있는 권한을 얻었습니다.

![image6](/resources/github-guide/image6.png)

# 2. git 설치 및 설정

## 2-1. git 프로그램 다운로드 및 설치

- macOS: `brew install git`
- Windows: [Git 공식 다운로드](https://git-scm.com/downloads)
- Ubuntu: `sudo apt install git`

window 사용자분들은 아래 본인의 컴퓨터에 맞는 setup 파일을 다운 받습니다.

일반적으로 64-bit git for windows setup을 클릭하여 다운 받고, 설치하시면 됩니다.

![image7](/resources/github-guide/image7.png)


![image8](/resources/github-guide/image8.png)


![image9](/resources/github-guide/image9.png)

## 2-2. git 설치 확인

아래 명령어를 명령 프롬프트(터미널)에서 실행하여 정상적으로 설치 되었는지 확인합니다.

```javascript
git --version
```


![image10](/resources/github-guide/image10.png)

## 2-3. git config 설정

해당 컴퓨터에서 사용할 git 계정의 정보를 등록합니다.

이전에 github 계정 만들었던 정보를 여기서 사용하시면 됩니다.

```jsx
git config --global user.name "Your Name"
git config --global user.email "youremail@example.com"
```

# 3. 프로젝트를 로컬(내 컴퓨터)에서 세팅하기

## 3-1. 프로젝트 repository 접속

https://github.com/2025ajou-capstone/2025ajou-capstone

위 링크로 접속하여 repository에 접근되는지 확인합니다.

3-2. Code 버튼 클릭


![image11](/resources/github-guide/image11.png)

## 3-3. 터미널 클론 (권장 O)

> GitHub에 있는 원격 저장소를 내 로컬 컴퓨터로 복사하는 작업입니다.
> 

복사하고자 하는 폴더의 위치에서 터미널을 실행하고, 아래 명령어를 통해 복사합니다.
![image12](/resources/github-guide/image12.png)



```javascript
git clone https://github.com/2025ajou-capstone/2025ajou-capstone.git
```

## 3-3. zip 파일 다운 (권장 X)

download zip 파일을 클릭하여, 프로젝트를 다운 받을 수 있습니다.

명령어를 통해서 다운 받지 않다보니, git의 기능을 온전히 사용할 수 없어서 권장하지 않습니다.

다른 사람의 변경사항등을 쉽게 가져오기 어렵습니다.

→ google drive 다운로드와 유사합니다.

![image13](/resources/github-guide/image13.png)


# 4. 개발 환경 세팅

# 5. 코드 기여하기








