# คัมภีร์ AWS Certified Solutions Architect – Professional (SAP-C02) ภาษาไทย

> ฉบับสังเคราะห์จาก Stella League Week 1–8, ข้อสอบฝึก 75 ข้อ, คลังแบบทดสอบ และ AWS Exam Guide ปัจจุบัน
>
> เนื้อหาหลัก: 10 สิงหาคม 2026 · ปรับภาษาให้อ่านต่อได้คล่อง: 26 ตุลาคม 2026
>
> ลำดับหัวข้อเดิมทั้งหมด อ่านต่อจากจุดเดิมได้เลย ตัวย่อสำคัญมีคำเต็มกำกับเมื่อเริ่มหัวข้อ ส่วนชื่อบริการและ tech term ยังใช้ตามที่เจอในข้อสอบ

## คำเตือนที่จริงใจ

AWS ย่อมาจาก **Amazon Web Services**

เอกสารนี้ออกแบบให้เป็นแกนหลักสำหรับสอบผ่าน SAP-C02 แต่ไม่มีเอกสารใดรับประกันผลสอบได้ 100% เพราะข้อสอบวัดการตัดสินใจเชิงสถาปัตยกรรม ไม่ใช่การจำชื่อบริการอย่างเดียว ต้องอ่านเอกสารนี้ควบคู่กับการทำโจทย์ในเว็บไซต์ `sap-c02-practice`, วิเคราะห์ทุกข้อที่ผิด และมีประสบการณ์ลงมือทำหรือวาด data flow ด้วยตัวเอง

คำว่า **trick / cheat** ในเอกสารนี้หมายถึง **cheat sheet, วิธีตัดตัวเลือก และหลักจำที่ถูกต้อง** ไม่ใช่ข้อสอบหลุดหรือการโกงข้อสอบจริง

---

## 1. วิธีใช้คัมภีร์เล่มนี้ให้คุ้มที่สุด

ถ้ามีเวลาเตรียมตัวหลายวัน ให้อ่าน 3 รอบตามนี้ ถ้าสอบพรุ่งนี้ อ่านต่อจากจุดเดิม แล้วใช้ข้อ 16, 17 และ 21 ทวนก่อนสอบ:

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

AWS Exam Guide ปัจจุบันระบุหัวข้อ Responsible AI (Artificial Intelligence) ได้แก่:

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
- **fastest recovery** → warm standby / multi-site / promoted replica ตาม RTO (Recovery Time Objective — เวลาหยุดระบบสูงสุดที่ยอมได้)/RPO (Recovery Point Objective — ช่วงข้อมูลย้อนหลังที่ยอมเสียได้)
- **near real time** → streaming/event-driven ไม่ใช่ scheduled batch

### ขั้นที่ 2 — ขีดเส้นใต้ข้อห้ามและ SLA

คำว่า `must`, `cannot`, `without`, `within`, `all accounts`, `existing and future`, `no public internet`, `RPO`, `RTO` มักเป็นเงื่อนไขที่ใช้ตัดตัวลวง

ตัวอย่าง: “retrieve within 5 hours” ทำให้ Glacier Deep Archive ผิด แม้ราคาถูกกว่า

### ขั้นที่ 3 — ระบุ scope ให้ถูก

ถามตัวเอง:

- บัญชีเดียวหรือทั้ง Organization?
- AZ (Availability Zone) เดียว, หลาย AZ หรือหลาย Region?
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
| ให้/จำกัดสิทธิ์ | IAM (Identity and Access Management), resource policy, SCP (Service Control Policy), permission boundary |
| กำหนดเส้นทาง | Route table, Transit Gateway route table, Route 53 policy |
| กรอง network | Security group, NACL (Network Access Control List), WAF (Web Application Firewall), Network Firewall |
| เข้ารหัส | KMS (Key Management Service), CloudHSM, ACM (AWS Certificate Manager), TLS (Transport Layer Security) |
| ตรวจและบันทึก | CloudTrail, Config, CloudWatch, Flow Logs |
| รวม security findings | Security Hub |

Distractor ที่พบบ่อยคือเอาเครื่องมือคนละ plane มาแทนกัน เช่น ใช้ IAM policy แทนการ share Transit Gateway หรือใช้ Flow Logs เพื่ออ่าน packet payload

### ขั้นที่ 6 — ตัด self-managed ก่อนเมื่อ requirement ไม่ได้บังคับ

ถ้ามี managed service ที่ทำ requirement ครบ มักชนะการสร้าง EC2 (Elastic Compute Cloud) + script + cron + custom Lambda จำนวนมาก โดยเฉพาะเมื่อโจทย์มีคำว่า least operational overhead

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

## AWS Product Primer — รู้จักบริการแบบ Engineer ที่เพิ่งเริ่ม AWS

ส่วนนี้มีไว้แปลชื่อ product ให้เป็นภาพที่ engineer คุ้นเคย ไม่จำเป็นต้องจำ marketing phrase ให้จำว่า **service อยู่ชั้นไหน รับ input อะไร และส่งมอบ responsibility อะไรให้ AWS ดูแลแทนเรา**

### แนวคิดพื้นฐานก่อนรู้จัก product

**ศัพท์พื้นฐานที่เจอบ่อย:** API (Application Programming Interface) = ช่องทางเรียก service; IP (Internet Protocol) = ที่อยู่ใน network; CPU (Central Processing Unit) = หน่วยประมวลผล

**protocol:** HTTP (Hypertext Transfer Protocol) / HTTPS (Hypertext Transfer Protocol Secure) ใช้กับเว็บ; TCP (Transmission Control Protocol) เน้นส่งครบตามลำดับ; UDP (User Datagram Protocol) ไม่รับประกันการส่งถึง; SSH (Secure Shell) ใช้เข้าเครื่องระยะไกล; SQL (Structured Query Language) ใช้ query database

| คำ AWS | อธิบายแบบ engineer |
|---|---|
| AWS account | security, billing และ quota boundary คล้าย cloud project/subscription ขนาดใหญ่ ไม่ใช่แค่ user login |
| Organization | กลุ่มหลาย AWS accounts ภายใต้บริษัทเดียว มี policy และ billing ส่วนกลาง |
| Region | พื้นที่ภูมิศาสตร์ เช่น Singapore หรือ Tokyo แต่ละ Region แยกกันโดย design |
| AZ (Availability Zone) | กลุ่ม data center ที่แยก failure domain ภายใน Region เดียวกัน เชื่อมกันด้วย network latency ต่ำ |
| VPC (Virtual Private Cloud) | private software-defined network ของเราในหนึ่ง Region |
| Subnet | ช่วง IP ภายใน VPC และผูกกับ AZ เดียว ใช้แบ่ง public/private/app/data tiers |
| Resource | สิ่งที่สร้างใน AWS เช่น EC2 (Elastic Compute Cloud) instance, S3 (Simple Storage Service) bucket, RDS (Relational Database Service) database |
| ARN (Amazon Resource Name) | identifier แบบเต็มของ resource/principal ใช้ใน IAM (Identity and Access Management) policy และ API |
| Managed service | AWS ดูแล infrastructure/patching/scaling บางส่วนหรือเกือบทั้งหมดให้ แต่เรายังรับผิดชอบ configuration, data และ access |
| Global service | control plane หรือ service ที่มองทั้ง AWS เช่น Organizations/IAM บางส่วน; ต้องอ่าน behavior ราย service |
| Regional service | สร้างและใช้งานภายใน Region เช่น Lambda, RDS, DynamoDB |
| Zonal resource | ผูกกับ AZ เช่น EC2 instance, EBS (Elastic Block Store) volume, NAT (Network Address Translation) Gateway |

Mental model ที่ใช้ได้เกือบทุก architecture:

`Organization → Account → Region → VPC → Subnet/AZ → Compute → Data → Integration → Observability/Security`

### Accounts, identity และ governance

| Product | มันคืออะไรแบบง่าย | ใช้เมื่อไร | อย่าสับสนกับ |
|---|---|---|---|
| AWS Organizations | parent control plane สำหรับรวมหลาย accounts เป็น Root/OU (Organizational Unit) และใส่ policy ส่วนกลาง | บริษัทมีหลายทีม/environment/account และต้องการ governance + consolidated billing | IAM ซึ่งให้สิทธิ์ principal ภายใน/cross-account; Organizations ไม่ได้ login แทน user |
| AWS Control Tower | ตัวติดตั้งและดูแล multi-account landing zone ตามแนวทาง AWS โดยประกอบ Organizations, Identity Center, Config และ logging | ต้องการเริ่มหลาย accounts ให้ baseline เหมือนกันโดยไม่ต่อ service เองทั้งหมด | Organizations ซึ่งเป็นโครงสร้างพื้นฐาน; Control Tower เป็น orchestration และ opinionated setup บนโครงนั้น |
| IAM | ระบบ authorization ของ AWS: users, roles, policies และ temporary credentials | กำหนดว่าใครหรือ workload ใดเรียก action ใดกับ resource ใดได้ | IAM Identity Center ซึ่งจัด workforce SSO (Single Sign-On) หลาย accounts |
| IAM Identity Center | portal SSO สำหรับพนักงาน เข้า AWS accounts/apps ด้วย identity กลางและ permission sets | มี workforce หลายคน/หลาย accounts หรือเชื่อม corporate IdP (Identity Provider) | Cognito ซึ่งทำ identity ให้ลูกค้าของ application |
| AWS RAM (Resource Access Manager) | share resource บางชนิดข้าม account โดยไม่ต้อง copy เช่น Transit Gateway/subnet/Resolver rule | หลาย accounts ต้องใช้ network/resource กลางร่วมกัน | IAM permission; share resource แล้วผู้ใช้ยังต้องมี authorization ที่ถูก |
| AWS Service Catalog | catalog ของ infrastructure products ที่ platform team อนุมัติแล้วให้ทีมอื่น self-service | ต้องการให้ developer กดสร้างเฉพาะ pattern ที่ผ่านมาตรฐาน | CloudFormation ซึ่งเป็น engine สำหรับสร้าง resource; Service Catalog ห่อ template เป็น product/portfolio |
| CloudFormation | Infrastructure as Code แบบ declarative: ระบุ desired resources แล้ว AWS สร้าง/update เป็น stack | ต้องการ repeatable, versioned, reviewable infrastructure และ rollback | Systems Manager ซึ่งดูแล resource และ OS หลังสร้างแล้ว |
| CloudFormation StackSets | deploy stack เดียวไปหลาย account และหลาย Region จากส่วนกลาง | rollout baseline, IAM role, Config rule หรือ resource pattern ข้ามองค์กร | stack ปกติที่ทำงานใน target account/Region เดียว |
| Systems Manager | ชุด fleet operations เช่น inventory, patch, run command, session, parameter และ automation | ดูแล EC2/hybrid servers โดยลด SSH/manual scripts | CloudWatch/Config ซึ่ง observe มากกว่า execute operational action |
| AWS Config | inventory + configuration history + compliance evaluation ของ resources | ต้องรู้ว่า resource ตั้งค่าอะไร เปลี่ยนเมื่อไร และผิด rule หรือไม่ | CloudTrail ซึ่งบันทึก API activity ว่าใครเรียกอะไร |

### Network, connectivity และ edge

| Product | มันคืออะไรแบบง่าย | ใช้เมื่อไร | อย่าสับสนกับ |
|---|---|---|---|
| Amazon VPC | private network boundary ที่เรากำหนด CIDR (Classless Inter-Domain Routing), subnet, route และ security | ทุก workload ที่ต้องควบคุม private network | AWS account; account หนึ่งมีหลาย VPC ได้ |
| Internet Gateway | managed gateway ที่เชื่อม VPC กับ internet สำหรับ resource ที่มี route/public IP | public-facing subnet/instance ตาม design | NAT Gateway ซึ่งให้ private subnet ออก internet แต่ไม่รับ inbound ใหม่โดยตรง |
| NAT Gateway | managed outbound translation จาก private subnet ไป internet อยู่ใน AZ | private instances ต้อง download package/call public endpoint | Internet Gateway; NAT ยังต้องมี Internet Gateway path และมีค่า data processing |
| VPC Peering | private one-to-one routing ระหว่างสอง VPC | VPC จำนวนน้อย, CIDR ไม่ชน และไม่ต้อง transitive routing | Transit Gateway ที่เป็น hub สำหรับหลาย networks |
| Transit Gateway | regional network hub เชื่อมหลาย VPC, VPN (Virtual Private Network) และ Direct Connect | hub-and-spoke, route segmentation และ network scale | simple router ที่ทุก attachment คุยกันเสมอ; Transit Gateway route tables ต้องออกแบบ |
| AWS PrivateLink | เปิด service ให้ VPC อื่นเข้าผ่าน private endpoint/ENI (Elastic Network Interface) โดยไม่เปิด network ทั้งก้อน | provider-consumer service access และลด CIDR/transitive complexity | VPC Peering/Transit Gateway ซึ่งให้ network connectivity กว้างกว่า |
| VPC Lattice | application service network สำหรับ connect, discover และ authorize service-to-service ข้าม VPC/account | microservices หลาย VPC/accounts ต้องการ connectivity + policy ระดับ service | Transit Gateway ที่ทำ routing ระดับ network |
| Site-to-Site VPN | managed IPsec tunnels ระหว่าง on-prem/site กับ AWS ผ่าน internet | เชื่อมเร็ว, encrypted และ bandwidth requirement ไม่สูงเท่า dedicated link | Client VPN ที่ต่อผู้ใช้รายบุคคล |
| AWS Client VPN | managed remote-access VPN ใช้ client บน laptop/user device | พนักงาน remote ต้องเข้าถึง private VPC | Site-to-Site VPN ที่เชื่อม network-to-network |
| Direct Connect | dedicated private circuit จาก site/colo ไป AWS | ต้องการ bandwidth/latency สม่ำเสมอและไม่วิ่งบน public internet path | encryption; Direct Connect ไม่ encrypted โดยอัตโนมัติและควรมี high availability design |
| Route 53 | authoritative DNS (Domain Name System) + routing policies + health checks | map domain ไป endpoints และทำ DNS-level routing/failover | load balancer; DNS response ไม่ proxy ทุก packet |
| Route 53 Resolver | managed DNS resolver/endpoints/rules สำหรับ VPC และ hybrid DNS | on-prem resolve private AWS names หรือ AWS resolve on-prem names | Route 53 hosted zone ที่เก็บ DNS records |
| CloudFront | CDN (Content Delivery Network) ที่ cache/serve HTTP(S) ผ่าน edge locations และรัน edge logic ได้ | web/static/media/global HTTP latency, origin protection | Global Accelerator ซึ่งไม่ cache และรองรับ TCP/UDP |
| Global Accelerator | anycast static IP front door ที่พา TCP/UDP เข้า AWS global backbone ไป healthy endpoint | game/VoIP/non-HTTP/global app/static IP/fast failover | CloudFront CDN และ Route 53 DNS routing |
| ALB (Application Load Balancer) | Layer 7 load balancer สำหรับ HTTP/HTTPS/gRPC (gRPC Remote Procedure Calls) และ route ตาม host/path/header | web/API/microservices | NLB (Network Load Balancer) สำหรับ TCP/UDP/TLS (Transport Layer Security) และ performance/static IP |
| NLB | Layer 4 load balancer throughput สูง รองรับ TCP/UDP/TLS และ IP targets | non-HTTP, source IP, static IP per AZ, very high performance | ALB ที่เข้าใจ HTTP request |
| GWLB (Gateway Load Balancer) | transparent gateway/load balancer สำหรับ network security appliances | scale third-party firewall/inspection fleet | AWS Network Firewall ซึ่งเป็น managed firewall service โดยตรง |

### Compute, containers และ application runtime

| Product | มันคืออะไรแบบง่าย | ใช้เมื่อไร | เราต้องดูแลอะไร |
|---|---|---|---|
| EC2 | virtual machine ที่เลือก OS, instance type, network และ disk ได้ | ต้องควบคุม OS (Operating System), custom agent/driver, long-running legacy workload | OS patch, runtime, scaling และ application |
| Auto Scaling | controller ที่เพิ่ม/ลด/แทน EC2 instances ตาม desired capacity/metric/health | stateless fleet, variable demand, self-healing | launch template, metric, cooldown/warmup และ state placement |
| Elastic Beanstalk | application platform ที่ deploy code แล้ว AWS สร้าง EC2/load balancer/Auto Scaling group environment ให้ | web app ที่อยากลด infrastructure setup แต่ยังใช้ EC2 model | app/config และ platform updates บางส่วน |
| ECS (Elastic Container Service) | AWS-native container orchestrator จัด task/service/cluster | ทีมต้องการ containers โดยไม่ต้องใช้ Kubernetes API | task definition, service, networking, image และ scaling |
| EKS (Elastic Kubernetes Service) | managed Kubernetes control plane | มี Kubernetes ecosystem/skills/workload requirement | cluster add-ons, workload, policy และ node/Fargate choice |
| Fargate | serverless compute capacity สำหรับ ECS/EKS tasks | รัน container โดยไม่ provision/patch worker nodes | container image, task sizing, networking และ app |
| Lambda | event-driven function runtime ที่ scale ต่อ invocation | short-lived API/event/file/queue processing | function code, timeout, concurrency, idempotency และ downstream limits |
| AWS Batch | managed job queues/scheduler ที่ใช้ EC2/Fargate compute environments | batch/HPC (High Performance Computing)/render/ETL (Extract, Transform, Load) jobs ที่มี dependency และ retry | job definition/image/data และ compute strategy |
| Lightsail | simplified virtual private server/bundle price พร้อม templates | small predictable web app หรือทีมใหม่ที่ไม่ต้องการ AWS primitives จำนวนมาก | instance/app/backup ตาม bundle |
| ECR (Elastic Container Registry) | private container image registry | เก็บ image สำหรับ ECS/EKS/Lambda containers | image lifecycle, scanning และ access policy |

### Storage และ file systems

| Product | มันคืออะไรแบบง่าย | ใช้เมื่อไร | Key behavior |
|---|---|---|---|
| S3 | durable object storage เข้าผ่าน API; ไม่ใช่ mounted block disk โดยธรรมชาติ | files, backup, data lake, static assets, logs | bucket อยู่ระดับ Region; object key ไม่ใช่ POSIX (Portable Operating System Interface) path จริง |
| EBS | block volume คล้าย virtual disk ต่อกับ EC2 | boot/data disk, database block storage ใน AZ | ผูก AZ, snapshot ไป S3-managed backend, Multi-Attach มีข้อจำกัด |
| EFS (Elastic File System) | managed elastic NFS (Network File System) file system หลาย AZ | Linux instances/containers ต้องแชร์ POSIX files | regional mount targets, throughput/latency ต่างจาก local block disk |
| FSx for Windows File Server | managed Windows SMB (Server Message Block) file server รวม AD (Active Directory) integration | Windows apps, home directories, SMB shares | Windows semantics/permissions |
| FSx for Lustre | high-performance parallel file system | HPC/machine learning/large dataset processing และเชื่อม S3 ได้ | performance-oriented ไม่ใช่ general cheap archive |
| Storage Gateway | appliance/service bridge ให้ on-prem ใช้ file/volume/tape interface โดย backend อยู่ AWS | hybrid storage และ gradual migration | มี File, Volume และ Tape Gateway คนละ access model |
| AWS Backup | central policy, schedule, vault และ restore สำหรับหลาย AWS resource types | standardized backup ข้าม accounts/Regions | ต้องตรวจ resource support, retention, vault policy และ restore testing |

### Databases, cache และ analytics

| Product | มันคืออะไรแบบง่าย | ใช้เมื่อไร | อย่าสับสนกับ |
|---|---|---|---|
| RDS | managed relational database engines เช่น PostgreSQL/MySQL/Oracle/SQL Server | app ต้อง SQL, transaction, joins และไม่อยากดูแล database host เองทั้งหมด | database บน EC2 ที่เราดูแล OS และ engine เอง |
| Aurora | AWS-built relational engine compatible กับ MySQL/PostgreSQL แยก compute/storage และมี high availability/read scale สูง | cloud-native relational, fast failover, Global Database | RDS engine ทั่วไป; feature/price/compatibility ต้องตรวจ |
| DynamoDB | serverless key-value/document database ที่ scale ด้วย partition key | predictable access by key, massive scale, low latency | relational database; ไม่มี joins/ad-hoc SQL แบบเดียวกัน |
| DAX (DynamoDB Accelerator) | managed in-memory cache ที่เข้าใจ DynamoDB API | repeated eventually consistent reads ต้อง microseconds | ElastiCache general cache และ DynamoDB table เอง |
| ElastiCache | managed Redis/Valkey หรือ Memcached cache | cache, session, leaderboard, rate data ลด database load | durable primary database; persistence/high availability ขึ้นกับ engine/config |
| MemoryDB | durable Redis-compatible in-memory database พร้อม Multi-AZ transaction log | ต้องการ Redis API เป็น primary database และ durability | ElastiCache ซึ่งเป้าหมายหลักคือ cache |
| Redshift | managed columnar data warehouse | analytical SQL บน structured/curated data ปริมาณมาก | RDS งาน transaction ของ application และ S3 data lake |
| Athena | serverless SQL query บน data ใน S3 | ad-hoc analysis/log query โดยไม่ provision cluster | database ที่รับ application transactions |
| AWS Glue | serverless data integration/ETL + Data Catalog | discover schema, transform/move data, catalog datasets | Lake Formation ที่เน้น build/govern data lake permissions |
| Lake Formation | orchestration/governance layer สำหรับ data lake บน S3/Glue | central fine-grained data access และ data lake setup | S3 storage หรือ query engine |
| Amazon EMR (แพลตฟอร์ม managed Spark/Hadoop) | managed platform สำหรับ Spark/Hadoop/Trino ecosystem | big-data jobs ที่ต้อง framework/control มากกว่า serverless SQL | Glue/Athena ที่ลด cluster management มากกว่า |
| OpenSearch Service | managed search/analytics engine | full-text search, log analytics, dashboards | relational database |
| QuickSight | managed business intelligence visualization/dashboard | business users สำรวจ Athena/Redshift/RDS datasets | data warehouse/ETL engine |

### Messaging, events และ workflow

| Product | มันคืออะไรแบบง่าย | ใช้เมื่อไร | Delivery mental model |
|---|---|---|---|
| SQS (Simple Queue Service) | durable queue คั่น producer กับ workers | buffer spike, async work, independent scaling | consumer pull; Standard at-least-once, FIFO (First In, First Out) order/dedup ตามเงื่อนไข |
| SNS (Simple Notification Service) | push pub/sub topic | fan-out notification/event ไปหลาย subscribers | publisher ส่งครั้งเดียวแล้ว SNS push ไป endpoints/queues |
| EventBridge | managed event bus ที่ route ตาม event content/schema | AWS/SaaS (Software as a Service)/custom events, cross-account routing, event-driven automation | router ไม่ใช่ work queue ทดแทน SQS ทุกกรณี |
| Kinesis Data Streams | partitioned real-time stream ที่ retain/replay records | telemetry/click/log/financial stream และหลาย consumers | ordering ต่อ shard; ต้องออกแบบ partition key/capacity |
| Kinesis Data Firehose | delivery pipe ที่ buffer/transform แล้วส่ง stream ไป destination เช่น S3/Redshift/OpenSearch | ต้องส่ง streaming data ไป storage/analytics ด้วย ops ต่ำ | ไม่ใช่ general replayable stream แบบ Data Streams |
| Amazon MQ | managed ActiveMQ/RabbitMQ broker | migrate legacy messaging protocol เดิม เช่น AMQP หรือ MQTT app โดยลด protocol rewrite | cloud-native queue อย่าง SQS ที่มี API/semantics คนละแบบ |
| Step Functions | state machine/orchestrator ที่เก็บ state ระหว่าง steps | retry, branch, parallel, wait, long workflow, human approval | Lambda function เดียวยาว ๆ หรือ EventBridge router |

### Security, encryption และ observability

| Product | มันคืออะไรแบบง่าย | ใช้เมื่อไร | Output ที่ได้ |
|---|---|---|---|
| KMS (Key Management Service) | managed cryptographic key control plane ที่ integrate กับ AWS services | encrypt S3/EBS/RDS/secrets และ application envelope encryption | KMS keys, policies, grants และ audit events |
| CloudHSM | single-tenant general-purpose HSM (Hardware Security Module) cluster ที่ลูกค้าควบคุม crypto users/keys/algorithms มากกว่า | direct HSM APIs, standard cryptographic interface เช่น PKCS#11, special compliance/control | HSM cluster ที่ operational responsibility สูงกว่า KMS |
| Secrets Manager | encrypted secret store + rotation workflow/integration | database credentials/API keys ที่ต้อง rotate | secret versions และ retrieval API |
| Parameter Store | hierarchical configuration/key-value store มี SecureString | app config/feature settings/simple secrets | parameter; rotation automation ไม่ครบเท่า Secrets Manager |
| ACM (AWS Certificate Manager) | certificate lifecycle service | TLS cert สำหรับ ALB, CloudFront, API Gateway และ private certificate authority use cases | managed certificates; private key export/placement มีข้อจำกัดตาม cert type |
| WAF (Web Application Firewall) | Layer 7 web request rules | SQL injection / cross-site scripting/rate/bot/geo filtering หน้า CloudFront/ALB/API Gateway | allowed/blocked/count web requests |
| Shield | managed DDoS (Distributed Denial of Service) protection; Standard มีพื้นฐานและ Advanced เพิ่ม response/visibility | internet-facing workloads ที่ต้อง DDoS posture สูง | attack detection/mitigation ไม่แทน WAF application rules |
| Network Firewall | managed VPC firewall สำหรับ stateful/stateless traffic inspection | central ingress/egress/east-west filtering | firewall endpoints/rules/logs |
| GuardDuty | threat detection วิเคราะห์ CloudTrail, DNS, VPC และ data sources อื่น | หา compromised credential, crypto mining, suspicious behavior | security findings ไม่ใช่ packet block โดยตัวมันเอง |
| Inspector | vulnerability/exposure scanning สำหรับ supported workloads | หา package vulnerabilities และ network exposure ใน EC2/container/Lambda ตาม coverage | vulnerability findings |
| Macie | sensitive-data discovery และ S3 security monitoring | หา ข้อมูลส่วนบุคคล/credentials/sensitive patterns ใน S3 | sensitive-data findings/classification |
| IAM Access Analyzer | reasoning จาก policies เพื่อหา external/public access และ validate policy | ตรวจ resource share ออกนอก zone of trust | access findings/policy validation |
| Security Hub | central dashboard/normalization/correlation ของ security findings | รวม GuardDuty, Inspector, Macie และ standards ข้าม accounts/Regions | aggregated findings ไม่ได้แทน detector ต้นทาง |
| CloudTrail | audit log ของ AWS API activity | สืบว่าใครทำ action อะไร เมื่อไร จาก IP/role ใด | management/data/network activity events ตาม configuration |
| CloudWatch | metrics, logs, alarms, dashboards และ application observability | ดู health/performance และ trigger automation | time-series metrics/log events/alarms |
| VPC Flow Logs | metadata ของ accepted/rejected IP flows | troubleshoot network path/ports/bytes | flow records ไม่มี packet payload |

### Migration, transfer และ cost

| Product | มันคืออะไรแบบง่าย | ใช้เมื่อไร | จุดตัดสิน |
|---|---|---|---|
| Migration Hub | dashboard กลางติดตาม servers/apps และ migration tools | portfolio/wave tracking | track ไม่ได้ย้าย workload เอง |
| Application Discovery Service | เก็บ inventory/utilization/dependency ของ on-prem servers | assessment ก่อนวาง wave | discovery ไม่ใช่ migration engine |
| Application Migration Service (MGN) | block-level continuous replication แล้ว launch server บน EC2 | rehost physical/virtual machine servers ด้วย downtime ต่ำ | รักษา server model ไม่ได้ modernize app ให้เอง |
| Database Migration Service (DMS) | move/replicate database data ด้วย full load + CDC (Change Data Capture) | homogeneous/heterogeneous database migration | data movement; schema conversion ใช้ SCT (Schema Conversion Tool) เมื่อ engine ต่างกัน |
| Schema Conversion Tool (SCT) | วิเคราะห์และ convert database schema/code | Oracle/SQL Server/Db2 ไป target engine คนละชนิด | ไม่ได้ย้าย transactional rows แทน DMS |
| DataSync | agent-based accelerated online file/object transfer | NFS/SMB/object transfer ซ้ำหรือ scheduled | online network transfer ไม่ใช่ offline appliance |
| Snow Family | physical/edge devices สำหรับ offline bulk transfer/edge compute | network ช้ามาก, data ใหญ่มาก, disconnected location | ต้องรวม shipping/import time ใน calculation |
| Transfer Family | managed SFTP (SSH File Transfer Protocol)/FTPS (File Transfer Protocol over TLS)/FTP (File Transfer Protocol)/AS2 front door ไป S3/EFS | partner/client ต้องใช้ file-transfer protocol เดิม | ไม่ใช่ bulk migration optimizer แบบ DataSync |
| Cost Explorer | หน้าจอใช้งาน/API วิเคราะห์ cost/usage trend | หา spend pattern และ forecast | ไม่ใช่ hard budget enforcement |
| AWS Budgets | threshold/forecast notification และ action | เตือน/จำกัดก่อนหรือเมื่อเกินงบ | data อาจไม่ real-time; billing control ไม่ใช่ resource architecture ทั้งหมด |
| Compute Optimizer | recommendation จาก utilization metrics | rightsize EC2/EBS/Lambda/ECS ตาม supported resources | recommendation ต้อง validate business context |
| Savings Plans | commitment ค่า compute ต่อชั่วโมงเพื่อรับส่วนลด | baseline usage ที่คาดการณ์ได้ | ไม่ใช่ capacity reservation โดยตัวมันเอง |
| Reserved Instances | pricing/capacity construct ตาม service/type | baseline database/EC2 patterns ตามชนิด Reserved Instances | Standard/Convertible/Regional/Zonal มี trade-off ต่างกัน |
| Spot | spare EC2 capacity ราคาต่ำแต่ถูก interrupt ได้ | batch, fault-tolerant, stateless, flexible jobs | ห้ามใช้เป็น capacity เดียวของงานที่หยุดไม่ได้ |

### วิธีอ่านตาราง Product Primer

อย่าท่องว่า service ใด “ดีที่สุด” ให้ถามสามข้อ:

1. service นี้รับผิดชอบ **ชั้นไหน** — identity, network, compute, data, integration หรือ observation?
2. requirement ต้องการ **connect, protect, store, process, route, observe หรือ govern**?
3. หลังเลือก service แล้ว ทีมเรายังต้องดูแล **อะไรที่ AWS ไม่ได้ดูแลให้**?

เมื่อเข้าใจสามข้อนี้ ชื่อบริการจะไม่ใช่ศัพท์โดด ๆ แต่กลายเป็น building blocks ที่ประกอบ architecture ได้

---

# ภาคที่ 1 — เนื้อหาตาม Domain

## 4. Domain 1 — Design Solutions for Organizational Complexity (26%)

### 4.1 Multi-account foundation

สถาปัตยกรรมมาตรฐานขององค์กรควรคิดเป็นชั้น:

1. **AWS Organizations** — สร้างลำดับ Root → OU (Organizational Unit) → Account, consolidated billing และ policy inheritance
2. **AWS Control Tower** — สร้าง landing zone และ orchestration ของ Organizations, IAM Identity Center, Config, CloudTrail/central logging
3. **IAM Identity Center** — SSO (Single Sign-On), permission sets และ federation กับ external IdP (Identity Provider)
4. **Security/Log Archive/Audit accounts** — แยก blast radius และหน้าที่
5. **Delegated administrator** — ให้ account เฉพาะดูแล Security Hub, GuardDuty, Config, Backup ฯลฯ แทน management account
6. **Account Factory / Service Catalog** — provision account และ approved products แบบมาตรฐาน

ถ้าเพิ่งรู้จัก AWS ให้คิดภาพเป็นบริษัทที่มีหลายทีม:

`บริษัท (Organization) → แผนก/สภาพแวดล้อม (OU) → ห้องแยกของแต่ละ workload (Account) → พนักงานใช้บัตรกลางเข้าแต่ละห้อง (Identity Center)`

#### AWS Organizations — โครงสร้างบริษัทและ policy ส่วนกลาง

Organizations เป็น service ที่เอา AWS accounts หลายบัญชีมาอยู่ใต้การบริหารเดียวกัน แทนที่จะให้ทุกทีมเปิด account แยกโดยไม่มีมาตรฐาน

- **Root** คือจุดบนสุดของ organization ไม่ใช่ root user
- **OU (Organizational Unit)** คือ folder เชิงนโยบาย เช่น `Security`, `Infrastructure`, `Production`, `NonProduction`, `Sandbox`
- **Account** เป็น security/billing/quota boundary ที่รัน workload จริง เช่น `payments-prod` หรือ `central-logs`
- policy ที่ attach กับ Root/OU จะถูก inherit ลงไปยัง accounts ใต้จุดนั้นตามชนิด policy
- consolidated billing รวมค่าใช้จ่ายเพื่อจ่ายส่วนกลางและใช้ volume discount/benefit บางชนิดร่วมกัน

Organizations **ไม่ได้สร้างสิทธิ์ให้ developer เข้า resource** งานนั้นยังเป็น IAM (Identity and Access Management)/Identity Center และ Organizations **ไม่ได้ deploy application** แต่กำหนดโครงสร้าง, guardrail และ relationship ระหว่าง accounts

ตัวอย่าง: บริษัทมี 40 applications แทนที่จะใส่ทุกระบบใน account เดียว เราแยก production/non-production accounts แล้วใช้ SCP (Service Control Policy) ที่ Production OU ห้ามปิด CloudTrail และห้ามใช้ Region ที่ไม่อนุมัติ

#### AWS Control Tower — ตัวสร้าง landing zone ให้พร้อมใช้

Landing zone คือ multi-account foundation ที่เตรียม identity, logging, audit และ guardrails ไว้ก่อนทีม application เข้ามาใช้ ถ้าสร้างเองต้องต่อ Organizations, IAM Identity Center, Config, CloudTrail และ automation หลายชุด Control Tower ทำหน้าที่ orchestrate setup เหล่านี้ตามแนวทาง AWS

Control Tower มักสร้าง/ใช้:

- management account สำหรับ control plane; ไม่ควรวาง application workload ทั่วไป
- Log Archive account สำหรับเก็บ log ส่วนกลาง
- Audit/Security account สำหรับทีม security ตรวจ accounts อื่น
- IAM Identity Center สำหรับ workforce access
- controls เพื่อ preventive/detective/proactive governance
- Account Factory สำหรับสร้าง member account ใหม่จาก baseline

Control Tower ไม่ใช่ runtime ที่รับ user traffic และไม่ใช่ ระบบรวมและวิเคราะห์เหตุการณ์ security มันคือบริการดูแล **multi-account environment lifecycle**

#### IAM Identity Center — ประตู SSO ของพนักงาน

Identity Center เชื่อม user/group จาก corporate directory หรือสร้าง identity ภายใน แล้วให้ user login ที่ portal เดียวเพื่อเห็น AWS accounts และ roles ที่ได้รับ

แนวคิดสำคัญคือ **permission set**: template ของสิทธิ์ เช่น `ReadOnly`, `Developer`, `SecurityAudit` เมื่อ assign user/group + permission set ให้ account ระบบจะ provision IAM role ที่เกี่ยวข้องใน account เป้าหมาย

จึงไม่ต้องสร้าง IAM user/password ซ้ำใน 40 accounts และเมื่อพนักงานออกจากบริษัทสามารถปิดที่ identity source ส่วนกลางได้

อย่าสับสนกับ Amazon Cognito: Identity Center ใช้กับ **workforce/พนักงาน**, Cognito ใช้กับ **ผู้ใช้ application เช่นลูกค้า mobile/web app**

#### Security, Log Archive และ Audit accounts — แยกหน้าที่เพื่อลด blast radius

การแยก account ไม่ได้มีไว้จัด folder สวย ๆ แต่ใช้ AWS account เป็น isolation boundary:

- **Log Archive account** รับ CloudTrail/Config/log สำคัญจาก accounts อื่น ผู้ดูแล workload ไม่ควรแก้หรือลบ log ได้
- **Security Tooling account** เป็น delegated admin ของ GuardDuty, Security Hub, Inspector หรือเครื่องมือ security กลาง
- **Audit account** ให้ auditor/security role อ่าน evidence และตรวจข้าม account โดยไม่ต้องใช้ management account
- บางองค์กรแยก Network, Backup หรือ Shared Services accounts เพิ่มตาม ownership และ risk

ถ้า production credential ถูก compromise ผู้โจมตีไม่ควรลบ audit logs หรือปิด detector ส่วนกลางได้ง่าย นี่คือเหตุผลของการแยก blast radius

#### Delegated administrator — มอบงาน service ให้ account ผู้เชี่ยวชาญ

Management account มีอำนาจสูงมาก จึงไม่ควรให้ทีมใช้ทำงานประจำ Organizations-integrated services หลายตัวอนุญาตให้แต่งตั้ง member account เป็น delegated administrator

ตัวอย่าง: ตั้ง `security-tooling` เป็น delegated admin ของ Security Hub และ GuardDuty จากนั้นทีม security จัดการ members/findings จาก account นี้ โดยไม่ต้อง login management account

ข้อดี:

- แยก duty และลดการใช้ management account
- เปิด/จัดการ service ให้ current/future member accounts จากส่วนกลางได้ตาม capability
- รวม findings/configuration/backup policy โดยไม่เขียน script loop ทุก account

แต่ละ service มี delegated-admin behavior และ Region behavior ต่างกัน ต้อง enable trusted access และตั้ง home/aggregation Region ตามเอกสารของ service

#### Account Factory และ Service Catalog — โรงงานสร้างของมาตรฐาน

**Account Factory** อยู่ใน Control Tower ใช้สร้าง AWS account ใหม่พร้อม baseline เช่น OU, network option, SSO access และ controls แทนการเปิด account แล้วตั้งค่าด้วยมือ

**Service Catalog** เป็น catalog ของ infrastructure products เช่น “VPC (Virtual Private Cloud) มาตรฐาน”, “three-tier app”, “approved RDS (Relational Database Service) database” Platform team publish product จาก CloudFormation/Terraform configuration แล้วให้ทีม application deploy แบบ self-service ภายใต้ constraints

จำความสัมพันธ์:

- CloudFormation = engine สร้าง resources
- Service Catalog = หน้าร้าน/approval boundary ของ templates ที่อนุมัติ
- Account Factory = product/process เฉพาะสำหรับสร้าง governed AWS accounts

#### ตัวอย่าง end-to-end

เมื่อทีม Payments ขอ production account:

1. Platform team ใช้ Account Factory สร้าง `payments-prod` ใต้ Production OU
2. SCP ของ OU จำกัด Region และห้ามปิด security logging
3. Developer login ผ่าน Identity Center และ assume role จาก permission set
4. ทีม deploy เฉพาะ approved products ผ่าน Service Catalog
5. CloudTrail/Config ส่ง evidence ไป Log Archive account
6. GuardDuty/Security Hub findings ถูกรวมที่ Security delegated-admin account

นี่คือเหตุผลที่ข้อสอบมักเลือก Organizations + Control Tower + Identity Center + delegated administration แทนการสร้าง IAM users และ Lambda scripts แยกทุก account

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

- Share Transit Gateway, subnet, Route 53 Resolver rule ฯลฯ ด้วย AWS RAM (Resource Access Manager)
- เปิด trusted access / sharing with Organizations เมื่อต้อง share ทั้งองค์กร
- Resource-based policy ใช้ได้กับ S3 (Simple Storage Service), SQS (Simple Queue Service), KMS (Key Management Service) และบริการที่รองรับ

### 4.3 Network at organization scale

#### VPC Peering vs Transit Gateway vs PrivateLink

| ทางเลือก | เหมาะกับ | ข้อจำกัดสำคัญ |
|---|---|---|
| VPC Peering | เชื่อมไม่กี่ VPC แบบ one-to-one | ไม่ transitive, CIDR (Classless Inter-Domain Routing) ห้ามซ้อน, full mesh โตยาก |
| Transit Gateway | hub-and-spoke หลาย VPC/VPN (Virtual Private Network)/Direct Connect | ต้องออกแบบ Transit Gateway route tables และ segmentation |
| AWS PrivateLink | expose service แบบ private ให้ consumer | one-way service access ไม่ใช่ full network connectivity |
| VPC Lattice | service-to-service connectivity หลาย VPC/account | เน้น application service network และ policy |
| Cloud WAN (Wide Area Network) | global network policy หลาย Region/site | เหมาะ global enterprise network มากกว่า Transit Gateway เดี่ยว |

#### Hybrid connectivity

| Requirement | คำตอบหลัก |
|---|---|
| remote user รายบุคคล | AWS Client VPN |
| site/branch เชื่อมผ่าน internet แบบ encrypted | Site-to-Site VPN |
| private bandwidth สม่ำเสมอ | Direct Connect |
| Direct Connect ต้อง encrypted end-to-end | VPN over Direct Connect |
| หลาย VPC ผ่าน Direct Connect | Direct Connect Gateway + Transit VIF (Virtual Interface) + Transit Gateway |
| high availability ของ Direct Connect | connection อีกเส้น/อีก location และ VPN backup |

Direct Connect VIF:

- **Public VIF** → public AWS endpoints
- **Private VIF** → private IP ใน VPC ผ่าน Virtual Private Gateway/Direct Connect Gateway
- **Transit VIF** → Transit Gateway ผ่าน Direct Connect Gateway

จำว่า Direct Connect connection เดียวไม่ใช่ high availability และ Direct Connect Gateway ไม่ได้ทำให้ association สองฝั่ง route หากันเองโดยอัตโนมัติ

#### Hybrid DNS

- on-prem query private AWS zone → Route 53 Resolver **inbound endpoint** + conditional forwarder ที่ on-prem
- AWS query on-prem domain → Resolver **outbound endpoint** + forwarding rule
- share rule ข้าม account → AWS RAM
- ต้องมี network path ก่อน DNS (Domain Name System) จึงทำงาน

#### Specialized infrastructure ตาม latency/data residency

| Service | ใช้เมื่อ |
|---|---|
| AWS Outposts | ต้องการ AWS infrastructure/services ใน data center ของลูกค้า เพื่อ latency/local processing/residency |
| AWS Local Zones | ต้องการ compute/storage/database บางบริการใกล้เมือง/ผู้ใช้ปลายทางกว่าการใช้ Region |
| AWS Wavelength | ultra-low latency application บนเครือข่าย 5G ของผู้ให้บริการ |
| Snowball Edge | offline transfer และ edge compute ในพื้นที่ disconnected/limited connectivity |

อย่าเลือก Outposts เพียงเพราะมีระบบ on-prem; ถ้าโจทย์ต้องการเพียง connectivity ให้คิด Direct Connect/VPN ก่อน

### 4.4 Security at organization scale

รูปแบบที่ข้อสอบชอบ:

- GuardDuty ตรวจ threat/activity anomaly
- Inspector ตรวจ vulnerability/exposure ของ workload
- Macie ค้นหา sensitive data ใน S3
- IAM Access Analyzer หา external/public access จาก policy
- Security Hub รวมและจัดลำดับ findings ข้าม account/Region
- Firewall Manager บังคับ WAF (Web Application Firewall), Shield Advanced, security group, Network Firewall policy หลาย account
- Organizations + delegated admin ลดงาน setup per account

อย่าสับสน:

- Security Hub ไม่ใช่ตัวสร้าง finding ทุกชนิด แต่เป็น aggregator/normalizer
- GuardDuty เน้นตรวจภัยคุกคาม; การ scan ช่องโหว่ package เป็นงานของ Inspector
- Flow Logs มี metadata เช่น IP, port, จำนวน bytes และผล accept/reject; ไม่มีเนื้อหา packet; ถ้าต้องอ่าน payload ใช้ Traffic Mirroring ไปยัง inspection appliance

### 4.5 Resilience และ DR

**DR (Disaster Recovery)** คือแผนกู้ระบบหลังเหตุร้าย เริ่มจาก business requirement:

- **RPO (Recovery Point Objective)** = ยอมเสียข้อมูลย้อนหลังได้เท่าไร
- **RTO (Recovery Time Objective)** = ยอมให้ระบบหยุดได้นานเท่าไร

| Strategy | Cost | RTO/RPO โดยเปรียบเทียบ | สภาพระบบ Region สำรอง |
|---|---:|---|---|
| Backup & Restore | ต่ำสุด | ช้าที่สุด | มี backup ยังไม่มี workload พร้อม |
| Pilot Light | ต่ำ | เร็วขึ้น | core data/service เปิดอยู่, compute ส่วนใหญ่ปิด |
| Warm Standby | กลาง-สูง | เร็ว | ระบบขนาดเล็กทำงานอยู่ตลอด |
| Multi-site active-active | สูงสุด | เร็วที่สุด | รับ traffic เต็มทั้งสองฝั่ง |

เลือกจากตัวเลข RTO/RPO ไม่ใช่เลือก multi-Region แพงที่สุดโดยอัตโนมัติ และต้องรวม DNS/failover orchestration, data replication, secrets, quotas, dependencies และการทดสอบ disaster recovery

### 4.6 Cost visibility

- Cost Explorer → วิเคราะห์ cost/usage และ trend
- AWS Budgets → threshold/forecast alert และ Budgets Actions
- Cost and Usage Report → ข้อมูลละเอียดที่สุดสำหรับ Athena/business intelligence
- Compute Optimizer → rightsizing จาก metrics
- Trusted Advisor → recommendations หลายหมวด
- Savings Plans → commitment ตาม compute spend; ยืดหยุ่นกว่า Reserved Instances ในหลายกรณี
- Reserved Instances → benefit ผูกกับ service/attributes ตามชนิด; Standard ลดสูงกว่า Convertible แต่ยืดหยุ่นน้อยกว่า
- Spot → interruptible, เหมาะ batch/restartable/stateless
- Tags + account/OU structure → cost allocation และ ownership

---

## 5. Domain 2 — Design for New Solutions (29%)

### 5.1 แปลง requirement เป็น architecture

ก่อนเลือก service ให้สร้าง acceptance criteria:

- Availability/SLA (Service Level Agreement)
- RTO (Recovery Time Objective — เวลาหยุดระบบสูงสุดที่ยอมได้)/RPO (Recovery Point Objective — ช่วงข้อมูลย้อนหลังที่ยอมเสียได้)
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
| AWS resources แบบ declarative | CloudFormation/CDK (Cloud Development Kit) |
| หลาย account/Region | StackSets |
| software install ตาม runbook ระหว่าง EC2 (Elastic Compute Cloud) launch | CloudFormation + EC2 user data หรือ Systems Manager |
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

CI/CD (Continuous Integration / Continuous Delivery) building blocks:

- CodePipeline → orchestrate stages
- CodeBuild → managed build/test
- CodeDeploy → deployment ไป EC2/on-prem, Lambda หรือ ECS (Elastic Container Service) ตาม deployment capability
- CodeArtifact → managed package repository
- ECR (Elastic Container Registry) → container image registry
- CloudFormation/CDK → provision infrastructure ที่ version/control/repeat ได้

หลักข้อสอบคือ pipeline ต้องมี test, approval ตาม risk, immutable artifact, least-privilege role, observability และ automatic rollback จาก health/alarm

### 5.3 Reliability และ loose coupling

หลักออกแบบ:

- ใช้ **stateless compute** หลัง load balancer: ไม่เก็บข้อมูล session สำคัญไว้ที่เครื่องใดเครื่องหนึ่ง
- Auto Scaling หลาย AZ (Availability Zone)
- เก็บ **state** ใน managed database หรือ storage ที่รองรับ high availability แทนการผูกไว้กับเครื่องเดียว
- ใช้ **queue เป็น buffer** รองรับ traffic ที่พุ่งขึ้น ก่อนให้ worker ทยอยทำงาน
- **retry แบบ exponential backoff + jitter**: ลองใหม่โดยเว้นช่วงนานขึ้นและสุ่มเวลา เพื่อไม่ให้ทุก client ยิงซ้ำพร้อมกัน
- **idempotency**: รับคำสั่งเดิมซ้ำได้โดยไม่เกิดผลซ้ำ เช่น ไม่ตัดเงินรอบที่สอง
- **timeout / circuit breaker**: หยุดรอหรือหยุดเรียกระบบที่ล่มชั่วคราว เพื่อไม่ให้ระบบอื่นล่มตาม
- **DLQ (Dead-Letter Queue)** เก็บ message ที่ทำไม่สำเร็จซ้ำ ๆ แยกไว้ตรวจสาเหตุ ไม่ให้วนขวางงานอื่น
- quota monitoring ก่อน launch

เลือก integration ให้ตรงกับวิธีรับส่งและประมวลผลงาน:

- **SQS (Simple Queue Service) → คิวพักงาน**; worker ดึงงานไปทำ ช่วยรับ traffic spike และแยกการ scale ของผู้ส่งกับผู้รับ
- **SNS (Simple Notification Service) → ส่งข้อความเดียวไปหลายผู้รับ** แบบ push หรือ fan-out
- **EventBridge → ส่ง event ตามเงื่อนไขในข้อความ** ข้าม service หรือ account
- **Kinesis Data Streams → stream ข้อมูลต่อเนื่อง**; เรียงลำดับภายใน shard และอ่านย้อนหลังได้ภายใน retention
- **Amazon MQ → ใช้ protocol ของ ActiveMQ/RabbitMQ เดิม** เพื่อลดการแก้ application
- **Step Functions → คุม workflow หลายขั้น** เช่น retry, แยกเงื่อนไข, รอผล หรือรอคนอนุมัติ

### 5.4 Auto Scaling ให้ดู metric ที่สัมพันธ์กับ demand

- workload แต่ละ request หนักไม่เท่ากัน → CPU อาจดีกว่า request count
- CPU ไม่สัมพันธ์กับ traffic → `ALBRequestCountPerTarget`
- **queue worker → ดูงานค้างต่อ instance** (backlog per instance) ไม่ใช่จำนวนงานค้างรวมอย่างเดียว
- **target tracking → เพิ่ม/ลดเครื่องเพื่อรักษา metric ให้ใกล้ค่าเป้าหมาย**
- **step scaling → เพิ่ม/ลดเครื่องตามความรุนแรงของ alarm** กำหนดได้หลายระดับ เหมาะกับ spike ใหญ่
- **scheduled scaling → เพิ่ม/ลดเครื่องตามเวลาที่รู้ล่วงหน้า**
- **predictive scaling → ใช้ข้อมูลย้อนหลังคาดการณ์ load ที่เกิดเป็นรอบ**

### 5.5 Security by design

- ใช้ role และ temporary credentials แทน access key ฝังใน code
- Secrets Manager สำหรับ secret + rotation; Parameter Store สำหรับ configuration/secret ที่ไม่ต้องการ rotation workflow ขั้นสูง
- KMS (Key Management Service) สำหรับ managed key integration; CloudHSM เมื่อจำเป็นต้องใช้ single-tenant HSM (Hardware Security Module) ที่ควบคุม user/algorithm/key operation โดยตรง หรือใช้ crypto interface เฉพาะ
- ACM (AWS Certificate Manager) จัดการ public/private certificates ตาม use case
- private subnet ไม่เท่ากับ “ออก internet ไม่ได้” ถ้ามี NAT (Network Address Translation) route
- VPC (Virtual Private Cloud) endpoint ลดการผ่าน public internet และ NAT cost
- **WAF (Web Application Firewall) กรอง web request**, **Shield ป้องกัน DDoS** (Distributed Denial of Service), **Network Firewall ตรวจและกรอง traffic ในเครือข่าย VPC**
- เข้ารหัสทั้ง **at rest** (ข้อมูลที่เก็บอยู่) และ **in transit** (ข้อมูลระหว่างส่ง) พร้อมกำหนด key policy/grant ให้ถูก

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

- **อ่านข้อมูลเดิมซ้ำมาก → cache**; ถ้าเป็น DynamoDB ให้พิจารณา DAX (DynamoDB Accelerator) ถ้าเป็น relational database ให้พิจารณา read replica ตามเงื่อนไข
- static global content → CloudFront + TTL (Time To Live) สูง
- TCP/UDP global latency + static IP → Global Accelerator
- tightly coupled HPC (High Performance Computing) → EFA (Elastic Fabric Adapter) + cluster placement group + single AZ
- shared POSIX (Portable Operating System Interface) file หลาย AZ → EFS (Elastic File System)
- Windows SMB (Server Message Block) → FSx for Windows File Server
- high-performance temporary scratch/HPC → FSx for Lustre

### 5.7 Cost — ถูกที่สุดที่ “ผ่าน requirement”

- **ใช้งานพื้นฐานสม่ำเสมอ → Savings Plans / Reserved Instances**
- burst ไม่แน่นอน → On-Demand + Auto Scaling
- **งานหยุดแล้วเริ่มใหม่ได้ → Spot**
- **งานมาเป็นครั้งคราว → serverless** ช่วยลดค่าเครื่องที่เปิดรอเฉย ๆ
- S3 (Simple Storage Service) lifecycle ตาม access + retrieval SLA
- cache ช่วยทั้ง latency และ origin/data-transfer cost
- NAT Gateway cost อาจลดได้ด้วย gateway/interface endpoints
- cross-AZ และ cross-Region data transfer ต้องอยู่ใน cost model

---

## 6. Domain 3 — Continuous Improvement for Existing Solutions (25%)

Domain นี้ถามว่า “ระบบมีอยู่แล้ว จะตรวจและปรับอย่างไร” คำตอบที่ดีต้องเริ่มจาก evidence และลด manual work

### 6.1 Operational Excellence

วงจรที่ควรจำ:

**เก็บ metrics/logs → วัดค่าปกติ (baseline) → ตรวจพบปัญหา → หาสาเหตุ → แก้อัตโนมัติ → ตรวจผล → บันทึกบทเรียน**

| ต้องการ | เครื่องมือหลัก |
|---|---|
| metrics, alarms, logs, dashboard | CloudWatch |
| API activity: ใครทำอะไร เมื่อไร จากไหน | CloudTrail |
| resource configuration/compliance/history | AWS Config |
| inventory, patch, run command, session, automation | Systems Manager |
| trace distributed application | AWS X-Ray / application tracing |
| event-driven remediation | EventBridge → Lambda/Systems Manager Automation |

กฎเลือก:

- “ใครลบ/แก้ resource?” → CloudTrail
- “resource เคยมี configuration อะไร และ compliant ไหม?” → AWS Config
- “CPU/latency/log มีค่าเท่าไร?” → CloudWatch
- “เข้า shell โดยไม่เปิด port 22 พร้อมบันทึก session” → Session Manager
- “บังคับ patch fleet” → Systems Manager Patch Manager

### 6.2 Improve security

ลำดับงานที่ถูกต้อง:

1. **รวบรวม findings** หรือผลตรวจจากเครื่องมือ security
2. **จัดลำดับความสำคัญ** ตามความรุนแรงและผลต่อธุรกิจ
3. **แก้ปัญหา (remediate)** อัตโนมัติเมื่อกำหนดวิธีที่ปลอดภัยได้
4. **ตรวจซ้ำ** ว่ากลับมาตรงตามข้อกำหนดแล้ว
5. **เก็บหลักฐานและป้องกันการเกิดซ้ำ**

Patterns:

- Config rule ตรวจ noncompliance → EventBridge → Systems Manager Automation/Lambda แก้
- Security Hub + Organizations → central delegated admin ข้าม accounts/Regions
- Access Analyzer → external access และ policy validation
- Inspector → vulnerability management
- Macie → sensitive data discovery
- GuardDuty → threat detection จาก logs/signals
- AWS Backup + Vault Lock → centralized immutable backup ตาม compliance

### 6.3 Improve performance

อย่า scale โดยไม่มี evidence:

- กำหนด **ตัวชี้วัดจากธุรกิจ** เช่น p95 latency (95% ของคำขอใช้เวลาไม่เกินค่านี้), error rate และ orders/minute
- baseline ก่อนเปลี่ยน
- หา bottleneck ด้วย metrics/tracing
- เปลี่ยนทีละส่วนและวัดผล
- ทดสอบ load/failure
- rightsize ตามรูปแบบใช้งาน ไม่ใช่ peak ชั่วคราวอย่างเดียว

ตัวเลือกแก้ที่พบบ่อย:

- read-heavy relational → read replicas/cache
- **DynamoDB อ่าน key เดิมซ้ำ ๆ → DAX** (DynamoDB Accelerator); ไม่ใช่ cache ทั่วไปสำหรับทุก database
- static/HTTP global → CloudFront
- dynamic TCP/UDP global → Global Accelerator
- network-heavy HPC (High Performance Computing) → EFA (Elastic Fabric Adapter)/cluster placement group
- **write burst → พักข้อมูลด้วย SQS (Simple Queue Service) หรือ Kinesis** ตามว่าต้องการคิวงานหรือ stream
- database CPU สูงจาก query → index/query tuning ก่อนเพิ่ม instance โดยไม่วิเคราะห์

### 6.4 Improve reliability

ตรวจ **single point of failure** หรือจุดเดียวที่พังแล้วทำให้ทั้งระบบใช้ไม่ได้ ทีละชั้น:

- DNS (Domain Name System)/traffic entry
- load balancer
- compute AZ (Availability Zone) distribution
- state/database failover
- shared file/storage
- NAT (Network Address Translation)/egress
- on-prem link
- secrets/config dependencies
- quota/limit
- deployment/control plane

บางองค์ประกอบดูเหมือนมีตัวเดียว แต่บริการจัดการความทนทานให้แล้ว ต้องดูขอบเขตของแต่ละบริการ:

- Internet Gateway หนึ่งตัวต่อ VPC (Virtual Private Cloud) เป็น horizontally scaled/high availability โดย service design
- DynamoDB เป็น Regional service
- ALB (Application Load Balancer) ข้ามหลาย AZ ได้
- แต่ NAT Gateway เป็น AZ-scoped จึงควรมีต่อ AZ พร้อม route ของแต่ละ subnet

### 6.5 Improve cost

ทำตามลำดับ:

1. **Eliminate** — ปิดของที่ไม่ได้ใช้ ลบ disk, Elastic IP, snapshot หรือ log ที่ไม่มีงานใช้งานแล้วตาม retention ที่ต้องเก็บ
2. **Rightsize** — instance/database/storage/throughput
3. **Elasticize** — เพิ่ม/ลดตาม load, ใช้ serverless หรือปิดระบบทดสอบนอกเวลางาน
4. **Price** — เลือก Savings Plans, Reserved Instances หรือ Spot ให้ตรงรูปแบบใช้งาน
5. **Architect** — managed/purpose-built service, caching, lifecycle, endpoint ลด NAT
6. **Govern** — ตั้งงบ, tag เจ้าของงาน, วิเคราะห์ Cost and Usage Report, ตรวจค่าใช้จ่ายผิดปกติ และให้เจ้าของงานดำเนินการ

อย่าซื้อ commitment เพื่อแก้ resource ที่ควรถูกปิดหรือ rightsize ก่อน

---

## 7. Domain 4 — Migration and Modernization (20%)

### 7.1 Migration phases

1. **Assess** — สำรวจระบบและ dependencies, ประเมินความคุ้มค่า ต้นทุนรวม และความพร้อม
2. **Mobilize** — เตรียม landing zone, governance, ทีม, security, เครื่องมือ และแบ่งแผนย้ายเป็นรอบ (waves)
3. **Migrate and Modernize** — ย้ายทีละ wave, ตรวจผล, สลับระบบจริงไปปลายทาง (cutover) แล้วปรับปรุงต่อ

เครื่องมือ:

- AWS Application Discovery Service → เก็บข้อมูล server/dependency
- Migration Evaluator → business case/total cost of ownership จาก utilization
- AWS Migration Hub → track portfolio และ migration status
- AWS Application Migration Service (MGN) → block-level replication/rehost servers
- AWS DMS (Database Migration Service) → ย้าย/replicate database data
- AWS SCT (Schema Conversion Tool) → convert schema/code สำหรับ heterogeneous database migration
- AWS Control Tower → landing zone/governance

### 7.2 7 Rs

| R | ความหมาย | สัญญาณในโจทย์ |
|---|---|---|
| Retire | เลิกใช้ | ไม่มี owner/usage/business value |
| Retain | ยังไม่ย้าย | dependency/compliance/เวลาไม่พร้อม |
| Rehost | lift and shift | deadline สั้น, source code ไม่มี, minimal change |
| Relocate | ย้าย platform โดยไม่ redesign เช่น VMware | ต้องย้ายเร็วและรักษา environment |
| Replatform | เปลี่ยนบางชั้น | ย้าย database ไป RDS (Relational Database Service), containerize โดยแก้ app น้อย |
| Repurchase | เปลี่ยนเป็น SaaS (Software as a Service)/product ใหม่ | ซอฟต์แวร์สำเร็จรูป/SaaS ตอบโจทย์แทนระบบเดิม |
| Refactor/Re-architect | redesign cloud-native | ต้อง scale/innovate และยอมลงทุนพัฒนา |

อย่าเลือก refactor เพียงเพราะ “ดีที่สุดในระยะยาว” หากโจทย์กำหนด 90 วันและ minimal application changes

### 7.3 Data transfer decision tree

| เงื่อนไข | บริการ |
|---|---|
| ย้ายไฟล์ผ่าน NFS (Network File System) หรือ SMB (Server Message Block) ทาง network ซ้ำหรือตามเวลา | AWS DataSync |
| client ต้องส่งไฟล์ด้วย SFTP (SSH File Transfer Protocol), FTPS (File Transfer Protocol over TLS) หรือ FTP (File Transfer Protocol) | AWS Transfer Family |
| accelerate upload ผ่าน public internet ไป S3 (Simple Storage Service) | S3 Transfer Acceleration |
| petabyte/offline และ network ไม่พอ | AWS Snow Family |
| hybrid file access เดิม + S3 backend | S3 File Gateway |
| block/iSCSI (Internet Small Computer Systems Interface) hybrid | Volume Gateway |
| virtual tape | Tape Gateway |
| ย้าย database ระหว่างที่ต้นทางยังรับงาน โดยตามคัดลอกข้อมูลที่เปลี่ยน | AWS DMS |
| server block replication/rehost | AWS MGN |

คำนวณคร่าว ๆ ก่อนเลือก Snow: ถ้า internet transfer ใช้เวลาไม่กี่วัน แต่การส่งอุปกรณ์ไป-กลับนานกว่า online transfer อาจชนะ

### 7.4 Database migration

- **Homogeneous = engine เดิม → engine เดิม**: ใช้ DMS หรือเครื่องมือของ database นั้น
- **Heterogeneous = เปลี่ยน engine**: ใช้ **Schema Conversion Tool แปลง schema/code + Database Migration Service ย้ายข้อมูล**
- **ต้อง downtime ต่ำ → full load + CDC (Change Data Capture) แล้ว cutover**: ย้ายข้อมูลก้อนแรก ตามคัดลอกข้อมูลที่เปลี่ยน แล้วสลับ application ไปปลายทาง
- ตรวจชนิดข้อมูล, object ที่ปลายทางไม่รองรับ, ข้อมูลขนาดใหญ่ (large objects), replication lag, network, ผลการย้าย และแผน rollback

ตัวอย่าง: **Oracle → Aurora PostgreSQL ต้องแปลง schema/code และย้ายข้อมูล**; เครื่องมือย้ายข้อมูลอย่างเดียวทำไม่ครบ

### 7.5 Modernization

ลำดับความเปลี่ยนแปลงจากน้อยไปมาก:

**ย้าย server เดิมมา EC2 (Elastic Compute Cloud) → ใช้ managed database/storage → containers → serverless/event-driven → เลือก database เฉพาะทางตามงาน**

เลือกตามข้อจำกัด:

- ต้องปรับ OS (Operating System), ใช้ driver เฉพาะ หรือรัน legacy binary → EC2
- container แต่ไม่อยากจัดการ server → ECS (Elastic Container Service)/EKS (Elastic Kubernetes Service) on Fargate
- short-lived event function → Lambda
- orchestration หลายขั้น → Step Functions
- decouple producer/consumer → SQS (Simple Queue Service)/EventBridge/SNS (Simple Notification Service)/Kinesis ตาม semantics
- ต้องรักษา protocol ของ ActiveMQ/RabbitMQ → Amazon MQ ลดการ rewrite
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

**DNS (Domain Name System)** แปลงชื่อ domain เป็นปลายทาง; **edge** คือจุดบริการใกล้ผู้ใช้ ในบทนี้ HTTP/HTTPS คือ traffic เว็บ ส่วน TCP/UDP คือ protocol ระดับ network ที่ใช้แยกโจทย์ load balancer และ Global Accelerator

### 8.1 CloudFront vs Global Accelerator vs Route 53

| คุณสมบัติ | CloudFront | Global Accelerator | Route 53 |
|---|---|---|---|
| ชั้นหลัก | cache และกระจายเนื้อหาเว็บ | เร่งเส้นทาง network สำหรับ TCP/UDP | แปลงชื่อ domain และเลือกปลายทาง |
| Protocol | HTTP/HTTPS | TCP/UDP | DNS (Domain Name System) response |
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
- “apex domain” → Route 53 alias ไม่ใช่ CNAME (Canonical Name)

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
| ALB (Application Load Balancer) | HTTP/HTTPS/gRPC (gRPC Remote Procedure Calls) | route ตาม host/path/header เหมาะกับ web และ microservices |
| NLB (Network Load Balancer) | TCP/UDP/TLS (Transport Layer Security) | throughput สูง, static IP ต่อ Availability Zone และรองรับการคง source IP |
| GWLB (Gateway Load Balancer) | network traffic ระดับ IP | แทรกและ scale firewall/appliance ในเส้นทาง traffic |
| CLB (Classic Load Balancer) | legacy | workload เก่า; ระบบใหม่เลือก ALB หรือ NLB ตาม protocol |

ALB target health ไม่เหมือน Route 53 health check: ALB ตรวจ targets ภายใน target group ส่วน Route 53 ใช้ DNS-level endpoint routing/failover

### 8.4 VPC endpoints

- Gateway endpoint → S3 (Simple Storage Service) และ DynamoDB, route table, ไม่มี hourly charge แบบ interface endpoint
- Interface endpoint → AWS PrivateLink/ENI (Elastic Network Interface)/private IP, หลาย AWS services, security group, มีค่าใช้จ่าย
- Gateway Load Balancer endpoint → ส่ง traffic ไป security virtual appliances
- endpoint policy จำกัดสิทธิ์ผ่าน endpoint แต่ไม่แทน IAM (Identity and Access Management)/resource policy ทั้งหมด

### 8.5 Stateful vs stateless

**Stateful = จำ connection; stateless = ตรวจแต่ละ packet แยกกัน**

- Security Group = stateful; allow ขาไปแล้ว return traffic ได้อัตโนมัติ
- **NACL (Network Access Control List) = stateless**: ต้อง allow ทั้งขาไปและขากลับ รวม ephemeral ports (port ชั่วคราวที่ client ใช้รับคำตอบ)
- Flow Logs ขึ้น `ACCEPT` outbound แต่ `REJECT` return ที่ ENI → สงสัย NACL ก่อน Security Group
- Route table ใช้ **longest-prefix match**: route ที่ระบุช่วง IP แคบและเจาะจงกว่าชนะ

### 8.6 Network security

| Service | หน้าที่ |
|---|---|
| AWS WAF (Web Application Firewall) | Layer 7 (application layer) HTTP(S), SQL injection / cross-site scripting/rate/geo/custom rules |
| Shield Standard | DDoS (Distributed Denial of Service) protection พื้นฐานอัตโนมัติ |
| Shield Advanced | DDoS ระดับสูง, visibility, ทีมตอบสนองเหตุ DDoS ของ AWS และ cost protection ตามเงื่อนไข |
| AWS Network Firewall | managed stateful VPC (Virtual Private Cloud) firewall/inspection |
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
| Standard-IA (Infrequent Access) | infrequent, ต้อง multi-AZ (Availability Zone) | retrieval/minimum duration charge |
| One Zone-IA (Infrequent Access) | re-creatable หรือ secondary copy | AZ เดียว ไม่เหมาะข้อมูลสำคัญสำเนาเดียว |
| Glacier Instant Retrieval | archive แต่ต้อง milliseconds | retrieval cost สูงกว่า archive ลึก |
| Glacier Flexible Retrieval | minutes–hours | standard retrieval โดยทั่วไปราว 3–5 ชม. |
| Glacier Deep Archive | ถูกสุด, ยอมรอนาน | standard retrieval โดยทั่วไปราว 12 ชม. |

เลือก archive tier จาก **retrieval SLA** (Service Level Agreement) ก่อนราคา

### 9.2 S3 high-yield features

- existing objects + future replication → S3 (Simple Storage Service) Batch Replication สำหรับของเก่า + replication rule สำหรับของใหม่
- billions of objects → S3 Inventory + Batch Operations
- access pattern หลายทีม/prefix → S3 Access Points
- immutable retention → S3 Object Lock
- privileged user ก็ห้ามลบ → compliance mode
- **Object Lock เปิดกับ bucket เดิมได้** แต่ต้องใช้ Versioning; เปิดแล้วปิด Object Lock หรือ suspend Versioning ไม่ได้ ([AWS: Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock-configure.html))
- sensitive data discovery → Macie
- cost/usage visibility หลาย bucket/account → S3 Storage Lens

### 9.3 Block, file, object

| Need | Service |
|---|---|
| block disk ของ EC2 (Elastic Compute Cloud) ใน AZ | EBS (Elastic Block Store) |
| shared NFS (Network File System)/POSIX (Portable Operating System Interface) หลาย AZ | EFS (Elastic File System) |
| managed Windows SMB (Server Message Block)/AD (Active Directory) | FSx for Windows File Server |
| high-performance parallel Linux/HPC (High Performance Computing) | FSx for Lustre |
| ONTAP features/NFS/SMB/iSCSI (Internet Small Computer Systems Interface) | FSx for NetApp ONTAP |
| object, web-scale, API access | S3 |

EBS Multi-Attach ยังอยู่ใน AZ เดียวและต้องใช้ cluster-aware filesystem จึงไม่ใช่คำตอบทั่วไปสำหรับ shared file high availability

---

## 10. Database และ Cache

| Requirement | ตัวเลือกที่เด่น |
|---|---|
| relational managed | RDS (Relational Database Service) |
| cloud-native relational, faster failover/read scale | Aurora |
| global relational reads/disaster recovery | Aurora Global Database |
| key-value/document, massive scale | DynamoDB |
| microsecond DynamoDB read cache | DAX (DynamoDB Accelerator) |
| in-memory cache/session | ElastiCache Redis/Valkey |
| simple distributed cache, no replication/failover | Memcached |
| durable Redis-compatible primary database | MemoryDB |
| graph relationships | Neptune |
| search/log analytics | OpenSearch |
| data warehouse analytics | Redshift |
| time series | Timestream |

### Redis/Memcached/MemoryDB

- Redis/Valkey → replication, persistence options, Multi-AZ (Availability Zone) automatic failover
- Memcached → simple multithreaded cache; client ต้องรู้ node ใหม่; ไม่มี replication/Multi-AZ failover แบบ Redis
- MemoryDB → durable Multi-AZ transaction log เหมาะใช้เป็น primary database ที่ต้อง Redis-compatible และความทนทาน

### RDS/Aurora resilience

- **RDS Multi-AZ DB instance → failover**; standby ไม่รับงานอ่าน ส่วน **Multi-AZ DB cluster มี reader ที่รับงานอ่านได้** อย่าเหมารวมสองแบบนี้ ([AWS: DB instance](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZSingleStandby.html), [DB cluster](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/multi-az-db-clusters-concepts.html))
- read replica → read scaling/disaster recovery และ promote ได้
- Aurora reader endpoint → กระจาย read
- Aurora Global Database → cross-Region, low-latency global reads/disaster recovery
- planned managed failover เหมาะทดสอบ/switchover โดยลด data loss risk

### Analytics และ data lake

| Need | Service/แนวทาง |
|---|---|
| query S3 (Simple Storage Service) ด้วย SQL แบบ serverless โดยไม่ดูแล cluster | Athena — ค่า query แบบ on-demand ขึ้นกับปริมาณข้อมูลที่สแกน |
| metadata catalog/ETL (Extract, Transform, Load) | AWS Glue + Data Catalog |
| สร้างและ govern data lake | Lake Formation |
| managed Hadoop/Spark ecosystem | Amazon EMR (แพลตฟอร์ม managed Spark/Hadoop) |
| enterprise data warehouse | Redshift |
| business intelligence dashboard | QuickSight |
| real-time delivery เข้า S3/Redshift/OpenSearch | Kinesis Data Firehose |

**Athena: งานดูแลน้อย ≠ ค่าใช้งานต่ำเสมอ** — บริบทเพิ่มเติมจาก AWS docs

- **ค่า query แบบ on-demand คิดจาก data scanned** ไม่ใช่จำนวนไฟล์อย่างเดียว; ยังมีค่า S3 requests, storage และ Data Catalog ตามการใช้งาน ตัวอย่างราคาในหน้า AWS คือ $5 ต่อข้อมูลที่สแกน 1 TB ดังนั้นสแกน 1 TB ซ้ำ 100 ครั้ง = $500 เฉพาะค่า query ([AWS pricing](https://aws.amazon.com/athena/pricing/))
- **ไฟล์เล็กเป็นล้าน ๆ ไฟล์** เพิ่ม overhead ในการ list/open/read และจำนวน requests; รวมไฟล์เล็ก (compaction) ให้ขนาดเหมาะสม แทนการเปิดอ่านไฟล์จิ๋วจำนวนมาก
- **ลดการสแกน:** partition เช่นตามวันที่ แล้ว query โดยกรอง partition key; ใช้ Parquet + compression และเลือกเฉพาะ column ที่ต้องใช้ การมี `WHERE` อย่างเดียวไม่ได้แปลว่าจะสแกนน้อยเสมอ ([AWS: Optimize data](https://docs.aws.amazon.com/athena/latest/ug/performance-tuning-data-optimization-techniques.html))
- **จำไปสอบ:** query logs/data lake เป็นครั้งคราว + ไม่อยากดูแล cluster → Athena; ถ้า query ชุดใหญ่ซ้ำถี่ ๆ ให้ประเมิน data layout, cache/result reuse, summary tables และเปรียบเทียบ data warehouse เช่น Redshift ตาม workload ไม่ใช่ตัดสินจากจำนวนไฟล์อย่างเดียว

Data lake มักใช้ schema-on-read และ S3 เป็น storage layer; data warehouse ใช้ curated/schema-on-write เพื่อ analytics ที่มีโครงสร้างกว่า Lake Formation ช่วย permissions/governance และสร้าง ingestion workflows ผ่าน Glue ไม่ได้แทน S3 หรือ query engine ทั้งหมด

---

## 11. Compute, Containers และ Serverless

| Requirement | เลือก |
|---|---|
| ต้องควบคุม OS (Operating System) หรือใช้ driver เฉพาะ | EC2 (Elastic Compute Cloud) |
| web app deploy ง่าย ยังอยากให้ AWS จัด infra | Elastic Beanstalk |
| simple virtual private server/predictable bundle price | Lightsail |
| container orchestration AWS-native | ECS (Elastic Container Service) |
| Kubernetes ecosystem/API | EKS (Elastic Kubernetes Service) |
| container โดยไม่จัดการ host | Fargate |
| short event-driven execution | Lambda |
| managed batch scheduling/queues | AWS Batch |
| VMware workload relocate | VMware Cloud on AWS ตาม scenario |

### Placement groups และ HPC

**HPC (High Performance Computing)** คืองานคำนวณประสิทธิภาพสูง ซึ่งมักใช้หลายเครื่องร่วมกัน ต้องดูว่าเน้นสื่อสารเร็วหรือแยกความเสี่ยงเครื่องพัง

- Cluster → instance อยู่ใกล้กันใน AZ (Availability Zone) เดียว, latency ต่ำ/throughput สูง
- Partition → แยกกลุ่ม instance คนละ rack ลด correlated failure, เหมาะ distributed systems ใหญ่
- Spread → แยก instance จำนวนน้อยแต่ละเครื่องคนละ hardware
- EFA (Elastic Fabric Adapter) → low-latency/high-throughput HPC (High Performance Computing)/machine learning communication
- tightly coupled HPC มักต้อง single AZ + cluster placement group + EFA; multi-AZ เพิ่ม latency

### EC2 purchasing

- On-Demand → ไม่มี commitment, load ผันผวน/ชั่วคราว
- Savings Plans → commitment รายชั่วโมง เหมาะ baseline compute
- Reserved Instances → billing discount/capacity reservation บางชนิดตามรายละเอียด
- Spot → ถูกมากแต่ถูก interrupt ได้
- Dedicated Hosts → license/compliance/host visibility
- Capacity Reservations → reserve capacity ใน AZ แต่ไม่ใช่ส่วนลดราคาโดยตัวมันเอง

### Hibernation trap

EC2 hibernation ต้องรองรับ instance/AMI (Amazon Machine Image), root EBS (Elastic Block Store) encrypted และเปิดตอน launch อย่าเลือกคำตอบที่พยายามเปิด hibernation ให้ instance เดิมย้อนหลังถ้า requirement ไม่รองรับ

---

## 12. Messaging, Streaming และ Workflow

| Service | Model | Ordering/Replay | ใช้เมื่อ |
|---|---|---|---|
| SQS (Simple Queue Service) Standard | worker ดึงงานจากคิว | ส่งอย่างน้อยหนึ่งครั้ง; อาจซ้ำและสลับลำดับ | คั่นระบบ, พักงาน, throughput สูง |
| SQS FIFO (First In, First Out) | worker ดึงงานจากคิว | เรียงตาม message group และลดการส่งซ้ำตามข้อกำหนด | งานต้องเรียงลำดับ; application ยังควรป้องกันผลซ้ำ |
| SNS (Simple Notification Service) | ผู้ส่ง publish แล้วบริการ push ไปผู้รับ | ไม่ใช่ stream สำหรับ replay | กระจายข้อความเดียวไปหลายผู้รับ |
| EventBridge | event bus/rules | event routing/archive/replay capability | content-based routing, SaaS (Software as a Service)/AWS/account integration |
| Kinesis Data Streams | stream แบ่งเป็น shard | เรียงภายใน shard; อ่านย้อนหลังได้ตาม retention | ข้อมูลต่อเนื่องที่มีหลาย consumer |
| Amazon MQ | managed broker | ตาม ActiveMQ/RabbitMQ | legacy protocol ลด app rewrite |
| Step Functions | workflow หลายขั้น | บันทึกประวัติตามชนิด workflow | คุมลำดับ, retry, รอ, ทำขนาน และอนุมัติ |

กับดักสำคัญ:

- เปลี่ยน SQS Standard queue เดิมเป็น FIFO ไม่ได้ ต้องสร้าง FIFO queue ใหม่
- **Visibility timeout = เวลาซ่อน message หลัง worker รับไปทำ** ควรนานพอสำหรับประมวลผล หรือขยายระหว่างทำ ไม่เช่นนั้น worker อื่นอาจรับงานเดียวกันซ้ำ
- **DLQ (Dead-Letter Queue)** แยก message ที่ทำไม่สำเร็จซ้ำ ๆ ไว้วิเคราะห์และส่งกลับไปทำใหม่; ไม่ได้แก้สาเหตุให้อัตโนมัติ
- SQS service integration/API Gateway service proxy ลด Lambda/EC2 (Elastic Compute Cloud) ที่ไม่จำเป็น
- SNS + SQS fan-out ให้ subscriber แต่ละราย retry/scale แยกกัน

---

## 13. Security, Identity และ Encryption

### 13.1 IAM evaluation mental model

**IAM (Identity and Access Management)** ตัดสินสิทธิ์ของแต่ละ request โดยต้องดู policy ทุกชั้นที่เกี่ยวข้อง

1. ต้องมี **Allow ที่ใช้กับ request นี้ได้จริง**
2. **Explicit Deny ชนะ Allow** เสมอ
3. ตรวจ SCP (Service Control Policy) ว่าจำกัดสิทธิ์ระดับองค์กรหรือไม่
4. ตรวจ resource policy/trust policy
5. ตรวจ **permissions boundary** (เพดานสิทธิ์ของ user/role) และ **session policy** (จำกัดสิทธิ์ session ที่รับมา)
6. ตรวจ condition keys, principal, Region, tags และ KMS (Key Management Service) key policy

### 13.2 Identity services

| Need | Service |
|---|---|
| workforce SSO (Single Sign-On) หลาย AWS accounts/apps | IAM Identity Center |
| app user authentication | Cognito user pool |
| ให้ app user รับ temporary AWS credentials | Cognito identity pool |
| Microsoft AD (Active Directory) managed | AWS Managed Microsoft AD |
| proxy ไป on-prem AD ไม่เก็บ credential ใน AWS | AD Connector |
| simple directory need น้อย | Simple AD แต่ตรวจ feature เช่น MFA (Multi-Factor Authentication) ก่อน |

Cognito:

- User pool = authentication/user directory/tokens
- Identity pool = federation แล้วออก temporary AWS credentials
- custom identity ที่ไม่ใช่ SAML (Security Assertion Markup Language)/OIDC (OpenID Connect) และมี developer backend → developer-authenticated identity กับ identity pool

### 13.3 Encryption and secrets

| Need | เลือก |
|---|---|
| managed integration/envelope encryption | KMS |
| single-tenant HSM (Hardware Security Module), direct user/algorithm/key control, standard crypto APIs | CloudHSM หรือ KMS custom key store ตาม integration requirement |
| application secret + automatic rotation | Secrets Manager |
| config/parameter, SecureString ได้ | Systems Manager Parameter Store |
| TLS (Transport Layer Security) certificate lifecycle | ACM (AWS Certificate Manager) |

KMS high-yield:

- ปัจจุบัน AWS KMS standard key store ใช้ HSM ที่ validated ระดับ FIPS (Federal Information Processing Standards) 140-3 Security Level 3 เช่นกัน ดังนั้นคำว่า “FIPS Level 3” เพียงอย่างเดียวไม่พอให้สรุปว่าเป็น CloudHSM; ให้ดู requirement เรื่อง single tenancy, direct control, algorithm/API และ operational responsibility
- key policy สำคัญเสมอ; IAM (Identity and Access Management) Allow อย่างเดียวอาจไม่พอ
- multi-Region keys ช่วย client-side/application use cases แต่ไม่ได้ replicate encrypted data ให้เอง
- automatic rotation ตาม key type/capability; imported key material มีข้อจำกัดต่างกัน
- deletion มี waiting period; EventBridge แจ้ง admin ได้
- **Envelope encryption**: ใช้ data key เข้ารหัสข้อมูล แล้วใช้ KMS key เข้ารหัส data key อีกชั้น

### 13.4 Logging and evidence

| คำถาม | คำตอบ |
|---|---|
| ใครเรียก API จาก console หรือ SDK (Software Development Kit) | CloudTrail trail เดียวครอบคลุมทั้งสองประเภท |
| ตรวจว่า CloudTrail log ถูกแก้หรือไม่ | log file integrity validation |
| central immutable logs | Organization trail → dedicated Log Archive S3 (Simple Storage Service) + restrictive bucket/KMS policy/Object Lock ตาม requirement |
| network metadata | VPC (Virtual Private Cloud) Flow Logs |
| DNS (Domain Name System) query | Route 53 Resolver query logging |
| S3 object-level/API data events | CloudTrail data events |

---

## 14. Governance และ Automation Cheat Sheet

| Scenario | คำตอบที่ควรนึกถึงก่อน |
|---|---|
| บังคับ guardrail ทุก current/future account | Organizations policy/SCP (Service Control Policy) + trusted access |
| central security findings | Security Hub delegated admin |
| central GuardDuty | GuardDuty delegated admin + auto-enable members |
| central backup | Organizations backup policy + AWS Backup |
| Config rules หลาย account ยกเว้นบาง account | organization conformance pack + exclusion list |
| deploy infrastructure หลาย account/Region | StackSets |
| distribute approved AMI (Amazon Machine Image) + template | Service Catalog portfolio/product หรือ StackSets ตามผู้ deploy/ownership |
| self-service ได้แค่ approved patterns | Service Catalog + launch constraints |
| central event from member accounts | EventBridge central event bus + per-account forwarding rules |
| standardized tags | tag policy; ถ้าต้องบังคับตอนสร้างเพิ่ม SCP condition |
| account vending | Control Tower Account Factory |

### Control Tower controls

- **Preventive = ป้องกันก่อนเกิด** เช่น ใช้ Service Control Policy ห้าม action
- **Detective = ตรวจพบหลังเกิด** เช่น ใช้ Config ตรวจ resource ที่ตั้งค่าผิด
- **Proactive = ตรวจ resource ใน CloudFormation ก่อนสร้าง**

### Delegated administration rule

เมื่อเห็น “many accounts/Regions + least operational overhead” ให้มองหา native Organizations integration และ delegated administrator ก่อน custom Lambda loop ทุก account

---

# ภาคที่ 3 — กฎตัดสินและกับดัก

## 15. เห็นคำนี้ ให้คิดถึงสิ่งนี้

อ่านแต่ละข้อเป็น **“ถ้าโจทย์มีเงื่อนไขนี้ → ควรทำอะไร → เพราะอะไร”** คำตัวหนาคือจุดที่ใช้ตัดสินคำตอบ แต่ยังต้องตรวจข้อจำกัดอื่นในโจทย์ด้วย

1. ถ้าโจทย์ต้องการให้ policy หรือบริการ **ครอบคลุมทุก account ทั้งที่มีอยู่และที่จะสร้างใหม่** ให้เลือก **AWS Organizations integration พร้อม auto-enrollment/auto-enable** ที่บริการนั้นรองรับ เพื่อให้ account ใหม่เข้าระบบส่วนกลางได้ด้วย ไม่ต้องตามตั้งค่าทีละ account
2. ถ้าโจทย์เน้น **least operational overhead หรือดูแลระบบให้น้อยที่สุด** ให้เลือก **managed service และการเชื่อมต่อที่ AWS มีให้โดยตรง** เมื่อทำ requirement ครบ; ถ้ามีหลาย account ให้ดู delegated administrator ก่อนเขียน script วนจัดการเอง งานดูแลน้อยไม่ได้แปลว่าค่าใช้งานถูกที่สุดเสมอ
3. ถ้าทีมส่วนกลางต้อง **deploy infrastructure ชุดเดียวกันไปหลาย account หรือหลาย Region** ให้ใช้ **CloudFormation StackSets** เพื่อกระจายและอัปเดต stack จากส่วนกลาง แทนการเข้าไป deploy ทีละที่
4. ถ้าต้องการให้ developer **เลือกสร้าง infrastructure เองได้ แต่เลือกได้เฉพาะแบบที่องค์กรอนุมัติ** ให้ใช้ **AWS Service Catalog** จัด template เป็น product พร้อมข้อจำกัดการ deploy ต่างจาก StackSets ซึ่งเน้นให้ส่วนกลาง deploy ให้
5. ถ้าต้องการ **ห้าม action หรือจำกัด Region ของ account ในองค์กร** ให้ใช้ **SCP (Service Control Policy)** กำหนดเพดานสิทธิ์ แต่ยังต้องมี policy อนุญาตให้ผู้ใช้ทำงานด้วย เพราะ SCP ไม่ได้ให้สิทธิ์ด้วยตัวเอง
6. ถ้าต้องตรวจว่า resource **เปิดสิทธิ์ให้คนนอก account หรือองค์กรหรือไม่** ให้ใช้ **IAM Access Analyzer (IAM ย่อมาจาก Identity and Access Management)** และกำหนด zone of trust ให้ตรงขอบเขตที่เชื่อถือ เช่น เลือกทั้ง Organization ถ้า account ภายในบริษัทไม่ควรถูกนับเป็นคนนอก
7. ถ้ามี **ผลตรวจ security จากหลายบริการ หลาย account หรือหลาย Region** และต้องการดูรวมกัน ให้ใช้ **Security Hub** เป็นศูนย์รวม findings พร้อมตั้ง delegated administrator และการรวมข้าม Region; ตัวตรวจต้นทางอย่าง GuardDuty หรือ Macie ยังทำหน้าที่ตรวจของตัวเอง
8. ถ้าโจทย์ต้องการ **ดูเนื้อหาภายใน packet เพื่อวิเคราะห์ traffic** ให้ใช้ **VPC Traffic Mirroring (Virtual Private Cloud Traffic Mirroring)** กับ network interface ที่รองรับ เพื่อคัดลอก traffic ไปเครื่องวิเคราะห์; Flow Logs มีข้อมูลการรับส่ง แต่ไม่มีเนื้อหา packet
9. ถ้า **request ขาไปผ่าน แต่ response ขากลับถูก REJECT** ให้ตรวจ **NACL (Network Access Control List)** และ ephemeral ports หรือ port ชั่วคราวฝั่ง client เพราะ NACL ตรวจขาไปและขากลับแยกกัน ส่วน Security Group จำ connection และอนุญาต response ของ connection ที่ผ่านแล้วโดยอัตโนมัติ
10. ถ้า network ของ **production กับ development ใช้ Transit Gateway ตัวเดียวกัน แต่ห้ามคุยข้ามกัน** ให้แยก **Transit Gateway route tables** แล้วผูกแต่ละ connection หรือ attachment เข้าตารางของกลุ่มตัวเอง (association) และไม่เพิ่มเส้นทางของอีกกลุ่มเข้ามา (propagation) เช่น prod มี route ไป prod เท่านั้น
11. ถ้า application มีผู้ใช้ทั่วโลก และ firewall ของลูกค้า **ต้องอนุญาตปลายทางด้วย static IP สองค่าที่ไม่เปลี่ยน** ให้พิจารณา **Global Accelerator** เพราะให้ static anycast IP เป็นทางเข้าระดับโลก แล้วส่ง traffic ไปยัง endpoint ที่พร้อมใช้งาน
12. ถ้าเป็นเกมหรือ application ที่ใช้ **UDP (User Datagram Protocol) และต้องการลด latency สำหรับผู้ใช้ทั่วโลก** ให้พิจารณา **Global Accelerator** เพราะรองรับ traffic แบบนี้และใช้เครือข่าย AWS พาไปยัง endpoint; CloudFront เน้นรับส่งเว็บ จึงไม่ใช่ตัวแทนสำหรับ UDP ทั่วไป
13. ถ้าโจทย์ต้องการ **cache รูป วิดีโอ หรือเนื้อหาเว็บใกล้ผู้ใช้** ให้ใช้ **CloudFront** เพื่อลดเวลาโหลดและการเรียก origin; ถ้าต้องปรับ request/response ที่ edge ให้เลือก CloudFront Functions หรือ Lambda@Edge ตามความสามารถที่งานต้องใช้
14. ถ้าต้องการให้ **ชื่อ domain หลักแบบไม่มี www เช่น `example.com` ชี้ไป CloudFront หรือ load balancer** ให้ใช้ **Route 53 Alias record** เพราะชื่อระดับนี้เรียกว่า apex domain และใช้ CNAME (Canonical Name) ไม่ได้; Alias ชี้ได้เฉพาะปลายทางที่รองรับ
15. ถ้า server ใน **data center ของบริษัทต้องแปลงชื่อ private domain ฝั่ง AWS** ให้ตั้ง **Route 53 Resolver inbound endpoint** และตั้ง DNS (Domain Name System) ฝั่งบริษัทให้ forward คำถามของ domain นั้นเข้ามา; จำว่า “คำถามเข้ามาใน AWS = inbound” และต้องมี network เชื่อมถึงกันก่อน
16. ถ้า application ใน **AWS ต้องแปลงชื่อ domain ภายใน data center ของบริษัท** ให้ตั้ง **Route 53 Resolver outbound endpoint พร้อม forwarding rule** ส่งคำถามไป DNS server ของบริษัท; จำว่า “คำถามออกจาก AWS = outbound” และต้องมี network เชื่อมถึงกันก่อน
17. ถ้าต้อง **เข้า shell ของ server โดยไม่เปิด inbound port สำหรับ SSH (Secure Shell)** ให้ใช้ **Systems Manager Session Manager** และกำหนดสิทธิ์จากส่วนกลาง สามารถตั้ง log สำหรับ shell session ปกติได้; ถ้าใช้ port forwarding หรือ SSH tunnel จะบันทึกเนื้อหาภายใน session ด้วยวิธีนี้ไม่ได้
18. ถ้าเก็บไฟล์ใน **S3 (Simple Storage Service) และต้องการให้ผู้ใช้อ่านผ่าน CloudFront เท่านั้น** ให้ใช้ **Origin Access Control พร้อม bucket policy** อนุญาต CloudFront distribution ของเรา และปิด public access ของ bucket วิธีนี้ใช้กับ S3 origin ปกติ ไม่ใช่ S3 website endpoint
19. ถ้าใช้ **CloudFront อยู่หน้า ALB (Application Load Balancer) ที่เปิด public และต้องกันผู้ใช้ยิงเข้า ALB โดยตรง** ให้ CloudFront **แนบ custom header ที่มีค่าลับ** และตั้ง **WAF (Web Application Firewall) ที่ ALB ให้ block request ที่ไม่มี header หรือค่าไม่ตรง**; ถ้าโจทย์กำหนดว่า origin ต้องเป็น private ให้พิจารณา **CloudFront VPC origins** แทน
20. ถ้าเป็น **batch job ที่ต้องใช้ custom AMI (Amazon Machine Image) และหยุดแล้วเริ่มงานใหม่ได้** ให้ใช้ **AWS Batch บน EC2 (Elastic Compute Cloud) พร้อม Spot Instances** เพื่อใช้ image ที่ต้องการและลดค่า compute; ต้องออกแบบ retry หรือ checkpoint รองรับการถูกเรียกคืนเครื่องด้วย
21. ถ้าเป็น **HPC (High Performance Computing) ที่หลายเครื่องต้องคุยกันเร็วมาก** ให้พิจารณา **cluster placement group ใน Availability Zone เดียว พร้อม EFA (Elastic Fabric Adapter)** บน instance ที่รองรับ เพื่อให้ latency ระหว่างเครื่องต่ำ; การกระจายข้ามหลายโซนอาจทำให้การคุยกันช้าลง
22. ถ้า **แต่ละ request ใช้แรงประมวลผลไม่เท่ากัน** อย่าเพิ่มเครื่องตามจำนวน request อย่างเดียว ให้เลือก **metric ที่สะท้อนภาระจริง เช่น CPU (Central Processing Unit) utilization** เมื่อสัมพันธ์กับงาน เพราะ request สิบงานเบาอาจใช้เครื่องน้อยกว่างานหนักเพียงงานเดียว
23. ถ้า **CPU utilization ไม่สะท้อนความต้องการเพิ่มเครื่อง แต่จำนวน web request ต่อเครื่องสะท้อนได้ดี** ให้ใช้ Auto Scaling แบบ **target tracking ด้วย `ALBRequestCountPerTarget`** หรือ custom metric ที่เหมาะกับธุรกิจ แทนการยึด CPU ทุกกรณี
24. ถ้ามี **worker หลายเครื่องดึงงานจากคิว และต้องเพิ่ม/ลด worker ตามงานค้าง** ให้ scale จาก **backlog per instance หรือจำนวนงานค้างต่อ worker** ไม่ใช่งานค้างรวมอย่างเดียว เช่น งานค้าง 1,000 ชิ้นกับ worker 2 เครื่องมีภาระต่อเครื่องมากกว่า worker 20 เครื่อง
25. ถ้า application บน Linux หลายเครื่องใน **หลาย Availability Zones ต้อง mount และใช้ไฟล์ชุดเดียวกัน** ให้เลือก **EFS (Elastic File System) แบบ Regional** ซึ่งเป็น shared file storage; disk EBS (Elastic Block Store) ทั่วไปผูกกับโซนเดียว จึงไม่ใช่ตัวแทนสำหรับโจทย์นี้
26. ถ้า Windows application ต้อง **แชร์ไฟล์ผ่าน SMB (Server Message Block) และใช้สิทธิ์จาก Active Directory** ให้เลือก **FSx for Windows File Server** เพราะให้ file system และการเชื่อมต่อ directory ที่ตรงกับ Windows workload
27. ถ้าเก็บข้อมูลใน S3 แล้ว **เดาไม่ได้ว่าไฟล์ไหนจะถูกอ่านบ่อยหรือเงียบไปนาน** ให้พิจารณา **S3 Intelligent-Tiering** เพื่อปรับ tier ตามการเข้าถึง โดยต้องพิจารณาค่า monitoring และเปิด archive tiers เองหากต้องการใช้
28. ถ้าข้อมูลเป็น archive ที่อ่านไม่บ่อย และ **ยอมรอ restore ประมาณ 3–5 ชั่วโมงได้** ให้พิจารณา **S3 Glacier Flexible Retrieval แบบ Standard retrieval**; เวลานี้เป็นระยะเวลาทั่วไป ไม่ใช่การรับประกันตายตัว และต้องเลือก retrieval option ให้ตรงโจทย์
29. ถ้าเป็น archive ที่เก็บยาว อ่านน้อยมาก และ **ยอมรอ restore ราว 12 ชั่วโมงได้โดยต้องการค่าจัดเก็บต่ำ** ให้พิจารณา **S3 Glacier Deep Archive แบบ Standard retrieval** พร้อมคิดค่า restore และ minimum storage duration; ถ้าต้องได้ข้อมูลภายในไม่กี่ชั่วโมง ตัวนี้อาจไม่ผ่าน requirement
30. ถ้าข้อมูล **อ่านไม่บ่อย แต่สร้างใหม่ได้หรือมีสำเนาหลักอยู่ที่อื่น** ให้พิจารณา **S3 One Zone-IA (Infrequent Access)** เพื่อลดค่าเก็บ เพราะเก็บในโซนเดียว จึงไม่ควรใช้เป็นสำเนาเดียวของข้อมูลที่สูญเสียไม่ได้
31. ถ้าต้องเก็บข้อมูล **ห้ามลบหรือเขียนทับเป็นเวลา 5 ปี แม้แต่ admin ก็ห้าม** ให้ใช้ **S3 Object Lock แบบ compliance mode** พร้อมตั้ง retention ตามกำหนด เพราะ governance mode ยังมีช่องให้ผู้มีสิทธิ์ bypass ได้ แต่ compliance mode ห้ามลบ object version ที่ล็อกไว้ก่อนครบกำหนด
32. ถ้าต้อง **แก้ tag, copy หรือทำงานแบบเดียวกันกับ S3 objects เดิมหลายล้านรายการ** ให้ใช้ **S3 Batch Operations** โดยใช้ S3 Inventory เป็นรายการตั้งต้นได้ แทนการเขียน script เรียกทีละ object; Inventory ทำหน้าที่สำรวจรายการ ไม่ได้แก้ไฟล์ให้เอง
33. ถ้าต้องการ **replicate S3 ทั้งไฟล์เก่าที่มีอยู่แล้วและไฟล์ใหม่ที่จะเข้ามา** ให้ใช้ **S3 Batch Replication สำหรับของเก่า และ replication rule สำหรับของใหม่** เพราะการสร้าง replication rule ใหม่อย่างเดียวไม่ได้ตามคัดลอกของเก่าให้ทั้งหมด
34. ถ้ามี **หลายทีมใช้ S3 bucket เดียว แต่ต้องเข้าถึงคนละกลุ่มไฟล์หรือใช้ policy ต่างกัน** ให้พิจารณา **S3 Access Points** เพื่อแยกทางเข้าและ policy ตามการใช้งาน ช่วยจัดการสิทธิ์ได้ง่ายกว่าการอัดทุกเงื่อนไขไว้ใน bucket policy เดียว; ไม่ได้เพิ่มความเร็วให้ bucket โดยอัตโนมัติ
35. ถ้า application ในอีก Region ต้อง **อ่านข้อมูลชุดใหญ่เดิมซ้ำบ่อย ๆ** ให้เปรียบเทียบ **replication ไปเก็บใกล้ application** กับการอ่านข้าม Region ทุกครั้ง โดยคิดทั้งค่าเก็บสำเนา ค่า replicate ความสดของข้อมูล และค่า transfer; จำนวนการอ่านมากอาจทำให้เก็บสำเนาคุ้มกว่า
36. ถ้า application ในอีก Region **อ่านข้อมูลน้อยและนาน ๆ ครั้ง แต่ต้องใช้ private network** ให้เปรียบเทียบ **การเชื่อมต่อ private เพื่ออ่านจากต้นทาง** กับการ replicate ทั้งชุด อย่าคัดลอกข้อมูลก้อนใหญ่โดยอัตโนมัติเมื่อใช้งานจริงเพียงเล็กน้อย; ต้องคิดค่า connection และ data transfer ด้วย
37. ถ้า server ใน data center ต้อง **ใช้ file share แบบเดิมผ่าน NFS (Network File System) หรือ SMB แต่ต้องการเก็บข้อมูลปลายทางเป็น S3 objects** ให้ใช้ **S3 File Gateway** เพื่อเชื่อม file interface เดิมกับ S3 และ cache ข้อมูลที่ใช้บ่อยไว้ใกล้ server
38. ถ้าต้อง **กำหนด backup schedule และ retention ให้หลายชนิด resource หรือหลาย account จากส่วนกลาง** ให้ใช้ **AWS Backup** พร้อม policy ตามขอบเขตที่ต้องการ แทนการสร้างระบบตั้งเวลา backup แยกทุกบริการ; ตรวจด้วยว่า resource นั้นรองรับการ backup/restore แบบที่โจทย์ต้องการ
39. ถ้า **DynamoDB ถูกอ่าน key เดิมซ้ำมาก และยอมรับข้อมูลแบบ eventually consistent ได้** ให้พิจารณา **DAX (DynamoDB Accelerator)** เพื่อ cache ผลอ่านและลดงานของ table; ไม่ใช่ cache ทั่วไปสำหรับ database ทุกชนิด และการอ่านแบบ strongly consistent ไม่ได้ประโยชน์จาก cache แบบเดียวกัน
40. ถ้าต้องการ **database หลักที่ใช้ Redis-compatible interface และข้อมูลต้องทนต่อเครื่องล่ม** ให้พิจารณา **MemoryDB** ซึ่งมี transaction log ข้ามหลาย Availability Zones เพื่อความทนทาน ต่างจากการเลือก cache เพียงเพราะอ่านเขียนเร็ว
41. ถ้า application ใช้ **RDS (Relational Database Service) และต้องเปลี่ยนรหัสผ่าน database อัตโนมัติ** ให้ใช้ **Secrets Manager พร้อม rotation** และให้ application อ่าน secret ที่เป็นปัจจุบัน แทนการฝังรหัสผ่านคงที่ไว้ใน code หรือ image
42. ถ้า database ต้อง **ให้บริการต่อได้เมื่อเครื่องหลักหรือ Availability Zone ล่ม โดย failover อัตโนมัติ** ให้พิจารณา **RDS Multi-AZ (Multi-Availability Zone)**; แบบ database instance มี standby ที่ไม่รับงานอ่าน ส่วนแบบ database cluster มี reader ที่รับงานอ่านได้ จึงต้องดูชนิดให้ชัด
43. ถ้า **RDS รับงานอ่านไม่ไหว และ application ยอมรับ replication lag ได้** ให้ใช้ **read replica** แล้วแยก read traffic ไปที่ replica; การเพิ่ม standby ของ Multi-AZ database instance ช่วย failover แต่ไม่ได้เพิ่มปลายทางสำหรับอ่าน
44. ถ้าใช้ Aurora และต้อง **ให้อีก Region อ่านข้อมูลได้ใกล้ผู้ใช้ พร้อมมีทางกู้ระบบเมื่อ Region หลักล่ม** ให้พิจารณา **Aurora Global Database** ซึ่ง replicate ข้าม Region; ยังต้องวางแผน failover และยอมรับ replication lag ตาม requirement
45. ถ้า backend ใช้เวลา **90 วินาที แต่ client รอได้เพียง 10 วินาที** ให้เปลี่ยนเป็น **asynchronous processing**: รับคำขอแล้วส่งงานเข้า **SQS (Simple Queue Service)**, ตอบกลับพร้อมรหัสติดตามงาน แล้วให้ worker ทำต่อและให้ client ตรวจผลภายหลัง แทนการบังคับให้ connection เดิมรอจนงานเสร็จ
46. ถ้าคิวงานต้อง **รักษาลำดับและลด message ที่ส่งซ้ำ** ให้ใช้ **SQS FIFO (First In, First Out)** และกำหนด message group ตามลำดับที่ต้องรักษา ถ้ามี Standard queue อยู่แล้วต้องสร้าง FIFO queue ใหม่; application ยังควรป้องกันผลซ้ำ เช่น ไม่ตัดเงินซ้ำเมื่อ message ถูกประมวลผลใหม่
47. ถ้า application เดิมใช้ **ActiveMQ หรือ RabbitMQ และต้องย้ายโดยแก้ code/protocol ให้น้อยที่สุด** ให้ใช้ **Amazon MQ** เพราะรองรับ broker ที่ application รู้จักอยู่แล้ว การเปลี่ยนไปใช้ SQS อาจต้องแก้วิธีส่งและรับข้อความ
48. ถ้างานมี **หลายขั้น ต้อง retry, แยกเงื่อนไข, รอผล, ทำขนาน หรือรอคนอนุมัติ** ให้ใช้ **Step Functions** คุม workflow แทนการเขียน function เดียวยาว ๆ ที่ต้องจำสถานะและจัดการ retry เองทั้งหมด
49. ถ้าเว็บต้อง **รัน code ฝั่ง server เพื่อสร้างหน้าเว็บทุกครั้งที่มี request** ให้ใช้ **compute เช่น EC2, container หรือ Lambda ตาม runtime**; S3 static website hosting ส่งไฟล์ที่เก็บไว้ได้ แต่รัน backend code เพื่อสร้างหน้าเว็บให้ไม่ได้
50. ถ้าทีมต้อง **รัน container แต่ไม่อยาก provision หรือ patch host ที่รองรับ container** ให้ใช้ **Fargate** ร่วมกับ **ECS (Elastic Container Service) หรือ EKS (Elastic Kubernetes Service)** โดยทีมยังต้องดูแล image, configuration และตัว application
51. ถ้าเป็น **เว็บหรือ application ขนาดเล็ก ใช้ stack มาตรฐาน และต้องการราคาชุดที่คาดเดาง่าย** ให้พิจารณา **Lightsail** เช่น เว็บ Linux + Apache + MySQL + PHP; ถ้าต้องใช้ network หรือ infrastructure ที่ซับซ้อน ให้ตรวจว่าเกินขอบเขตความเรียบง่ายที่ Lightsail เหมาะจะดูแลหรือไม่
52. ถ้าต้อง **สร้าง infrastructure และติดตั้ง software ตามขั้นตอนเดิมซ้ำได้ทุกครั้ง** ให้ใช้ **CloudFormation สร้าง resource** แล้วใช้ **EC2 user data** สำหรับ bootstrap ตอน launch หรือ **Systems Manager** สำหรับรันขั้นตอนจัดการเครื่อง ตามช่วงเวลาที่โจทย์ต้องการ ไม่ใช่ให้คนเข้าไปติดตั้งด้วยมือทุกเครื่อง
53. ถ้ามี **ระบบ login ของ application เดิมที่ไม่รองรับ SAML (Security Assertion Markup Language) หรือ OIDC (OpenID Connect)** และต้องการให้ผู้ใช้ที่ login แล้วได้รับสิทธิ์เรียก AWS ให้พิจารณา **Cognito identity pool แบบ developer-authenticated identities** โดยให้ backend ที่เชื่อถือได้ยืนยันผู้ใช้ก่อน; ไม่ใช่ส่งรหัสผ่าน AWS ให้ client
54. ถ้าต้องสร้าง **contact center ที่เข้าใจว่าลูกค้าต้องการทำอะไร แล้วเรียก backend ไปทำงานต่อ** ให้ใช้ **Amazon Connect รับสาย, Amazon Lex เข้าใจคำพูด/เจตนา และ Lambda เรียก business logic** เช่น ลูกค้าขอตรวจสถานะคำสั่งซื้อ แล้วระบบดึงข้อมูลมาตอบ
55. ถ้าต้อง **ย้าย server ภายในเวลาจำกัด เช่น 90 วัน และไม่มี source code ให้แก้** ให้พิจารณา **AWS Application Migration Service เพื่อ rehost** โดย replicate server แล้วเปิดใช้งานบน EC2 แทนการเริ่ม redesign application ใหม่ตั้งแต่ต้น
56. ถ้าต้อง **ย้าย database ข้าม engine เช่น Oracle ไป Aurora PostgreSQL** ต้องทำทั้งสองงาน: **Schema Conversion Tool แปลง schema/code และ Database Migration Service ย้ายข้อมูล**; ถ้าต้อง downtime ต่ำ ให้ตามคัดลอกข้อมูลที่เปลี่ยนระหว่างย้ายด้วย **CDC (Change Data Capture)** ก่อน cutover
57. ถ้าต้อง **ย้ายหรือ sync ไฟล์ผ่าน network ซ้ำ ๆ ตาม schedule** ให้พิจารณา **AWS DataSync** ซึ่งช่วยจัดการการส่งและตรวจสอบข้อมูล; ถ้าโจทย์ต้องการเพียงเปิด server รับไฟล์ด้วย protocol เดิมของคู่ค้า ให้แยกไปพิจารณา Transfer Family
58. ถ้าต้องย้ายข้อมูล **ใหญ่มากจนส่งผ่าน network ไม่ทันกำหนด** ให้พิจารณา **offline transfer** และรวมเวลาส่งอุปกรณ์/นำเข้าข้อมูลด้วย ในเนื้อหาหลักสูตรเดิมตัวอย่างคือ **Snowball Edge**; ปัจจุบันเปิดให้เฉพาะลูกค้าเดิมตั้งแต่ 7 พฤศจิกายน 2025 ลูกค้าใหม่ต้องดูทางเลือกที่เปิดให้ใช้ เช่น Data Transfer Terminal หรือ partner solution
59. ถ้าคู่ค้าต้อง **อัปโหลดหรือดาวน์โหลดไฟล์ด้วย SFTP (SSH File Transfer Protocol) เดิม โดยไม่อยากดูแล file-transfer server เอง** ให้ใช้ **AWS Transfer Family** เชื่อมไปยัง storage ที่รองรับ; จุดตัดสินคือรักษาวิธีเชื่อมต่อของ client ไม่ใช่การย้ายข้อมูลก้อนใหญ่ให้เร็วที่สุด
60. ถ้าต้อง **ตรวจย้อนหลังว่าใครเรียก AWS ผ่านทั้ง console และ code พร้อมตรวจว่า log ถูกแก้หรือไม่** ให้ใช้ **CloudTrail** บันทึก activity และเปิด **log file integrity validation**; การตรวจความถูกต้องของ log ช่วยพบการเปลี่ยนแปลง แต่ไม่ได้ป้องกันการลบแทนการตั้งสิทธิ์และ retention
61. ถ้า requirement ต้อง **ใช้ hardware เก็บ key แบบ single-tenant และควบคุมผู้ใช้ key, algorithm หรือ cryptographic interface เองโดยตรง** ให้พิจารณา **CloudHSM (Hardware Security Module)**; ถ้าต้องการ managed key ที่เชื่อม AWS services ง่ายให้ดู **KMS (Key Management Service)** และอย่าใช้คำว่า FIPS (Federal Information Processing Standards) Level 3 เพียงอย่างเดียวตัดสิน เพราะ KMS standard key store ก็มีการรับรองระดับนี้
62. ถ้าต้อง **เตือนก่อนสิ้นเดือนว่าค่าใช้จ่ายมีแนวโน้มเกินงบ และให้ทำ action เมื่อถึงเกณฑ์** ให้ใช้ **AWS Budgets แบบ forecasted alert พร้อม Budget Actions ที่รองรับ** เช่น จำกัดการสร้าง resource; ต้องตั้ง action และสิทธิ์เพิ่มเอง ไม่ใช่ตั้งงบแล้ว AWS จะหยุดค่าใช้จ่ายทั้งหมดให้ทันที
63. ถ้าระบบมี **การใช้งานพื้นฐานสม่ำเสมอและคาดว่าจะใช้ต่อระยะยาว** ให้พิจารณา **Savings Plans หรือ Reserved Instances** ตามบริการและความยืดหยุ่นที่ต้องการ โดย commit เฉพาะส่วนที่มั่นใจว่าจะใช้จริง แทนการจ่าย On-Demand ทั้งหมดหรือซื้อส่วนลดเผื่อ load สูงสุดชั่วคราว
64. ถ้าเป็น **batch job ที่ถูกขัดจังหวะได้และ retry หรือเริ่มจาก checkpoint ได้** ให้ใช้ **Spot Instances** เพื่อลดค่า compute เพราะ AWS เรียกคืนเครื่องได้; ถ้าห้ามหยุดกลางงานและไม่มีวิธีรับมือ การใช้ Spot เป็นกำลังหลักเพียงอย่างเดียวอาจไม่ผ่าน requirement
65. ถ้าต้อง **รวม event จากหลาย account แล้วแก้ปัญหาจากส่วนกลางโดยอัตโนมัติ** ให้ใช้ **EventBridge ส่ง event ไป central event bus** พร้อม policy ที่อนุญาต แล้วให้ **Lambda หรือ Systems Manager Automation** ทำ remediation ตาม rule; การรวม event อย่างเดียวไม่ได้แก้ resource ให้เอง
66. ถ้าโจทย์ถามว่า **ใครลบหรือแก้ resource เมื่อไร และทำผ่าน role ไหน** ให้ดู **CloudTrail** เพราะบันทึก AWS activity โดยต้องเปิด event ประเภทที่เกี่ยวข้อง เช่น งานระดับ object ใน S3 ต้องดู data events ไม่ใช่คาดว่าจะอยู่ใน management events ทั้งหมด
67. ถ้าโจทย์ถามว่า **resource เคยตั้งค่าไว้อย่างไร เปลี่ยนจากอะไร และตรงข้อกำหนดหรือไม่** ให้ใช้ **AWS Config** เก็บประวัติ configuration และประเมิน compliance; ถ้าถามว่าใครเป็นคนกดเปลี่ยน ให้กลับไปดู CloudTrail
68. ถ้าต้องดู **CPU utilization, latency, error rate, application logs หรือให้ alarm เมื่อเกินค่า** ให้ใช้ **CloudWatch** พร้อมส่ง metric/log ที่ต้องการและตั้ง alarm; ถ้าเป็น custom application metric ต้อง instrument ให้ระบบส่งข้อมูลนั้นด้วย
69. ถ้าต้อง **ค้นหาข้อมูลส่วนบุคคลหรือข้อมูลอ่อนไหวใน S3 เช่น เลขบัตรเครดิตหรือข้อมูลส่วนบุคคล** ให้ใช้ **Amazon Macie** เพื่อจำแนกข้อมูลและสร้าง findings; Macie ช่วยตรวจพบ แต่ไม่ได้ลบหรือปกปิดข้อมูลให้โดยอัตโนมัติ
70. ถ้าต้อง **ตรวจช่องโหว่ของ software/package บน EC2, container image หรือ Lambda ที่บริการรองรับ** ให้ใช้ **Amazon Inspector**; ถ้าโจทย์เน้นพฤติกรรมน่าสงสัย เช่น credential ถูกขโมยหรือเครื่องถูกใช้ขุดเหรียญ ให้พิจารณา GuardDuty ซึ่งทำหน้าที่ตรวจภัยคุกคามคนละด้าน

**แหล่งตรวจเงื่อนไขเพิ่มเติมจาก AWS:** [Transit Gateway association/propagation](https://docs.aws.amazon.com/vpc/latest/tgw/how-transit-gateways-work.html), [Route 53 Alias กับ apex domain](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resource-record-sets-choosing-alias-non-alias.html), [Session Manager และข้อจำกัด session logs](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html), [CloudFront กับ public load balancer](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/restrict-access-to-load-balancer.html), [CloudFront private origins](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-vpc-origins.html), [เวลา restore ของ Glacier](https://docs.aws.amazon.com/AmazonS3/latest/userguide/glacier-storage-classes.html), [SQS และการประมวลผลซ้ำ](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/designing-for-outage-recovery-scenarios.html), [Snowball availability ปัจจุบัน](https://aws.amazon.com/snowball/faqs/), [Budget Actions](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-controls.html)

---

## 16. สิ่งที่เปลี่ยนย้อนหลังไม่ได้หรือมีข้อจำกัดสำคัญ

ข้อสอบชอบ distractor ประเภท “แก้ของเดิมง่าย ๆ” ทั้งที่ service ไม่รองรับ:

- SQS (Simple Queue Service) Standard เปลี่ยนเป็น FIFO (First In, First Out) ไม่ได้
- EC2 (Elastic Compute Cloud) hibernation ต้องเปิดและรองรับตั้งแต่ launch
- **S3 (Simple Storage Service) Object Lock เปิดกับ bucket เดิมได้**; สิ่งที่ย้อนกลับไม่ได้คือปิด Object Lock หรือ suspend Versioning หลังเปิดใช้ ([AWS: Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock-configure.html))
- EBS (Elastic Block Store) volume ใช้ได้ภายใน AZ (Availability Zone) เดียว
- EBS Multi-Attach ไม่ใช่ shared filesystem หลาย AZ
- VPC (Virtual Private Cloud) Peering ไม่ transitive
- Security Group stateful; NACL (Network Access Control List) stateless
- NAT (Network Address Translation) Gateway ผูกกับ Availability Zone
- **RDS (Relational Database Service) Multi-AZ ต้องแยกชนิด**: DB instance มี standby ที่ไม่รับงานอ่าน; DB cluster มี reader ที่รับงานอ่านได้
- replication rule ใหม่ไม่จัดการ S3 objects เก่าเองหากไม่ใช้ Batch Replication
- Memcached เพิ่ม node แล้ว client อาจต้อง discover/configure node ใหม่
- Simple AD (Active Directory) ไม่มี feature เทียบเท่า AWS Managed Microsoft AD ทุกอย่าง เช่น MFA (Multi-Factor Authentication)-related requirements บางรูปแบบ
- CloudFront/Route 53/Global Accelerator ทำคนละ layer แทนกันไม่ได้ทุก use case

---

## 17. บทเรียนเฉพาะจาก 4 ข้อที่เคยพลาดใน Official Practice Exam

ผลฝึกเดิมได้ 71/75 ข้อ จุดพลาดทั้งสี่เป็นเรื่อง “scope และเครื่องมือ native” มากกว่าความจำชื่อ service

### 17.1 บังคับ SSH source CIDR ใน 50 accounts และ member ห้ามแก้

หลักคิด:

- ต้อง enforce ข้ามองค์กร
- member account แก้ไม่ได้
- เลือก Organizations-native preventive control/SCP (Service Control Policy) ที่เหมาะกับ policy condition ไม่ใช่ Config อย่างเดียว เพราะ Config เป็น detective

กฎจำ: **“ห้ามก่อนเกิด” = preventive; “เจอหลังเกิด” = detective**

### 17.2 แก้ tag ที่ผิดและบังคับมาตรฐานในอนาคต

ต้องแยกสามงาน:

1. tag policy ระบุมาตรฐาน value/key
2. Resource Groups/Tag Editor หรือ automation แก้ของเดิม
3. SCP condition บังคับ request ใหม่ให้มี tag/ค่าตามต้องการ เมื่อ requirement ต้อง hard enforcement

กฎจำ: **Tag policy กำหนดมาตรฐาน → Service Control Policy บังคับ request ที่รองรับ → remediation แก้ resource เดิม**

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

> **ถ้าสอบพรุ่งนี้ ข้ามแผน 21 วันนี้ได้เลย** อ่านต่อจากจุดเดิม แล้วทวนข้อ 16 (กับดัก), 17 (ข้อที่เคยผิด), 21 (ภาพรวม) และ 19 (จัดเวลาสอบ) ใช้ข้อ 15 ค้นเฉพาะเรื่องที่ยังสับสน

### สัปดาห์ 1 — สร้าง decision framework

| วัน | เนื้อหา | ผลลัพธ์ที่ต้องทำได้ |
|---|---|---|
| 1 | Exam algorithm + D1 Organizations | อธิบาย SCP (Service Control Policy)/IAM (Identity and Access Management)/Control Tower/delegated admin ได้ |
| 2 | Network/Transit Gateway/Direct Connect/VPN (Virtual Private Network)/DNS (Domain Name System) | วาด hybrid data path และ segmentation ได้ |
| 3 | Security/KMS (Key Management Service)/central findings | เลือก detector/aggregator/remediator ถูก |
| 4 | disaster recovery/RTO (Recovery Time Objective — เวลาหยุดระบบสูงสุดที่ยอมได้)/RPO (Recovery Point Objective — ช่วงข้อมูลย้อนหลังที่ยอมเสียได้) | เลือก 4 disaster recovery patterns จาก SLA (Service Level Agreement) ได้ |
| 5 | D2 deployment/reliability | เลือก deployment และ decoupling pattern ได้ |
| 6 | Storage/database/cache | เลือกจาก access pattern/retrieval SLA ได้ |
| 7 | ทำ Study mode 50 ข้อ | จดกฎทุกข้อที่ผิด ไม่ดูแค่คะแนน |

### สัปดาห์ 2 — ปิดช่องว่างและฝึกโจทย์ยาว

| วัน | เนื้อหา | ผลลัพธ์ที่ต้องทำได้ |
|---|---|---|
| 8 | D3 observability/automation | แยก CloudTrail/Config/CloudWatch/Systems Manager ได้ |
| 9 | Cost/performance | เลือก metric, scaling, pricing, lifecycle ได้ |
| 10 | D4 7Rs + migration tools | จับคู่ MGN (Application Migration Service)/DMS (Database Migration Service)/SCT (Schema Conversion Tool)/DataSync/Snow ได้ |
| 11 | Modernization/integration | เลือก SQS (Simple Queue Service)/SNS (Simple Notification Service)/EventBridge/Kinesis/MQ/Step Functions ได้ |
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
- ขีดคำว่า least, most, all, existing, future, RTO (Recovery Time Objective — เวลาหยุดระบบสูงสุดที่ยอมได้)/RPO (Recovery Point Objective — ช่วงข้อมูลย้อนหลังที่ยอมเสียได้), protocol, Region/account scope
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
2. scope ถูก account/AZ (Availability Zone)/Region/protocol หรือไม่?
3. มี hidden operational work อะไร?
4. รองรับ existing resources และ future resources ครบหรือไม่?
5. มีข้อจำกัดเปลี่ยนย้อนหลังไม่ได้หรือไม่?
6. data/return path และ permission path ครบหรือไม่?
7. มี AWS-native managed option ที่ตรงกว่าไหม?

### Distractor patterns

- **ถูก service แต่ผิด feature** เช่น RDS (Relational Database Service) Multi-AZ แทน read replica
- **ถูกเฉพาะ happy path** แต่ไม่มี failover/return route
- **แก้เพียงของใหม่** ทั้งที่โจทย์ถาม existing + future
- **scale ไม่ได้** เช่น Lambda per account แทน delegated admin
- **ละเมิด protocol** เช่น SQS (Simple Queue Service) แทน proprietary ActiveMQ โดยไม่ยอมแก้ app
- **แพงเกิน requirement** เช่น active-active เมื่อ RTO (Recovery Time Objective — เวลาหยุดระบบสูงสุดที่ยอมได้) ยอม 24 ชั่วโมง
- **ราคาถูกแต่ผิด SLA** (Service Level Agreement) เช่น Deep Archive เมื่อ retrieval ต้องภายใน 5 ชั่วโมง
- **monitor แต่ไม่ enforce** เช่น Config rule เมื่อต้องป้องกันไม่ให้สร้าง
- **enforce แต่ไม่ remediate ของเดิม** เช่น SCP (Service Control Policy) เมื่อโจทย์ต้องแก้ resource เก่า

---

## 21. One-page mental model ก่อนเข้าห้องสอบ

อ่านเป็นคู่ **“เงื่อนไข → ตัวเลือก”** ถ้าบอกเหตุผลได้แล้วให้ผ่าน ไม่ต้องย้อนอ่านทั้งบท

### Organization

**โครงสร้างหลาย account → Organizations**; จัดกลุ่มด้วย Organizational Unit; จำกัดเพดานสิทธิ์ด้วย Service Control Policy; สร้าง baseline ด้วย Control Tower; พนักงานเข้าใช้ผ่าน IAM Identity Center; ให้ account ผู้เชี่ยวชาญเป็น delegated admin

**ส่วนกลาง deploy เอง → StackSets**; ให้ทีมเลือกของที่อนุมัติแล้วไป deploy → Service Catalog

### Network

**เชื่อม VPC (Virtual Private Cloud) ไม่กี่วง → Peering**; หลายวงต้องมี hub → Transit Gateway; เปิดเฉพาะ service ให้เข้าผ่าน private network → PrivateLink

**เชื่อม data center แบบ private → Direct Connect**; tunnel เข้ารหัสผ่าน internet → VPN (Virtual Private Network); แปลงชื่อข้าม AWS กับ data center → Resolver inbound/outbound endpoints

### Edge

**cache เว็บ → CloudFront**; TCP/UDP จากทั่วโลกและต้อง static IP → Global Accelerator; เลือกปลายทางผ่าน DNS (Domain Name System) → Route 53

### Security

**สิทธิ์ผู้ใช้/role → IAM** (Identity and Access Management); เพดานสิทธิ์ทั้งองค์กร → Service Control Policy; กรอง web request → WAF (Web Application Firewall); ป้องกัน DDoS (Distributed Denial of Service) → Shield

**พฤติกรรมน่าสงสัย → GuardDuty**; ช่องโหว่ → Inspector; ข้อมูลอ่อนไหวใน S3 (Simple Storage Service) → Macie; สิทธิ์เปิดออกนอกองค์กร → Access Analyzer; รวม findings → Security Hub

### Observability

**ใครแก้อะไร → CloudTrail**; resource ตั้งค่าตรงข้อกำหนดไหม → Config; metric/log/alarm → CloudWatch; network metadata → Flow Logs; patch/run command/เข้า session → Systems Manager

### Data

**เก็บ object → S3**; disk ต่อเครื่อง → EBS (Elastic Block Store); Linux แชร์ไฟล์ → EFS (Elastic File System); Windows แชร์ไฟล์ → FSx for Windows; parallel file สำหรับงานคำนวณหนัก → FSx for Lustre

**relational database → RDS (Relational Database Service)/Aurora**; key-value → DynamoDB; cache ทั่วไป → ElastiCache; cache สำหรับ DynamoDB → DAX (DynamoDB Accelerator); Redis-compatible primary database ที่ต้อง durable → MemoryDB

### Integration

**พักงานในคิว → SQS** (Simple Queue Service); กระจายข้อความเดียวไปหลายผู้รับ → SNS (Simple Notification Service); route ตาม event → EventBridge; stream และอ่านย้อนหลัง → Kinesis Data Streams; ใช้ broker protocol เดิม → Amazon MQ; คุม workflow หลายขั้น → Step Functions

### Migration

**ย้าย server โดยแก้ให้น้อย → Application Migration Service**; ย้ายข้อมูล database → Database Migration Service; แปลง schema ข้าม engine → Schema Conversion Tool

**ย้ายไฟล์ผ่าน network → DataSync**; client ต้องใช้ SFTP (SSH File Transfer Protocol) เดิม → Transfer Family; ข้อมูลใหญ่มากและ network ไม่ไหว → ตรวจทางเลือก offline ตามบริการที่เปิดให้ใช้งาน

### DR

**DR (Disaster Recovery)** = การกู้ระบบหลังเหตุร้าย

**RPO (Recovery Point Objective)** = ยอมเสียข้อมูลย้อนหลังเท่าไร; **RTO (Recovery Time Objective)** = ยอมหยุดนานเท่าไร

จากประหยัดแต่กู้ช้า → แพงแต่กู้เร็ว: **backup/restore → pilot light → warm standby → active-active** ต้องตรวจว่าแต่ละแบบทำเวลาตามโจทย์ได้จริง

### Cost

**ปิดของไม่ใช้ → rightsize → scale ตาม load → เลือกรูปแบบราคา → ปรับ storage lifecycle/ค่า transfer → ตั้งงบและเจ้าของค่าใช้จ่าย**

---

## 22. Checklist ความรู้ก่อนจองสอบ

ตอบ “ได้และอธิบายเหตุผลได้” ให้ครบ:

- [ ] SCP (Service Control Policy), IAM (Identity and Access Management), trust policy และ resource policy ต่างกันอย่างไร
- [ ] Control Tower, Account Factory, Service Catalog และ StackSets ใช้เมื่อไร
- [ ] VPC (Virtual Private Cloud) Peering, Transit Gateway, PrivateLink, Direct Connect, VPN (Virtual Private Network) และ Cloud WAN ต่างกันอย่างไร
- [ ] Resolver inbound/outbound endpoint ใช้ทิศไหน
- [ ] Security Group stateful/NACL (Network Access Control List) stateless และ ephemeral ports
- [ ] CloudFront/Global Accelerator/Route 53 ต่างกันอย่างไร
- [ ] WAF (Web Application Firewall)/Shield/Network Firewall/Firewall Manager ต่างกันอย่างไร
- [ ] GuardDuty/Inspector/Macie/Access Analyzer/Security Hub ต่างกันอย่างไร
- [ ] CloudTrail/Config/CloudWatch/Flow Logs ต่างกันอย่างไร
- [ ] KMS (Key Management Service)/CloudHSM/Secrets Manager/Parameter Store ต่างกันอย่างไร
- [ ] เลือก disaster recovery strategy จาก RTO (Recovery Time Objective — เวลาหยุดระบบสูงสุดที่ยอมได้)/RPO (Recovery Point Objective — ช่วงข้อมูลย้อนหลังที่ยอมเสียได้) ได้
- [ ] Multi-AZ (Availability Zone)/read replica/Aurora Global Database ต่างกันอย่างไร
- [ ] S3 (Simple Storage Service) storage class จาก access/retrieval SLA (Service Level Agreement) ได้
- [ ] EBS (Elastic Block Store)/EFS (Elastic File System)/FSx/S3 ใช้ตาม access protocol ได้
- [ ] SQS (Simple Queue Service)/SNS (Simple Notification Service)/EventBridge/Kinesis/MQ/Step Functions ต่างกันอย่างไร
- [ ] เลือก Auto Scaling metric ที่สัมพันธ์กับงานได้
- [ ] เลือก purchase model จาก workload ได้
- [ ] อธิบาย 7Rs และ migration phases ได้
- [ ] เลือก MGN (Application Migration Service)/DMS (Database Migration Service)/SCT (Schema Conversion Tool)/DataSync/Snow/Transfer Family ได้
- [ ] รู้สิ่งที่เปลี่ยนย้อนหลังไม่ได้และหลีกเลี่ยง distractor ได้
- [ ] ทำ full mock ผ่านเกณฑ์ readiness ต่อเนื่อง

---

## 23. สิ่งที่ไม่ควรเสียเวลาจำเกินไป

- ราคาตัวเลขละเอียดที่เปลี่ยนได้ — จำ cost model และ trade-off
- quota ตัวเลขทุกบริการ — จำว่าต้องตรวจ quota และขอเพิ่มล่วงหน้า
- CLI (Command Line Interface) syntax ทั้งหมด — ข้อสอบวัด architecture มากกว่า command syntax
- feature ย่อยนอก scope ที่ไม่ช่วยตัดสิน requirement
- คำตอบแบบ “บริการ X ดีที่สุดเสมอ” — ไม่มีจริง ต้องผูกกับ constraint

สิ่งที่ควรจำแม่นกว่าคือ service boundary, scope, protocol, consistency, durability, RTO (Recovery Time Objective — เวลาหยุดระบบสูงสุดที่ยอมได้)/RPO (Recovery Point Objective — ช่วงข้อมูลย้อนหลังที่ยอมเสียได้), operational ownership และข้อจำกัดที่แก้ย้อนหลังไม่ได้

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
- [AWS KMS (Key Management Service) data protection and current HSM (Hardware Security Module) validation](https://docs.aws.amazon.com/kms/latest/developerguide/data-protection.html)
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
