# 순장훈련학교 순편성 프로그램

**Date**: 							2022.08.31

**Name**:  						ChangMin An

**Github**: 						[Link](https://github.com/ckdals915/CCC)



## I. Introduction

CCC 순장훈련학교 조편성할 때 많은 인원으로 인해 현장에서 조를 편성하는 데에 있어서 어려움이 있었다. 이를 보완하고 순장 3~5명, 순원 1~2명으로 편성하는 알고리즘을 구현하였다.



## II. Flow-Chart

<img src="https://github.com/ckdals915/CCC/picture/flowchart.jpg?raw=true?raw=true?raw=true?raw=true" style="zoom:80%;" />



## III. PointNet Architecture

<img src="https://github.com/ckdals915/LiDAR/blob/main/docs/pictures/PointNet_Architecture.jpg?raw=true?raw=true?raw=true?raw=true" style="zoom:80%;" />

Architecture에는 3가지 주요 모듈이 있다. **max pooling layer**는 모든 점들로부터 정보를 모으기 위한 symmetric 함수이며, **지역 및 전역 정보 조합 구조**, 입력 점군과 점 특징들을 정렬하는 2개의 **joint alignment network**로 구성된다. 



### 1. Symmetry Function for Unordered Input

정렬은 2차원에서 좋은 solution이지만 높은 차원(3D)의 자료 정렬은 존재하지 않는다. 예를 들어, 고차원 공간의 점들을 1차원 실수 선으로 projection한 후 정렬할 수 있으나, 이에 대한 역변환으로 원 데이터를 복구할 수 없다. 이를 해결하기 위한 PointNet의 아이디어는 변환된 요소에 대한 **symmetric function**(max-pooling)을 적용한 점군을 정의하는 것이다. 이는 순서에 상관없이 결과가 일정하게 나오기 위함이다. 

f({x1, ..., xn}) = g(h(x1), ..., h(xn))

이 때 g가 max pooling을 해주는 symmetric function이다.



### 2. A Local and Global Information Combination Structure

벡터 f1, ..., fk 형태의 출력은 입력 집합에 대한 global information이다. SVM이나 MLP를 이용해 형상의 전역 특징을 학습하는 것은 쉽지만, local 및 global information을 구분해 얻는 것이 필요하다. **전역 특징이 계산된 후, 각 점들의 특징과 전역 특징을 연결하여 포인트 특징을 얻는다.** 



### 3. Joint Alignment Network

점군의 labeling은 형상 변환(translation, rotation)에 대해 불변이어야 한다. 이를 위해 mini-network(T-net)을 정의하고 적용한다. 이 때 T-net에서 transformation된 matrix를 추정하여 사용한다. 

