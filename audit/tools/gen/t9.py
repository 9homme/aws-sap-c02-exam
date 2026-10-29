from common import tfix

MQ_ISSUE = "prompt: 'commercial JMS broker' ทำให้คำตอบ Amazon MQ ไม่แน่นอน (Amazon MQ รองรับเฉพาะ ActiveMQ และ RabbitMQ) จึงระบุว่าเป็น ActiveMQ Classic"

tfix("pro-57", {
 "A": ("Publish both the business events and the telemetry to one Kinesis Data Streams stream, have each downstream application read every record and discard events it does not need, and connect Amazon Data Firehose to the stream for S3 delivery.",
       "ตกข้อ (1): KDS และ Firehose ตอบเรื่อง telemetry ได้ แต่การให้ทุก consumer อ่านทุก business event แล้วกรองเองใน code ไม่ใช่ rule-based routing และทุกแอปต้องรู้รูปแบบ event ทั้งหมด ทำให้ coupling สูงและเพิ่มภาระ throughput ของ stream"),
 "B": ("Use Amazon EventBridge rules for the business events, and send the telemetry directly to an Amazon Data Firehose delivery stream that writes encrypted batches to S3; the consumer teams reprocess telemetry from the S3 objects.",
       "ตกข้อ (2): EventBridge และ Firehose ถูกต้อง แต่ Firehose ไม่มี consumer API ที่หลายทีมอ่านแยกกันพร้อม checkpoint และไม่รักษาลำดับต่อ shard การอ่านซ้ำจาก S3 จึงไม่ใช่ replay ของ stream ตามตำแหน่งที่ทีมต้องการหลังแก้ defect"),
 "C": ("Use Amazon EventBridge rules for the business events and Kinesis Data Streams for the telemetry, and run an AWS Lambda consumer that batches telemetry records, encrypts them, and writes objects to S3.",
       "ตกข้อ (3): routing และ replayable stream ถูกต้อง แต่ Lambda ที่ batch, เข้ารหัส และเขียน S3 เองคือ custom writer ที่ต้องดูแล retry, ขนาดไฟล์ และ error handling เอง Firehose ทำงานนี้แบบ managed โดยอ่านจาก stream ได้โดยตรง"),
 "D": ("Use EventBridge event buses and rules for business events, Kinesis Data Streams for replayable telemetry, and Amazon Data Firehose delivery streams into S3 for buffered archiving.",
       "ถูก: EventBridge ส่ง business events ไปยัง target ต่าง ๆ ตาม rules โดย producer ไม่ต้องรู้จัก consumer Kinesis Data Streams เก็บ telemetry ตาม retention ที่ตั้งและรักษาลำดับต่อ shard ทีมต่าง ๆ อ่านและ replay ได้อิสระ ส่วน Firehose ใช้ stream เป็น source แล้ว buffer, เข้ารหัส และส่ง batch เข้า S3 แบบ managed"),
},
 clue="business events ต้อง route ตาม rules, telemetry ต้อง replay ได้หลาย consumer, ส่ง telemetry เข้า S3 แบบ managed",
 reasoning="1) แยกรูปแบบ event: business events ต้องการ content-based routing (EventBridge) ส่วน telemetry ต้องการ stream ที่ replay ได้ (KDS) และ delivery เข้า S3 (Firehose) 2) A ใช้ stream แทน routing 3) B ไม่มี stream ที่ replay ได้ 4) C เขียน delivery เอง 5) D แยกบริการตามหน้าที่ครบทั้งสามข้อ",
 refs=[("What is Amazon EventBridge?", "https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html"),
       ("What is Amazon Kinesis Data Streams?", "https://docs.aws.amazon.com/streams/latest/dev/introduction.html"),
       ("Send data to Firehose from Kinesis Data Streams", "https://docs.aws.amazon.com/firehose/latest/dev/writing-with-kinesis-streams.html")])

tfix("pro-58", {
 "A": ("Replace the broker with Amazon SQS queues on day one by using the Amazon SQS Java Messaging Library, store the database credentials in Secrets Manager with rotation, and keep the flags in Systems Manager Parameter Store.",
       "ตกข้อ (1): การจัดการ secret และ configuration ถูกต้อง แต่ JMS library ของ SQS ไม่รองรับ semantics ของ broker เดิมทั้งหมด เช่น request/reply ด้วย temporary queues และ message selectors การย้ายไป SQS ทันทีจึงต้องแก้ services ที่เกี่ยวข้องหลายสิบตัว"),
 "B": ("Use Amazon MQ for ActiveMQ for the messaging, and store the database passwords and the flags as Systems Manager Parameter Store parameters, with SecureString for the passwords that the operations team updates on the approved schedule.",
       "ตกข้อ (2): Amazon MQ ถูกต้อง แต่ Parameter Store ไม่มี managed rotation สำหรับรหัสผ่าน database การให้ทีมเปลี่ยนเองตามรอบไม่ใช่ purpose-built secret lifecycle และเสี่ยงต่อการลืมหรือเปลี่ยนไม่พร้อมกันระหว่าง database กับแอป"),
 "C": ("Use Amazon MQ with a compatible broker engine, Secrets Manager for database credential rotation, and Systems Manager Parameter Store for nonsecret flags and settings.",
       "ถูก: Amazon MQ for ActiveMQ รองรับ JMS, request/reply และ selectors client จึงเปลี่ยนเพียง endpoint Secrets Manager หมุนรหัสผ่าน database ตามตารางด้วย rotation function หรือ managed rotation และเข้ารหัสด้วย KMS ส่วน Parameter Store เก็บ flags ที่ไม่เป็นความลับพร้อม versioning และ IAM ตาม path แยกจาก secrets"),
 "D": ("Use Amazon MQ for ActiveMQ for the messaging, and store both the database credentials and all of the nonsecret feature flags and timeouts as secrets in AWS Secrets Manager with rotation enabled.",
       "ตกข้อ (3): Amazon MQ และการหมุน credentials ถูกต้อง แต่การเก็บ configuration ที่ไม่เป็นความลับหลายร้อยรายการเป็น secrets รวมสองประเภทเข้าด้วยกันตามที่องค์กรไม่ต้องการ เพิ่มค่าใช้จ่ายต่อ secret และ rotation ไม่มีความหมายสำหรับ feature flags"),
},
 clue="ต้องคง JMS semantics ตอน migration, หมุนรหัส database ด้วยบริการเฉพาะ, เก็บ config ธรรมดาแยกจาก secrets",
 reasoning="1) ข้อ (1) ต้องคง JMS broker จึงใช้ Amazon MQ ไม่ใช่ SQS ทันที (A) 2) ข้อ (2) credential rotation = Secrets Manager ไม่ใช่ Parameter Store ที่เปลี่ยนเอง (B) 3) ข้อ (3) config ที่ไม่เป็นความลับควรอยู่ใน Parameter Store ไม่ใช่รวมใน Secrets Manager (D) 4) C แยกบริการตามประเภทข้อมูลครบ",
 refs=[("What is Amazon MQ?", "https://docs.aws.amazon.com/amazon-mq/latest/developer-guide/welcome.html"),
       ("Rotate AWS Secrets Manager secrets", "https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets.html"),
       ("AWS Systems Manager Parameter Store", "https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html")],
 edits=[("uses a commercial JMS broker with", "uses an Apache ActiveMQ Classic JMS broker with")], extra_issue=MQ_ISSUE)

tfix("pro-59", {
 "A": ("Create an AWS KMS custom key store that is backed by an AWS CloudHSM cluster for the signing keys, use Amazon Inspector for EC2 and container image vulnerabilities, and use Amazon Macie for sensitive S3 data.",
       "ตกข้อ (1): Inspector และ Macie ถูกต้อง แต่ custom key store ยังต้องเรียกผ่าน KMS API และรองรับเฉพาะ symmetric encryption keys ไม่ได้ให้ library เรียก PKCS#11 โดยตรงหรือให้ลูกค้าถือ HSM credentials เอง vendor จึงต้องเขียน library ใหม่ซึ่งไม่ยอม"),
 "B": ("Use AWS CloudHSM for the PKCS#11 signing library, enable Amazon GuardDuty Malware Protection to find software vulnerabilities on EC2 instances and container images, and use Amazon Macie for sensitive S3 data.",
       "ตกข้อ (2): CloudHSM และ Macie ถูกต้อง แต่ GuardDuty Malware Protection สแกนหา malware เมื่อพบพฤติกรรมน่าสงสัย ไม่ใช่การประเมินช่องโหว่ของ software packages ตาม CVE Amazon Inspector เป็นบริการที่ทำหน้าที่นี้สำหรับ EC2, ECR images และ Lambda"),
 "C": ("Use AWS CloudHSM for the PKCS#11 signing library and Amazon Inspector for EC2 and container image vulnerabilities, and configure Amazon Inspector to also scan the S3 support documents for personal information.",
       "ตกข้อ (3): CloudHSM และ Inspector ถูกต้องในหน้าที่ของตัวเอง แต่ Inspector ไม่สแกนเนื้อหา object ใน S3 เพื่อหาข้อมูลส่วนบุคคล การค้นหาและจำแนก sensitive data ใน S3 เป็นหน้าที่ของ Amazon Macie"),
 "D": ("Use AWS CloudHSM for compatible HSM signing, Amazon Inspector for applicable compute/image vulnerabilities, and Amazon Macie for sensitive S3 data discovery.",
       "ถูก: CloudHSM ให้ HSM แบบ single-tenant ที่ลูกค้าคุม crypto user credentials และมี PKCS#11 library ให้แอป signing ใช้โดยไม่ต้องเขียนใหม่ Inspector สแกนช่องโหว่ของ EC2 และ container images อย่างต่อเนื่อง ส่วน Macie ใช้ managed และ custom data identifiers ค้นหา PII ใน S3 แต่ละบริการดูแล asset คนละประเภท"),
},
 clue="signing ต้องใช้ PKCS#11 และ HSM ที่ลูกค้าคุมเอง, สแกนช่องโหว่ EC2/container, ค้นหา PII ใน S3 แยกจากการสแกนช่องโหว่",
 reasoning="1) แต่ละ asset ใช้บริการต่างกัน: crypto ที่ต้องการ PKCS#11 = CloudHSM, software vulnerabilities = Inspector, sensitive data ใน S3 = Macie 2) A ใช้ KMS custom key store ที่ไม่ให้ PKCS#11 3) B ใช้ GuardDuty แทน Inspector 4) C ใช้ Inspector แทน Macie 5) D จับคู่ถูกต้องทั้งหมด ไม่ใช้ key-management product เป็น detector ทุกอย่าง",
 refs=[("What is AWS CloudHSM?", "https://docs.aws.amazon.com/cloudhsm/latest/userguide/introduction.html"),
       ("What is Amazon Inspector?", "https://docs.aws.amazon.com/inspector/latest/user/what-is-inspector.html"),
       ("What is Amazon Macie?", "https://docs.aws.amazon.com/macie/latest/user/what-is-macie.html")])

tfix("pro-60", {
 "A": ("Use AWS Transform for server discovery and migration-wave tracking, AWS SCT for assessment/conversion of incompatible database schema and procedures, and AWS DMS for initial full load with ongoing CDC before cutover.",
       "ถูก: AWS Transform รวบรวม utilization และ dependencies เพื่อจัด migration waves และให้มุมมองความคืบหน้าแบบรวมศูนย์สำหรับลูกค้าใหม่ AWS SCT (หรือ DMS Schema Conversion) ประเมินและแปลง stored procedures/data types ที่ไม่เข้ากัน ส่วน DMS ทำ full load แล้ว CDC ต่อเนื่องจนถึงช่วง cutover โดยแยกเครื่องมือ database ออกจาก portfolio discovery ตามโจทย์"),
 "B": ("Deploy AWS Application Discovery Service agents and track the portfolio in AWS Migration Hub, use AWS SCT for schema conversion, and use AWS DMS full load plus CDC for the database.",
       "ตกข้อ (1)(2): SCT และ DMS ถูกต้อง แต่ AWS Migration Hub และ Application Discovery Service ไม่เปิดให้ลูกค้าใหม่แล้ว บริษัทที่ไม่เคยใช้จึงเริ่มใช้ไม่ได้ในปี 2026 ต้องใช้ AWS Transform สำหรับ discovery และ portfolio tracking"),
 "C": ("Use AWS Transform for server discovery and migration-wave tracking, and use AWS DMS full load plus CDC to move the database directly to the PostgreSQL-compatible target and convert the stored procedures automatically.",
       "ตกข้อ (3): discovery และ DMS CDC ถูกต้อง แต่ DMS ย้ายข้อมูลและสร้างตารางพื้นฐานเท่านั้น ไม่แปลง stored procedures หรือ data types ที่ไม่เข้ากันระหว่าง engine ต้องใช้ SCT หรือ DMS Schema Conversion ทดสอบการแปลงก่อน"),
 "D": ("Use AWS Transform for server discovery and migration-wave tracking and AWS SCT for schema conversion, and then stop all writes and run a one-time AWS DMS full-load task during an extended outage.",
       "ตกข้อ (3): discovery และการแปลง schema ถูกต้อง แต่ full load อย่างเดียวต้องหยุด business systems นานตลอดการโหลดข้อมูล ซึ่งขัดกับข้อกำหนดที่ระบบต้องเปลี่ยนข้อมูลได้จนถึง cutover ต้องใช้ full load ต่อด้วย CDC"),
},
 clue="ลูกค้าใหม่ปี 2026 ต้องการ discovery + wave + progress view, database ต้องแปลง schema/procedures และ full load + CDC",
 reasoning="1) ตรวจ availability: Migration Hub และ ADS ไม่รับลูกค้าใหม่ ตัด B 2) AWS Transform ตอบข้อ (1)(2) 3) database migration แบบ heterogeneous มีสองส่วน: แปลง schema/code (SCT) และย้ายข้อมูลที่เปลี่ยนตลอดด้วย full load + CDC (DMS) 4) C ขาด SCT และ D ขาด CDC 5) A ครบทุกข้อ",
 refs=[("AWS Migration Hub availability change", "https://docs.aws.amazon.com/migrationhub/latest/ug/migrationhub-availability-change.html"),
       ("What is the AWS Schema Conversion Tool?", "https://docs.aws.amazon.com/SchemaConversionTool/latest/userguide/CHAP_Welcome.html"),
       ("Creating tasks for ongoing replication using AWS DMS", "https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Task.CDC.html")])

tfix("pro-61", {
 "A": ("Order AWS Snowball Edge Storage Optimized devices to move the 1.1 PB collection, use AWS Transfer Family SFTP endpoints with scoped S3 access for the partners, and reconcile checksums after the import.",
       "ตกข้อ (1): Transfer Family และการ reconcile ถูกต้อง แต่ AWS Snowball Edge ไม่เปิดให้ลูกค้าใหม่แล้ว บริษัทที่ใช้ Snow Family ครั้งแรกจึงสั่งอุปกรณ์ไม่ได้ในปี 2026 AWS Data Transfer Terminal เป็นทางเลือก physical transfer ที่ใช้ได้"),
 "B": ("Use AWS Data Transfer Terminal sessions to ingest encrypted portable drives at high speed into S3, verify the imported data and reconcile deltas; use AWS Transfer Family SFTP endpoints with scoped S3 access for daily partner feeds.",
       "ถูก: Data Transfer Terminal ให้นำอุปกรณ์ของบริษัทไปอัปโหลดเข้า S3 ผ่านเครือข่ายความเร็วสูงโดยไม่พึ่ง WAN 100 Mbps หลังนำเข้าต้องเทียบ checksum และย้ายไฟล์ที่เปลี่ยนหลังการคัดลอก (delta) ก่อน cutover Transfer Family ให้ managed SFTP endpoint โดยกำหนด IAM role และ logical directory ต่อ partner เพื่อจำกัด S3 prefix ที่เขียนได้"),
 "C": ("Use AWS DataSync over the 100 Mbps WAN with the bandwidth limit set to the full circuit speed to transfer the 1.1 PB collection, and use AWS Transfer Family SFTP endpoints for the partners.",
       "ตกข้อ (1): DataSync เป็นเครื่องมือ online transfer ที่ดี แต่ 100 Mbps รับข้อมูลได้ราว 1 TB ต่อวันในกรณีดีที่สุด 1.1 PB จึงใช้เวลาประมาณสามปี ซึ่งพลาดกำหนดปิด site อย่างแน่นอน"),
 "D": ("Use AWS Data Transfer Terminal to upload the drives into S3 and treat the imported copy as final at cutover. Create one shared AWS Transfer Family SFTP user with write access to the whole bucket for all partners.",
       "ตกข้อ (3): บริการถูกเลือกถูกต้อง แต่การถือว่าข้อมูลที่ขนย้ายไปตรงกับต้นทางโดยไม่ตรวจ checksum และไม่ย้ายไฟล์ที่เปลี่ยนภายหลังเสี่ยงข้อมูลไม่ครบ ส่วนผู้ใช้ SFTP ร่วมที่เขียนได้ทั้ง bucket ขัดกับ identity boundaries และ S3 prefixes ที่ควบคุมได้"),
},
 clue="1.1 PB บน WAN 100 Mbps, ลูกค้า Snow Family ครั้งแรก, partner ใช้ SFTP เดิม, ต้อง reconcile และกำหนด identity/prefix ต่อ partner",
 reasoning="1) คำนวณ: 100 Mbps ≈ 1 TB/วัน 1.1 PB จึงต้องใช้ physical transfer ตัด DataSync (C) 2) Snowball Edge ไม่รับลูกค้าใหม่ ตัด A 3) ข้อ (3) ต้องตรวจ checksum, ย้าย delta และแยกสิทธิ์ต่อ partner ตัด D ที่ถือว่าสำเนาสมบูรณ์และใช้ผู้ใช้ร่วม 4) B ใช้ Data Transfer Terminal + Transfer Family พร้อมแผน reconcile ครบ",
 refs=[("AWS Data Transfer Terminal technical requirements", "https://docs.aws.amazon.com/datatransferterminal/latest/userguide/tech-requirements.html"),
       ("AWS Snowball Edge availability change", "https://docs.aws.amazon.com/snowball/latest/developer-guide/snowball-edge-availability-change.html"),
       ("Logical directories for AWS Transfer Family", "https://docs.aws.amazon.com/transfer/latest/userguide/logical-dir-mappings.html")])

tfix("pro-62", {
 "A": ("Follow the consultant's recommendation: purchase 3-year Reserved Instances centrally for all EC2 usage, and rely on AWS Organizations consolidated billing invoices for financial monitoring and on the reservations to standardize accounts.",
       "ตกข้อ (1)(2)(3): Reserved Instances เป็นส่วนลดราคาเท่านั้น ไม่ได้สร้างบัญชีหรือบังคับ governance และใบแจ้งหนี้รวมไม่ใช่ cost analysis แบบ tag/service หรือการแจ้งเตือนก่อนเกินงบ อีกทั้งการซื้อแทนทุกหน่วยธุรกิจขัดกับการให้แต่ละหน่วยประเมินเอง"),
 "B": ("Use AWS Organizations and AWS Control Tower for account onboarding, create Amazon CloudWatch billing alarms on EstimatedCharges in the management account for finance, and let business units assess Reserved Instances separately.",
       "ตกข้อ (2): governance และ RI ถูกต้อง แต่ billing alarm ดูได้เพียงยอดรวมโดยประมาณ ไม่ได้วิเคราะห์ตาม linked account, cost allocation tag หรือ service และไม่ได้แจ้งเตือนรายโครงการตามงบที่กำหนดได้เหมือน Cost Explorer กับ AWS Budgets"),
 "C": ("Use Organizations and Control Tower for governed landing-zone account onboarding, Cost Explorer for linked-account cost trends, and AWS Budgets for threshold alerts; assess RI suitability separately.",
       "ถูก: Control Tower Account Factory สร้างบัญชีตาม baseline ที่อนุมัติในแต่ละ OU โดยคงการแยกบัญชีของบริษัทลูก Cost Explorer วิเคราะห์ spend ตาม linked account, cost allocation tags และ service AWS Budgets แจ้งเตือนเมื่อค่าใช้จ่ายจริงหรือที่คาดการณ์ใกล้ threshold ส่วน RI เป็นการตัดสินใจด้าน cost optimization ที่แต่ละหน่วยประเมินจาก workload ที่คงที่"),
 "D": ("Use Organizations and Control Tower for account onboarding and Cost Explorer with AWS Budgets for finance, and purchase 3-year Reserved Instances in the management account for every running EC2 instance in all subsidiaries now.",
       "ตกข้อ (3): governance และ finance tools ถูกต้อง แต่การซื้อ RI ระยะ 3 ปีให้ทุก instance ทันทีข้ามการประเมินว่า workload ใดคงที่จริง และขัดกับข้อกำหนดให้หน่วยธุรกิจตัดสินใจเอง เสี่ยงจ่ายค่า reservation ที่ไม่ถูกใช้เมื่อ workload เปลี่ยน"),
},
 clue="standardize การสร้างบัญชีโดยแยกบริษัทลูก, วิเคราะห์ cost ข้ามบัญชี + budget alerts, RI เป็นเรื่อง cost optimization ที่ประเมินแยก",
 reasoning="1) แยกสามเรื่อง: governance (Organizations + Control Tower), visibility/alerts (Cost Explorer + Budgets), purchasing commitment (RI) 2) A ใช้ RI แทนทุกอย่างตามที่ consultant เสนอ ซึ่งผิดหน้าที่ 3) B ใช้ billing alarm แทน Cost Explorer/Budgets 4) D ซื้อ RI โดยไม่ประเมิน 5) C แยกหน้าที่ถูกต้องครบทั้งสามข้อ",
 refs=[("What is AWS Control Tower?", "https://docs.aws.amazon.com/controltower/latest/userguide/what-is-control-tower.html"),
       ("Managing your costs with AWS Budgets", "https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html"),
       ("Reserved Instances for Amazon EC2", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-reserved-instances.html")])

tfix("pro-63", {
 "A": ("Use Amazon MQ for the legacy JMS clients and also publish the cloud business events and the point-of-sale telemetry to Amazon MQ topics, with consumer applications writing the telemetry to S3.",
       "ตกข้อ (2)(3): Amazon MQ ตอบเรื่อง JMS ได้ แต่ broker ไม่ได้ทำ declarative event routing ตาม attributes แบบ EventBridge ข้อความใน queue ถูกลบเมื่อ consume แล้วจึง replay ไม่ได้ และยังต้องเขียน consumer ที่เขียน S3 เอง ใช้ผลิตภัณฑ์เดียวกับ semantics ที่ต่างกันตามที่วิศวกรเตือน"),
 "B": ("Use Amazon MQ for legacy compatible JMS clients, EventBridge for cloud business event rules, Kinesis Data Streams for replayable POS telemetry and Data Firehose for S3 delivery.",
       "ถูก: Amazon MQ for ActiveMQ รองรับ JMS producers/consumers และ acknowledgement modes เดิมโดยไม่แก้ binaries EventBridge rules ส่ง business events ไปยัง target ตาม attributes Kinesis Data Streams ให้สอง processors อ่านและ replay telemetry ได้อิสระ และ Firehose อ่านจาก stream แล้ว batch เข้า S3 แบบ managed แต่ละบริการตรงกับ delivery semantics ของตัวเอง"),
 "C": ("Use Amazon MQ for the legacy JMS clients and EventBridge rules for the business events, and send the point-of-sale telemetry directly to Amazon Data Firehose for S3 delivery, with both analytics processors reading the delivered S3 objects.",
       "ตกข้อ (2): JMS, routing และ S3 delivery ถูกต้อง แต่ Firehose ไม่ใช่ stream ที่ consumer หลายตัวอ่านและ replay ตามตำแหน่งได้ processors ต้องรอข้อมูลถูก buffer เป็น object และไม่ได้ checkpoint ของตัวเองแบบ Kinesis Data Streams"),
 "D": ("Rewrite the acquired system's messaging to Amazon SQS with the Amazon SQS Java Messaging Library, use EventBridge rules for business events, Kinesis Data Streams for telemetry, and Amazon Data Firehose for S3 delivery.",
       "ตกข้อ (1): ฝั่ง cloud-native ถูกต้อง แต่บริษัทตกลงไว้ว่าจะไม่เปลี่ยน binaries ใน wave แรก และ JMS library ของ SQS ก็ไม่รองรับ semantics ของ broker ทั้งหมด จึงต้องคง broker ที่เข้ากันได้อย่าง Amazon MQ ไว้ก่อน"),
},
 clue="JMS binaries ห้ามเปลี่ยนใน wave แรก, business events ต้อง route ตาม rules, telemetry ต้อง replay ได้สอง processors, archive เข้า S3 แบบ managed",
 reasoning="1) แยก semantics: message queue/JMS (Amazon MQ), event routing (EventBridge), replayable stream (Kinesis Data Streams), delivery pipeline (Firehose) 2) A ใช้ MQ กับทุกอย่าง 3) C ไม่มี stream ที่ replay ได้ 4) D เปลี่ยน JMS binaries ซึ่งขัดสัญญา 5) B ใช้บริการตรงกับแต่ละ semantics ครบทั้งสามข้อ",
 refs=[("What is Amazon MQ?", "https://docs.aws.amazon.com/amazon-mq/latest/developer-guide/welcome.html"),
       ("What is Amazon EventBridge?", "https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html"),
       ("Send data to Firehose from Kinesis Data Streams", "https://docs.aws.amazon.com/firehose/latest/dev/writing-with-kinesis-streams.html")],
 edits=[("using broker-specific acknowledgements", "connected to an Apache ActiveMQ Classic broker over OpenWire with client-acknowledge mode")], extra_issue=MQ_ISSUE)
