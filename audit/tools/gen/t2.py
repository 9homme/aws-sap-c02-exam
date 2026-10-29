from common import tfix

tfix("pro-16", {
 "A": ("Deploy VPC Lattice service networks for the internal HTTP services and use interface endpoints through AWS PrivateLink for the vendor endpoint service.",
       "ถูก: VPC Lattice เชื่อม service ข้ามบัญชีผ่าน service network ที่แชร์ด้วย RAM โดยไม่ต้อง route ระหว่าง VPC จึงใช้ได้แม้ CIDR ซ้อนกัน มี service discovery และ auth policy ที่อิง IAM ระดับ service แทนการอนุญาตทั้ง CIDR ส่วน vendor ใช้ interface endpoint ของ PrivateLink ซึ่งเปิดการเชื่อมต่อทางเดียวจาก consumer ไปยัง endpoint service โดย vendor ไม่ได้ route เข้ามาใน VPC ลูกค้า"),
 "B": ("Attach all service VPCs to a transit gateway, use security groups and network ACLs that allow the CIDR ranges of approved consumer VPCs, and consume the vendor service through an AWS PrivateLink interface endpoint.",
       "ตกข้อ (1): PrivateLink สำหรับ vendor ถูกต้อง แต่ Transit Gateway ต้อง route ตาม CIDR จึงใช้ไม่ได้กับ VPC ที่ CIDR ซ้อนกันหากไม่ทำ NAT เพิ่ม และการอนุญาตด้วย security group/NACL ตาม CIDR คือ network-level trust ที่โจทย์ต้องการเลี่ยง ไม่มี service discovery หรือ authorization ราย service"),
 "C": ("Deploy VPC Lattice service networks for the internal HTTP services, and create a VPC peering connection between the consumer VPC and the vendor's VPC to reach the vendor's TCP service.",
       "ตกข้อ (2): VPC Lattice ตอบเรื่อง HTTP services ข้ามบัญชีแล้ว แต่ VPC peering เปิด routing สองทางระหว่างสอง VPC ซึ่ง vendor ไม่ต้องการ และใช้ไม่ได้ถ้า CIDR ซ้อนกัน การใช้ endpoint service ที่ vendor มีอยู่แล้วผ่าน PrivateLink จึงเหมาะกว่า"),
 "D": ("Expose each of the 70 internal services as its own PrivateLink endpoint service behind a Network Load Balancer, have every consumer VPC create an interface endpoint for each service that it calls, and use the same pattern for the vendor service.",
       "ตกข้อ (1)(3): PrivateLink ทำงานได้กับ CIDR ที่ซ้อนกันและเหมาะกับ vendor แต่สำหรับ 70 services ต้องดูแล NLB และ interface endpoints จำนวนมากตามจำนวนคู่ consumer/service อีกทั้งไม่มี service discovery และ service-level authorization แบบรวมศูนย์ตามที่ทีมต้องการ"),
},
 clue="70 HTTP services ข้ามบัญชีที่ CIDR ซ้อนกัน ต้องมี discovery/auth ระดับ service, vendor TCP ต้องเข้าถึงแบบ private ทางเดียว, ห้ามทำ peering mesh",
 reasoning="1) แยกสอง pattern: service-to-service HTTP ภายใน กับการ consume service ของ vendor 2) CIDR ซ้อนกันทำให้ทางที่ต้อง route ตาม CIDR (Transit Gateway ใน B, peering ใน C) มีปัญหา 3) ฝั่งภายในต้องการ discovery และ authorization ราย service: VPC Lattice ให้ได้ ส่วน PrivateLink ราย service (D) ต้องดูแล endpoint จำนวนมาก 4) ฝั่ง vendor: PrivateLink interface endpoint เปิดทางเดียวจาก consumer โดย vendor ไม่ได้ route เข้ามา A จึงใช้เครื่องมือที่ถูกกับแต่ละ pattern",
 refs=[("What is Amazon VPC Lattice?", "https://docs.aws.amazon.com/vpc-lattice/latest/ug/what-is-vpc-lattice.html"),
       ("Access a SaaS product through an interface VPC endpoint", "https://docs.aws.amazon.com/vpc/latest/privatelink/privatelink-access-saas.html"),
       ("VPC peering limitations", "https://docs.aws.amazon.com/vpc/latest/peering/vpc-peering-basics.html")])

tfix("pro-17", {
 "A": ("Use CloudFront with AWS WAF and an ACM certificate for the website. For the game, create Route 53 latency-based records with health checks that point to Network Load Balancers with UDP listeners in each Region.",
       "ตกข้อ (2): ฝั่งเว็บถูกต้อง แต่ game ใช้ DNS ในการ failover ซึ่งโจทย์ระบุว่ายอมรับไม่ได้เพราะ client cache DNS answer อีกทั้ง NLB มี IP แยกตาม AZ และ Region จึงไม่ได้ชุด static anycast IP ขนาดเล็กให้ partner allowlist"),
 "B": ("Create one AWS Global Accelerator standard accelerator with a TCP 443 listener that points to Application Load Balancers for the website and a UDP listener that points to Network Load Balancers for the game, and attach AWS WAF to the ALBs.",
       "ตกข้อ (1): Global Accelerator ให้ static IP และ health-based routing ได้ทั้งสองทาง และ WAF ติดกับ ALB ได้ แต่ Global Accelerator ไม่ได้ cache เนื้อหา static ที่ edge ทุก request ของเว็บยังวิ่งไปถึง ALB ใน Region จึงไม่ได้ประโยชน์ของ CDN ตามข้อกำหนด"),
 "C": ("Use AWS Global Accelerator with health-checked Network Load Balancer UDP endpoints in both Regions for the game. Serve the website directly from an Amazon S3 static website endpoint protected by AWS Shield Advanced.",
       "ตกข้อ (1): ฝั่ง game ถูกต้อง แต่ S3 website endpoint ไม่รองรับ HTTPS ด้วย ACM certificate โดยตรง ไม่ได้ cache ใกล้ผู้ใช้ และไม่สามารถใช้ AWS WAF กรอง request ได้ Shield Advanced ช่วยเรื่อง DDoS แต่ไม่ได้แทน WAF rules"),
 "D": ("Use CloudFront with AWS WAF and ACM for HTTPS content, and Global Accelerator with health-checked regional UDP endpoints for the game.",
       "ถูก: CloudFront cache static HTTPS ที่ edge ใช้ ACM certificate (ต้องอยู่ใน us-east-1) และผูก WAF web ACL ได้ ส่วน Global Accelerator ให้ static anycast IP 2 ตัวสำหรับ allowlist รองรับ UDP และย้าย traffic ไป Region ที่ healthy โดยไม่พึ่ง DNS ทั้งสองเส้นทางแยก health check และ deployment ของตัวเอง Shield Standard คุ้มครองทั้งสองบริการโดยอัตโนมัติ"),
},
 clue="เว็บ static HTTPS ต้อง cache + WAF + ACM, game UDP ต้องมี static anycast IP และ failover ไม่พึ่ง DNS, แยกนโยบายสองเส้นทาง",
 reasoning="1) แยก workload: เว็บต้องการ CDN + WAF ส่วน game ต้องการ static anycast IP สำหรับ UDP 2) game: DNS failover (A) ถูกห้าม จึงต้องใช้ Global Accelerator 3) เว็บ: Global Accelerator (B) ไม่ cache และ S3 website endpoint (C) ไม่มี HTTPS/WAF จึงต้องใช้ CloudFront 4) D ใช้บริการที่เหมาะกับแต่ละเส้นทางและแยก health/deployment policy ได้",
 refs=[("How AWS Global Accelerator works", "https://docs.aws.amazon.com/global-accelerator/latest/dg/introduction-how-it-works.html"),
       ("Using AWS WAF with CloudFront", "https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/distribution-web-awswaf.html"),
       ("Requirements for using SSL/TLS certificates with CloudFront", "https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/cnames-and-https-requirements.html")])

tfix("pro-18", {
 "A": ("Use an ALB for the HTTP API, an NLB with a TLS listener that terminates TLS for the proprietary TCP protocol and is published as a PrivateLink endpoint service, and a Gateway Load Balancer for the inspection appliances.",
       "ตกข้อ (1): โครงสร้างโดยรวมถูก แต่ client ของ protocol นี้ต้องการ TLS pass-through การใช้ TLS listener บน NLB จะถอดรหัสที่ load balancer ทำให้ backend ไม่ได้ TLS session เดิม ต้องใช้ TCP listener เพื่อส่ง TLS ผ่านไปยัง target"),
 "B": ("Use ALB for the HTTP API, NLB for the TCP endpoint and PrivateLink endpoint service, and GWLB for transparent inspection appliance fleets.",
       "ถูก: ALB ใช้ host/path rules ระดับ layer 7 NLB ที่มี TCP listener ส่ง TLS ผ่านไปยัง target และมี static IP ต่อ AZ ทั้งยังเป็น load balancer ที่ใช้ทำ PrivateLink endpoint service ให้ลูกค้าอีกบัญชีเข้าถึงแบบ private ได้ ส่วน GWLB กระจาย traffic แบบ transparent ไปยัง appliances ด้วย GENEVE และ scale แยกจาก API ได้"),
 "C": ("Use an ALB for the HTTP API and an NLB with a TCP listener published as a PrivateLink endpoint service. Place the inspection appliances behind a second NLB, disable source/destination checks on the appliances, and route traffic through the NLB.",
       "ตกข้อ (2): ALB และ NLB/PrivateLink ถูกต้อง แต่ NLB ไม่ได้ออกแบบให้เป็นจุด bump-in-the-wire บน route table และไม่ได้คง packet เดิมพร้อม flow stickiness แบบ GWLB ที่ใช้ GENEVE การวาง appliances หลัง NLB จึงไม่ transparent และจัดการ return path ยาก"),
 "D": ("Use an ALB for the HTTP API, an NLB with a TCP listener for the proprietary service, and a Gateway Load Balancer for the appliances. Give the customer access through a VPC peering connection and security group rules that allow only the NLB.",
       "ตกข้อ (3): load balancer ครบทั้งสามชนิด แต่ VPC peering สร้าง routing ระหว่างทั้งสอง VPC ซึ่งโจทย์ห้าม และใช้ไม่ได้ถ้า CIDR ซ้อนกัน การจำกัดด้วย security group ไม่ได้ลดขอบเขต routing ส่วน PrivateLink endpoint service เปิดเฉพาะ service นั้นทางเดียว"),
},
 clue="API ต้องการ layer 7 rules, TCP ต้อง TLS pass-through, appliances ต้องเป็น transparent, ลูกค้าอีกบัญชีต้องเข้าแบบ private โดยไม่ route ทั้ง VPC",
 reasoning="1) จับคู่ load balancer กับ layer: HTTP host/path = ALB, TCP pass-through = NLB แบบ TCP listener (ไม่ใช่ TLS listener ใน A), transparent appliances = GWLB (ไม่ใช่ NLB ใน C) 2) การเปิดให้อีกบัญชีใช้แบบ private โดยไม่ route ทั้ง VPC คือ PrivateLink endpoint service ที่อยู่หน้า NLB ไม่ใช่ peering (D) 3) B เป็นข้อเดียวที่ทุกชิ้นตรงกับ requirement ของตน",
 refs=[("What is Elastic Load Balancing?", "https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/what-is-load-balancing.html"),
       ("What is a Gateway Load Balancer?", "https://docs.aws.amazon.com/elasticloadbalancing/latest/gateway/introduction.html"),
       ("Share your services through AWS PrivateLink", "https://docs.aws.amazon.com/vpc/latest/privatelink/privatelink-share-your-services.html")])

tfix("pro-19", {
 "A": ("Deploy AWS Client VPN endpoints with authorized routes to the VPC and connected data center, and integrate the applicable Route 53 Resolver inbound/outbound forwarding rules.",
       "ถูก: Client VPN ให้ TLS VPN รายผู้ใช้จาก network ใดก็ได้ พร้อม federated authentication ผ่าน SAML และ authorization rules ตามกลุ่ม route ไป data center ใช้เส้นทาง Direct Connect ที่ VPC มีอยู่แล้ว DNS ของ client ชี้ไปที่ Resolver ใน VPC (หรือ inbound endpoint) ซึ่ง resolve private hosted zone ได้ และ outbound forwarding rule ส่ง query ของ zone on premises ไปยัง DNS ของ data center แอปจึงไม่ต้องเปิดสู่ internet"),
 "B": ("Publish the internal application through an internet-facing Application Load Balancer that uses Amazon Cognito authentication, and publish the intranet through a reverse proxy in a public subnet.",
       "ตกข้อ (3): Cognito ช่วยยืนยันตัวตนผู้ใช้ได้ แต่ทางนี้เปิด endpoint ของแอปภายในและ intranet ให้ client บน internet เข้าถึงโดยตรง ซึ่งโจทย์ห้าม และไม่ได้แก้เรื่อง DNS ภายในเพราะเปลี่ยนเป็นชื่อ public แทน"),
 "C": ("Deploy an AWS Client VPN endpoint with SAML-based federated authentication and authorization rules for the VPC and data-center CIDRs, and configure the endpoint to use only the VPC's Amazon-provided DNS server without any Resolver rules.",
       "ตกข้อ (2): ฝั่ง VPN และ routing ถูกต้อง Amazon-provided DNS resolve private hosted zone ได้ แต่ไม่รู้จัก DNS zone ของ data center หากไม่มี outbound endpoint และ forwarding rule ผู้ใช้จึงเปิด intranet ด้วยชื่อไม่ได้"),
 "D": ("Deploy an AWS Client VPN endpoint that uses mutual certificate authentication with one shared client certificate distributed to all employees, and configure Route 53 Resolver inbound and outbound endpoints with forwarding rules.",
       "ตกข้อ (1): DNS ออกแบบถูกต้อง แต่ certificate เดียวที่แจกทุกคนไม่ใช่ federated authentication รายบุคคล แยกและถอนสิทธิ์ผู้ใช้คนเดียวไม่ได้ และไม่มี authorization ตามกลุ่มผู้ใช้จาก IdP ตามที่ security ต้องการ"),
},
 clue="ผู้ใช้ 1,200 คนจาก network ใดก็ได้ ต้อง federated auth ต่อคน, DNS ทั้ง private hosted zone และ zone on premises, ห้ามเปิดแอปสู่ internet",
 reasoning="1) remote user รายคนจาก network ที่ควบคุมไม่ได้ = Client VPN (Direct Connect และ Site-to-Site VPN เป็นการเชื่อมระดับ site) 2) auth ต้องเป็น federated รายบุคคล ตัด shared certificate (D) 3) DNS ต้อง resolve ทั้งสองฝั่ง: VPC resolver รู้ private hosted zone แต่ต้องมี outbound forwarding rule สำหรับ zone on premises ตัด C 4) ห้ามเปิดแอปสู่ internet ตัด B A จึงครบทั้งสามข้อ",
 refs=[("What is AWS Client VPN?", "https://docs.aws.amazon.com/vpn/latest/clientvpn-admin/what-is.html"),
       ("Client VPN authentication (SAML federation)", "https://docs.aws.amazon.com/vpn/latest/clientvpn-admin/client-authentication.html"),
       ("Forwarding outbound DNS queries to your network", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resolver-forwarding-outbound-queries.html")])

tfix("pro-20", {
 "A": ("Use target tracking scaling on ALBRequestCountPerTarget with ELB health checks and CloudWatch alarms on TargetResponseTime. Keep the checkpoint EBS volume, and use a lifecycle hook with an AWS Lambda function that detaches the volume from a terminated instance and attaches it to the replacement instance.",
       "ตกข้อ (2): scaling, health checks และ alarms ถูกต้อง แต่ EBS volume อยู่ใน AZ เดียว ถ้า replacement instance เกิดใน AZ อื่นหรือ AZ ของ volume ล่ม ก็ attach ไม่ได้ การย้าย volume ด้วย Lambda ยังเพิ่มความซับซ้อนและผูก recovery กับ AZ เดิม"),
 "B": ("Use target tracking scaling with ELB health checks and latency alarms. Replace the checkpoint volume with an io2 EBS volume that uses Multi-Attach so that every instance in the Auto Scaling group can mount it read/write.",
       "ตกข้อ (2): EBS Multi-Attach ใช้ได้เฉพาะ instance ใน AZ เดียวกับ volume และต้องใช้ cluster-aware file system เพื่อไม่ให้ข้อมูลเสียหายเมื่อเขียนพร้อมกัน จึงไม่รองรับ instance ทั้งสาม AZ และไม่ได้ทำให้ checkpoint ทนต่อการเสีย AZ"),
 "C": ("Use target tracking scaling on ALBRequestCountPerTarget with ELB health checks so that unhealthy instances are replaced, move the transaction checkpoints to Amazon DynamoDB, treat instance EBS volumes as disposable, and create CloudWatch alarms on ALB TargetResponseTime and HTTPCode_Target_5XX_Count.",
       "ถูก: scaling ตามจำนวน request ต่อ target สะท้อน demand จริง ELB health checks ให้ Auto Scaling แทนที่ instance ที่ไม่ healthy DynamoDB เป็นบริการระดับ Region ที่ทุก AZ เข้าถึงได้ checkpoint จึงไม่ผูกกับ EBS ใน AZ เดียว และ alarms บน latency/5xx ตรวจการละเมิด error budget ที่ลูกค้าเห็น แอปต้องปรับให้เขียน checkpoint แบบ idempotent"),
 "D": ("Move the transaction checkpoints to Amazon DynamoDB and use target tracking scaling on ALBRequestCountPerTarget. Rely on EC2 status checks for replacement and on the Auto Scaling group's default instance metrics, without additional alarms.",
       "ตกข้อ (3) และบางส่วนของ (1): checkpoint และ scaling ถูกต้อง แต่ EC2 status checks ตรวจได้แค่ปัญหาระดับ instance ไม่รู้ว่าแอปตอบ HTTP ผิดพลาด และไม่มี alarms บน latency หรือ error rate ที่ลูกค้าเห็น ทีมจึงไม่ได้รับการแจ้งเตือนเมื่อ error budget ถูกใช้หมด"),
},
 clue="scale ตาม demand ของแอปและแทน instance ที่เสียอัตโนมัติ, checkpoint ต้องไม่ผูกกับ EBS ใน AZ เดียว, ต้องมี alarm ด้าน latency/error",
 reasoning="1) EBS เป็น resource ระดับ AZ ทั้งการย้าย volume (A) และ Multi-Attach (B) จึงไม่ตอบข้อ (2) ต้องย้าย checkpoint ไปบริการระดับ Region เช่น DynamoDB หรือ EFS 2) ข้อ (1) ต้องใช้ ELB health checks เพื่อแทน instance ที่แอปเสีย ไม่ใช่เพียง EC2 status checks 3) ข้อ (3) ต้องมี CloudWatch alarms บน latency/5xx ซึ่ง D ไม่มี 4) C ครบทุกข้อ",
 refs=[("What is Amazon EC2 Auto Scaling?", "https://docs.aws.amazon.com/autoscaling/ec2/userguide/what-is-amazon-ec2-auto-scaling.html"),
       ("Target tracking scaling policies", "https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-target-tracking.html"),
       ("Attach a volume to multiple instances with EBS Multi-Attach", "https://docs.aws.amazon.com/ebs/latest/userguide/ebs-volumes-multi.html")])
