# คัมภีร์ AWS Certified Solutions Architect – Professional (SAP-C02) ภาษาไทย

> ฉบับสังเคราะห์จาก Stella League Week 1–8, ข้อสอบฝึก 75 ข้อ, คลังแบบทดสอบ และ AWS Exam Guide ปัจจุบัน
>
> อัปเดต: 10 สิงหาคม 2026

## คำเตือนที่จริงใจ

เอกสารนี้ออกแบบให้เป็นแกนหลักสำหรับสอบผ่าน SAP-C02 แต่ไม่มีเอกสารใดรับประกันผลสอบได้ 100% เพราะข้อสอบวัดการตัดสินใจเชิงสถาปัตยกรรม ไม่ใช่การจำชื่อบริการอย่างเดียว ต้องอ่านเอกสารนี้ควบคู่กับการทำโจทย์ในเว็บไซต์ `sap-c02-practice`, วิเคราะห์ทุกข้อที่ผิด และมีประสบการณ์ลงมือทำหรือวาด data flow ด้วยตัวเอง

คำว่า **trick / cheat** ในเอกสารนี้หมายถึง **cheat sheet, วิธีตัดตัวเลือก และหลักจำที่ถูกต้อง** ไม่ใช่ข้อสอบหลุดหรือการโกงข้อสอบจริง

---

## 1. วิธีใช้คัมภีร์เล่มนี้ให้คุ้มที่สุด

อ่าน 3 รอบ โดยแต่ละรอบมีเป้าหมายต่างกัน:

1. **รอบเข้าใจภาพใหญ่** — อ่านส่วนหลักคิด, 4 Domains และตารางเปรียบเทียบบริการ อย่าพยายามจำทุกบรรทัด
2. **รอบตัดสินใจ** — อ่านส่วน “เห็นคำนี้ ให้คิดถึงอะไร” และฝึกอธิบายว่าเหตุใดตัวเลือกอื่นจึงผิด
3. **รอบก่อนสอบ** — อ่าน One-page mental model, กับดัก, สิ่งที่เปลี่ยนย้อนหลังไม่ได้ และ checklist ความพร้อม

ทุกครั้งที่ทำโจทย์ผิด ให้เขียนกฎหนึ่งบรรทัดในรูปแบบนี้:

> **เงื่อนไขสำคัญ → บริการ/สถาปัตยกรรม → เหตุผลที่ชนะตัวเลือกอื่น**

ตัวอย่าง:

> UDP + ผู้ใช้ทั่วโลก + static IP → AWS Global Accelerator → CloudFront เน้น HTTP caching และ Route 53 ไม่ให้ anycast static IP

---

## 2. รู้จักข้อสอบก่อนเรียน

| รายการ | ข้อมูลที่ต้องจำ |
|---|---|
| รหัส | SAP-C02 |
| เวลา | 180 นาที |
| จำนวน | 75 ข้อ |
| รูปแบบ | Multiple choice และ multiple response |
| ข้อมีคะแนน | 65 ข้อ |
| ข้อทดลองไม่คิดคะแนน | 10 ข้อ และไม่บอกว่าเป็นข้อใด |
| คะแนน | 100–1,000; ผ่านที่ 750 |
| การให้คะแนน | แบบชดเชยรวมทั้งฉบับ ไม่จำเป็นต้องผ่านทุก Domain |
| เว้นว่าง | ผิด |
| เดา | ไม่มีการหักคะแนนเพิ่ม จึงต้องตอบทุกข้อ |

### น้ำหนัก Domain

| Domain | น้ำหนัก | ความหมายแบบสั้น |
|---|---:|---|
| D1 Design Solutions for Organizational Complexity | 26% | องค์กรหลายบัญชี, network, security, resilience, cost visibility |
| D2 Design for New Solutions | 29% | ออกแบบระบบใหม่ให้ deploy, secure, reliable, fast และคุ้มค่า |
| D3 Continuous Improvement for Existing Solutions | 25% | ตรวจ วัด แก้ และปรับระบบเดิมให้ดีขึ้น |
| D4 Accelerate Workload Migration and Modernization | 20% | ประเมิน ย้าย และ modernize workload |

### หัวข้อ emerging ที่อาจเจอแบบไม่คิดคะแนน

AWS Exam Guide ปัจจุบันระบุหัวข้อ Responsible AI ได้แก่:

- Amazon Bedrock Guardrails สำหรับ content filtering และ compliance
- AgentCore Identity สำหรับควบคุมการเข้าถึง generative/agentic AI
- AWS Step Functions สำหรับ human approval/oversight workflow

อย่าทุ่มเวลาให้หัวข้อนี้จนเบียดหัวข้อหลัก เพราะ AWS ระบุว่า emerging-topic questions เป็น pretest ที่ไม่คิดคะแนน แต่ควรรู้แนวคิดระดับสถาปัตยกรรม

---

## 3. อัลกอริทึมแก้โจทย์ SAP-C02

ข้อสอบ Professional มักให้ข้อมูลยาว แต่มี “คำตัดสิน” จริงเพียง 2–4 จุด ใช้ขั้นตอนนี้ทุกข้อ

### ขั้นที่ 1 — อ่านคำถามท้ายสุดก่อน

หา objective เช่น:

- **least operational overhead** → managed service, Organizations integration, event-driven automation
- **lowest cost** → ต้องผ่าน requirement ทั้งหมดก่อน แล้วจึงเลือกตัวที่ถูกสุดในกลุ่มที่ผ่าน
- **minimal application changes** → rehost/replatform, รักษา protocol/engine/API เดิม
- **most secure** → private path, least privilege, centralized audit, encryption, no long-lived credentials
- **fastest recovery** → warm standby / multi-site / promoted replica ตาม RTO/RPO
- **near real time** → streaming/event-driven ไม่ใช่ scheduled batch

### ขั้นที่ 2 — ขีดเส้นใต้ข้อห้ามและ SLA

คำว่า `must`, `cannot`, `without`, `within`, `all accounts`, `existing and future`, `no public internet`, `RPO`, `RTO` มักเป็นตัวฆ่า distractor

ตัวอย่าง: “retrieve within 5 hours” ทำให้ Glacier Deep Archive ผิด แม้ราคาถูกกว่า

### ขั้นที่ 3 — ระบุ scope ให้ถูก

ถามตัวเอง:

- บัญชีเดียวหรือทั้ง Organization?
- AZ เดียว, หลาย AZ หรือหลาย Region?
- HTTP หรือ TCP/UDP?
- AWS-to-AWS, on-prem-to-AWS หรือ user-to-AWS?
- ข้อมูลเก่า, ข้อมูลใหม่ หรือทั้งสองแบบ?
- control plane, data plane หรือ identity plane?

### ขั้นที่ 4 — วาด data path ในหัว

สำหรับ network ให้ไล่ทั้งขาไปและขากลับ:

`source → DNS → route table → attachment/endpoint/NAT/IGW/firewall → destination → return path`

สำหรับ event-driven:

`producer → buffer/router → consumer → retry/DLQ → observation`

สำหรับ cross-account permission:

`identity policy ฝั่งผู้เรียก + trust/resource policy ฝั่งปลายทาง + SCP/permission boundary ที่ครอบอยู่`

### ขั้นที่ 5 — แยกหน้าที่ของ control plane

| หน้าที่ | เครื่องมือ |
|---|---|
| ให้/จำกัดสิทธิ์ | IAM, resource policy, SCP, permission boundary |
| กำหนดเส้นทาง | Route table, TGW route table, Route 53 policy |
| กรอง network | Security group, NACL, WAF, Network Firewall |
| เข้ารหัส | KMS, CloudHSM, ACM, TLS |
| ตรวจและบันทึก | CloudTrail, Config, CloudWatch, Flow Logs |
| รวม security findings | Security Hub |

Distractor ที่พบบ่อยคือเอาเครื่องมือคนละ plane มาแทนกัน เช่น ใช้ IAM policy แทนการ share Transit Gateway หรือใช้ Flow Logs เพื่ออ่าน packet payload

### ขั้นที่ 6 — ตัด self-managed ก่อนเมื่อ requirement ไม่ได้บังคับ

ถ้ามี managed service ที่ทำ requirement ครบ มักชนะการสร้าง EC2 + script + cron + custom Lambda จำนวนมาก โดยเฉพาะเมื่อโจทย์มีคำว่า least operational overhead

### ขั้นที่ 7 — Multiple response ต้องครบชุด

AWS ให้คะแนนเมื่อเลือกคำตอบถูก **ทั้งหมด** เท่านั้น เลือกเกินหนึ่งข้อก็ผิดทั้งข้อ ตรวจว่าแต่ละตัวเลือกทำหน้าที่ต่างกันและรวมกันเป็น end-to-end solution จริง

### ใช้ AWS Well-Architected เป็น lens สุดท้าย

เมื่อเหลือสองตัวเลือกที่ดูถูกทั้งคู่ ให้ประเมิน 6 pillars:

| Pillar | คำถามที่ต้องถาม |
|---|---|
| Operational Excellence | deploy/operate/observe/learn และ rollback ได้หรือไม่ |
| Security | least privilege, traceability, protection at layers, encryption, incident response ครบหรือไม่ |
| Reliability | recover, scale, isolate fault, backup และ test recovery ได้หรือไม่ |
| Performance Efficiency | resource/purpose-built service ตรง access pattern หรือไม่ |
| Cost Optimization | จ่ายเฉพาะสิ่งที่ให้คุณค่าและ optimize ต่อเนื่องหรือไม่ |
| Sustainability | ลด idle/overprovisioning และใช้ managed/efficient resources หรือไม่ |

ข้อสอบมักให้หลายตัวเลือกที่ “ทำงานได้” แต่คำตอบที่ถูกคือแบบที่ balance pillars ตาม business constraint ได้ดีที่สุด

---

# ภาคที่ 1 — เนื้อหาตาม Domain

## 4. Domain 1 — Design Solutions for Organizational Complexity (26%)

### 4.1 Multi-account foundation

สถาปัตยกรรมมาตรฐานขององค์กรควรคิดเป็นชั้น:

1. **AWS Organizations** — สร้างลำดับ Root → OU → Account, consolidated billing และ policy inheritance
2. **AWS Control Tower** — สร้าง landing zone และ orchestration ของ Organizations, IAM Identity Center, Config, CloudTrail/central logging
3. **IAM Identity Center** — SSO, permission sets และ federation กับ external IdP
4. **Security/Log Archive/Audit accounts** — แยก blast radius และหน้าที่
5. **Delegated administrator** — ให้ account เฉพาะดูแล Security Hub, GuardDuty, Config, Backup ฯลฯ แทน management account
6. **Account Factory / Service Catalog** — provision account และ approved products แบบมาตรฐาน

#### SCP ไม่ใช่ IAM policy

- SCP กำหนด **เพดานสูงสุด** ของ permission ใน account/OU
- SCP **ไม่ grant** permission
- IAM policy ยังต้อง Allow
- Explicit Deny ชนะ Allow
- SCP มีผลถึง root user ใน member account แต่โดยทั่วไปไม่จำกัด management account เอง
- ถ้า IAM ดูเหมือน Allow แต่ยัง AccessDenied ให้ตรวจ SCP, permission boundary, session policy และ resource policy

#### Policy ที่มักสับสน

| ต้องการ | ใช้ |
|---|---|
| ห้าม service/action/Region ทั้ง OU | SCP |
| บังคับรูปแบบ tag value มาตรฐาน | Organizations tag policy |
| บังคับให้ request ต้องมี tag | SCP condition เช่น `aws:RequestTag` |
| backup ทุก account ตาม schedule | Organizations backup policy + AWS Backup |
| Deploy CloudFormation หลาย account/Region | CloudFormation StackSets |
| Deploy AWS Config rules เป็นชุดทั่วองค์กร | Organization conformance pack |
| ให้ทีมเลือก deploy ได้เฉพาะแบบที่อนุมัติ | Service Catalog product + launch constraint |

### 4.2 Cross-account access

หลัก AssumeRole ต้องครบสองด้าน:

- ฝั่ง caller มี identity policy อนุญาต `sts:AssumeRole`
- ฝั่ง role มี trust policy เชื่อ principal จาก account ต้นทาง
- role มี permissions policy สำหรับ resource ปลายทาง
- ไม่มี SCP/permission boundary มาปิด

การ share resource ไม่ใช่การให้ IAM permission เสมอไป:

- Share Transit Gateway, subnet, Route 53 Resolver rule ฯลฯ ด้วย AWS RAM
- เปิด trusted access / sharing with Organizations เมื่อต้อง share ทั้งองค์กร
- Resource-based policy ใช้ได้กับ S3, SQS, KMS และบริการที่รองรับ

### 4.3 Network at organization scale

#### VPC Peering vs Transit Gateway vs PrivateLink

| ทางเลือก | เหมาะกับ | ข้อจำกัดสำคัญ |
|---|---|---|
| VPC Peering | เชื่อมไม่กี่ VPC แบบ one-to-one | ไม่ transitive, CIDR ห้ามซ้อน, full mesh โตยาก |
| Transit Gateway | hub-and-spoke หลาย VPC/VPN/DX | ต้องออกแบบ TGW route tables และ segmentation |
| AWS PrivateLink | expose service แบบ private ให้ consumer | one-way service access ไม่ใช่ full network connectivity |
| VPC Lattice | service-to-service connectivity หลาย VPC/account | เน้น application service network และ policy |
| Cloud WAN | global network policy หลาย Region/site | เหมาะ global enterprise network มากกว่า TGW เดี่ยว |

#### Hybrid connectivity

| Requirement | คำตอบหลัก |
|---|---|
| remote user รายบุคคล | AWS Client VPN |
| site/branch เชื่อมผ่าน internet แบบ encrypted | Site-to-Site VPN |
| private bandwidth สม่ำเสมอ | Direct Connect |
| DX ต้อง encrypted end-to-end | VPN over Direct Connect |
| หลาย VPC ผ่าน DX | DX Gateway + Transit VIF + Transit Gateway |
| HA ของ DX | connection อีกเส้น/อีก location และ VPN backup |

Direct Connect VIF:

- **Public VIF** → public AWS endpoints
- **Private VIF** → private IP ใน VPC ผ่าน VGW/DX Gateway
- **Transit VIF** → Transit Gateway ผ่าน DX Gateway

จำว่า DX connection เดียวไม่ใช่ HA และ DX Gateway ไม่ได้ทำให้ association สองฝั่ง route หากันเองโดยอัตโนมัติ

#### Hybrid DNS

- on-prem query private AWS zone → Route 53 Resolver **inbound endpoint** + conditional forwarder ที่ on-prem
- AWS query on-prem domain → Resolver **outbound endpoint** + forwarding rule
- share rule ข้าม account → AWS RAM
- ต้องมี network path ก่อน DNS จึงทำงาน

#### Specialized infrastructure ตาม latency/data residency

| Service | ใช้เมื่อ |
|---|---|
| AWS Outposts | ต้องการ AWS infrastructure/services ใน data center ของลูกค้า เพื่อ latency/local processing/residency |
| AWS Local Zones | ต้องการ compute/storage/database บางบริการใกล้เมือง/ผู้ใช้ปลายทางกว่าการใช้ Region |
| AWS Wavelength | ultra-low latency application บนเครือข่าย 5G ของผู้ให้บริการ |
| Snowball Edge | offline transfer และ edge compute ในพื้นที่ disconnected/limited connectivity |

อย่าเลือก Outposts เพียงเพราะมีระบบ on-prem; ถ้าโจทย์ต้องการเพียง connectivity ให้คิด DX/VPN ก่อน

### 4.4 Security at organization scale

รูปแบบที่ข้อสอบชอบ:

- GuardDuty ตรวจ threat/activity anomaly
- Inspector ตรวจ vulnerability/exposure ของ workload
- Macie ค้นหา sensitive data ใน S3
- IAM Access Analyzer หา external/public access จาก policy
- Security Hub รวมและจัดลำดับ findings ข้าม account/Region
- Firewall Manager บังคับ WAF, Shield Advanced, security group, Network Firewall policy หลาย account
- Organizations + delegated admin ลดงาน setup per account

อย่าสับสน:

- Security Hub ไม่ใช่ตัวสร้าง finding ทุกชนิด แต่เป็น aggregator/normalizer
- GuardDuty ไม่ได้ scan package CVE แบบ Inspector
- Flow Logs มี metadata ไม่ใช่ packet payload; ถ้าต้องอ่าน payload ใช้ Traffic Mirroring ไปยัง inspection appliance

### 4.5 Resilience และ DR

เริ่มจาก business requirement:

- **RPO** = ยอมเสียข้อมูลย้อนหลังได้เท่าไร
- **RTO** = ยอมให้ระบบหยุดได้นานเท่าไร

| Strategy | Cost | RTO/RPO โดยเปรียบเทียบ | สภาพระบบ Region สำรอง |
|---|---:|---|---|
| Backup & Restore | ต่ำสุด | ช้าที่สุด | มี backup ยังไม่มี workload พร้อม |
| Pilot Light | ต่ำ | เร็วขึ้น | core data/service เปิดอยู่, compute ส่วนใหญ่ปิด |
| Warm Standby | กลาง-สูง | เร็ว | ระบบขนาดเล็กทำงานอยู่ตลอด |
| Multi-site active-active | สูงสุด | เร็วที่สุด | รับ traffic เต็มทั้งสองฝั่ง |

เลือกจากตัวเลข RTO/RPO ไม่ใช่เลือก multi-Region แพงที่สุดโดยอัตโนมัติ และต้องรวม DNS/failover orchestration, data replication, secrets, quotas, dependencies และการทดสอบ DR

### 4.6 Cost visibility

- Cost Explorer → วิเคราะห์ cost/usage และ trend
- AWS Budgets → threshold/forecast alert และ Budgets Actions
- Cost and Usage Report (CUR) → ข้อมูลละเอียดที่สุดสำหรับ Athena/BI
- Compute Optimizer → rightsizing จาก metrics
- Trusted Advisor → recommendations หลายหมวด
- Savings Plans → commitment ตาม compute spend; ยืดหยุ่นกว่า RI ในหลายกรณี
- Reserved Instances → benefit ผูกกับ service/attributes ตามชนิด; Standard ลดสูงกว่า Convertible แต่ยืดหยุ่นน้อยกว่า
- Spot → interruptible, เหมาะ batch/restartable/stateless
- Tags + account/OU structure → cost allocation และ ownership

---

## 5. Domain 2 — Design for New Solutions (29%)

### 5.1 แปลง requirement เป็น architecture

ก่อนเลือก service ให้สร้าง acceptance criteria:

- Availability/SLA
- RTO/RPO
- latency/throughput/concurrency
- data consistency/durability
- compliance, encryption, identity, audit
- deployment frequency/rollback
- operational ownership
- growth pattern และ quotas
- total cost รวม data transfer

### 5.2 Deployment และ Infrastructure as Code

| Requirement | แนวทาง |
|---|---|
| AWS resources แบบ declarative | CloudFormation/CDK |
| หลาย account/Region | StackSets |
| software install ตาม runbook ระหว่าง EC2 launch | CloudFormation + EC2 user data หรือ Systems Manager |
| approved self-service products | Service Catalog |
| central patch/config/inventory | Systems Manager |
| safe deployment ต้อง rollback ได้ | blue/green, canary, rolling ตาม risk |

Deployment patterns:

- **All-at-once** — เร็ว แต่ blast radius สูงและ downtime เป็นไปได้
- **Rolling** — เปลี่ยนเป็นชุด ลด capacity ชั่วคราว
- **Rolling with additional batch** — รักษา capacity แต่ใช้ resource เพิ่ม
- **Immutable** — สร้าง fleet ใหม่ ไม่แก้ของเดิม; rollback ชัด
- **Blue/green** — สอง environment สลับ traffic; ค่าใช้จ่ายชั่วคราวสูงแต่เสี่ยงต่ำ
- **Canary/linear** — ปล่อย traffic ส่วนน้อยก่อน เหมาะตรวจ metric แล้ว rollback

CI/CD building blocks:

- CodePipeline → orchestrate stages
- CodeBuild → managed build/test
- CodeDeploy → deployment ไป EC2/on-prem, Lambda หรือ ECS ตาม deployment capability
- CodeArtifact → managed package repository
- ECR → container image registry
- CloudFormation/CDK → provision infrastructure ที่ version/control/repeat ได้

หลักข้อสอบคือ pipeline ต้องมี test, approval ตาม risk, immutable artifact, least-privilege role, observability และ automatic rollback จาก health/alarm

### 5.3 Reliability และ loose coupling

หลักออกแบบ:

- stateless compute หลัง load balancer
- Auto Scaling หลาย AZ
- state อยู่ใน managed database/object/file service ที่รองรับ HA
- queue/buffer รับ traffic spike
- retry แบบ exponential backoff + jitter
- idempotency ป้องกันงานซ้ำ
- timeout/circuit breaker ป้องกัน cascading failure
- DLQ เก็บ poison messages
- quota monitoring ก่อน launch

เลือก integration ให้ตรง semantics:

- SQS → queue, pull, buffering, worker หลายตัว
- SNS → push fan-out
- EventBridge → event routing ตาม content ข้าม service/account
- Kinesis → ordered streaming throughput สูง, replay ตาม retention
- Amazon MQ → รักษา protocol ของ ActiveMQ/RabbitMQ เดิม
- Step Functions → workflow/state/orchestration, retry, branching, human approval

### 5.4 Auto Scaling ให้ดู metric ที่สัมพันธ์กับ demand

- workload แต่ละ request หนักไม่เท่ากัน → CPU อาจดีกว่า request count
- CPU ไม่สัมพันธ์กับ traffic → `ALBRequestCountPerTarget`
- queue worker → backlog per instance ไม่ใช่แค่ queue depth ดิบ
- target tracking → รักษา metric ที่เป้าหมาย
- step scaling → ตอบสนองตามระดับ alarm หลายขั้น เหมาะ spike ใหญ่
- scheduled scaling → pattern เวลาคาดเดาได้
- predictive scaling → pattern เป็นรอบและมีประวัติ

### 5.5 Security by design

- ใช้ role และ temporary credentials แทน access key ฝังใน code
- Secrets Manager สำหรับ secret + rotation; Parameter Store สำหรับ configuration/secret ที่ไม่ต้องการ rotation workflow ขั้นสูง
- KMS สำหรับ managed key integration; CloudHSM เมื่อจำเป็นต้องใช้ single-tenant HSM ที่ควบคุม user/algorithm/key operation โดยตรง หรือใช้ crypto interface เฉพาะ
- ACM จัดการ public/private certificates ตาม use case
- private subnet ไม่เท่ากับ “ออก internet ไม่ได้” ถ้ามี NAT route
- VPC endpoint ลดการผ่าน public internet และ NAT cost
- WAF ป้องกัน L7; Shield ป้องกัน DDoS; Network Firewall ตรวจ/กรอง VPC network traffic
- encrypt at rest + in transit และกำหนด key policy/grant ให้ถูก

### 5.6 Performance — เลือกตาม access pattern

อย่าเริ่มด้วยชื่อ database ให้เริ่มด้วยคำถาม:

- key-value, document, relational, graph, search หรือ time series?
- read/write ratio?
- consistency?
- latency เป้าหมาย?
- transaction/joins?
- data volume และ growth?
- global access?

Patterns ที่ออกบ่อย:

- hot read ซ้ำ → cache/DAX/read replica
- static global content → CloudFront + TTL สูง
- TCP/UDP global latency + static IP → Global Accelerator
- tightly coupled HPC → EFA + cluster placement group + single AZ
- shared POSIX file หลาย AZ → EFS
- Windows SMB → FSx for Windows File Server
- high-performance temporary scratch/HPC → FSx for Lustre

### 5.7 Cost — ถูกที่สุดที่ “ผ่าน requirement”

- baseline สม่ำเสมอ → Savings Plans/RI
- burst ไม่แน่นอน → On-Demand + Auto Scaling
- restartable/fault-tolerant → Spot
- serverless sporadic → จ่ายตามใช้ ลด idle
- S3 lifecycle ตาม access + retrieval SLA
- cache ช่วยทั้ง latency และ origin/data-transfer cost
- NAT Gateway cost อาจลดได้ด้วย gateway/interface endpoints
- cross-AZ และ cross-Region data transfer ต้องอยู่ใน cost model

---

## 6. Domain 3 — Continuous Improvement for Existing Solutions (25%)

Domain นี้ถามว่า “ระบบมีอยู่แล้ว จะตรวจและปรับอย่างไร” คำตอบที่ดีต้องเริ่มจาก evidence และลด manual work

### 6.1 Operational Excellence

วงจรที่ควรจำ:

`instrument → establish baseline → detect → diagnose → automate remediation → verify → document/learn`

| ต้องการ | เครื่องมือหลัก |
|---|---|
| metrics, alarms, logs, dashboard | CloudWatch |
| API activity: ใครทำอะไร เมื่อไร จากไหน | CloudTrail |
| resource configuration/compliance/history | AWS Config |
| inventory, patch, run command, session, automation | Systems Manager |
| trace distributed application | AWS X-Ray / application tracing |
| event-driven remediation | EventBridge → Lambda/SSM Automation |

กฎเลือก:

- “ใครลบ/แก้ resource?” → CloudTrail
- “resource เคยมี configuration อะไร และ compliant ไหม?” → AWS Config
- “CPU/latency/log มีค่าเท่าไร?” → CloudWatch
- “เข้า shell โดยไม่เปิด port 22 พร้อมบันทึก session” → Session Manager
- “บังคับ patch fleet” → Systems Manager Patch Manager

### 6.2 Improve security

ลำดับงานที่ถูกต้อง:

1. Discover/aggregate findings
2. Prioritize ตาม severity และ business context
3. Remediate อัตโนมัติเมื่อปลอดภัย
4. Validate compliance
5. เก็บ evidence และป้องกัน recurrence

Patterns:

- Config rule ตรวจ noncompliance → EventBridge → SSM Automation/Lambda แก้
- Security Hub + Organizations → central delegated admin ข้าม accounts/Regions
- Access Analyzer → external access และ policy validation
- Inspector → vulnerability management
- Macie → sensitive data discovery
- GuardDuty → threat detection จาก logs/signals
- AWS Backup + Vault Lock → centralized immutable backup ตาม compliance

### 6.3 Improve performance

อย่า scale โดยไม่มี evidence:

- กำหนด KPI จาก business เช่น p95 latency, error rate, orders/minute
- baseline ก่อนเปลี่ยน
- หา bottleneck ด้วย metrics/tracing
- เปลี่ยนทีละส่วนและวัดผล
- ทดสอบ load/failure
- rightsize ตามรูปแบบใช้งาน ไม่ใช่ peak ชั่วคราวอย่างเดียว

ตัวเลือกแก้ที่พบบ่อย:

- read-heavy relational → read replicas/cache
- repeated key-value reads → DAX
- static/HTTP global → CloudFront
- dynamic TCP/UDP global → Global Accelerator
- network-heavy HPC → EFA/cluster placement group
- write burst → buffer ด้วย SQS/Kinesis
- database CPU สูงจาก query → index/query tuning ก่อนเพิ่ม instance โดยไม่วิเคราะห์

### 6.4 Improve reliability

ตรวจ single points of failure ทีละชั้น:

- DNS/traffic entry
- load balancer
- compute AZ distribution
- state/database failover
- shared file/storage
- NAT/egress
- on-prem link
- secrets/config dependencies
- quota/limit
- deployment/control plane

ข้อสอบชอบสิ่งที่ดูเหมือน SPOF แต่จริง ๆ managed อยู่แล้ว:

- Internet Gateway หนึ่งตัวต่อ VPC เป็น horizontally scaled/HA โดย service design
- DynamoDB เป็น Regional service
- ALB ข้ามหลาย AZ ได้
- แต่ NAT Gateway เป็น AZ-scoped จึงควรมีต่อ AZ พร้อม route ของแต่ละ subnet

### 6.5 Improve cost

ทำตามลำดับ:

1. **Eliminate** — ปิดของไม่ได้ใช้, orphaned EBS/EIP/snapshot/log
2. **Rightsize** — instance/database/storage/throughput
3. **Elasticize** — scale in/out, serverless, schedule non-prod
4. **Price** — Savings Plans/RI/Spot
5. **Architect** — managed/purpose-built service, caching, lifecycle, endpoint ลด NAT
6. **Govern** — budget, tags, CUR, anomaly detection, owner action

อย่าซื้อ commitment เพื่อแก้ resource ที่ควรถูกปิดหรือ rightsize ก่อน

---

## 7. Domain 4 — Migration and Modernization (20%)

### 7.1 Migration phases

1. **Assess** — discover inventory/dependencies, business case, TCO, readiness
2. **Mobilize** — landing zone, governance, skills, security, wave plan, tools
3. **Migrate and Modernize** — ย้ายเป็น waves, validate, cut over, optimize

เครื่องมือ:

- AWS Application Discovery Service → เก็บข้อมูล server/dependency
- Migration Evaluator → business case/TCO จาก utilization
- AWS Migration Hub → track portfolio และ migration status
- AWS Application Migration Service (MGN) → block-level replication/rehost servers
- AWS DMS → ย้าย/replicate database data
- AWS SCT → convert schema/code สำหรับ heterogeneous database migration
- AWS Control Tower → landing zone/governance

### 7.2 7 Rs

| R | ความหมาย | สัญญาณในโจทย์ |
|---|---|---|
| Retire | เลิกใช้ | ไม่มี owner/usage/business value |
| Retain | ยังไม่ย้าย | dependency/compliance/เวลาไม่พร้อม |
| Rehost | lift and shift | deadline สั้น, source code ไม่มี, minimal change |
| Relocate | ย้าย platform โดยไม่ redesign เช่น VMware | ต้องย้ายเร็วและรักษา environment |
| Replatform | เปลี่ยนบางชั้น | ย้าย DB ไป RDS, containerize โดยแก้ app น้อย |
| Repurchase | เปลี่ยนเป็น SaaS/product ใหม่ | COTS/SaaS ตอบโจทย์แทนระบบเดิม |
| Refactor/Re-architect | redesign cloud-native | ต้อง scale/innovate และยอมลงทุนพัฒนา |

อย่าเลือก refactor เพียงเพราะ “ดีที่สุดในระยะยาว” หากโจทย์กำหนด 90 วันและ minimal application changes

### 7.3 Data transfer decision tree

| เงื่อนไข | บริการ |
|---|---|
| online NFS/SMB transfer, recurring/scheduled | AWS DataSync |
| SFTP/FTPS/FTP endpoint managed | AWS Transfer Family |
| accelerate upload ผ่าน public internet ไป S3 | S3 Transfer Acceleration |
| petabyte/offline และ network ไม่พอ | AWS Snow Family |
| hybrid file access เดิม + S3 backend | S3 File Gateway |
| block/iSCSI hybrid | Volume Gateway |
| virtual tape | Tape Gateway |
| database online migration/CDC | AWS DMS |
| server block replication/rehost | AWS MGN |

คำนวณคร่าว ๆ ก่อนเลือก Snow: ถ้า internet transfer ใช้เวลาไม่กี่วัน แต่การส่งอุปกรณ์ไป-กลับนานกว่า online transfer อาจชนะ

### 7.4 Database migration

- homogeneous: engine เดิม → engine เดิม; DMS/database-native tools
- heterogeneous: engine ต่างกัน → **SCT convert schema/code + DMS move/replicate data**
- minimal downtime → full load + CDC แล้ว cut over
- ตรวจ datatype, unsupported objects, LOB, latency, network, validation และ rollback

ตัวอย่าง: Oracle → Aurora PostgreSQL ต้องคิด SCT + DMS ไม่ใช่ DMS อย่างเดียว

### 7.5 Modernization

ลำดับความเปลี่ยนแปลงจากน้อยไปมาก:

`EC2 rehost → managed database/storage → containers → serverless/event-driven → purpose-built data services`

เลือกตามข้อจำกัด:

- custom OS/driver/legacy binary → EC2
- container แต่ไม่อยากจัดการ server → ECS/EKS on Fargate
- short-lived event function → Lambda
- orchestration หลายขั้น → Step Functions
- decouple producer/consumer → SQS/EventBridge/SNS/Kinesis ตาม semantics
- proprietary ActiveMQ/RabbitMQ protocol → Amazon MQ ลด rewrite
- relational transaction/joins → RDS/Aurora
- key-value scale → DynamoDB
- search/log analytics → OpenSearch

### 7.6 Mainframe modernization

แนวทางไม่ใช่มีเพียง rehost:

- automated refactoring → แปลง code/runtime ไป modern stack เมื่อ tooling รองรับ
- replatform → รักษา logic แต่ย้าย runtime/database บางชั้น
- data replication/integration → ลด downtime และแบ่ง migration เป็น waves
- strangler pattern → สร้าง capability ใหม่รอบระบบเดิม แล้วค่อยลดส่วนเดิม
- ต้องประเมิน job schedule, batch window, transaction consistency, dependency, licensing, test parity และ rollback

เมื่อ deadline สั้นและ risk สูง ให้เริ่มจากทางที่เปลี่ยนน้อย แล้ววาง modernization phase หลัง stabilize แทนการบังคับ rewrite ทั้งระบบในครั้งเดียว

---

# ภาคที่ 2 — ตารางเลือกบริการแบบออกสอบ

## 8. Networking, Edge และ DNS

### 8.1 CloudFront vs Global Accelerator vs Route 53

| คุณสมบัติ | CloudFront | Global Accelerator | Route 53 |
|---|---|---|---|
| ชั้นหลัก | L7 CDN | L4 network acceleration | DNS |
| Protocol | HTTP/HTTPS | TCP/UDP | DNS response |
| Cache | มี | ไม่มี | ไม่มี |
| Static anycast IP | ไม่ใช่จุดเด่น | มี 2 IP | ไม่มี |
| Edge compute | CloudFront Functions/Lambda@Edge | ไม่มี | ไม่มี |
| Health/failover | origin failover | endpoint health + traffic dial | health check + routing policy |
| เลือกเมื่อ | static/dynamic web, caching, edge logic | global non-HTTP/UDP/static IP/fast failover | DNS-level routing/failover |

คำใบ้:

- “UDP game” → Global Accelerator
- “สอง static IPs” → Global Accelerator
- “cache image/video/static site” → CloudFront
- “A/B ต่อ session/cookie” → Lambda@Edge หรือ CloudFront Functions ตาม capability
- “apex domain” → Route 53 alias ไม่ใช่ CNAME

### 8.2 Route 53 routing policies

| Policy | ใช้เมื่อ |
|---|---|
| Simple | ปลายทางเดียว/ไม่มี logic พิเศษ |
| Weighted | แบ่ง traffic ตามสัดส่วน |
| Latency | ไป Region ที่ latency ต่ำ |
| Failover | active-passive พร้อม health check |
| Geolocation | ตามตำแหน่ง user; ต้องมี default หากต้องรองรับทุกที่ |
| Geoproximity | ตามตำแหน่ง resource และปรับ bias |
| Multivalue answer | คืนหลาย healthy records แบบ DNS-level basic balancing |

### 8.3 Elastic Load Balancing

| Load balancer | Layer/protocol | ใช้เมื่อ |
|---|---|---|
| ALB | L7 HTTP/HTTPS/gRPC | host/path/header routing, web/microservices |
| NLB | L4 TCP/UDP/TLS | very high performance, static IP/EIP per AZ, source IP preservation |
| GWLB | L3 IP | transparent insertion/scaling ของ firewalls/appliances |
| CLB | legacy | workload เก่า; ระบบใหม่ควรเลือก ALB/NLB ตาม protocol |

ALB target health ไม่เหมือน Route 53 health check: ALB ตรวจ targets ภายใน target group ส่วน Route 53 ใช้ DNS-level endpoint routing/failover

### 8.4 VPC endpoints

- Gateway endpoint → S3 และ DynamoDB, route table, ไม่มี hourly charge แบบ interface endpoint
- Interface endpoint → AWS PrivateLink/ENI/private IP, หลาย AWS services, security group, มีค่าใช้จ่าย
- Gateway Load Balancer endpoint → ส่ง traffic ไป security virtual appliances
- endpoint policy จำกัดสิทธิ์ผ่าน endpoint แต่ไม่แทน IAM/resource policy ทั้งหมด

### 8.5 Stateful vs stateless

- Security Group = stateful; allow ขาไปแล้ว return traffic ได้อัตโนมัติ
- NACL = stateless; ต้อง allow ทั้งสองทิศและ ephemeral ports
- Flow Logs ขึ้น `ACCEPT` outbound แต่ `REJECT` return ที่ ENI → สงสัย NACL ก่อน SG
- Route table ตัดสินเส้นทางด้วย longest-prefix match

### 8.6 Network security

| Service | หน้าที่ |
|---|---|
| AWS WAF | L7 HTTP(S), SQLi/XSS/rate/geo/custom rules |
| Shield Standard | DDoS protection พื้นฐานอัตโนมัติ |
| Shield Advanced | DDoS ระดับสูง, visibility, DRT และ cost protection ตามเงื่อนไข |
| AWS Network Firewall | managed stateful VPC firewall/inspection |
| Firewall Manager | central policy หลาย account |
| Gateway Load Balancer | deploy/scale third-party virtual appliances |
| Traffic Mirroring | copy packet traffic เพื่อวิเคราะห์ payload |

---

## 9. Storage และ Data Lifecycle

### 9.1 S3 classes ตาม access pattern

| Class | เหมาะกับ | กับดัก |
|---|---|---|
| Standard | frequent access | แพงกว่าระยะยาว |
| Intelligent-Tiering | access เดาไม่ได้ | มี monitoring fee; archive tiers ต้องเปิดใช้ |
| Standard-IA | infrequent, ต้อง multi-AZ | retrieval/minimum duration charge |
| One Zone-IA | re-creatable หรือ secondary copy | AZ เดียว ไม่เหมาะข้อมูลสำคัญสำเนาเดียว |
| Glacier Instant Retrieval | archive แต่ต้อง milliseconds | retrieval cost สูงกว่า archive ลึก |
| Glacier Flexible Retrieval | minutes–hours | standard retrieval โดยทั่วไปราว 3–5 ชม. |
| Glacier Deep Archive | ถูกสุด, ยอมรอนาน | standard retrieval โดยทั่วไปราว 12 ชม. |

เลือก archive tier จาก **retrieval SLA** ก่อนราคา

### 9.2 S3 high-yield features

- existing objects + future replication → S3 Batch Replication สำหรับของเก่า + replication rule สำหรับของใหม่
- billions of objects → S3 Inventory + Batch Operations
- access pattern หลายทีม/prefix → S3 Access Points
- immutable retention → S3 Object Lock
- privileged user ก็ห้ามลบ → compliance mode
- Object Lock ต้องวางแผนตอนสร้าง bucket ตามเงื่อนไขของโจทย์; อย่าเชื่อ distractor ที่บอกเปิดย้อนหลังกับ bucket ที่ไม่รองรับ
- sensitive data discovery → Macie
- cost/usage visibility หลาย bucket/account → S3 Storage Lens

### 9.3 Block, file, object

| Need | Service |
|---|---|
| block disk ของ EC2 ใน AZ | EBS |
| shared NFS/POSIX หลาย AZ | EFS |
| managed Windows SMB/AD | FSx for Windows File Server |
| high-performance parallel Linux/HPC | FSx for Lustre |
| ONTAP features/NFS/SMB/iSCSI | FSx for NetApp ONTAP |
| object, web-scale, API access | S3 |

EBS Multi-Attach ยังอยู่ใน AZ เดียวและต้องใช้ cluster-aware filesystem จึงไม่ใช่คำตอบทั่วไปสำหรับ shared file HA

---

## 10. Database และ Cache

| Requirement | ตัวเลือกที่เด่น |
|---|---|
| relational managed | RDS |
| cloud-native relational, faster failover/read scale | Aurora |
| global relational reads/DR | Aurora Global Database |
| key-value/document, massive scale | DynamoDB |
| microsecond DynamoDB read cache | DAX |
| in-memory cache/session | ElastiCache Redis/Valkey |
| simple distributed cache, no replication/failover | Memcached |
| durable Redis-compatible primary database | MemoryDB |
| graph relationships | Neptune |
| search/log analytics | OpenSearch |
| data warehouse analytics | Redshift |
| time series | Timestream |

### Redis/Memcached/MemoryDB

- Redis/Valkey → replication, persistence options, Multi-AZ automatic failover
- Memcached → simple multithreaded cache; client ต้องรู้ node ใหม่; ไม่มี replication/Multi-AZ failover แบบ Redis
- MemoryDB → durable Multi-AZ transaction log เหมาะใช้เป็น primary database ที่ต้อง Redis-compatible และความทนทาน

### RDS/Aurora resilience

- RDS Multi-AZ → HA/failover ไม่ใช่ read scaling เป็นหลัก
- read replica → read scaling/DR และ promote ได้
- Aurora reader endpoint → กระจาย read
- Aurora Global Database → cross-Region, low-latency global reads/DR
- planned managed failover เหมาะทดสอบ/switchover โดยลด data loss risk

### Analytics และ data lake

| Need | Service/แนวทาง |
|---|---|
| query S3 ด้วย SQL แบบ serverless | Athena |
| metadata catalog/ETL | AWS Glue + Data Catalog |
| สร้างและ govern data lake | Lake Formation |
| managed Hadoop/Spark ecosystem | EMR |
| enterprise data warehouse | Redshift |
| BI dashboard | QuickSight |
| real-time delivery เข้า S3/Redshift/OpenSearch | Kinesis Data Firehose |

Data lake มักใช้ schema-on-read และ S3 เป็น storage layer; data warehouse ใช้ curated/schema-on-write เพื่อ analytics ที่มีโครงสร้างกว่า Lake Formation ช่วย permissions/governance และสร้าง ingestion workflows ผ่าน Glue ไม่ได้แทน S3 หรือ query engine ทั้งหมด

---

## 11. Compute, Containers และ Serverless

| Requirement | เลือก |
|---|---|
| OS/control/custom driver เต็ม | EC2 |
| web app deploy ง่าย ยังอยากให้ AWS จัด infra | Elastic Beanstalk |
| simple VPS/predictable bundle price | Lightsail |
| container orchestration AWS-native | ECS |
| Kubernetes ecosystem/API | EKS |
| container โดยไม่จัดการ host | Fargate |
| short event-driven execution | Lambda |
| managed batch scheduling/queues | AWS Batch |
| VMware workload relocate | VMware Cloud on AWS ตาม scenario |

### Placement groups และ HPC

- Cluster → instance อยู่ใกล้กันใน AZ เดียว, latency ต่ำ/throughput สูง
- Partition → แยกกลุ่ม instance คนละ rack ลด correlated failure, เหมาะ distributed systems ใหญ่
- Spread → แยก instance จำนวนน้อยแต่ละเครื่องคนละ hardware
- EFA → low-latency/high-throughput HPC/ML communication
- tightly coupled HPC มักต้อง single AZ + cluster placement group + EFA; multi-AZ เพิ่ม latency

### EC2 purchasing

- On-Demand → ไม่มี commitment, load ผันผวน/ชั่วคราว
- Savings Plans → commitment รายชั่วโมง เหมาะ baseline compute
- Reserved Instances → billing discount/capacity reservation บางชนิดตามรายละเอียด
- Spot → ถูกมากแต่ถูก interrupt ได้
- Dedicated Hosts → license/compliance/host visibility
- Capacity Reservations → reserve capacity ใน AZ แต่ไม่ใช่ส่วนลดราคาโดยตัวมันเอง

### Hibernation trap

EC2 hibernation ต้องรองรับ instance/AMI, root EBS encrypted และเปิดตอน launch อย่าเลือกคำตอบที่พยายามเปิด hibernation ให้ instance เดิมย้อนหลังถ้า requirement ไม่รองรับ

---

## 12. Messaging, Streaming และ Workflow

| Service | Model | Ordering/Replay | ใช้เมื่อ |
|---|---|---|---|
| SQS Standard | queue/pull | at-least-once, best-effort order | decouple, buffer, throughput สูง |
| SQS FIFO | queue/pull | order + dedup ภายในข้อกำหนด | transaction/order ต้องเรียงและลด duplicate |
| SNS | pub/sub push | ไม่ใช่ stream replay | fan-out notification |
| EventBridge | event bus/rules | event routing/archive/replay capability | content-based routing, SaaS/AWS/account integration |
| Kinesis Data Streams | partitioned stream | ordered ต่อ shard + retention/replay | real-time streaming หลาย consumer |
| Amazon MQ | managed broker | ตาม ActiveMQ/RabbitMQ | legacy protocol ลด app rewrite |
| Step Functions | state machine | workflow history | orchestration, retry, wait, parallel, approval |

กับดักสำคัญ:

- เปลี่ยน SQS Standard queue เดิมเป็น FIFO ไม่ได้ ต้องสร้าง FIFO queue ใหม่
- Visibility timeout ต้องยาวกว่าการประมวลผลหรือ extend ระหว่างทำ
- DLQ ไม่แก้สาเหตุ แต่แยก poison messages เพื่อวิเคราะห์/reprocess
- SQS service integration/API Gateway service proxy ลด Lambda/EC2 ที่ไม่จำเป็น
- SNS + SQS fan-out ให้ subscriber แต่ละราย retry/scale แยกกัน

---

## 13. Security, Identity และ Encryption

### 13.1 IAM evaluation mental model

1. ต้องมี applicable Allow
2. Explicit Deny จากที่ใดก็ตามชนะ
3. ตรวจ SCP
4. ตรวจ resource policy/trust policy
5. ตรวจ permission boundary/session policy
6. ตรวจ condition keys, principal, Region, tags และ KMS key policy

### 13.2 Identity services

| Need | Service |
|---|---|
| workforce SSO หลาย AWS accounts/apps | IAM Identity Center |
| app user authentication | Cognito user pool |
| ให้ app user รับ temporary AWS credentials | Cognito identity pool |
| Microsoft AD managed | AWS Managed Microsoft AD |
| proxy ไป on-prem AD ไม่เก็บ credential ใน AWS | AD Connector |
| simple directory need น้อย | Simple AD แต่ตรวจ feature เช่น MFA ก่อน |

Cognito:

- User pool = authentication/user directory/tokens
- Identity pool = federation แล้วออก temporary AWS credentials
- custom identity ที่ไม่ใช่ SAML/OIDC และมี developer backend → developer-authenticated identity กับ identity pool

### 13.3 Encryption and secrets

| Need | เลือก |
|---|---|
| managed integration/envelope encryption | KMS |
| single-tenant HSM, direct user/algorithm/key control, standard crypto APIs | CloudHSM หรือ KMS custom key store ตาม integration requirement |
| application secret + automatic rotation | Secrets Manager |
| config/parameter, SecureString ได้ | Systems Manager Parameter Store |
| TLS certificate lifecycle | ACM |

KMS high-yield:

- ปัจจุบัน AWS KMS standard key store ใช้ HSM ที่ validated ระดับ FIPS 140-3 Security Level 3 เช่นกัน ดังนั้นคำว่า “FIPS Level 3” เพียงอย่างเดียวไม่พอให้สรุปว่าเป็น CloudHSM; ให้ดู requirement เรื่อง single tenancy, direct control, algorithm/API และ operational responsibility
- key policy สำคัญเสมอ; IAM Allow อย่างเดียวอาจไม่พอ
- multi-Region keys ช่วย client-side/application use cases แต่ไม่ได้ replicate encrypted data ให้เอง
- automatic rotation ตาม key type/capability; imported key material มีข้อจำกัดต่างกัน
- deletion มี waiting period; EventBridge แจ้ง admin ได้
- envelope encryption ใช้ data key เข้ารหัสข้อมูล และ KMS key เข้ารหัส data key

### 13.4 Logging and evidence

| คำถาม | คำตอบ |
|---|---|
| API call จาก console/SDK | CloudTrail trail เดียวครอบคลุมทั้งสองประเภท |
| ตรวจว่า CloudTrail log ถูกแก้หรือไม่ | log file integrity validation |
| central immutable logs | Organization trail → dedicated Log Archive S3 + restrictive bucket/KMS policy/Object Lock ตาม requirement |
| network metadata | VPC Flow Logs |
| DNS query | Route 53 Resolver query logging |
| S3 object-level/API data events | CloudTrail data events |

---

## 14. Governance และ Automation Cheat Sheet

| Scenario | คำตอบที่ควรนึกถึงก่อน |
|---|---|
| บังคับ guardrail ทุก current/future account | Organizations policy/SCP + trusted access |
| central security findings | Security Hub delegated admin |
| central GuardDuty | GuardDuty delegated admin + auto-enable members |
| central backup | Organizations backup policy + AWS Backup |
| Config rules หลาย account ยกเว้นบาง account | organization conformance pack + exclusion list |
| deploy infrastructure หลาย account/Region | StackSets |
| distribute approved AMI + template | Service Catalog portfolio/product หรือ StackSets ตามผู้ deploy/ownership |
| self-service ได้แค่ approved patterns | Service Catalog + launch constraints |
| central event from member accounts | EventBridge central event bus + per-account forwarding rules |
| standardized tags | tag policy; ถ้าต้องบังคับตอนสร้างเพิ่ม SCP condition |
| account vending | Control Tower Account Factory |

### Control Tower controls

- Preventive → ห้าม action มักใช้ SCP
- Detective → ตรวจหลังเกิด มักใช้ Config
- Proactive → ตรวจ CloudFormation resource ก่อน provision

### Delegated administration rule

เมื่อเห็น “many accounts/Regions + least operational overhead” ให้มองหา native Organizations integration และ delegated administrator ก่อน custom Lambda loop ทุก account

---

# ภาคที่ 3 — กฎตัดสินและกับดัก

## 15. เห็นคำนี้ ให้คิดถึงสิ่งนี้

1. **all current and future accounts** → Organizations integration/auto-enrollment
2. **least operational overhead** → managed service/native integration/delegated admin
3. **cross-account infrastructure deployment** → StackSets
4. **approved self-service configurations** → Service Catalog
5. **SCP** → permission ceiling, ไม่ grant
6. **external principal access** → IAM Access Analyzer; zone of trust ต้องเป็น Organization หาก account ใน org ไม่ควรถูกนับว่า external
7. **central security findings** → Security Hub
8. **packet payload** → Traffic Mirroring; Flow Logs ไม่เห็น payload
9. **return traffic REJECT** → NACL/ephemeral ports เพราะ SG stateful
10. **segment prod/dev บน TGW** → separate TGW route tables/association/propagation
11. **two static global IPs** → Global Accelerator
12. **UDP global** → Global Accelerator
13. **HTTP cache/edge logic** → CloudFront
14. **apex domain** → Route 53 alias
15. **on-prem resolves private AWS name** → Resolver inbound endpoint
16. **AWS resolves on-prem name** → Resolver outbound endpoint + rule
17. **no inbound SSH + audit + port forwarding** → Session Manager
18. **CloudFront-only S3 origin** → Origin Access Control + bucket policy
19. **CloudFront-only ALB origin** → secret custom header + WAF validation หรือ architecture ที่ปิด direct access ตาม requirement
20. **custom AMI batch + restartable** → AWS Batch EC2 managed compute + Spot
21. **tightly coupled HPC** → EFA + cluster placement group + single AZ
22. **requests หนักไม่เท่ากัน** → scale ด้วย metric ที่สะท้อน work เช่น CPU
23. **CPU ไม่สัมพันธ์ traffic** → RequestCountPerTarget/custom business metric
24. **queue workers** → backlog-per-instance target tracking
25. **shared file multi-AZ** → EFS
26. **Windows SMB** → FSx for Windows
27. **unpredictable S3 access** → Intelligent-Tiering
28. **retrieve within 3–5 hours** → Glacier Flexible Retrieval
29. **12 hours acceptable/cheapest archive** → Deep Archive
30. **re-creatable infrequent data** → One Zone-IA อาจเหมาะ
31. **immutable 5 years no privileged deletion** → Object Lock compliance mode
32. **millions existing S3 objects bulk change** → Inventory + Batch Operations
33. **existing + future S3 replication** → Batch Replication + replication rule
34. **prefix/access pattern scale** → S3 Access Points
35. **repetitive cross-Region reads** → replication อาจคุ้มกว่า transfer ซ้ำ
36. **rare low-volume private cross-Region access** → private connectivity อาจคุ้มกว่า replicate dataset ทั้งก้อน
37. **hybrid NFS/SMB to S3 objects** → S3 File Gateway
38. **automated backup many resource types** → AWS Backup
39. **DynamoDB repeated hot-key reads** → DAX
40. **durable Redis-compatible DB** → MemoryDB
41. **RDS credential rotation** → Secrets Manager
42. **RDS HA** → Multi-AZ
43. **RDS read scale** → read replica
44. **global Aurora relational** → Aurora Global Database
45. **90-second backend but client timeout 10 seconds** → async API → SQS → worker
46. **duplicate/order strict queue** → SQS FIFO ใหม่ ไม่ใช่แก้ Standard เดิม
47. **legacy broker protocol** → Amazon MQ
48. **workflow retry/branch/wait/approval** → Step Functions
49. **server-rendered web app** → S3 static hosting ไม่ได้; container/compute
50. **eliminate OS administration for containers** → Fargate
51. **simple LAMP predictable price** → Lightsail
52. **runbook install + infrastructure** → CloudFormation + user data/SSM
53. **custom IdP neither SAML nor OIDC** → Cognito developer-authenticated identity pattern
54. **contact center intents** → Connect + Lex + Lambda
55. **90-day migration/no source** → MGN rehost
56. **heterogeneous database** → SCT + DMS
57. **online recurring file transfer** → DataSync
58. **offline huge data/network too slow** → Snow Family
59. **SFTP managed endpoint** → Transfer Family
60. **console and SDK audit + tamper detection** → CloudTrail + integrity validation
61. **single-tenant/direct HSM control + flexible crypto interface** → CloudHSM; FIPS Level 3 อย่างเดียวไม่ใช่ตัวแยกจาก KMS ปัจจุบัน
62. **forecast budget before threshold + action** → AWS Budgets forecasted alert/action
63. **baseline compute** → Savings Plans/RI
64. **fault-tolerant batch** → Spot
65. **central event remediation** → EventBridge + Lambda/SSM Automation
66. **who changed resource** → CloudTrail
67. **resource compliance/history** → Config
68. **application metric/log/alarm** → CloudWatch
69. **sensitive S3 data** → Macie
70. **EC2/package vulnerabilities** → Inspector

---

## 16. สิ่งที่เปลี่ยนย้อนหลังไม่ได้หรือมีข้อจำกัดสำคัญ

ข้อสอบชอบ distractor ประเภท “แก้ของเดิมง่าย ๆ” ทั้งที่ service ไม่รองรับ:

- SQS Standard เปลี่ยนเป็น FIFO ไม่ได้
- EC2 hibernation ต้องเปิดและรองรับตั้งแต่ launch
- S3 Object Lock ต้องตรวจเงื่อนไขการเปิดตอนสร้าง bucket/เวอร์ชันของบริการตามโจทย์
- EBS volume เป็น AZ-scoped
- EBS Multi-Attach ไม่ใช่ shared filesystem หลาย AZ
- VPC Peering ไม่ transitive
- Security Group stateful; NACL stateless
- NAT Gateway เป็น AZ-scoped
- RDS Multi-AZ ไม่ใช่ read scaling endpoint โดยอัตโนมัติ
- replication rule ใหม่ไม่จัดการ S3 objects เก่าเองหากไม่ใช้ Batch Replication
- Memcached เพิ่ม node แล้ว client อาจต้อง discover/configure node ใหม่
- Simple AD ไม่มี feature เทียบเท่า AWS Managed Microsoft AD ทุกอย่าง เช่น MFA-related requirements บางรูปแบบ
- CloudFront/Route 53/Global Accelerator ทำคนละ layer แทนกันไม่ได้ทุก use case

---

## 17. บทเรียนเฉพาะจาก 4 ข้อที่เคยพลาดใน Official Practice Exam

ผลฝึกเดิมได้ 71/75 ข้อ จุดพลาดทั้งสี่เป็นเรื่อง “scope และเครื่องมือ native” มากกว่าความจำชื่อ service

### 17.1 บังคับ SSH source CIDR ใน 50 accounts และ member ห้ามแก้

หลักคิด:

- ต้อง enforce ข้ามองค์กร
- member account แก้ไม่ได้
- เลือก Organizations-native preventive control/SCP ที่เหมาะกับ policy condition ไม่ใช่ Config อย่างเดียว เพราะ Config เป็น detective

กฎจำ: **“ห้ามก่อนเกิด” = preventive; “เจอหลังเกิด” = detective**

### 17.2 แก้ tag ที่ผิดและบังคับมาตรฐานในอนาคต

ต้องแยกสามงาน:

1. tag policy ระบุมาตรฐาน value/key
2. Resource Groups/Tag Editor หรือ automation แก้ของเดิม
3. SCP condition บังคับ request ใหม่ให้มี tag/ค่าตามต้องการ เมื่อ requirement ต้อง hard enforcement

กฎจำ: **Tag policy standardizes; SCP enforces presence/action boundary; remediation fixes existing resources.**

### 17.3 แจก custom AMI + CloudFormation template หลาย account/Region

แยกโจทย์ว่าใครเป็นผู้ deploy:

- central admin deploy โดยตรง → StackSets
- ต้อง publish approved package ให้ users self-service และ version/control → Service Catalog product/portfolio

อย่าเลือก custom script copy/deploy ทีละ account เมื่อ native service ครบกว่า

### 17.4 รวม GuardDuty, Macie, Access Analyzer findings หลาย account/Region

ใช้ Security Hub + Organizations + delegated administrator/member auto-enrollment และ enable aggregation ตาม Region strategy

กฎจำ: **ตัวตรวจแต่ละบริการสร้าง finding; Security Hub เป็นศูนย์รวม**

---

# ภาคที่ 4 — วิธีซ้อมและกลยุทธ์วันสอบ

## 18. แผนเตรียมสอบ 21 วัน

### สัปดาห์ 1 — สร้าง decision framework

| วัน | เนื้อหา | ผลลัพธ์ที่ต้องทำได้ |
|---|---|---|
| 1 | Exam algorithm + D1 Organizations | อธิบาย SCP/IAM/Control Tower/delegated admin ได้ |
| 2 | Network/TGW/DX/VPN/DNS | วาด hybrid data path และ segmentation ได้ |
| 3 | Security/KMS/central findings | เลือก detector/aggregator/remediator ถูก |
| 4 | DR/RTO/RPO | เลือก 4 DR patterns จาก SLA ได้ |
| 5 | D2 deployment/reliability | เลือก deployment และ decoupling pattern ได้ |
| 6 | Storage/database/cache | เลือกจาก access pattern/retrieval SLA ได้ |
| 7 | ทำ Study mode 50 ข้อ | จดกฎทุกข้อที่ผิด ไม่ดูแค่คะแนน |

### สัปดาห์ 2 — ปิดช่องว่างและฝึกโจทย์ยาว

| วัน | เนื้อหา | ผลลัพธ์ที่ต้องทำได้ |
|---|---|---|
| 8 | D3 observability/automation | แยก CloudTrail/Config/CloudWatch/SSM ได้ |
| 9 | Cost/performance | เลือก metric, scaling, pricing, lifecycle ได้ |
| 10 | D4 7Rs + migration tools | จับคู่ MGN/DMS/SCT/DataSync/Snow ได้ |
| 11 | Modernization/integration | เลือก SQS/SNS/EventBridge/Kinesis/MQ/Step Functions ได้ |
| 12 | Study mode เฉพาะ weak topics 50 ข้อ | weak topic ไม่มีหัวข้อใดต่ำกว่า 75% |
| 13 | Full mock 75 ข้อ | ทำให้จบใน 180 นาทีแบบไม่หยุดค้น |
| 14 | วิเคราะห์ full mock | อธิบายเหตุผลของทุกข้อผิดและทุกข้อที่เดา |

### สัปดาห์ 3 — ทำให้เสถียรเหมือนวันจริง

| วัน | งาน |
|---|---|
| 15 | ทวน D1/D2 + 25 ข้อ |
| 16 | ทวน D3/D4 + 25 ข้อ |
| 17 | Full mock ครั้งที่ 2 |
| 18 | แก้ weak topics + อ่าน AWS docs เฉพาะ gap |
| 19 | Full mock ครั้งที่ 3 เวลาเดียวกับเวลาสอบจริง |
| 20 | อ่าน One-page cheat sheet + 4 ข้อที่เคยพลาด; งด cram หนัก |
| 21 | สอบหรือพักให้พร้อม: sleep, ID, system check, route/เวลาเดินทาง |

### เกณฑ์ “พร้อมสอบ” ที่เข้มพอ

- full mock 75 ข้อ ได้อย่างน้อย **85% ต่อเนื่อง 2–3 ครั้ง** โดยไม่เปิดเอกสาร
- ทุก Domain อย่างน้อย **80%**
- ทำเสร็จภายใน **165 นาที** เพื่อเหลือ review 15 นาที
- ทุกข้อผิดมี decision rule หนึ่งบรรทัด
- ข้อที่ถูกเพราะเดาถูกต้องนับเป็น “ยังไม่รู้” และต้อง review
- multiple response ไม่พลาดเพราะเลือกเกิน/ขาด

คะแนนเว็บไซต์เป็น raw percentage ไม่ใช่ scaled score ของ AWS จึงใช้เป็น readiness signal ไม่ใช่การคำนวณคะแนนจริง

---

## 19. กลยุทธ์ 180 นาทีในวันสอบ

เวลาเฉลี่ยคือ 2 นาที 24 วินาทีต่อข้อ แต่ไม่ควรแบ่งเท่ากันทุกข้อ

### Pass 1 — 0–100 นาที

- ตอบข้อที่ตัดสินได้
- ข้อที่อ่านเกิน 2–3 นาทีแล้วยังไม่ชัด ให้เลือก best current answer + flag
- ขีดคำว่า least, most, all, existing, future, RTO/RPO, protocol, Region/account scope
- multiple response ตรวจจำนวนที่โจทย์บอก

### Pass 2 — 100–155 นาที

- กลับเฉพาะ flagged
- วาด data path/permission path แบบสั้น
- ตัดตัวเลือกที่ผิด scope หรือผิด control plane
- เปลี่ยนคำตอบเมื่อมีเหตุผลเชิง requirement ชัดเจน ไม่ใช่เพราะรู้สึกไม่มั่นใจ

### Final review — 155–180 นาที

- ตรวจ unanswered ทุกข้อ
- ตรวจ multiple response ว่าเลือกครบจำนวน
- ตรวจข้อที่มีคำว่า NOT/LEAST/MOST
- ถ้าไม่รู้ ให้เดา เพราะไม่มี penalty เพิ่ม

### วิธีอ่านโจทย์ยาว

แยกข้อมูลเป็น 4 ช่องในหัว:

1. **Current state** — มีอะไรอยู่แล้ว
2. **Constraint** — ห้ามเปลี่ยนอะไร/เวลา/งบ/protocol
3. **Target** — ต้องการ latency, RTO, security, scale เท่าไร
4. **Optimization** — least cost/ops/change หรือ highest performance/security

ข้อมูลประวัติที่ไม่เปลี่ยนคำตอบให้ลดน้ำหนักทันที

---

## 20. วิธีวิเคราะห์ตัวเลือกแบบมืออาชีพ

ให้ถาม 7 ข้อนี้กับแต่ละตัวเลือก:

1. ทำ requirement ครบทุกข้อหรือไม่?
2. scope ถูก account/AZ/Region/protocol หรือไม่?
3. มี hidden operational work อะไร?
4. รองรับ existing resources และ future resources ครบหรือไม่?
5. มีข้อจำกัดเปลี่ยนย้อนหลังไม่ได้หรือไม่?
6. data/return path และ permission path ครบหรือไม่?
7. มี AWS-native managed option ที่ตรงกว่าไหม?

### Distractor patterns

- **ถูก service แต่ผิด feature** เช่น RDS Multi-AZ แทน read replica
- **ถูกเฉพาะ happy path** แต่ไม่มี failover/return route
- **แก้เพียงของใหม่** ทั้งที่โจทย์ถาม existing + future
- **scale ไม่ได้** เช่น Lambda per account แทน delegated admin
- **ละเมิด protocol** เช่น SQS แทน proprietary ActiveMQ โดยไม่ยอมแก้ app
- **แพงเกิน requirement** เช่น active-active เมื่อ RTO ยอม 24 ชั่วโมง
- **ราคาถูกแต่ผิด SLA** เช่น Deep Archive เมื่อ retrieval ต้องภายใน 5 ชั่วโมง
- **monitor แต่ไม่ enforce** เช่น Config rule เมื่อต้องป้องกันไม่ให้สร้าง
- **enforce แต่ไม่ remediate ของเดิม** เช่น SCP เมื่อโจทย์ต้องแก้ resource เก่า

---

## 21. One-page mental model ก่อนเข้าห้องสอบ

### Organization

`Organizations/OUs → SCP ceiling → Control Tower landing zone → IAM Identity Center → delegated admins → StackSets/Service Catalog/Config/Backup policies`

### Network

`few VPCs = peering | many = TGW | private service = PrivateLink | global enterprise = Cloud WAN | hybrid private = DX | encrypted backup = VPN | hybrid DNS = Resolver endpoints`

### Edge

`HTTP cache = CloudFront | TCP/UDP + static anycast IP = Global Accelerator | DNS routing = Route 53`

### Security

`identity = IAM | organization boundary = SCP | L7 = WAF | DDoS = Shield | VPC inspection = Network Firewall | threat = GuardDuty | vulnerability = Inspector | sensitive S3 = Macie | external access = Access Analyzer | aggregate = Security Hub`

### Observability

`API = CloudTrail | configuration/compliance = Config | metric/log/alarm = CloudWatch | network metadata = Flow Logs | interactive fleet ops = SSM`

### Data

`object = S3 | block = EBS | NFS = EFS | Windows SMB = FSx Windows | HPC file = FSx Lustre | relational = RDS/Aurora | key-value = DynamoDB | cache = ElastiCache/DAX | durable Redis = MemoryDB`

### Integration

`queue = SQS | fan-out = SNS | event routing = EventBridge | streaming/replay = Kinesis | legacy broker = MQ | workflow = Step Functions`

### Migration

`discover/track = Discovery Service/Migration Hub | server rehost = MGN | DB data = DMS | DB schema = SCT | files online = DataSync | offline huge = Snow | SFTP = Transfer Family`

### DR

`RPO/RTO decides → backup/restore → pilot light → warm standby → active-active`

### Cost

`remove → rightsize → elasticize → price model → storage lifecycle/data transfer → govern`

---

## 22. Checklist ความรู้ก่อนจองสอบ

ตอบ “ได้และอธิบายเหตุผลได้” ให้ครบ:

- [ ] SCP, IAM, trust policy และ resource policy ต่างกันอย่างไร
- [ ] Control Tower, Account Factory, Service Catalog และ StackSets ใช้เมื่อไร
- [ ] VPC Peering, TGW, PrivateLink, DX, VPN และ Cloud WAN ต่างกันอย่างไร
- [ ] Resolver inbound/outbound endpoint ใช้ทิศไหน
- [ ] SG stateful/NACL stateless และ ephemeral ports
- [ ] CloudFront/Global Accelerator/Route 53 ต่างกันอย่างไร
- [ ] WAF/Shield/Network Firewall/Firewall Manager ต่างกันอย่างไร
- [ ] GuardDuty/Inspector/Macie/Access Analyzer/Security Hub ต่างกันอย่างไร
- [ ] CloudTrail/Config/CloudWatch/Flow Logs ต่างกันอย่างไร
- [ ] KMS/CloudHSM/Secrets Manager/Parameter Store ต่างกันอย่างไร
- [ ] เลือก DR strategy จาก RTO/RPO ได้
- [ ] Multi-AZ/read replica/Aurora Global Database ต่างกันอย่างไร
- [ ] S3 storage class จาก access/retrieval SLA ได้
- [ ] EBS/EFS/FSx/S3 ใช้ตาม access protocol ได้
- [ ] SQS/SNS/EventBridge/Kinesis/MQ/Step Functions ต่างกันอย่างไร
- [ ] เลือก Auto Scaling metric ที่สัมพันธ์กับงานได้
- [ ] เลือก purchase model จาก workload ได้
- [ ] อธิบาย 7Rs และ migration phases ได้
- [ ] เลือก MGN/DMS/SCT/DataSync/Snow/Transfer Family ได้
- [ ] รู้สิ่งที่เปลี่ยนย้อนหลังไม่ได้และหลีกเลี่ยง distractor ได้
- [ ] ทำ full mock ผ่านเกณฑ์ readiness ต่อเนื่อง

---

## 23. สิ่งที่ไม่ควรเสียเวลาจำเกินไป

- ราคาตัวเลขละเอียดที่เปลี่ยนได้ — จำ cost model และ trade-off
- quota ตัวเลขทุกบริการ — จำว่าต้องตรวจ quota และขอเพิ่มล่วงหน้า
- CLI syntax ทั้งหมด — ข้อสอบวัด architecture มากกว่า command syntax
- feature ย่อยนอก scope ที่ไม่ช่วยตัดสิน requirement
- คำตอบแบบ “บริการ X ดีที่สุดเสมอ” — ไม่มีจริง ต้องผูกกับ constraint

สิ่งที่ควรจำแม่นกว่าคือ service boundary, scope, protocol, consistency, durability, RTO/RPO, operational ownership และข้อจำกัดที่แก้ย้อนหลังไม่ได้

---

## 24. แหล่งฝึกใน workspace

- `sap-c02-practice/` — เว็บไซต์ฝึก 225 ข้อ พร้อมบันทึก session, explanation และ performance summary
- `week-8-practice-exam-questions.md` — บันทึกคำถามฝึก Week 8 จำนวน 75 ข้อ
- `aws_sap_c02_non_week8_quiz_bank.csv` — คลังคำถามจากแหล่งอื่นในหลักสูตร
- `week-1-study-notes.md` ถึง `week-8-study-notes.md` — รายละเอียดหลักสูตรแยกสัปดาห์

### วิธีใช้ practice site

1. เริ่ม Study mode 25–50 ข้อเพื่อเรียน decision rule
2. Review ข้อผิดและข้อถูกเพราะเดา
3. ใช้ weak-topic dashboard เลือกหัวข้อซ้ำ
4. เมื่อแต่ละ Domain ≥80% ให้ทำ Full mock 75 ข้อ
5. ทำซ้ำจน raw score ≥85% ต่อเนื่อง โดยไม่เปิดโน้ต

---

## 25. แหล่งอ้างอิง AWS ทางการ

เอกสารนี้แยกสองระดับข้อมูล:

- **Course-derived:** สรุปจาก Stella League, Advanced Architecting on AWS, Domain Review/Practice, SimuLearn และ Official Practice Exam ที่บันทึกใน Week 1–8
- **Official current context:** รายละเอียดรูปแบบข้อสอบ, น้ำหนัก Domain, task statements และ emerging topics จาก AWS Exam Guide ปัจจุบัน

ลิงก์หลัก:

- [AWS SAP-C02 Exam Guide](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02.html)
- [Domain 1 — Organizational Complexity](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02-domain1.html)
- [Domain 2 — New Solutions](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02-domain2.html)
- [Domain 3 — Continuous Improvement](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02-domain3.html)
- [Domain 4 — Migration and Modernization](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02-domain4.html)
- [AWS Certified Solutions Architect – Professional overview](https://aws.amazon.com/certification/certified-solutions-architect-professional/)
- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)
- [AWS KMS data protection and current HSM validation](https://docs.aws.amazon.com/kms/latest/developerguide/data-protection.html)
- [AWS CloudHSM capabilities and control model](https://docs.aws.amazon.com/cloudhsm/latest/userguide/introduction.html)

AWS services และ Exam Guide เปลี่ยนได้ ให้ตรวจ Exam Guide อีกครั้งในสัปดาห์ก่อนสอบ

---

## 26. บทส่งท้าย

คนที่สอบผ่าน SAP-C02 ไม่ได้ชนะเพราะจำ service ได้มากที่สุด แต่ชนะเพราะมอง scenario แล้วแยกได้ว่า:

1. requirement ใดเป็นตัวตัดสิน
2. scope อยู่ที่ไหน
3. data/permission path เดินอย่างไร
4. failure mode คืออะไร
5. managed AWS primitive ใดทำครบด้วย operational overhead ต่ำที่สุด

ถ้าคุณอ่านคัมภีร์นี้จนสามารถ **สอนเหตุผลของแต่ละ decision rule ให้คนอื่นฟังได้** และทำ full mock ตามเกณฑ์ readiness ได้ต่อเนื่อง โอกาสสอบผ่านจะสูงกว่าการท่องชื่อบริการหรือจำเฉลยอย่างมาก
