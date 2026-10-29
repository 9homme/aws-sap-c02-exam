from common import tfix

tfix("pro-49", {
 "A": ("Use AWS Control Tower with Account Factory and AWS Organizations OUs for enrollment and controls, and create Amazon CloudWatch billing alarms on the EstimatedCharges metric in the management account for cost tracking.",
       "ตกข้อ (2): governance ถูกต้อง แต่ billing alarm ดูได้เพียงยอดรวมโดยประมาณ ไม่มีการวิเคราะห์แนวโน้มแยกตาม account/service และไม่ได้กำหนดงบต่อหน่วยธุรกิจที่ถูกซื้อมา finance จึงไม่เห็นว่าหน่วยใดใช้เกินจัดสรรก่อนสิ้นงวด"),
 "B": ("Use AWS Control Tower, Organizations, Cost Explorer, and AWS Budgets, and give each account owner an IAM user in the management account with administrator permissions so that they can create resources in their accounts.",
       "ตกข้อ (3): Control Tower และเครื่องมือด้าน cost ถูกต้อง แต่การให้สิทธิ์ admin ใน management account เปิดให้แก้ governance ทั้งองค์กรได้ ซึ่งโจทย์ห้าม account owners ควรเข้าบัญชีของตนผ่าน IAM Identity Center ภายใต้ controls ของ OU"),
 "C": ("Use AWS Organizations with SCPs attached to experimental and production OUs, have the operations team create and configure each account manually from a runbook, and use Cost Explorer and AWS Budgets for finance.",
       "ตกข้อ (1): SCP เป็น preventive control ได้ และ Cost Explorer/Budgets ตอบเรื่อง finance แต่การสร้างบัญชีด้วยมือไม่ใช่ enrollment path ที่บริหารจากส่วนกลาง ไม่มี detective controls และ baseline logging ที่สม่ำเสมอ ทีมที่ไม่มีเวลาจึงทำซ้ำ 200 บัญชีไม่ไหว"),
 "D": ("Use Control Tower for the landing zone and account enrollment, AWS Organizations for the account hierarchy, Cost Explorer for spend analysis and AWS Budgets for threshold alerts.",
       "ถูก: Control Tower ให้ Account Factory และ enroll บัญชีเดิมที่เข้าเงื่อนไข พร้อม preventive/detective controls และ log archive Organizations จัด OU แยก experimental/production และรวม billing Cost Explorer วิเคราะห์แนวโน้มตาม account/service ส่วน Budgets แจ้งเตือนเมื่อ actual หรือ forecast ใกล้เกินงบ account owners ทำงานในบัญชีของตนผ่าน Identity Center โดยไม่ต้องมีสิทธิ์ใน management account"),
},
 clue="enrollment บัญชีใหม่และเดิมพร้อม controls, finance ต้องวิเคราะห์ cost ข้ามบัญชีและเตือนงบล่วงหน้า, owners ไม่ได้สิทธิ์ admin ใน management account",
 reasoning="1) ข้อ (1) ต้องการ enrollment ที่บริหารจากส่วนกลาง = Control Tower ไม่ใช่สร้างบัญชีด้วยมือ (C) 2) ข้อ (2) ต้องการวิเคราะห์ตาม account/service และงบต่อหน่วย = Cost Explorer + Budgets ไม่ใช่ billing alarm (A) 3) ข้อ (3) owners ต้องไม่มีสิทธิ์ใน management account ตัด B 4) D ใช้ governance และ cost tools แยกหน้าที่ครบทั้งสามข้อ",
 refs=[("What is AWS Control Tower?", "https://docs.aws.amazon.com/controltower/latest/userguide/what-is-control-tower.html"),
       ("Managing your costs with AWS Budgets", "https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html"),
       ("Analyzing your costs with Cost Explorer", "https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html")])

tfix("pro-50", {
 "A": ("Purchase 3-year Standard Reserved Instances for every currently running instance size now to capture savings immediately, then review Compute Optimizer recommendations next year.",
       "ตกข้อ (1): RI ให้ส่วนลดจริงแต่เป็นการ commit กับขนาด instance ปัจจุบันที่บางตัวใหญ่เกินจริง เมื่อ rightsize ภายหลัง RI ที่ซื้อไว้อาจไม่ถูกใช้เต็ม operations manager จึงไม่ยอมรับ ต้องวิเคราะห์ utilization ก่อนซื้อ commitment"),
 "B": ("Use Compute Optimizer recommendations and CloudWatch utilization to right-size first, then assess eligible Reserved Instances for stable demand, verify cost in Cost Explorer and configure AWS Budgets alerts.",
       "ถูก: Compute Optimizer ใช้ utilization metrics แนะนำขนาดที่เหมาะสมพร้อมระดับความเสี่ยง เมื่อ rightsize แล้วจึงซื้อ RI ให้ตรงกับ baseline ที่เหลืออยู่ เช่น batch ช่วงกลางคืน โดยพิจารณา term 1 ปีหรือ Convertible RI หากยังไม่มั่นใจ Cost Explorer ติดตามว่าค่าใช้จ่ายลดลงจริงและดู RI utilization/coverage ส่วน Budgets แจ้งเตือนเมื่อใกล้เกินงบรายไตรมาส"),
 "C": ("Use Compute Optimizer to right-size the instances, and move the steady baseline fleet to Spot Instances instead of evaluating any commitment discounts. Track spend in Cost Explorer and configure AWS Budgets alerts.",
       "ตกข้อ (2): rightsizing และการติดตาม cost ถูกต้อง แต่ Spot ไม่ใช่ commitment discount และอาจถูกเรียกคืน จึงไม่เหมาะกับ baseline ที่ต้องรันต่อเนื่อง โจทย์ต้องการประเมินส่วนลดแบบ commit สำหรับ baseline ที่เสถียรพร้อมเข้าใจเงื่อนไขของ term"),
 "D": ("Use Compute Optimizer to right-size the instances and purchase Reserved Instances for the stable baseline afterward, and review the consolidated invoice at the end of each quarter to confirm the savings.",
       "ตกข้อ (3): ลำดับ rightsize → RI ถูกต้อง แต่การดูใบแจ้งหนี้ตอนสิ้นไตรมาสพบปัญหาหลังจากเกินงบไปแล้ว ไม่มีการวิเคราะห์ระหว่างไตรมาสและไม่มีการแจ้งเตือนตาม threshold ที่ finance ต้องการ"),
},
 clue="rightsize จาก utilization ก่อนซื้อ commitment, ประเมิน RI สำหรับ baseline โดยเข้าใจ term, ติดตาม spend และเตือนตลอดไตรมาส",
 reasoning="1) ลำดับสำคัญ: rightsize ก่อนแล้วจึง commit ตัด A ที่ซื้อ RI ทันที 2) baseline ที่เสถียรควรใช้ commitment discount ไม่ใช่ Spot (C) 3) ต้องติดตามและเตือนระหว่างไตรมาส ไม่ใช่รอใบแจ้งหนี้ (D) 4) B: Compute Optimizer → RI สำหรับ baseline หลัง rightsize → Cost Explorer วัดผล → Budgets แจ้งเตือน",
 refs=[("What is AWS Compute Optimizer?", "https://docs.aws.amazon.com/compute-optimizer/latest/ug/what-is.html"),
       ("Reserved Instances for Amazon EC2", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-reserved-instances.html"),
       ("Managing your costs with AWS Budgets", "https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html")])

tfix("pro-51", {
 "A": ("Peer both VPCs, configure route tables and security rules, and provision AWS Client VPN with identity authentication and least-privilege network authorization for contractors.",
       "ถูก: VPC peering เชื่อมสอง VPC ที่ CIDR ไม่ทับกันข้ามบัญชีได้โดยไม่มี hub เพิ่ม route เฉพาะ prefix ที่จำเป็นและจำกัดด้วย security groups ส่วน Client VPN ใช้ SAML กับ IdP ขององค์กรเพื่อยืนยันตัวตนรายคน authorization rules จำกัดให้เข้าถึงเฉพาะ subnet ของ admin tools และถอนสิทธิ์ได้ทันทีที่ IdP"),
 "B": ("Attach both VPCs to a new AWS Transit Gateway with route tables for the two attachments, and provision AWS Client VPN with SAML-based federated authentication and authorization rules for the contractors.",
       "ตกข้อ (1)(3): ทำงานได้ถูกต้อง แต่ Transit Gateway เป็น hub ที่มีค่า attachment และงานดูแลเพิ่มสำหรับเพียงสอง VPC ที่จะไม่ขยายใน 3 ปี ซึ่ง network operations ระบุว่าจะปฏิเสธหากไม่จำเป็นจริง VPC peering ให้ผลเดียวกันโดยง่ายกว่า"),
 "C": ("Peer both VPCs and configure route tables and security groups. Publish the administration tools through an internet-facing Application Load Balancer that authenticates contractors with the corporate identity provider through OIDC.",
       "ตกข้อ (2)(3): peering ถูกต้อง และ ALB authentication ยืนยันตัวตนรายคนได้ แต่ admin tools ถูกเปิดสู่ internet ซึ่งโจทย์ห้าม และไม่ใช่ VPN access ไปยัง private resources ตามที่กำหนด"),
 "D": ("Peer both VPCs and configure route tables and security groups. Provision AWS Client VPN with mutual certificate authentication that uses one client certificate shared by all contractors.",
       "ตกข้อ (2): peering และ Client VPN ถูกต้อง แต่ certificate เดียวที่ใช้ร่วมกันไม่ได้ยืนยันตัวตนรายบุคคล ถอนสิทธิ์คนเดียวต้องเปลี่ยน certificate ของทุกคน และ authorization rules แยกตามกลุ่มจาก IdP ไม่ได้ ขัดกับข้อกำหนดเรื่อง revoke ทันที"),
},
 clue="แค่สอง VPC ที่ CIDR ไม่ทับและไม่ขยาย, ผู้รับเหมารายคนต้อง VPN แบบยืนยันตัวตนและถอนสิทธิ์ได้ทันที, ห้ามเปิด public และห้ามมี hub ที่ไม่จำเป็น",
 reasoning="1) VPC-to-VPC สองตัวที่ไม่ขยาย: peering ง่ายที่สุด Transit Gateway (B) เป็น hub ที่ไม่จำเป็น 2) human remote access ต้องเป็น Client VPN แบบ federated รายคน ตัด shared certificate (D) 3) ห้ามเปิด endpoint สู่ internet ตัด ALB สาธารณะ (C) 4) A แยก workload connectivity (peering) ออกจาก human access (Client VPN) และครบทุกข้อ",
 refs=[("What is VPC peering?", "https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html"),
       ("What is AWS Client VPN?", "https://docs.aws.amazon.com/vpn/latest/clientvpn-admin/what-is.html"),
       ("Client VPN authentication", "https://docs.aws.amazon.com/vpn/latest/clientvpn-admin/client-authentication.html")])

tfix("pro-52", {
 "A": ("Deploy Network Load Balancers in each Region for the game servers, create Route 53 latency-based records with health checks for the NLBs, and use VPC Lattice service networks with auth policies for the internal HTTP services.",
       "ตกข้อ (1): NLB และ Lattice ถูกต้อง แต่ Route 53 ให้ IP ของ NLB แยกตาม AZ และ Region ไม่ใช่ static anycast IP ชุดเล็กที่ client allowlist ไว้ และ failover ขึ้นกับ DNS TTL/การ cache ของ client จึงไม่รวดเร็วตามที่ต้องการ"),
 "B": ("Use AWS Global Accelerator with Application Load Balancer endpoints in each Region for the game traffic, and use VPC Lattice service networks with auth policies for the internal HTTP services.",
       "ตกข้อ (2): Global Accelerator ให้ static anycast IP และ Lattice ตอบฝั่ง internal แต่ ALB รับเฉพาะ HTTP/HTTPS (และ gRPC) ไม่สามารถ balance custom TCP protocol ของเกมได้ ต้องใช้ NLB เป็น endpoint"),
 "C": ("Expose the game service with Global Accelerator using regional NLB endpoints, and use VPC Lattice service networks with auth policies for internal HTTP services.",
       "ถูก: Global Accelerator ให้ static anycast IP สำหรับ allowlist ส่ง traffic ผ่าน AWS global network ไปยัง Region ที่ใกล้และ healthy และ failover โดยไม่พึ่ง DNS NLB balance TCP connections ข้าม AZ ภายใน Region ส่วน VPC Lattice เชื่อม HTTP services ข้ามบัญชีแม้ CIDR ทับกัน พร้อม service discovery และ IAM auth policies โดยไม่เปิด public ingress"),
 "D": ("Use AWS Global Accelerator with regional NLB endpoints for the game traffic, and connect the internal service VPCs through a shared transit gateway with security groups that allow traffic from approved CIDR ranges.",
       "ตกข้อ (3): ฝั่งเกมถูกต้อง แต่ Transit Gateway route ตาม CIDR จึงใช้ไม่ได้ตรง ๆ กับ VPC ที่ CIDR ทับกัน และการอนุญาตตาม CIDR ไม่ใช่ service-level authentication/authorization ที่ทีมต้องการ VPC Lattice แก้ทั้งสองเรื่องนี้"),
},
 clue="static anycast IP + failover ข้าม Region สำหรับ TCP, balance TCP ภายใน Region, internal HTTP ข้ามบัญชีที่ CIDR ทับกันพร้อม service-level auth",
 reasoning="1) สามชั้นต่างกัน: global edge (Global Accelerator), L4 balancing ใน Region (NLB), private service network (VPC Lattice) 2) A ใช้ DNS แทน anycast 3) B ใช้ ALB กับ custom TCP 4) D ใช้ Transit Gateway กับ CIDR ที่ทับกันและไม่มี service-level auth 5) C ใช้บริการที่ตรงกับแต่ละชั้น ไม่ใช่ ALB ตัวเดียวสำหรับทุกอย่างตามที่ reviewer เสนอ",
 refs=[("Endpoints for standard accelerators", "https://docs.aws.amazon.com/global-accelerator/latest/dg/about-endpoints.html"),
       ("What is Amazon VPC Lattice?", "https://docs.aws.amazon.com/vpc-lattice/latest/ug/what-is-vpc-lattice.html"),
       ("What is a Network Load Balancer?", "https://docs.aws.amazon.com/elasticloadbalancing/latest/network/introduction.html")])

tfix("pro-53", {
 "A": ("Insert the third-party appliances with a Gateway Load Balancer and Gateway Load Balancer endpoints, and implement the second division's egress policy with security groups and network ACLs that allow only approved destination IP ranges. Enable VPC Flow Logs.",
       "ตกข้อ (2): GWLB สำหรับ appliances ถูกต้อง แต่ security groups และ NACLs กรองตาม IP/port แบบ stateless (NACL) หรือ per-ENI ไม่มี domain-based filtering และไม่ใช่ managed stateful firewall ที่บริหาร policy จากส่วนกลางตามที่ division ที่สองต้องการ"),
 "B": ("Deploy AWS Network Firewall for both divisions, translate the proprietary appliance's inspection logic into Suricata-compatible rule groups, and enable VPC Flow Logs and firewall logs.",
       "ตกข้อ (1): Network Firewall ตอบ division ที่สองได้ แต่ appliance ของ line of business แรกเป็น certified image ที่ต้องใช้ต่อ การแปลงเป็น Suricata rules ไม่ได้ทำซ้ำ proprietary inspection และไม่ผ่านการรับรองเดิม"),
 "C": ("Use a Gateway Load Balancer for the appliance fleet and AWS Network Firewall for the second division in the inspection VPC, attach the inspection VPC to the transit gateway with appliance mode disabled, and enable VPC Flow Logs.",
       "ตกข้อ (3): บริการถูกเลือกถูกต้อง แต่เมื่อปิด appliance mode บน attachment ของ inspection VPC Transit Gateway อาจส่ง traffic ขาไปและขากลับผ่านคนละ AZ ทำให้ stateful inspection เห็น flow ไม่ครบและ drop connection ต้องเปิด appliance mode เพื่อให้ routing สมมาตร"),
 "D": ("Use GWLB with Gateway Load Balancer endpoints for the supported appliance-fleet traffic, deploy Network Firewall for the AWS-managed inspection path, design symmetric routing per AZ and retain VPC Flow Logs.",
       "ถูก: GWLB กระจาย traffic แบบ transparent ไปยัง appliance fleet ที่ scale ได้ด้วย Auto Scaling Network Firewall ให้ stateful rules และ domain filtering แบบ managed สำหรับอีก path การเปิด appliance mode บน Transit Gateway attachment และวาง endpoint ต่อ AZ ทำให้ routing สมมาตรและทนต่อการเสีย AZ ส่วน Flow Logs ให้ metadata สำหรับสอบสวน"),
},
 clue="ต้องใช้ certified third-party appliance ที่ scale ได้, อีก division ต้องการ managed stateful + domain filtering, routing สมมาตรหลาย AZ และ flow metadata",
 reasoning="1) ข้อ (1) appliance ของบุคคลที่สามแบบ transparent = GWLB ห้ามแทนด้วยบริการอื่น (B) 2) ข้อ (2) managed stateful + domain filtering = Network Firewall ไม่ใช่ SG/NACL (A) 3) ข้อ (3) stateful inspection ผ่าน Transit Gateway ต้องเปิด appliance mode เพื่อให้ขาไปและขากลับผ่าน AZ เดียวกัน (C ปิดไว้) 4) D รวมทั้งสามข้อ",
 refs=[("What is a Gateway Load Balancer?", "https://docs.aws.amazon.com/elasticloadbalancing/latest/gateway/introduction.html"),
       ("AWS Network Firewall deployment architectures", "https://docs.aws.amazon.com/network-firewall/latest/developerguide/architectures.html"),
       ("Transit gateway appliance mode", "https://docs.aws.amazon.com/vpc/latest/tgw/transit-gateway-appliance-scenario.html")])

tfix("pro-54", {
 "A": ("Deploy EKS for the Kubernetes jobs and attach Amazon FSx for Lustre using supported CSI integration; integrate dataset import/export with S3 and validate lifecycle settings.",
       "ถูก: EKS คง Kubernetes API, operators และ Helm charts เดิม FSx for Lustre CSI driver ให้ pods mount parallel file system ที่รองรับ metadata และ random read สูง data repository association กับ S3 ทำให้เห็น dataset 30 TB เป็นไฟล์และ export ผลลัพธ์กลับ S3 ได้ ไม่ต้องดูแล Lustre เอง ควรตั้ง lifecycle ของ file system ให้สอดคล้องกับรอบงาน"),
 "B": ("Convert the Kubernetes jobs into AWS Batch job definitions on EC2 compute environments and mount an Amazon FSx for Lustre file system that is linked to the S3 dataset.",
       "ตกข้อ (1): FSx for Lustre ถูกต้อง และ Batch เป็นบริการ managed ที่ดี แต่การแปลง jobs เป็น Batch job definitions ทำให้เลิกใช้ Kubernetes scheduling, admission policies, operators และ Helm charts เดิม ซึ่งนักวิทยาศาสตร์ยืนยันให้คงไว้"),
 "C": ("Run the jobs on Amazon EKS and mount the S3 dataset into the pods with the Mountpoint for Amazon S3 CSI driver, writing intermediate results back to the bucket.",
       "ตกข้อ (2): EKS ถูกต้อง แต่ Mountpoint for S3 ไม่ใช่ POSIX file system เต็มรูปแบบ ไม่รองรับการแก้ไขไฟล์เดิมหรือ random write และไม่ได้ออกแบบสำหรับ metadata operations หนัก ๆ แบบ parallel ปัญหาจึงคล้ายกับ wrapper เดิมที่ทำงานช้า"),
 "D": ("Run the jobs on Amazon EKS and deploy a self-managed Lustre cluster on EC2 instances with metadata and object storage servers, synchronizing data with Amazon S3 by using scheduled scripts.",
       "ตกข้อ (3): ได้ parallel POSIX file system และคง Kubernetes ได้ แต่ทีมต้องดูแล Lustre servers, HA และ script sync กับ S3 เอง ซึ่งโจทย์ระบุให้หลีกเลี่ยง FSx for Lustre ให้ความสามารถเดียวกันแบบ managed"),
},
 clue="ต้องคง Kubernetes/operators/Helm, ต้องการ parallel POSIX file system ประสิทธิภาพสูงที่เชื่อม S3, ห้ามดูแล Lustre เอง",
 reasoning="1) ข้อ (1) ต้องคง Kubernetes จึงใช้ EKS ไม่ใช่แปลงเป็น Batch (B) 2) ข้อ (2) ต้องการ POSIX แบบ parallel ที่รองรับ metadata/random access ซึ่ง Mountpoint for S3 (C) ไม่ได้ออกแบบมา 3) ข้อ (3) ห้าม self-managed Lustre (D) 4) A ใช้ FSx for Lustre ผ่าน CSI driver บน EKS พร้อม data repository association กับ S3",
 refs=[("Amazon FSx for Lustre CSI driver on Amazon EKS", "https://docs.aws.amazon.com/eks/latest/userguide/fsx-csi.html"),
       ("Linking FSx for Lustre to an S3 data repository", "https://docs.aws.amazon.com/fsx/latest/LustreGuide/create-dra-linked-data-repo.html"),
       ("Mountpoint for Amazon S3", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/mountpoint.html")])

tfix("pro-55", {
 "A": ("Use DAX in front of the DynamoDB catalog, and use Amazon MemoryDB both for the session cache and for the wallet service.",
       "ตกข้อ (2): DAX และ MemoryDB สำหรับ wallet ถูกต้อง แต่ session cache ที่สร้างใหม่ได้จากระบบหลักไม่ต้องการความทนทานของ MemoryDB ซึ่งมีค่าใช้จ่ายสูงกว่าและ write latency สูงกว่าเพราะต้องบันทึก transaction log ข้าม AZ ElastiCache เหมาะกับ cache แบบ disposable มากกว่า"),
 "B": ("Use DAX in front of DynamoDB, ElastiCache for repopulatable session data, and MemoryDB for the Redis-compatible durable data store.",
       "ถูก: DAX เร่งการอ่าน DynamoDB ด้วย API เดิมโดย DynamoDB ยังเป็น source of truth ElastiCache เป็น in-memory cache ราคาคุ้มสำหรับ session ที่สร้างใหม่ได้หลัง outage ส่วน MemoryDB เก็บทุก write ใน Multi-AZ transaction log จึงเป็น primary database ที่ทนทานสำหรับ wallet แม้ node ถูกแทนที่"),
 "C": ("Use DAX in front of DynamoDB and ElastiCache for the session cache, and use an Amazon ElastiCache (Redis OSS) cluster with Multi-AZ replicas and daily snapshots as the wallet service's primary data store.",
       "ตกข้อ (3): สองส่วนแรกถูกต้อง แต่ ElastiCache ใช้ asynchronous replication และ snapshot เป็นรอบ เมื่อ primary node ล้มอาจเสีย write ล่าสุดก่อน replica ได้รับ จึงไม่เหมาะกับ wallet ที่ต้องให้ database ทนทานด้วยตัวเอง"),
 "D": ("Migrate the catalog from DynamoDB into Amazon MemoryDB as its new primary store, use ElastiCache for the session cache, and use MemoryDB for the wallet service.",
       "ตกข้อ (1): MemoryDB เร็วและทนทาน แต่การย้าย catalog ออกจาก DynamoDB คือการเปลี่ยน source of truth และต้องเขียน access pattern ใหม่ทั้งหมด ซึ่งโจทย์ห้าม DAX เร่ง path เดิมได้โดยไม่ต้องเปลี่ยน"),
},
 clue="เร่ง DynamoDB โดยคง source of truth, session cache ที่ทิ้งได้และต้องคุ้มค่า, wallet ต้องการ Redis-compatible ที่ทนทานด้วยตัวเอง",
 reasoning="1) แยกตาม persistence และ API: DynamoDB path = DAX, cache ที่สร้างใหม่ได้ = ElastiCache, Redis-compatible primary durable = MemoryDB 2) A ใช้ MemoryDB กับ cache ที่ไม่ต้องทนทานจึงแพงเกินจำเป็น 3) C ใช้ ElastiCache เป็น primary store ซึ่งอาจเสียข้อมูล 4) D เปลี่ยน source of truth ของ catalog 5) B จับคู่ครบตามที่วิศวกรเตือนว่าใช้ผลิตภัณฑ์เดียวไม่ได้",
 refs=[("In-memory acceleration with DynamoDB Accelerator (DAX)", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.html"),
       ("What is Amazon ElastiCache?", "https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/WhatIs.html"),
       ("What is Amazon MemoryDB?", "https://docs.aws.amazon.com/memorydb/latest/devguide/what-is-memorydb.html")])

tfix("pro-56", {
 "A": ("Register the S3 datasets with Lake Formation and grant column- and row-level permissions for Athena, build dashboards in Amazon QuickSight, and have operations engineers search delivery events with Athena LIKE queries over the raw S3 data.",
       "ตกข้อ (3): Lake Formation และ QuickSight ถูกต้อง แต่ Athena ต้องสแกนข้อมูลทุกครั้งและไม่มี inverted index การค้นหาข้อความอิสระด้วย LIKE จึงช้าและแพงสำหรับ troubleshooting console ที่ต้องการ latency ต่ำ ซึ่งโจทย์เตือนไม่ให้สับสน full-text search กับ SQL"),
 "B": ("Create S3 bucket policies and IAM policies for each business unit that allow access to approved prefixes, query with Athena, build dashboards in QuickSight, and index operational documents in Amazon OpenSearch Service.",
       "ตกข้อ (1): QuickSight และ OpenSearch ถูกต้อง แต่ IAM/bucket policy คุมได้แค่ระดับ object หรือ prefix ไม่สามารถจำกัดเฉพาะคอลัมน์ที่อนุมัติในตารางได้ และต้องดูแลสิทธิ์ที่ระดับ storage แทน catalog"),
 "C": ("Register S3 datasets and permissions with Lake Formation and compatible catalog/query integrations, build BI in QuickSight, and index operational documents in OpenSearch Service.",
       "ถูก: Lake Formation กำหนดสิทธิ์ระดับ table/column/row บน Glue Data Catalog ให้ Athena และ engine ที่รองรับ โดยผู้ใช้ไม่ต้องมีสิทธิ์ bucket ตรง QuickSight ให้ dashboard ที่จัดการสิทธิ์ผู้ใช้และตั้งเวลาส่งรายงานได้ OpenSearch Service index เอกสารเพื่อค้นหาข้อความและกรองแบบ latency ต่ำ สิทธิ์ของแต่ละชั้นแยกจัดการและเข้ารหัสได้"),
 "D": ("Register the S3 datasets with Lake Formation and grant column-level permissions for Athena, index the operational documents in OpenSearch Service, and give executives Athena console access to run saved queries instead of building dashboards.",
       "ตกข้อ (2): ชั้นสิทธิ์และ search ถูกต้อง แต่การให้ผู้บริหารรัน saved queries ใน Athena console ไม่ใช่ governed dashboard ที่มี visual analysis และ scheduled sharing ผู้บริหารยังต้องมีสิทธิ์ query และเห็นผลเป็นตาราง ไม่ใช่ dashboard"),
},
 clue="สิทธิ์ระดับคอลัมน์/หน่วยธุรกิจบน catalog สำหรับ SQL, dashboard ผู้บริหารที่ตั้งเวลาแชร์, ค้นหาเอกสาร operations แบบ full-text latency ต่ำ",
 reasoning="1) แยกสามชั้น: data permissions (Lake Formation), BI dashboards (QuickSight), full-text search (OpenSearch) 2) B ใช้ IAM ระดับ prefix ซึ่งไม่ถึงระดับคอลัมน์ 3) D ไม่มี dashboard 4) A ใช้ Athena LIKE แทน search index 5) C ใช้บริการที่ตรงกับแต่ละชั้นและจัดการสิทธิ์แยกกันตามที่ security ต้องการ",
 refs=[("Lake Formation permissions model", "https://docs.aws.amazon.com/lake-formation/latest/dg/managing-permissions.html"),
       ("What is Amazon QuickSight?", "https://docs.aws.amazon.com/quicksight/latest/user/welcome.html"),
       ("What is Amazon OpenSearch Service?", "https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html")])
