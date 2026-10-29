from common import tfix

tfix("pro-11", {
 "A": ("Use a scheduled script that calls the AWS Organizations CreateAccount API and moves each new account into the right OU. Deploy an organization CloudTrail trail and AWS Config rules to all accounts with service-managed CloudFormation StackSets, attach SCPs to the OUs, and federate IAM Identity Center with the workforce identity provider.",
       "ตกข้อ (2) และข้อจำกัดของทีม: StackSets, SCP และ Identity Center ทำงานได้จริง แต่การสร้างบัญชีและจัดเข้า OU ด้วย script เองคือ custom account vending ที่ทีม 4 คนต้องดูแล และไม่มี enrollment process ที่ตรวจสอบได้ว่าบัญชีได้ baseline ครบตามข้อ (1)"),
 "B": ("Deploy AWS Control Tower with an Organizations landing zone and Account Factory, enroll eligible existing accounts, configure its guardrails and organization logging, and integrate IAM Identity Center with the workforce identity source.",
       "ถูก: Control Tower ให้ landing zone, Account Factory สร้างบัญชีเข้า OU ที่อนุมัติพร้อม baseline และ enroll บัญชีเดิมได้ controls แบบ preventive/detective บังคับใช้ตาม OU และมี organization trail กับ Config ให้ audit ส่วน Identity Center เชื่อม IdP เดิมเพื่อมอบสิทธิ์ตามบัญชีและ job function ต้องตรวจว่าบัญชีเดิมพร้อม enroll เช่น ไม่มี Config recorder ที่ขัดกัน"),
 "C": ("Deploy AWS Control Tower with Account Factory and enroll existing accounts. Use Account Factory Customization to create IAM users with console passwords for each employee in every account that the employee needs.",
       "ตกข้อ (3): ข้อ (1) และ (2) ผ่านเพราะใช้ Control Tower แต่การสร้าง IAM user ต่อพนักงานในทุกบัญชีเป็นการสร้าง identity ซ้ำแทนการ federate จาก workforce IdP ทำให้มี credentials ถาวรจำนวนมาก และยากต่อการถอนสิทธิ์เมื่อพนักงานย้ายงานหรือลาออก"),
 "D": ("Deploy AWS Control Tower with Account Factory for all new accounts and integrate IAM Identity Center with the workforce identity provider. Leave the accounts from earlier acquisitions outside Control Tower and govern them with separately maintained SCPs and per-account trails.",
       "ตกข้อ (1): บัญชีใหม่ได้ governance ครบ แต่โจทย์กำหนดให้ทั้งบัญชีใหม่และบัญชีเดิมรับ controls ส่วนกลางผ่าน enrollment ที่ตรวจสอบได้ การปล่อยบัญชีจากการควบรวมเดิมไว้ข้างนอกทำให้ต้องดูแลสองมาตรฐานและ trail รายบัญชีที่ทีมโปรดักต์อาจปิดได้"),
},
 clue="บัญชีใหม่ 300 บัญชีและบัญชีเดิม ต้องได้ controls + OU + baseline อัตโนมัติ, ห้ามทำ account-vending เอง, ผู้ใช้ federate จาก IdP เดิม",
 reasoning="1) แยก 3 requirement: governance ทั้งบัญชีใหม่และเดิม, การสร้างบัญชีพร้อม baseline อัตโนมัติ และ workforce federation 2) ทีมมีแค่ 4 คนและห้ามทำ account vending เอง จึงตัด script + StackSets (A) แม้ชิ้นส่วนจะใช้ได้ 3) Control Tower ตอบข้อ (1)(2) ได้ แต่ต้อง enroll บัญชีเดิมด้วย ตัด D ที่ทิ้งบัญชีเดิมไว้ข้างนอก 4) human access ต้องมาจาก IdP เดิมผ่าน IAM Identity Center ไม่ใช่ IAM users (C) จึงเหลือ B ที่ครบทั้งสามข้อ",
 refs=[("What is AWS Control Tower?", "https://docs.aws.amazon.com/controltower/latest/userguide/what-is-control-tower.html"),
       ("Enroll an existing AWS account in Control Tower", "https://docs.aws.amazon.com/controltower/latest/userguide/enroll-account.html"),
       ("IAM Identity Center external identity providers", "https://docs.aws.amazon.com/singlesignon/latest/userguide/manage-your-identity-source-idp.html")])

tfix("pro-12", {
 "A": ("Use IAM Identity Center permission sets federated with the SAML identity provider for developer access, keep the existing SCPs and local application IAM roles, and deploy the AWS Config managed rule s3-bucket-public-read-prohibited to every account to detect exposed buckets.",
       "ตกข้อ (2): Identity Center และ SCP ตอบข้อ (1)(3) ได้ แต่ rule นี้ตรวจเฉพาะ bucket ที่อ่านได้แบบ public เหตุการณ์ในโจทย์คือ resource policy ที่แชร์ให้ AWS account อื่น ซึ่งไม่ใช่ public access จึงตรวจไม่พบ และครอบคลุมเฉพาะ S3 ไม่ใช่ resource policy ประเภทอื่น"),
 "B": ("Use IAM Identity Center permission sets for developers and an organization-level IAM Access Analyzer external access analyzer. Replace all application IAM roles with centrally managed permission sets, and attach an SCP that denies iam:* actions in workload accounts.",
       "ตกข้อ (3): Identity Center กับ Access Analyzer ถูกต้อง แต่ permission sets ใช้กับการเข้าถึงของคน ไม่ใช่ role ที่ application ใช้ การห้าม iam:* ทั้งหมดทำให้เจ้าของผลิตภัณฑ์กำหนดสิทธิ์ละเอียดให้แอปของตนเองไม่ได้ ซึ่งโจทย์ระบุให้คงความสามารถนี้ไว้"),
 "C": ("Create IAM users with MFA for each developer in every account, rotate their access keys every 90 days with AWS Secrets Manager, enable an organization-level IAM Access Analyzer, and keep the SCPs and local application roles.",
       "ตกข้อ (1): Access Analyzer และ SCP ใช้ได้ แต่ IAM users ที่มี access keys ยังเป็น credentials ถาวร แม้จะหมุนทุก 90 วันก็ยังไม่ใช่ short-lived access จาก IdP กลางที่โจทย์ต้องการ และต้องดูแลผู้ใช้ซ้ำในทั้ง 80 บัญชี"),
 "D": ("Use IAM Identity Center permission sets for workforce account access, run IAM Access Analyzer to detect unintended external resource access, and retain least-privilege IAM roles and organization SCPs.",
       "ถูก: Identity Center federate กับ SAML IdP และให้ credentials ชั่วคราวตาม permission set ต่อบัญชี ส่วน Access Analyzer ระดับองค์กรวิเคราะห์ resource policy เช่น S3, KMS, IAM roles เพื่อหาการเข้าถึงจากภายนอก organization ที่ไม่ตั้งใจ ทีมยังกำหนด IAM roles ของแอปได้เองภายใต้ SCP ที่เป็นเพดานสิทธิ์ ควรใช้ archive rules ลด finding ที่ตั้งใจแชร์"),
},
 clue="ต้องเลิก access keys ถาวร, หา resource policy ที่แชร์ข้ามบัญชีโดยไม่ตั้งใจ, ทีมยังต้องกำหนดสิทธิ์ของแอปเองภายใต้ SCP",
 reasoning="1) ข้อ (1) ตัด IAM users + access keys (C) เพราะยังเป็น credentials ถาวร 2) ข้อ (2) เหตุการณ์คือแชร์ให้บัญชีอื่น ไม่ใช่ public จึงต้องใช้ IAM Access Analyzer ที่ใช้ organization เป็น zone of trust ไม่ใช่ rule เรื่อง public bucket (A) 3) ข้อ (3) permission sets ไม่ได้แทน application roles และการห้าม iam:* (B) ทำลายสิทธิ์ที่ต้องคงไว้ 4) D ครบทั้งสามข้อ: SCP เป็นเพดาน, IAM role ในบัญชีกำหนดสิทธิ์จริง, Identity Center ให้ human access ชั่วคราว",
 refs=[("Using IAM Access Analyzer", "https://docs.aws.amazon.com/IAM/latest/UserGuide/what-is-access-analyzer.html"),
       ("Permission sets in IAM Identity Center", "https://docs.aws.amazon.com/singlesignon/latest/userguide/permissionsetsconcept.html"),
       ("Service control policies", "https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html")])

tfix("pro-13", {
 "A": ("Share the transit gateway using AWS RAM, deploy baselines through CloudFormation StackSets using organization integration, and publish controlled products in AWS Service Catalog.",
       "ถูก: RAM แชร์ transit gateway โดยเจ้าของยังเป็น networking account บัญชีปลายทางแค่สร้าง attachment ได้ StackSets แบบ service-managed พร้อม automatic deployment ลง baseline ให้บัญชีใน OU และ Region ที่กำหนดรวมถึงบัญชีใหม่ ส่วน Service Catalog ให้ทีมเลือกเฉพาะ product/version ที่อนุมัติผ่าน launch constraint จึงไม่ต้องให้สิทธิ์สร้าง resource ทั้งหมดโดยตรง"),
 "B": ("Share the transit gateway and shared subnets with AWS RAM and deploy the baseline with service-managed StackSets. Let product teams deploy any CloudFormation template from a central S3 bucket by using an IAM role that has permissions to create all required resources.",
       "ตกข้อ (3): การแชร์เครือข่ายและ baseline ถูกต้อง แต่การให้ deploy template ใดก็ได้ด้วย role ที่สร้าง resource ได้ทั้งหมด ไม่ได้จำกัดให้ใช้เฉพาะ template ที่อนุมัติ และ platform group คุมเวอร์ชันไม่ได้ ทีมจึงสร้าง infrastructure นอกมาตรฐานได้"),
 "C": ("Create a transit gateway in each application account and peer it with the central transit gateway. Deploy the baseline with service-managed StackSets, and publish approved products in shared AWS Service Catalog portfolios.",
       "ตกข้อ (1): StackSets และ Service Catalog ถูกต้อง แต่การสร้าง transit gateway ในทุกบัญชีกระจาย routing ไปให้ทีมโปรดักต์เป็นเจ้าของ แทนที่จะคงความเป็นเจ้าของไว้ที่ networking account ต้องดูแล peering และ static routes จำนวนมากเมื่อมีบัญชีใหม่ทุกสัปดาห์"),
 "D": ("Share the transit gateway using AWS RAM and publish approved infrastructure products in AWS Service Catalog. Add the baseline resources as a mandatory Service Catalog product that each account owner launches after the account is created.",
       "ตกข้อ (2): RAM และ Service Catalog ถูกต้อง แต่ baseline ที่ต้องรอเจ้าของบัญชีกด launch เองไม่ใช่การ deploy อัตโนมัติ บัญชีใหม่ทุกสัปดาห์อาจขาด baseline หรือถูกลบภายหลังได้ ต่างจาก StackSets automatic deployment ที่จัดการจากส่วนกลาง"),
},
 clue="แชร์ TGW โดยคงความเป็นเจ้าของส่วนกลาง, baseline อัตโนมัติทุกบัญชี/Region, ทีมเลือกได้เฉพาะ template ที่อนุมัติ",
 reasoning="1) จับคู่ requirement กับบริการ: แชร์ resource ข้ามบัญชีโดยไม่โอนความเป็นเจ้าของ = AWS RAM, baseline ที่บังคับลงทุกบัญชี = StackSets automatic deployment, self-service ที่จำกัดเฉพาะของที่อนุมัติ = Service Catalog 2) ตัวลวงแต่ละข้อเปลี่ยนชิ้นเดียว: C ทิ้ง RAM ไปสร้าง TGW รายบัญชี, D ให้ baseline เป็นการกดเอง, B เปิดให้ deploy template ใดก็ได้ 3) A เป็นข้อเดียวที่ทั้งสามชิ้นทำหน้าที่ของตัวเองครบ",
 refs=[("Sharing transit gateways with AWS RAM", "https://docs.aws.amazon.com/vpc/latest/tgw/tgw-transit-gateways.html"),
       ("StackSets automatic deployment for Organizations", "https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-orgs-manage-auto-deployment.html"),
       ("Service Catalog launch constraints", "https://docs.aws.amazon.com/servicecatalog/latest/adminguide/constraints-launch.html")])

tfix("pro-14", {
 "A": ("Validate every CloudFormation template with AWS CloudFormation Guard rules and CloudFormation Hooks before deployment, and run CloudFormation drift detection on a schedule to find changes made outside the templates.",
       "ตกข้อ (1)(3): การตรวจ template ก่อน deploy ป้องกันค่าที่ผิดใน template ได้ แต่ไม่ได้ตรวจสถานะจริงของ resource ที่สร้างหรือแก้นอก CloudFormation และ drift detection ครอบคลุมเฉพาะ resource ใน stack ไม่มี configuration history ระดับองค์กร ซึ่งโจทย์ห้ามใช้ deployment-time validation แทน"),
 "B": ("Configure AWS Config organization rules and aggregators with Systems Manager Automation remediation documents and controlled execution roles.",
       "ถูก: Config บันทึก configuration history และประเมิน resource จริงในทุกบัญชี/Region ที่ recorder ทำงาน organization rules ครอบคลุมบัญชีใหม่ aggregator ให้มุมมองรวม ส่วน remediation ผูก rule แต่ละตัวกับ Automation runbook ที่อนุมัติและ execution role ที่จำกัดสิทธิ์ จึงแก้เฉพาะ violation ที่ระบุ ไม่กระทบการ deploy ด้วย CloudFormation"),
 "C": ("Configure AWS Config organization rules and an aggregator, and send all noncompliant evaluations through Amazon EventBridge to an AWS Lambda function with AdministratorAccess that modifies any noncompliant resource to a compliant state.",
       "ตกข้อ (2): ส่วนการตรวจจับและ history ถูกต้อง แต่ Lambda ที่มี AdministratorAccess และแก้ทุก resource ที่ noncompliant เป็น custom code ที่ไม่ได้จำกัดเฉพาะ violation ที่อนุมัติ และไม่ใช้ approved operational documents กับ execution role ที่จำกัดสิทธิ์ตามโจทย์"),
 "D": ("Create Amazon EventBridge rules in each account that match CloudTrail events such as DisableEbsEncryptionByDefault and public-access changes, and start Systems Manager Automation runbooks to revert the change.",
       "ตกข้อ (1)(3): ใช้ approved runbooks ได้ แต่เป็นการตอบ API event ไม่ใช่การประเมินสถานะจริง resource ที่ผิดอยู่ก่อนแล้วหรือเปลี่ยนด้วยวิธีที่ไม่ตรง pattern จะไม่ถูกตรวจ ไม่มี configuration history สำหรับ audit และต้องดูแล rule ในทุกบัญชี/Region เอง"),
},
 clue="ตรวจสถานะจริงของ resource ทั้งองค์กร, แก้อัตโนมัติด้วย runbook ที่อนุมัติและ role จำกัด, ต้องมี configuration history และห้ามใช้การตรวจตอน deploy แทน",
 reasoning="1) ข้อ (1)(3) ต้องการ configuration state + history ซึ่งเป็นหน้าที่ของ AWS Config ไม่ใช่การตรวจ template (A) หรือการจับ API events (D) 2) ข้อ (2) remediation ต้องจำกัดเฉพาะ violation ที่อนุมัติด้วย Automation runbooks และ execution role ที่กำหนด ไม่ใช่ Lambda สิทธิ์ admin ที่แก้ทุกอย่าง (C) 3) B ใช้ organization rules ครอบคลุมบัญชีใหม่, aggregator ให้ภาพรวม และ remediation configuration ต่อ rule ครบทั้งสามข้อ",
 refs=[("Remediating noncompliant resources with AWS Config", "https://docs.aws.amazon.com/config/latest/developerguide/remediation.html"),
       ("Managing AWS Config rules across all accounts in your organization", "https://docs.aws.amazon.com/config/latest/developerguide/config-rule-multi-account-deployment.html"),
       ("Detecting unmanaged configuration changes with drift detection", "https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-drift.html")])

tfix("pro-15", {
 "A": ("Deploy one NAT gateway in a public subnet in each Availability Zone with AZ-specific private route tables. Restrict outbound traffic with security group rules that allow TCP 443 only to the partners' published IP ranges, and enable VPC Flow Logs.",
       "ตกข้อ (2): NAT ต่อ AZ แก้ปัญหา single AZ และ cross-AZ ได้ และ Flow Logs ให้ metadata แต่ security group กรองตาม IP/port ไม่ใช่ domain และไม่ใช่ centralized egress policy เมื่อ partner เปลี่ยน IP ก็ต้องแก้ทุก security group จึงไม่ตอบ stateful domain-based filtering ที่ security ต้องการ"),
 "B": ("Route all private subnets through AWS Network Firewall endpoints in a centralized inspection VPC that uses domain allow-list rule groups, then through one NAT gateway in the inspection VPC, and enable VPC Flow Logs and firewall alert logs.",
       "ตกข้อ (3): Network Firewall ให้ domain-based stateful filtering และ logs ครบ แต่ NAT gateway ตัวเดียวยังผูก egress ทั้งหมดไว้กับ AZ เดียว ถ้า AZ นั้นล่ม outbound ทั้งระบบหยุด และ traffic จาก AZ อื่นยังข้าม AZ ซึ่งเป็นปัญหาเดิมที่โจทย์ต้องการแก้"),
 "C": ("Deploy highly available NAT gateways in the appropriate AZs, enforce egress inspection with AWS Network Firewall and symmetric routes, and enable VPC Flow Logs for network metadata.",
       "ถูก: NAT gateway ต่อ AZ ทำให้ egress ไม่ผูกกับ AZ เดียวและไม่ข้าม AZ โดยไม่จำเป็น Network Firewall ใช้ stateful domain allow-list ก่อนออก internet ต้องจัด route ให้ขาไปและขากลับผ่าน firewall endpoint ใน AZ เดียวกัน (หรือเปิด appliance mode เมื่อใช้ inspection VPC ผ่าน Transit Gateway) Flow Logs รวมการเชื่อมต่อที่ถูก reject ให้ใช้สอบสวน instance ใน private subnet ยังรับ inbound ที่ไม่ได้ร้องขอจาก internet ไม่ได้"),
 "D": ("Replace the NAT gateway with an egress-only internet gateway, route private subnets through AWS Network Firewall endpoints in each AZ with domain allow-list rules, and enable VPC Flow Logs.",
       "ตกข้อ (1): egress-only internet gateway ใช้ได้กับ IPv6 เท่านั้น ไม่ได้ให้ outbound IPv4 internet access ที่ workload ต้องใช้ แม้ Network Firewall ต่อ AZ และ Flow Logs จะตอบข้อ (2)(3) แต่ IPv4 traffic ก็ออก internet ไม่ได้"),
},
 clue="outbound IPv4 ที่ทนต่อการเสีย AZ, กรอง egress แบบ stateful ตาม domain พร้อม metadata, เลี่ยง NAT gateway AZ เดียวและ cross-AZ",
 reasoning="1) ข้อ (1) ต้องมี IPv4 egress ผ่าน NAT gateway ตัด egress-only IGW (D) ที่เป็น IPv6 เท่านั้น 2) ข้อ (3) NAT ตัวเดียวคือต้นเหตุของ outage และค่าข้าม AZ ตัด B 3) ข้อ (2) ต้องการ stateful domain-based filtering จากส่วนกลาง security group (A) กรองได้เพียง IP/port 4) C รวม NAT ต่อ AZ, Network Firewall ที่ route สมมาตร และ Flow Logs จึงครบทั้งสามข้อ",
 refs=[("AWS Network Firewall deployment architectures", "https://docs.aws.amazon.com/network-firewall/latest/developerguide/architectures.html"),
       ("NAT gateways", "https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html"),
       ("Egress-only internet gateways", "https://docs.aws.amazon.com/vpc/latest/userguide/egress-only-internet-gateway.html")])
