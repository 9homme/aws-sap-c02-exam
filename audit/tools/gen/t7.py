from common import tfix

tfix("pro-41", {
 "A": ("Order AWS Snowball Edge Storage Optimized devices to import the 1.5 PB backlog into Amazon S3, use AWS Transfer Family for the partners' SFTP feed, and use AWS DataSync for the branch synchronization.",
       "ตกข้อ (1): Transfer Family และ DataSync ถูกต้อง แต่ AWS Snowball Edge ไม่เปิดให้ลูกค้าใหม่แล้ว สตูดิโอที่ไม่เคยใช้ Snow Family จึงสั่งอุปกรณ์ไม่ได้ในปี 2026 สำหรับ physical transfer ต้องใช้ AWS Data Transfer Terminal หรือ partner แทน"),
 "B": ("Run AWS DataSync over the satellite link with a high bandwidth limit for the 1.5 PB backlog, use AWS Transfer Family for the partners' SFTP feed, and use DataSync for the branch synchronization.",
       "ตกข้อ (1): DataSync เหมาะกับ online transfer ที่มี bandwidth พอ แต่ลิงก์ดาวเทียมแบนด์วิดท์ต่ำทำให้ 1.5 PB ใช้เวลานานเกินรับได้ตามที่โจทย์ระบุ การเพิ่ม bandwidth limit ไม่ได้เพิ่มความจุของลิงก์จริง"),
 "C": ("Take the encrypted portable drives to an AWS Data Transfer Terminal for the backlog, run an OpenSSH SFTP server on an EC2 instance in a public subnet that writes to Amazon S3 for the partners, and use AWS DataSync for the branch.",
       "ตกข้อ (2): Data Transfer Terminal และ DataSync ถูกต้อง แต่ SFTP server บน EC2 ใน public subnet คือ public SFTP host ที่ต้อง patch, ดูแล availability และความปลอดภัยเอง ซึ่งโจทย์ห้าม Transfer Family ให้ managed SFTP endpoint ที่เขียนเข้า S3 โดยตรง"),
 "D": ("Upload the encrypted portable drives at a reserved AWS Data Transfer Terminal, use AWS Transfer Family for partners’ SFTP ingress into S3, and use DataSync with transfer verification for the fast-link branch.",
       "ถูก: Data Transfer Terminal ให้ลูกค้านำอุปกรณ์จัดเก็บของตัวเองไปเชื่อมต่อเครือข่ายความเร็วสูงของ AWS เพื่ออัปโหลดเข้า S3 จึงแก้ปัญหาลิงก์ดาวเทียมสำหรับ backlog ระดับ PB Transfer Family ให้ partner ใช้ SFTP client เดิมโดยไม่มี server ให้ดูแล ส่วน DataSync ส่งเฉพาะไฟล์ที่เปลี่ยนจาก branch และตรวจความถูกต้องของข้อมูลได้"),
},
 clue="backlog 1.5 PB บนลิงก์ดาวเทียมช้า และไม่เคยใช้ Snow Family, partner ใช้ SFTP โดยห้ามดูแล SFTP host, branch ต้อง sync ไฟล์ที่เปลี่ยนพร้อม verification",
 reasoning="1) ข้อ (1): bandwidth ไม่พอสำหรับ online transfer (B) และ Snowball Edge ไม่รับลูกค้าใหม่ (A) ทางเลือก physical ที่ใช้ได้คือ Data Transfer Terminal 2) ข้อ (2): SFTP แบบ managed เข้าสู่ S3 = Transfer Family ไม่ใช่ server บน EC2 (C) 3) ข้อ (3): sync ไฟล์ที่เปลี่ยนผ่านลิงก์ที่เร็วพร้อม verification = DataSync 4) D ใช้บริการที่ตรงกับแต่ละ workflow และเปิดรับลูกค้าใหม่ทั้งหมด",
 refs=[("AWS Data Transfer Terminal technical requirements", "https://docs.aws.amazon.com/datatransferterminal/latest/userguide/tech-requirements.html"),
       ("AWS Snowball Edge availability change", "https://docs.aws.amazon.com/snowball/latest/developer-guide/snowball-edge-availability-change.html"),
       ("What is AWS Transfer Family?", "https://docs.aws.amazon.com/transfer/latest/userguide/what-is-aws-transfer-family.html")])

tfix("pro-42", {
 "A": ("Use Cost Explorer to analyze spend, AWS Budgets for threshold notifications, Compute Optimizer for resource recommendations, and then evaluate Savings Plans from a measured usage baseline.",
       "ถูก: Cost Explorer วิเคราะห์ค่าใช้จ่ายย้อนหลังและพยากรณ์แยกตาม account, service และ cost allocation tags สำหรับ chargeback AWS Budgets แจ้งเตือนทั้ง actual และ forecasted ก่อนเกินงบ Compute Optimizer ใช้ utilization metrics แนะนำการ rightsize EC2 เมื่อ rightsize แล้วจึงใช้ baseline ที่วัดได้ไปประเมิน Savings Plans เพื่อไม่ commit กับขนาดที่ใหญ่เกินจริง"),
 "B": ("Use Cost Explorer for historical and forecast analysis, create Amazon CloudWatch billing alarms on the EstimatedCharges metric in the management account, and use Compute Optimizer for EC2 rightsizing recommendations.",
       "ตกข้อ (2): billing alarm เตือนเมื่อค่าใช้จ่ายจริงสะสมเกินค่าที่ตั้งเท่านั้น ไม่มีการเตือนจาก forecast และไม่ได้แบ่งตามงบที่อนุมัติของแต่ละทีม/account ผู้จัดการจึงไม่ได้รับคำเตือนล่วงหน้าแบบที่ AWS Budgets ให้ได้"),
 "C": ("Use Cost Explorer for spend analysis and AWS Budgets for actual and forecast alerts, and immediately purchase the Savings Plans that Cost Explorer recommends based on the current On-Demand spend.",
       "ตกข้อ (3): การซื้อ commitment ทันทีจากการใช้งานปัจจุบันที่มี instance ขนาดใหญ่เกินจริง จะ lock ส่วนลดไว้กับ spend ที่ควรลดได้ และไม่มีการวิเคราะห์ utilization เพื่อ rightsize ก่อน ซึ่งโจทย์ระบุลำดับว่าต้องเข้าใจ utilization ก่อนซื้อ"),
 "D": ("Use Cost Explorer for spend analysis and AWS Budgets for actual and forecast alerts, and run a Systems Manager Automation runbook that changes every development instance to the smallest burstable instance type.",
       "ตกข้อ (3): Cost Explorer และ Budgets ถูกต้อง แต่การลดขนาดทุก instance แบบเหมารวมคือ arbitrary downgrade ที่ SRE ไม่ต้องการ อาจทำให้ workload ที่ต้องใช้ CPU/memory มีปัญหา Compute Optimizer ให้คำแนะนำจาก utilization จริงพร้อมความเสี่ยงด้านประสิทธิภาพ"),
},
 clue="วิเคราะห์ค่าใช้จ่ายย้อนหลัง/พยากรณ์สำหรับ chargeback, เตือนทั้ง actual และ forecast ต่องบ, rightsize จาก utilization ก่อนซื้อ commitment",
 reasoning="1) แต่ละ requirement มีเครื่องมือเฉพาะ: วิเคราะห์ = Cost Explorer, งบและการเตือน forecast = AWS Budgets, rightsizing = Compute Optimizer 2) B ใช้ billing alarm ที่ไม่มี forecast 3) C ซื้อ Savings Plans ก่อน rightsize ขัดลำดับในโจทย์ 4) D ลดขนาดแบบไม่มีข้อมูล 5) A เรียงขั้นตอนถูก: เข้าใจ spend → ตั้งงบ → rightsize → ประเมิน commitment",
 refs=[("Managing your costs with AWS Budgets", "https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html"),
       ("Analyzing your costs with Cost Explorer", "https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html"),
       ("What is AWS Compute Optimizer?", "https://docs.aws.amazon.com/compute-optimizer/latest/ug/what-is-compute-optimizer.html")])

tfix("pro-43", {
 "A": ("Purchase 3-year EC2 Instance Savings Plans for the instance families that the baseline uses today, run the promotion workers on Spot Instances in an Auto Scaling group with mixed instance types, and keep the database on On-Demand capacity.",
       "ตกข้อ (1): Spot สำหรับ workers และการเก็บ database บน capacity ที่เสถียรถูกต้อง แต่ EC2 Instance Savings Plans ผูกกับ instance family ใน Region และไม่ครอบคลุม Fargate เมื่อเปลี่ยน mix ปีหน้าส่วนลดจะไม่ตามไป Compute Savings Plans ยืดหยุ่นกว่า"),
 "B": ("Buy appropriate Compute Savings Plans for the predictable commitment, run fault-tolerant burst workers on EC2 Spot with Auto Scaling capacity mix, and keep critical stateful workloads on reliable capacity.",
       "ถูก: Compute Savings Plans ให้ส่วนลดกับ EC2 ทุก family/Region รวมถึง Fargate และ Lambda จึงรองรับการเปลี่ยน mix Spot ลดต้นทุน workers ที่ stateless และ retry ได้ โดย Auto Scaling ปรับจำนวนตาม demand และกระจายหลาย instance types ส่วน database ที่ต้องพร้อมใช้ตลอดอยู่บน capacity ที่ไม่ถูกเรียกคืน commitment ควรเท่ากับ baseline ไม่ใช่ peak"),
 "C": ("Buy Compute Savings Plans for the baseline and move both the promotion workers and the transaction database to Spot Instances in Auto Scaling groups with capacity rebalancing to minimize cost.",
       "ตกข้อ (2): Compute Savings Plans ถูกต้อง แต่ database ที่ต้องพร้อมใช้ต่อเนื่องไม่ควรอยู่บน Spot ซึ่งอาจถูกเรียกคืนพร้อมแจ้งล่วงหน้าเพียง 2 นาที capacity rebalancing ช่วยลดผลกระทบแต่ไม่ได้รับประกันว่า instance จะไม่ถูกเรียกคืน"),
 "D": ("Buy Compute Savings Plans sized to the peak promotional usage and keep a fixed fleet of On-Demand Instances provisioned for peak demand throughout the year so that capacity is always available.",
       "ตกข้อ (3): การ commit และ provision ตาม peak ที่เกิดไม่สม่ำเสมอทำให้จ่ายค่า capacity ที่ว่างเกือบตลอดปี และ Savings Plans ส่วนที่เกิน baseline จะไม่ถูกใช้ ขัดกับการ scale ตาม demand และข้อห้าม commit กับ peak ที่คาดเดาไม่ได้"),
},
 clue="baseline คงที่แต่จะเปลี่ยน family/Fargate, surge workers ทน interruption ได้, database ต้องพร้อมใช้ตลอด, ห้าม commit กับ peak",
 reasoning="1) แยก price commitment ออกจาก availability: commitment ใช้กับ baseline เท่านั้น 2) ข้อ (1) baseline จะเปลี่ยน family และใช้ Fargate มากขึ้น ต้องใช้ Compute Savings Plans ไม่ใช่ EC2 Instance Savings Plans (A) 3) ข้อ (2) Spot ใช้ได้กับ workers ที่ทน interruption แต่ไม่ใช่ database (C) 4) ข้อ (3) ต้อง scale ตาม demand ไม่ใช่ provision ตาม peak ทั้งปี (D) B จึงครบทุกข้อ",
 refs=[("What are Savings Plans?", "https://docs.aws.amazon.com/savingsplans/latest/userguide/what-is-savings-plans.html"),
       ("Savings Plans types", "https://docs.aws.amazon.com/savingsplans/latest/userguide/plan-types.html"),
       ("Auto Scaling groups with multiple instance types and purchase options", "https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-mixed-instances-groups.html")])

tfix("pro-44", {
 "A": ("Create a Route 53 Resolver outbound endpoint in the shared-services VPC with forwarding rules for legacy.corp.internal to the corporate DNS servers and for aws.corp.internal to the Amazon-provided DNS server, and point the corporate DNS servers at the outbound endpoint.",
       "ตกข้อ (1): outbound endpoint ส่ง query ออกจาก VPC ไปยัง DNS ภายนอกเท่านั้น ไม่ได้รับ query ที่เข้ามาจาก on premises ฝั่งสำนักงานจึงยัง resolve aws.corp.internal ไม่ได้ ต้องมี inbound endpoint สำหรับทิศทางนั้น"),
 "B": ("Create a Route 53 Resolver inbound endpoint so that the corporate DNS servers can forward aws.corp.internal queries into the VPC. Create a private hosted zone named legacy.corp.internal in AWS and copy the corporate database records into it.",
       "ตกข้อ (2): ทิศทาง on premises → AWS ถูกต้อง แต่การสร้าง zone ซ้ำใน AWS และคัดลอก records ด้วยมือทำให้ข้อมูลสองที่ไม่ตรงกันเมื่อมีการเปลี่ยน และขัดกับข้อกำหนดให้ทีมดูแล zone เดิมโดยไม่ทำสำเนา ควรใช้ outbound endpoint ที่ forward suffix นี้ไปยัง DNS ขององค์กร"),
 "C": ("Use Route 53 Resolver inbound endpoints for on-premises-to-AWS queries, outbound endpoints with forwarding rules for AWS-to-on-premises queries, and private hosted zone associations as required.",
       "ถูก: corporate DNS ตั้ง conditional forwarder สำหรับ aws.corp.internal ไปยัง IP ของ inbound endpoint ที่กระจายหลาย AZ ส่วน VPC resolver ใช้ forwarding rule เฉพาะ legacy.corp.internal ผ่าน outbound endpoint ไปยัง DNS ขององค์กร private hosted zone ต้อง associate กับ VPC ของ endpoint ทุก query วิ่งผ่าน Direct Connect ที่ redundant และ zone ทั้งสองยังเป็น private"),
 "D": ("Publish aws.corp.internal as a Route 53 public hosted zone that contains the private IP addresses of the API endpoints, and create a Resolver outbound endpoint with a forwarding rule for legacy.corp.internal to the corporate DNS servers.",
       "ตกข้อ (3): ทิศทาง AWS → on premises ถูกต้อง แต่การเผยแพร่ aws.corp.internal ใน public hosted zone เปิดเผยชื่อและ IP ภายในต่อสาธารณะ ซึ่ง security ห้ามโดยตรง แม้ IP จะเป็น private ก็ตาม"),
},
 clue="DNS สองทิศทาง: on premises → private hosted zone และ VPC → legacy.corp.internal, ห้ามใช้ public DNS, ไม่ทำสำเนา records",
 reasoning="1) แยกทิศทางของ query: เข้ามาใน AWS = inbound endpoint, ออกจาก AWS = outbound endpoint + forwarding rule 2) A มีแต่ outbound จึงตอบเพียงทิศเดียว 3) B แก้ทิศ AWS → on premises ด้วยการคัดลอก records ซึ่งโจทย์ห้าม 4) D ใช้ public hosted zone ซึ่งขัดข้อ (3) 5) C ใช้ endpoint สองทิศทาง forward เฉพาะ suffix ที่จำเป็น และคงความเป็น private ของทั้งสอง zone",
 refs=[("Resolving DNS queries between VPCs and your network", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resolver-overview-DSN-queries-to-vpc.html"),
       ("Forwarding outbound DNS queries to your network", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resolver-forwarding-outbound-queries.html")])

tfix("pro-45", {
 "A": ("Add NAT gateways and a default route for all private subnets, and let the applications reach the AWS APIs through their public endpoints and the vendor through its public internet endpoint.",
       "ตกข้อ (1): NAT ทำให้ workload ใน private subnet เรียกออกได้โดยไม่รับ inbound แต่ traffic ไปยัง AWS APIs และ vendor จะวิ่งผ่าน internet ซึ่ง compliance ห้ามสำหรับการเชื่อมต่อเหล่านี้ และยังให้ทุก workload ออก internet ได้ทั่วไป"),
 "B": ("Create interface and gateway VPC endpoints for the required AWS services and an interface endpoint for the vendor's PrivateLink service, and move the package-download batch jobs to public subnets with public IP addresses.",
       "ตกข้อ (2)(3): endpoints สำหรับ AWS services และ vendor ถูกต้อง แต่การย้าย batch jobs ไป public subnet พร้อม public IP ทำให้เครื่องเหล่านั้นมี internet reachability ซึ่งโจทย์ห้ามย้าย server ไป public subnet เพื่อแก้ connectivity ควรใช้ NAT gateway เป็นทางออกที่ควบคุมได้"),
 "C": ("Create interface and gateway VPC endpoints for the required AWS services and an interface endpoint for the vendor's PrivateLink service, and add a NAT gateway default route to every private subnet route table.",
       "ตกข้อ (3): endpoints ถูกต้อง แต่การเพิ่ม default route ไป NAT ให้ทุก private subnet เปิด outbound internet ให้ทุก workload ไม่ใช่เฉพาะ package-download jobs ที่ได้รับอนุมัติ ควรแยก subnet/route table ของ batch jobs และให้เฉพาะ route table นั้นมี route ไป NAT"),
 "D": ("Create suitable VPC interface or gateway endpoints for supported AWS services, a PrivateLink interface endpoint for the vendor, and controlled NAT egress only for the separate package-download traffic.",
       "ถูก: interface endpoints (PrivateLink) และ gateway endpoints สำหรับ S3/DynamoDB ทำให้ traffic ไปยัง AWS APIs ไม่ผ่าน internet interface endpoint ของ vendor เปิดทางเดียวเข้าสู่ endpoint service ส่วน NAT gateway ใช้เฉพาะ route table ของ subnet ที่ batch jobs อยู่ ทุก workload ยังอยู่ใน private subnet จึงไม่รับ inbound จาก internet ที่ไม่ได้ร้องขอ"),
},
 clue="AWS APIs และ vendor ต้องไม่ผ่าน internet, workload ทั้งหมดอยู่ private, outbound internet เฉพาะ batch jobs ที่อนุมัติ",
 reasoning="1) แยก private access ออกจาก internet egress: VPC endpoints/PrivateLink เข้าถึงบริการโดยไม่ผ่าน internet ส่วน NAT เป็นทางออก internet 2) A ใช้ NAT สำหรับทุกอย่าง จึงขัดข้อ (1) 3) B ย้ายเครื่องไป public subnet ขัดข้อ (2) 4) C ให้ทุก subnet ออก internet ได้ ขัดข้อ (3) 5) D ใช้ endpoints สำหรับ AWS/vendor และจำกัด NAT เฉพาะ subnet ของ batch jobs",
 refs=[("What is AWS PrivateLink?", "https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html"),
       ("Gateway endpoints", "https://docs.aws.amazon.com/vpc/latest/privatelink/gateway-endpoints.html"),
       ("NAT gateways", "https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html")])

tfix("pro-46", {
 "A": ("Use AWS Backup policies with Organizations, approved cross-account backup copies and vault lock where appropriate, and configure KMS permissions and tested restore workflows.",
       "ถูก: backup policies ใน Organizations กำหนดแผนสำรองให้ทุกบัญชีจากส่วนกลาง copy rule ส่ง recovery points ไปยัง vault ในบัญชี security ที่แยกออกจาก workload และ Vault Lock แบบ compliance mode ป้องกันการลบก่อนครบ retention แม้แต่ root ต้องใช้ customer managed KMS key ที่ key policy อนุญาตบัญชีปลายทาง และใช้ AWS Backup restore testing เพื่อพิสูจน์ว่ากู้คืนได้จริง"),
 "B": ("Use AWS Backup policies with Organizations to create backup plans in every account, store the recovery points in a vault in each workload account, and attach vault access policies that deny deletion to everyone except the account's backup administrators.",
       "ตกข้อ (2): แผนสำรองรวมศูนย์ถูกต้อง แต่สำเนาทั้งหมดยังอยู่ในบัญชี workload หากบัญชีถูกยึดสิทธิ์ ผู้โจมตีที่ได้สิทธิ์ admin สามารถแก้ vault access policy แล้วลบได้ ไม่มีสำเนาแยกในบัญชีที่ security ควบคุมและไม่มี Vault Lock ที่ล็อกถาวร"),
 "C": ("Use AWS Backup policies with Organizations and copy recovery points to a vault with AWS Backup Vault Lock in compliance mode in the security account. Encrypt the source resources with the AWS managed keys and rely on successful backup job status as proof of recoverability.",
       "ตกข้อ (3): การแยกบัญชีและ Vault Lock ถูกต้อง แต่ snapshot ที่เข้ารหัสด้วย AWS managed key แชร์หรือ copy ข้ามบัญชีไม่ได้สำหรับหลายประเภท resource จึงต้องใช้ customer managed key และสถานะ backup job สำเร็จไม่ได้พิสูจน์ว่าแอปกู้คืนได้ ต้องมี restore testing"),
 "D": ("Deploy an AWS Lambda function in each account that creates EBS and database snapshots on a schedule, exports them to an Amazon S3 bucket with S3 Object Lock in a security account, and records each run in a spreadsheet.",
       "ตกข้อ (1): Object Lock ช่วยเรื่องการลบ แต่ script ในทุกบัญชีไม่ใช่แผนสำรองที่บริหารจากส่วนกลาง ต้องเขียนรองรับแต่ละ engine เอง และหลาย resource ไม่สามารถ export snapshot ไป S3 เป็นรูปแบบที่กู้คืนได้ตรง ๆ AWS Backup รองรับประเภท resource เหล่านี้แบบ native"),
},
 clue="แผนสำรองรวมศูนย์ทุกบัญชี, สำเนาแยกบัญชีที่ลบก่อนกำหนดไม่ได้, สิทธิ์ KMS ข้ามบัญชี และทดสอบการกู้คืนจริง",
 reasoning="1) ข้อ (1) ต้องใช้ AWS Backup policies ผ่าน Organizations ไม่ใช่ script รายบัญชี (D) 2) ข้อ (2) ต้องมีสำเนาในบัญชีที่แยกและล็อกด้วย Vault Lock ไม่ใช่เพียง access policy ในบัญชีเดิม (B) 3) ข้อ (3) การ copy ข้ามบัญชีต้องใช้ customer managed KMS key และต้องทดสอบ restore ไม่ใช่ดูแค่ job status (C) 4) A ครบทั้งสามข้อ",
 refs=[("AWS Backup Vault Lock", "https://docs.aws.amazon.com/aws-backup/latest/devguide/vault-lock.html"),
       ("Creating backup copies across AWS accounts", "https://docs.aws.amazon.com/aws-backup/latest/devguide/create-cross-account-backup.html"),
       ("Restore testing", "https://docs.aws.amazon.com/aws-backup/latest/devguide/restore-testing.html")])

tfix("pro-47", {
 "A": ("Deploy both the brochure website and the production application to AWS Elastic Beanstalk environments with Application Load Balancers and EC2 Auto Scaling across multiple Availability Zones.",
       "ตกข้อ (1): ฝั่ง production ถูกต้อง แต่ brochure site ที่ traffic ต่ำและต้องการงบรายเดือนคงที่ไม่จำเป็นต้องมี load balancer และ Auto Scaling หลาย AZ ทำให้ค่าใช้จ่ายและสิ่งที่ต้องดูแลมากเกินจำเป็น ซึ่งเจ้าของไม่ต้องการ over-engineer"),
 "B": ("Use Lightsail for the small brochure deployment and Elastic Beanstalk with ALB and EC2 Auto Scaling capabilities for the dynamic production application.",
       "ถูก: Lightsail ให้ instance พร้อม storage และ data transfer ในราคารายเดือนคงที่และจัดการง่าย เหมาะกับเว็บเล็กที่ traffic คาดเดาได้ ส่วน Elastic Beanstalk จัดการ ALB, Auto Scaling group หลาย AZ, rolling deployments, environment configuration และ health-based replacement ให้ โดยทีมดูแลแค่ application code"),
 "C": ("Host the brochure website on a Lightsail instance, and run the production application on several Lightsail instances behind a Lightsail load balancer, adding instances manually during traffic spikes.",
       "ตกข้อ (2): Lightsail เหมาะกับ brochure site แต่สำหรับ production ที่ traffic ผันผวน Lightsail ไม่มี automated scaling และ managed rolling deployment แบบ Elastic Beanstalk การเพิ่ม instance ด้วยมือทำให้รับ spike ไม่ทันและเสี่ยงต่อ availability"),
 "D": ("Host the brochure website on Lightsail, and run the production application on an EC2 Auto Scaling group behind an ALB, deploying new versions with custom Systems Manager Run Command scripts that update instances in batches.",
       "ตกข้อ (3): Lightsail และ ASG + ALB ถูกต้อง แต่ script deploy แบบ batch ที่เขียนเอง คือ custom deployment framework ที่ agency ไม่ต้องการ ต้องจัดการ rollback, health check ระหว่าง deploy และ configuration เอง ขณะที่ Elastic Beanstalk มี rolling deployment ให้แล้ว"),
},
 clue="brochure site ต้องการราคาคงที่และดูแลน้อย, production ต้องการ managed deployment + autoscaling หลาย AZ, ห้าม custom orchestration",
 reasoning="1) เลือกตามขนาดและความต้องการของแต่ละ workload ไม่ใช้บริการเดียวกับทุกอย่าง 2) brochure: Lightsail ราคาคงที่และง่าย ตัด A ที่ over-engineer 3) production: ต้องมี autoscaling และ managed deployment ตัด Lightsail (C) และ custom scripts (D) 4) B จับคู่ Lightsail กับงานเล็ก และ Elastic Beanstalk กับงาน production",
 refs=[("What is Amazon Lightsail?", "https://docs.aws.amazon.com/lightsail/latest/userguide/what-is-amazon-lightsail.html"),
       ("Elastic Beanstalk deployment policies", "https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features.rolling-version-deploy.html"),
       ("Auto Scaling group for your Elastic Beanstalk environment", "https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features.managing.as.html")])

tfix("pro-48", {
 "A": ("Deploy Amazon FSx for Windows File Server and join it to the on-premises domain through an AD Connector directory in the VPC, and give factory clients access to the FSx share over the private connection.",
       "ตกข้อ (2): AD Connector เป็น proxy สำหรับบริการที่รองรับ เช่น WorkSpaces แต่ FSx for Windows File Server ไม่รองรับการ join ผ่าน AD Connector ต้อง join กับ AWS Managed Microsoft AD (ใช้ forest trust กับ AD เดิมได้) หรือกับ self-managed AD โดยตรง จึงไม่ใช่ directory topology ที่ใช้ได้"),
 "B": ("Deploy Amazon FSx for Windows File Server joined to AWS Managed Microsoft AD with a forest trust, and deploy an Amazon FSx File Gateway at each factory to cache the FSx shares locally for latency-sensitive clients.",
       "ตกข้อ (3): FSx และ forest trust ถูกต้อง แต่ Amazon FSx File Gateway ไม่เปิดให้ลูกค้าใหม่แล้ว จึงวางแผนใช้เป็น local cache สำหรับโรงงานไม่ได้ โจทย์เตือนให้ไม่สมมติว่ามี gateway cache สำหรับ FSx share ต้องคง local SMB service ไว้ชั่วคราวและวางแผน sync/cutover"),
 "C": ("Use FSx for Windows File Server with a supported Active Directory trust or self-managed AD integration; connect suitable on-prem SMB clients privately and keep a local SMB service temporarily for latency-critical factory workloads until an explicit synchronization and cutover plan is ready.",
       "ถูก: FSx for Windows File Server เป็น managed SMB ที่รองรับ NTFS ACLs, file locking และ Multi-AZ โดยไม่ต้องดูแล failover cluster เอง join กับ AWS Managed Microsoft AD ที่มี forest trust กับ AD เดิม หรือ join กับ self-managed AD โดยตรง จึงใช้ identities เดิมได้ client ที่รับ latency ได้เข้าผ่านเครือข่าย private ส่วนโรงงานที่ไวต่อ latency ใช้ file server ในพื้นที่ต่อไปจนพร้อม sync ด้วย DataSync และ cutover"),
 "D": ("Build a Windows Server failover cluster with Storage Spaces Direct on EC2 instances across two Availability Zones, join it to the on-premises domain over the private connection, and keep a local SMB server at each factory during the transition.",
       "ตกข้อ (1): ได้ SMB, ACL และ AD integration ครบ แต่ IT ต้องดูแล Windows failover cluster, storage และ patch เอง ซึ่งโจทย์ระบุว่าไม่ต้องการ FSx for Windows File Server ให้ความสามารถเดียวกันแบบ managed"),
},
 clue="managed SMB ที่คง ACL/file locking, ใช้ AD identities เดิมผ่าน topology ที่รองรับ, โรงงานไวต่อ latency โดยห้ามสมมติว่ามี gateway cache สำหรับ FSx",
 reasoning="1) ข้อ (1) ต้องการ managed SMB ตัด failover cluster บน EC2 (D) 2) ข้อ (2) FSx join ได้กับ AWS Managed Microsoft AD (ผ่าน trust) หรือ self-managed AD ไม่ใช่ AD Connector (A) 3) ข้อ (3) FSx File Gateway ไม่เปิดให้ลูกค้าใหม่แล้ว จึงไม่ควรวางแผนพึ่งพา (B) 4) C ใช้ FSx กับ directory topology ที่รองรับ และวางแผน phased cutover สำหรับโรงงานอย่างชัดเจน",
 refs=[("What is FSx for Windows File Server?", "https://docs.aws.amazon.com/fsx/latest/WindowsGuide/what-is.html"),
       ("Using Microsoft Active Directory with FSx for Windows File Server", "https://docs.aws.amazon.com/fsx/latest/WindowsGuide/aws-ad-integration-fsxW.html"),
       ("Amazon FSx File Gateway availability change", "https://docs.aws.amazon.com/filegateway/latest/filefsxw/what-is-file-fsxw.html")])
