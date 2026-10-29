from common import tfix

tfix("pro-36", {
 "A": ("Use AWS KMS customer managed keys for S3 and RDS encryption, create KMS asymmetric signing keys for the signing application, use AWS Secrets Manager rotation for database passwords, and store configuration in Systems Manager Parameter Store.",
       "ตกข้อ (2): KMS รองรับ asymmetric signing ได้จริง แต่ HSM ของ KMS เป็นแบบ multi-tenant ที่ AWS จัดการ ไม่ใช่ dedicated HSM ภายใต้การควบคุมของลูกค้าตามสัญญา และ KMS ไม่มี PKCS#11 interface ที่แอป signing ใช้ ส่วนอื่นของตัวเลือกถูกต้อง"),
 "B": ("Use AWS KMS for S3 and RDS encryption and AWS CloudHSM for the signing application. Store database passwords as Systems Manager Parameter Store SecureString parameters and have each application team update them on a schedule.",
       "ตกข้อ (3): KMS และ CloudHSM ถูกที่แล้ว แต่ Parameter Store ไม่มี managed rotation สำหรับรหัสผ่าน database ทีมแอปต้องเขียนและตั้งเวลาการเปลี่ยนรหัสเอง ซึ่งโจทย์ห้าม Secrets Manager มี managed rotation สำหรับ RDS และ engines ที่รองรับ"),
 "C": ("Use AWS KMS for integrated service encryption, CloudHSM for the specialized HSM signing requirement, Secrets Manager for rotation, and Systems Manager Parameter Store for ordinary configuration.",
       "ถูก: KMS ผสานกับ S3/RDS แบบ envelope encryption และคุมด้วย key policy ที่ audit ได้ผ่าน CloudTrail CloudHSM ให้ HSM แบบ single-tenant ที่ลูกค้าคุม crypto users และรองรับ PKCS#11 Secrets Manager หมุนรหัสผ่าน database อัตโนมัติ (รวมถึง managed rotation ของ RDS) ส่วน Parameter Store เก็บ configuration ที่ไม่เป็นความลับได้ในราคาต่ำ"),
 "D": ("Create an AWS KMS custom key store backed by an AWS CloudHSM cluster and use its KMS keys for the signing application and the S3 and RDS data. Store all database passwords and configuration flags in AWS Secrets Manager with rotation enabled.",
       "ตกข้อ (2)(3): custom key store รองรับเฉพาะ symmetric encryption KMS keys และแอปยังเรียกผ่าน KMS API ไม่ใช่ PKCS#11 จึงไม่ตอบงาน signing ส่วนการเก็บ configuration ที่ไม่เป็นความลับหลายร้อยรายการใน Secrets Manager เพิ่มค่าใช้จ่ายรายความลับโดยไม่จำเป็น Parameter Store เหมาะกว่า"),
},
 clue="encryption ที่ผสานกับบริการ AWS, dedicated HSM + PKCS#11 สำหรับ signing, หมุนรหัส database อัตโนมัติ, config ทั่วไปใน parameter store",
 reasoning="1) แยกตามชนิดงาน: service encryption = KMS, dedicated HSM/PKCS#11 = CloudHSM, credential rotation = Secrets Manager, config ธรรมดา = Parameter Store 2) KMS asymmetric keys (A) และ custom key store (D) ไม่ใช่ dedicated HSM ที่เรียกด้วย PKCS#11 3) Parameter Store ไม่มี managed rotation (B) 4) C ใช้แต่ละบริการตรงหน้าที่ ไม่ได้ใช้เครื่องมือเดียวแทนทุกอย่างตามที่ security board เตือน",
 refs=[("AWS KMS concepts", "https://docs.aws.amazon.com/kms/latest/developerguide/overview.html"),
       ("What is AWS CloudHSM?", "https://docs.aws.amazon.com/cloudhsm/latest/userguide/introduction.html"),
       ("Rotate AWS Secrets Manager secrets", "https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets.html"),
       ("AWS KMS custom key stores", "https://docs.aws.amazon.com/kms/latest/developerguide/key-store-overview.html")])

tfix("pro-37", {
 "A": ("Use CloudFront with ACM certificates in front of the static content and the ALB, and subscribe to AWS Shield Advanced for the distribution and the ALB without creating AWS WAF web ACLs.",
       "ตกข้อ (2): Shield Advanced ช่วยรับมือ DDoS ระดับ network/transport และให้ทีม Shield Response แต่การบล็อก pattern อันตรายและการจำกัดอัตรา client ระดับ HTTP ต้องใช้ AWS WAF web ACL และ rate-based rules การ mitigate layer 7 อัตโนมัติของ Shield Advanced ก็ทำงานผ่าน web ACL ที่ผูกไว้เช่นกัน"),
 "B": ("Use the ALB as the only public entry point with an ACM certificate, attach an AWS WAF web ACL with managed rules and rate-based rules to the ALB, and subscribe the ALB to AWS Shield Advanced.",
       "ตกข้อ (1)(3): WAF และ Shield Advanced ป้องกันได้ แต่ไม่มี edge caching รูปภาพ static ทุก request จึงวิ่งถึง ALB และ origin ทำให้ load ช่วงข่าวใหญ่สูงขึ้น และไม่ได้ประโยชน์จากการกระจายรับ traffic ที่ edge ของ CloudFront"),
 "C": ("Use CloudFront with ACM certificates and attach an AWS WAF web ACL with managed rules and rate-based rules. Apply the CachingDisabled cache policy to all paths so that every request is evaluated by the origin.",
       "ตกข้อ (3): WAF และ CloudFront ถูกต้อง แต่การปิด cache ทุก path ทำให้ static images ทุก request ต้องไปถึง origin ซึ่งโจทย์ห้าม ควรใช้ cache behavior แยก: cache static content และส่ง /api ไปยัง ALB ด้วย policy ที่ไม่ cache"),
 "D": ("Use CloudFront with ACM certificates, attach AWS WAF web ACLs and appropriate rate-based rules, and assess AWS Shield Advanced for its additional DDoS protections and response capabilities.",
       "ถูก: CloudFront cache รูปภาพที่ edge และส่ง API ไปยัง ALB ผ่าน cache behavior แยก ACM ต่ออายุ certificate อัตโนมัติ (สำหรับ CloudFront ต้องอยู่ใน us-east-1) WAF บล็อก pattern อันตรายและจำกัดอัตราด้วย rate-based rules Shield Standard คุ้มครอง layer 3/4 อยู่แล้ว ส่วน Shield Advanced เพิ่ม visibility, การตอบสนองจาก SRT และ cost protection ซึ่งคุ้มเมื่อ availability ช่วงข่าวใหญ่สำคัญ"),
},
 clue="cache static ที่ edge + ACM, กรอง HTTP flood ด้วย rules/rate limit, DDoS ระดับ network แยกจาก WAF, ไม่ส่ง asset ที่ cache ได้ไป origin",
 reasoning="1) แยกชั้น: CloudFront = edge cache และจุดรับ traffic, WAF = กรองระดับ HTTP, Shield = DDoS ระดับ network และบริการเสริม 2) A ไม่มี WAF จึงไม่กรอง layer 7 3) B ไม่มี CloudFront จึงไม่ cache 4) C ปิด cache ทั้งหมด 5) D ใช้ทั้งสามชั้นถูกต้องและแยก cache behavior สำหรับ static/API",
 refs=[("AWS WAF, AWS Shield and Firewall Manager", "https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html"),
       ("Rate-based rule statement", "https://docs.aws.amazon.com/waf/latest/developerguide/waf-rule-statement-type-rate-based.html"),
       ("AWS Shield Advanced overview", "https://docs.aws.amazon.com/waf/latest/developerguide/ddos-advanced-summary.html")])

tfix("pro-38", {
 "A": ("Use GuardDuty for threat detection, Inspector for vulnerability assessments, Macie for sensitive S3 data discovery, IAM Access Analyzer for access exposure, and Security Hub for centralized findings.",
       "ถูก: GuardDuty วิเคราะห์ CloudTrail, VPC Flow Logs และ DNS logs หาพฤติกรรมผิดปกติ เช่น credentials ถูกขโมย Inspector สแกน CVE ของ EC2, container images และ Lambda Macie ค้นหาข้อมูลส่วนบุคคลใน S3 Access Analyzer หา resource policy ที่เปิดให้ภายนอกเข้าถึง และ Security Hub รวม findings ทุกบัญชี/Region เพื่อจัดลำดับความสำคัญ การตรวจพบยังต้องมีขั้นตอนแก้สิทธิ์แยกต่างหาก"),
 "B": ("Use GuardDuty, including its Malware Protection feature, to detect both suspicious activity and package vulnerabilities on EC2. Use Macie for sensitive S3 data, IAM Access Analyzer for external access, and Security Hub to aggregate findings.",
       "ตกข้อ (1): GuardDuty Malware Protection สแกนหา malware บน EBS volume เมื่อพบ finding ที่น่าสงสัย ไม่ใช่การประเมินช่องโหว่ของ packages ตาม CVE การใช้ GuardDuty แทน Inspector จึงทำให้ทีม vulnerability ไม่ได้ข้อมูลที่ต้องการ และขัดกับโจทย์ที่ให้แยกสองประเภทนี้"),
 "C": ("Use GuardDuty for threat detection, Inspector for vulnerability assessments, Macie for sensitive S3 data, and Security Hub to aggregate findings and automatically revoke any external access that its controls detect.",
       "ตกข้อ (2): ขาด IAM Access Analyzer ที่วิเคราะห์ resource policies หลายชนิดเพื่อหาการเข้าถึงจากภายนอก และ Security Hub เป็นที่รวมและจัดลำดับ findings ไม่ได้เพิกถอนสิทธิ์ให้เองโดยอัตโนมัติ ซึ่งโจทย์เตือนไว้ว่าการตรวจพบไม่เท่ากับการแก้สิทธิ์"),
 "D": ("Enable GuardDuty, Inspector, Macie, and IAM Access Analyzer in every account, and have each service publish its findings to a separate Amazon SNS topic in each account that emails the account owners.",
       "ตกข้อ (3): detectors ครบทุกตัว แต่ findings กระจายอยู่ในแต่ละบัญชีและส่งเป็นอีเมล ไม่มีที่รวมเพื่อ triage ระดับองค์กร ไม่มีรูปแบบ finding กลางและการจัดลำดับความสำคัญข้ามบัญชี/Region ซึ่ง Security Hub ทำให้ได้"),
},
 clue="แยก threat detection กับ vulnerability, หา sensitive data ใน S3 และ resource policy ที่เปิดออกนอก, รวม findings ระดับองค์กร",
 reasoning="1) แต่ละบริการตรวจคนละชนิด: GuardDuty = threats/compromised credentials, Inspector = CVE, Macie = sensitive data, Access Analyzer = external access, Security Hub = aggregation 2) B ใช้ GuardDuty แทน Inspector 3) C ขาด Access Analyzer และเข้าใจผิดว่า Security Hub เพิกถอนสิทธิ์เอง 4) D ไม่มีที่รวม findings 5) A จับคู่บริการกับงานครบ",
 refs=[("What is AWS Security Hub CSPM?", "https://docs.aws.amazon.com/securityhub/latest/userguide/what-is-securityhub.html"),
       ("What is Amazon GuardDuty?", "https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html"),
       ("What is Amazon Inspector?", "https://docs.aws.amazon.com/inspector/latest/user/what-is-inspector.html"),
       ("What is Amazon Macie?", "https://docs.aws.amazon.com/macie/latest/user/what-is-macie.html")])

tfix("pro-39", {
 "A": ("Enable an organization CloudTrail trail, AWS Config recording, and CloudWatch metrics and alarms. Configure VPC Traffic Mirroring from every instance to a packet-capture appliance for network investigations.",
       "ตกข้อ (3) ด้านความเหมาะสม: สามส่วนแรกถูกต้อง แต่ Traffic Mirroring คัดลอก packet ทั้งหมดรวม payload ไปยัง appliance ซึ่งต้องดูแลเครื่องและพื้นที่เก็บ และมีค่าใช้จ่ายสูง โจทย์ต้องการเพียง metadata ของ flow ที่ accept/reject ซึ่ง VPC Flow Logs ให้ได้ตรงกว่า"),
 "B": ("Enable organization CloudTrail events, AWS Config history, CloudWatch metrics/alarms, and VPC Flow Logs delivered to controlled log destinations.",
       "ถูก: CloudTrail บอกว่าใครเรียก API อะไรเมื่อไร Config เก็บ configuration items ของ security group ทั้งเดือนเพื่อแสดงสถานะก่อน/หลัง CloudWatch เก็บ metric latency และแจ้งเตือนด้วย alarms VPC Flow Logs บันทึก metadata ของ flow (IP, port, ACCEPT/REJECT) โดยไม่เก็บ payload ทั้งหมดส่งไป log archive ที่คุมสิทธิ์และ retention"),
 "C": ("Enable an organization CloudTrail trail and use CloudTrail event history to reconstruct both API callers and the full security group configuration history. Use CloudWatch metrics and alarms, and enable VPC Flow Logs.",
       "ตกข้อ (1): CloudTrail ให้ข้อมูลผู้เรียกและ parameter ของ API แต่ไม่ได้เก็บ configuration state ของ resource ในแต่ละช่วงเวลา การประกอบสถานะย้อนหลังจาก API calls ทำได้ยากและเสี่ยงตกหล่น regulator ต้องการ configuration history ซึ่งเป็นหน้าที่ของ AWS Config"),
 "D": ("Enable AWS Config recording to show both the configuration history and the IAM principal that made each change, use CloudWatch metrics and alarms, and enable VPC Flow Logs.",
       "ตกข้อ (1): Config บันทึกการเปลี่ยนแปลงของ configuration แต่ไม่ใช่แหล่งข้อมูลหลักว่าใครเรียก API ข้อมูลผู้เรียกมาจาก CloudTrail ซึ่ง Config อ้างถึงได้เมื่อ CloudTrail เปิดอยู่ หากไม่เปิด organization trail จึงตอบคำถามว่าใครเปลี่ยน security group ไม่ได้"),
},
 clue="คำถาม 4 ประเภท: ใครเปลี่ยน API, configuration เปลี่ยนอย่างไรทั้งเดือน, latency ของแอป, metadata ของ network flow",
 reasoning="1) จับคู่หลักฐานกับแหล่งข้อมูล: ผู้เรียก API = CloudTrail, configuration history = AWS Config, metrics/alarms = CloudWatch, flow metadata = VPC Flow Logs 2) C ใช้ CloudTrail แทน Config และ D ใช้ Config แทน CloudTrail ซึ่งแต่ละตัวให้ข้อมูลคนละมุม 3) A ใช้ packet capture ซึ่งเกินความต้องการและหนักกว่า Flow Logs 4) B ใช้แหล่งข้อมูลถูกต้องครบทุกประเภท",
 refs=[("What is AWS CloudTrail?", "https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html"),
       ("How AWS Config works", "https://docs.aws.amazon.com/config/latest/developerguide/how-does-config-work.html"),
       ("Logging IP traffic using VPC Flow Logs", "https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html")])

tfix("pro-40", {
 "A": ("Install AWS Application Discovery Service agents on the servers, track the portfolio in AWS Migration Hub, and use AWS Transform MGN to replicate and cut over the servers to EC2.",
       "ตกข้อ (1)(2): สถาปัตยกรรมนี้ใช้ได้กับลูกค้าเดิม แต่ AWS Migration Hub และ AWS Application Discovery Service ไม่เปิดให้ลูกค้าใหม่แล้ว บริษัทที่ไม่เคยใช้จึงเริ่มใช้ไม่ได้ในปี 2026 AWS แนะนำ AWS Transform สำหรับ discovery และการวางแผนแทน"),
 "B": ("Use AWS Transform for server discovery, dependency analysis, and migration wave planning, and then rehost each virtual machine by exporting its disk images and importing them with VM Import/Export.",
       "ตกข้อ (3): discovery และ wave planning ถูกต้อง แต่ VM Import/Export เป็นการแปลง image ครั้งเดียว ไม่มี continuous block-level replication หรือ test/cutover workflow ทุกการเปลี่ยนแปลงหลังการ export จะหายและต้องหยุดเครื่องนาน สำหรับ 450 VMs จึงเพิ่มงานและ downtime"),
 "C": ("Use AWS Transform for server discovery, dependency analysis, migration wave planning and progress visibility; use its supported server migration workflow backed by AWS Transform MGN for replication-based EC2 rehosting and test cutovers.",
       "ถูก: AWS Transform รวบรวม inventory และ dependency เพื่อจัด migration waves และติดตามความคืบหน้า แล้วใช้ AWS Transform MGN (เดิมชื่อ AWS Application Migration Service) ทำ continuous block-level replication ไป EC2 พร้อม launch test instances ก่อน cutover จริง แอปจึงไม่ต้องเปลี่ยนก่อนหมดสัญญาเช่า และ modernization ทำต่อภายหลังได้"),
 "D": ("Use AWS Transform for discovery and wave planning, replicate the servers with AWS Elastic Disaster Recovery, launch recovery instances in AWS as the cutover, and track each wave in a shared spreadsheet.",
       "ตกข้อ (2)(3) ด้านความเหมาะสม: DRS ทำ block-level replication ได้จริงแต่ออกแบบสำหรับ disaster recovery และ failback ไม่ใช่ migration workflow ที่มีสถานะ test/cutover สำหรับ waves และการติดตามด้วย spreadsheet ไม่ใช่ portfolio view รวมศูนย์ตามที่ทีมต้องการ"),
},
 clue="ลูกค้าใหม่ในปี 2026, ต้องการ discovery + dependency + wave planning + progress view, rehost 450 VMs ด้วย replication และ test cutover",
 reasoning="1) ตรวจ availability ก่อน: Migration Hub และ Application Discovery Service ไม่เปิดรับลูกค้าใหม่ ตัด A 2) ข้อ (1)(2) ใช้ AWS Transform ที่ทำ discovery, wave planning และติดตามความคืบหน้า 3) ข้อ (3) ต้องการ continuous replication และ test cutover = AWS Transform MGN ไม่ใช่ VM Import/Export (B) หรือ DRS + spreadsheet (D) 4) C จึงครบทุกข้อ",
 refs=[("AWS Transform for VMware", "https://docs.aws.amazon.com/transform/latest/userguide/vmware-jobs.html"),
       ("AWS Migration Hub availability change", "https://docs.aws.amazon.com/migrationhub/latest/ug/migrationhub-availability-change.html"),
       ("AWS Application Discovery Service availability change", "https://docs.aws.amazon.com/application-discovery/latest/userguide/application-discovery-service-availability-change.html"),
       ("Application Migration Service workflow", "https://docs.aws.amazon.com/mgn/latest/ug/what-is-mgn.html")])
