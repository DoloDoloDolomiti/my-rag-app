# 청크 크기(Chunk Size)별 RAG 성능 비교 실험 결과

**실험 질문:** `SLB의 로드 밸런싱 정책 중 Persistence-based 알고리즘에는 어떤 것들이 있으며 각각 어떤 특징이 있나요?`

> 동일한 질문에 대해 문서 조각 크기(100, 200, 300, 400자)를 다르게 했을 때, 검색되는 내용과 AI의 답변 품질이 어떻게 달라지는지 비교합니다.

---

## 📏 청크 크기: 100자
- **생성된 총 청크 수:** 24개
- **임베딩 소요 시간:** 11.96초
### 🔍 검색된 문맥 (상위 3개 청크, 총 314자)
```text
웨이 설정: /cfg/ip/gw 1 에서 addr 설정 및 ena로 활성화. 로드밸런싱 정책은 strict/roundrobin이 있다.

SLB (Server Load Balanc

---

ing)
- 장점: 성능 향상, 용이한 확장성 보장, 서버의 효율성 증가, 서버의 보안성 향상, 고 가용성
- 작동 원리: SLB의 핵심 개념은 Session ID(클라이언트의 I

---

IP 주소.
- 로드 밸런싱 정책 (Metric):
  1) Load-based 알고리즘 (LeastConns, RoundRobin)
  2) Persistence-based 알고
```
### 🤖 Gemini의 답변
> 문서에 해당 내용이 없습니다.

---

## 📏 청크 크기: 200자
- **생성된 총 청크 수:** 12개
- **임베딩 소요 시간:** 5.95초
### 🔍 검색된 문맥 (상위 3개 청크, 총 614자)
```text
ing)
- 장점: 성능 향상, 용이한 확장성 보장, 서버의 효율성 증가, 서버의 보안성 향상, 고 가용성
- 작동 원리: SLB의 핵심 개념은 Session ID(클라이언트의 IP와 TCP 포트 번호의 조합). Session ID 대치 기능이 작동함 (NAT와 유사).
- 가상 IP 주소(VIP): 실제 해당서비스에 대하여 외부의 클라이언트가 보게 되는 

---

IP 주소.
- 로드 밸런싱 정책 (Metric):
  1) Load-based 알고리즘 (LeastConns, RoundRobin)
  2) Persistence-based 알고리즘 (Hashing, Minmiss)
- 설정 명령어:
  리얼서버 설정: /cfg/slb/real 1
  리얼서버 그룹 설정: /cfg/slb/gr 1
  가상서버 설정: /c

---

대해서만 중간에서 가로채 지정된 Cache로 돌려준다).
- 설정 명령어: 필터 적용 (/cfg/slb/fil 100), 필터 활성화(adv, action, group, rport, ena).

FWLB (Firewall Load Balancing)
- 장점: 성능 향상(256개의 FWLB 지원), 가용성(Active-Active), 투명함, 플랫폼 독립적
```
### 🤖 Gemini의 답변
> 참고 문서에 따르면 SLB의 Persistence-based 알고리즘 종류로는 **Hashing**과 **Minmiss**가 있습니다. 

다만, 각 알고리즘의 구체적인 특징에 대해서는 **문서에 해당 내용이 없습니다.**

---

## 📏 청크 크기: 300자
- **생성된 총 청크 수:** 8개
- **임베딩 소요 시간:** 4.84초
### 🔍 검색된 문맥 (상위 3개 청크, 총 914자)
```text
ing)
- 장점: 성능 향상, 용이한 확장성 보장, 서버의 효율성 증가, 서버의 보안성 향상, 고 가용성
- 작동 원리: SLB의 핵심 개념은 Session ID(클라이언트의 IP와 TCP 포트 번호의 조합). Session ID 대치 기능이 작동함 (NAT와 유사).
- 가상 IP 주소(VIP): 실제 해당서비스에 대하여 외부의 클라이언트가 보게 되는 IP 주소.
- 로드 밸런싱 정책 (Metric):
  1) Load-based 알고리즘 (LeastConns, RoundRobin)
  2) Persistence-based 알고

---

기본 설정 사항
- 명령어 체계: 글로벌 커멘드 (help, up, print, pwd, diff, apply, save 등)
- 시스템 기본설정: /cfg/sys 메뉴에서 날짜, 시간, 웹포트, 텔넷 허용 옵션 등 설정
- 스위치 IP 설정: /cfg/ip/if 1 에서 addr, mask, broad, vlan 설정 및 ena로 활성화
- 스위치 게이트웨이 설정: /cfg/ip/gw 1 에서 addr 설정 및 ena로 활성화. 로드밸런싱 정책은 strict/roundrobin이 있다.

SLB (Server Load Balanc

---

대해서만 중간에서 가로채 지정된 Cache로 돌려준다).
- 설정 명령어: 필터 적용 (/cfg/slb/fil 100), 필터 활성화(adv, action, group, rport, ena).

FWLB (Firewall Load Balancing)
- 장점: 성능 향상(256개의 FWLB 지원), 가용성(Active-Active), 투명함, 플랫폼 독립적.
- 개념: 화이어 월 서버의 로드 밸런싱이 아니라 두개의 경로에 대한 로드 밸런싱. 스위치는 설정된 정적 라우팅을 사용하여 강제로 트래픽을 동일한 경로로 보낸다. Hash 정책
```
### 🤖 Gemini의 답변
> 문서에 해당 내용이 없습니다.

---

## 📏 청크 크기: 400자
- **생성된 총 청크 수:** 6개
- **임베딩 소요 시간:** 3.41초
### 🔍 검색된 문맥 (상위 3개 청크, 총 1177자)
```text
ing)
- 장점: 성능 향상, 용이한 확장성 보장, 서버의 효율성 증가, 서버의 보안성 향상, 고 가용성
- 작동 원리: SLB의 핵심 개념은 Session ID(클라이언트의 IP와 TCP 포트 번호의 조합). Session ID 대치 기능이 작동함 (NAT와 유사).
- 가상 IP 주소(VIP): 실제 해당서비스에 대하여 외부의 클라이언트가 보게 되는 IP 주소.
- 로드 밸런싱 정책 (Metric):
  1) Load-based 알고리즘 (LeastConns, RoundRobin)
  2) Persistence-based 알고리즘 (Hashing, Minmiss)
- 설정 명령어:
  리얼서버 설정: /cfg/slb/real 1
  리얼서버 그룹 설정: /cfg/slb/gr 1
  가상서버 설정: /c

---

.
- 개념: 화이어 월 서버의 로드 밸런싱이 아니라 두개의 경로에 대한 로드 밸런싱. 스위치는 설정된 정적 라우팅을 사용하여 강제로 트래픽을 동일한 경로로 보낸다. Hash 정책을 사용(SIP, DIP 변수).
- 설정 절차: 스위치 인터페이스 설정, VLAN 설정, 리얼 서버/그룹 설정, IP 포워딩 설정(/cfg/ip/frwd on), 트래픽 리다이렉션 필터 설정.

VRRP (Virtual Router Redundancy Protocol)
- 스위치에 대한 리던던시(Redundancy)를 제공한다. Cisco의 HSRP와 유사한 개념.
- 구성 가능 형태: Hot-Standby, Active-Standby, Active-Active.


---

위치의 FDB 테이블 참조)
- Layer 4 스위칭: 스위칭의 결정 요소가 서비스 타입(Port)이 된다. VIP로 오는 http트래픽인 경우 리얼서버 중 하나로 스위칭한다.

기본 설정 사항
- 명령어 체계: 글로벌 커멘드 (help, up, print, pwd, diff, apply, save 등)
- 시스템 기본설정: /cfg/sys 메뉴에서 날짜, 시간, 웹포트, 텔넷 허용 옵션 등 설정
- 스위치 IP 설정: /cfg/ip/if 1 에서 addr, mask, broad, vlan 설정 및 ena로 활성화
- 스위치 게이트웨이 설정: /cfg/ip/gw 1 에서 addr 설정 및 ena로 활성화. 로드밸런싱 정책은 strict/roundrobin이 있다.

SLB (Server Load Balanc
```
### 🤖 Gemini의 답변
> 참고 문서에 따르면 SLB의 Persistence-based 알고리즘에는 **Hashing**과 **Minmiss**가 있습니다.

다만, 각각의 세부 특징에 대한 내용은 문서에 나와 있지 않습니다.

---
