from common import tfix

tfix("pro-31", {
 "A": ("Run the custom Spark jobs on a long-running Amazon EMR cluster on EC2 that stays up between campaigns, use the AWS Glue Data Catalog as the metastore, and query curated tables in Amazon Redshift.",
       "ตกข้อ (1) ด้าน elastic capacity: EMR รองรับ Spark และ third-party libraries ได้ Glue Catalog และ Redshift ถูกต้อง แต่ cluster ที่เปิดค้างไว้ระหว่าง campaign คือสิ่งที่ทีมต้องการเลี่ยง ต้องจ่ายค่า EC2 ช่วงว่างและดูแล cluster เอง EMR Serverless หรือ cluster ชั่วคราวให้ capacity ตามงานได้ดีกว่า"),
 "B": ("Use Amazon EMR on an appropriate managed execution mode for custom Spark jobs, stage data in S3 and Glue Data Catalog, and query curated warehouse tables using Redshift.",
       "ถูก: EMR (เช่น EMR Serverless หรือ cluster ชั่วคราว) รัน Spark ที่มี Java libraries ภายนอกและ graph algorithms ได้ โดยจ่ายเฉพาะช่วงที่มีงาน Glue Data Catalog เก็บ schema ของ datasets ใน S3 ให้ EMR, Athena และ Redshift Spectrum ใช้ร่วมกัน ส่วน Redshift ให้ warehouse สำหรับ join ซ้ำ ๆ และ BI ที่ต้องการประสิทธิภาพคงที่"),
 "C": ("Run the Spark jobs on Amazon EMR Serverless with the AWS Glue Data Catalog as the metastore, and have the reporting department run all BI and join queries with Amazon Athena on the curated S3 data instead of using a data warehouse.",
       "ตกข้อ (2): EMR Serverless และ Glue Catalog ถูกต้อง แต่โจทย์ต้องการคง interactive data warehouse สำหรับ fact/dimension joins และ BI ซ้ำ ๆ Athena เหมาะกับ ad hoc query บน S3 แต่ประสิทธิภาพของ dashboard ที่ join หนักและใช้พร้อมกันจำนวนมากคาดเดาได้ยากกว่า Redshift"),
 "D": ("Run the Spark jobs on Amazon EMR Serverless with a separate Hive metastore defined in each job, and load the curated data into Amazon Redshift tables with COPY commands that define their own table schemas.",
       "ตกข้อ (3): compute และ warehouse เลือกได้ดี แต่การให้แต่ละงานนิยาม schema เองโดยไม่มี catalog กลาง ทำให้ data engineering และ analytics ค้นหา dataset เดียวกันไม่ได้และต้องนิยาม schema ซ้ำ ขัดกับข้อกำหนดให้ใช้ cataloged S3 datasets ร่วมกัน"),
},
 clue="Spark แบบ custom ที่มี third-party libraries และ capacity ตามงาน, ต้องคง data warehouse สำหรับ BI, ใช้ catalog กลางสำหรับ datasets ใน S3",
 reasoning="1) ข้อ (1) งาน Spark custom ต้องการ EMR ที่ไม่เปิดค้างระหว่าง campaign จึงตัด long-running cluster (A) 2) ข้อ (2) โจทย์ต้องการคง warehouse ตัด Athena-only (C) 3) ข้อ (3) ต้องมี Glue Data Catalog กลางให้ทุกเครื่องมือใช้ schema เดียวกัน ตัด D ที่นิยาม schema แยก 4) B แบ่งหน้าที่ EMR สำหรับ transform, S3 + Glue Catalog สำหรับ staging/discovery และ Redshift สำหรับ BI",
 refs=[("What is Amazon EMR?", "https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-what-is-emr.html"),
       ("What is Amazon EMR Serverless?", "https://docs.aws.amazon.com/emr/latest/EMR-Serverless-UserGuide/emr-serverless.html"),
       ("Using the AWS Glue Data Catalog as the metastore for Spark", "https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-spark-glue.html")])

tfix("pro-32", {
 "A": ("Use AWS DMS with a full load plus change data capture task from SQL Server to Amazon Aurora PostgreSQL-Compatible Edition, and let DMS create the target tables and convert the stored procedures during the migration.",
       "ตกข้อ (1): DMS ย้ายข้อมูลและ replicate การเปลี่ยนแปลงได้ดี แต่สร้างเพียงโครงสร้างตารางพื้นฐานและไม่แปลง stored procedures, functions หรือ proprietary data types ระหว่าง engine ต่างชนิด ต้องใช้ AWS SCT หรือ DMS Schema Conversion ประเมินและแปลง code ก่อน"),
 "B": ("Use AWS SCT to convert the schema and stored procedures to Aurora PostgreSQL, stop all application writes, and run a one-time AWS DMS full-load task before switching the application to Aurora.",
       "ตกข้อ (2): การแปลง schema ถูกต้อง แต่ full load อย่างเดียวต้องหยุด write ตลอดเวลาที่โหลดข้อมูลขนาดใหญ่ ซึ่งอาจนานหลายวัน ขัดกับ downtime ไม่กี่นาที ต้องเพิ่ม CDC เพื่อ replicate การเปลี่ยนแปลงระหว่างที่แอปยังรับ transaction"),
 "C": ("Use AWS SCT to assess and convert compatible schema/code, AWS DMS for full-load plus CDC migration, and Aurora PostgreSQL as the managed target.",
       "ถูก: SCT (หรือ DMS Schema Conversion) ทำ assessment report และแปลง schema/stored procedures ส่วนที่แปลงอัตโนมัติไม่ได้ให้วิศวกรแก้ก่อน cutover DMS ทำ full load แล้วต่อด้วย CDC จาก transaction log ของ SQL Server ทำให้ cutover ใช้เวลาเพียงช่วงหยุด write สั้น ๆ Aurora PostgreSQL เป็น managed target ไม่ต้องดูแล host ต้องเปิด prerequisites ของ CDC บน SQL Server เช่น MS-CDC หรือ MS-Replication"),
 "D": ("Use AWS SCT to convert the schema and code, use AWS DMS full load plus CDC, and target a PostgreSQL database that runs on Amazon EC2 instances in two Availability Zones with streaming replication.",
       "ตกข้อ (3): ขั้นตอน migration ถูกต้อง แต่ target บน EC2 ทำให้ทีมต้องดูแล PostgreSQL, replication, failover และ backup เอง ซึ่งโจทย์ต้องการ managed PostgreSQL-compatible target อย่าง Aurora หรือ RDS"),
},
 clue="SQL Server → PostgreSQL ที่มี stored procedures, downtime ไม่กี่นาทีจึงต้อง full load + CDC, target ต้องเป็น managed",
 reasoning="1) heterogeneous migration มีสองงานแยกกัน: แปลง schema/code และย้ายข้อมูลที่เปลี่ยนตลอดเวลา 2) ข้อ (1) DMS ไม่แปลง stored procedures ตัด A 3) ข้อ (2) downtime ไม่กี่นาทีต้องมี CDC ตัด full load อย่างเดียว (B) 4) ข้อ (3) target ต้อง managed ตัด EC2 (D) C จึงครบ: SCT แปลง, DMS full load + CDC, Aurora PostgreSQL",
 refs=[("What is AWS Database Migration Service?", "https://docs.aws.amazon.com/dms/latest/userguide/Welcome.html"),
       ("What is the AWS Schema Conversion Tool?", "https://docs.aws.amazon.com/SchemaConversionTool/latest/userguide/CHAP_Welcome.html"),
       ("Using SQL Server as a source for AWS DMS (CDC prerequisites)", "https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.SQLServer.html")])

tfix("pro-33", {
 "A": ("Use EventBridge rules for event routing, an SQS queue with a DLQ for warehouse processing, and SNS for notification fanout. Implement fulfillment as a chain of Lambda functions that invoke each other and handle retries and compensation in code.",
       "ตกข้อ (3): routing, buffering และ fanout ถูกต้อง แต่ Lambda ที่เรียกต่อกันเองต้องเก็บ state, wait, retry และ compensation ใน code ไม่มี state transitions ที่ชัดเจนหรือ execution history ให้ติดตาม end-to-end Step Functions ให้สิ่งเหล่านี้แบบ managed"),
 "B": ("Use EventBridge rules for event routing and Step Functions for fulfillment. Subscribe the warehouse Lambda function and the notification endpoints directly to an SNS topic that receives all order events.",
       "ตกข้อ (2): SNS fanout เหมาะกับ notification แต่ warehouse service ที่ subscribe ตรงกับ SNS ไม่มีคิวพักงานช่วง burst หาก consumer ถูก throttle หรือล้ม message จะ retry ตามนโยบายของ SNS แล้วไป DLQ ของ subscription เท่านั้น ไม่ได้ buffer และควบคุมอัตราการประมวลผลแบบ SQS"),
 "C": ("Have each producer service publish order events directly to the warehouse SQS queue and to the notification SNS topic, and use Step Functions for fulfillment.",
       "ตกข้อ (1): SQS, SNS และ Step Functions ถูกต้องในหน้าที่ของตัวเอง แต่ producer ต้องรู้จักทุก consumer และต้องแก้ code ทุกครั้งที่มีทีมใหม่ต้องการ event ซึ่งเป็น tight coupling ที่โจทย์ห้าม EventBridge rules ให้ filter ตาม source, detail-type และ attributes โดยไม่แตะ producer"),
 "D": ("Use EventBridge rules for event routing, an SQS queue with DLQ for warehouse processing, SNS for notification fanout where suitable, and Step Functions for the fulfillment orchestration.",
       "ถูก: EventBridge event bus รับ event จากทุก service และใช้ rules กรองตาม source, detail-type และ attributes ส่งไปยัง target ใหม่โดยไม่แก้ producer SQS พร้อม DLQ พักงาน burst และแยก poison messages SNS กระจาย notification ไปหลาย endpoints ส่วน Step Functions จัดการ workflow หลายขั้นตอนพร้อม Wait, Retry/Catch และ execution history"),
},
 clue="routing ตาม source/detail-type โดยไม่แก้ producer, consumer สำคัญต้องมี buffer + DLQ, notification fanout, workflow หลายขั้นที่มี error transitions",
 reasoning="1) แต่ละบริการมีบทบาทเฉพาะ: EventBridge = content-based routing, SQS = buffer/retry/DLQ, SNS = push fanout, Step Functions = stateful orchestration 2) C ให้ producer ส่งตรงถึง consumer จึง coupling สูง 3) B ข้าม SQS ทำให้ warehouse ไม่มี buffer 4) A ใช้ Lambda chain แทน workflow ที่มี state ชัดเจน 5) D วางทุกบริการตรงกับหน้าที่ จึงครบทั้งสามข้อ",
 refs=[("What is Amazon EventBridge?", "https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html"),
       ("Amazon SQS dead-letter queues", "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html"),
       ("Handling errors in Step Functions workflows", "https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html")])

tfix("pro-34", {
 "A": ("Publish to Kinesis Data Streams for replayable stream consumption, connect a managed Amazon Data Firehose delivery stream to S3, and use Lambda for eligible record transforms when needed.",
       "ถูก: Kinesis Data Streams เก็บข้อมูลตาม retention ที่ตั้ง ให้ consumer หลายตัวอ่านและเก็บ checkpoint ของตัวเองได้ (เช่นด้วย KCL หรือ enhanced fan-out) จึง replay ได้ Firehose ใช้ stream นี้เป็น source แล้ว buffer, บีบอัด, retry และส่งเข้า S3 แบบ managed โดยใช้ Lambda transform เมื่อจำเป็น producer เขียนเข้า stream โดยไม่ต้องรอ consumer"),
 "B": ("Send the telemetry directly to an Amazon Data Firehose delivery stream that writes compressed objects to S3, and have the fraud-detection consumer read new objects from S3 as they arrive.",
       "ตกข้อ (1): Firehose ส่งข้อมูลเข้า S3 ได้ดี แต่ไม่มี consumer API ให้หลายตัวอ่านและ replay พร้อม checkpoint ข้อมูลถูก buffer เป็นนาทีก่อนเขียนเป็น object การอ่านจาก S3 จึงช้ากว่า near-real-time และไม่ใช่ stream ที่ replay ตามตำแหน่งได้"),
 "C": ("Publish to Kinesis Data Streams for the fraud-detection consumer, and add a second consumer Lambda function that batches records in memory, compresses them, and writes objects to S3 with custom retry logic.",
       "ตกข้อ (2): Kinesis Data Streams ตอบข้อ (1)(3) ได้ แต่การเขียน Lambda ที่รวม batch, บีบอัด, ตั้งชื่อ object และ retry เอง คือ custom data-delivery infrastructure ที่ Firehose ทำให้แบบ managed อยู่แล้ว ทั้งยังต้องจัดการกรณี batch ใหญ่หรือ function timeout เอง"),
 "D": ("Send the telemetry to an Amazon SQS standard queue, have the fraud-detection service poll the queue, and use a second queue that is subscribed through Amazon SNS for analytics delivery to S3.",
       "ตกข้อ (1): SQS แยก producer ออกจาก consumer ได้ แต่ message ถูกลบเมื่อประมวลผลแล้ว จึง replay ย้อนหลังไม่ได้ และไม่มี checkpoint ตามตำแหน่งแบบ stream อีกทั้งยังต้องเขียนส่วนที่ batch ข้อมูลเข้า S3 เองอีกด้วย"),
},
 clue="consumer หลายตัวที่ replay ได้พร้อม checkpoint ของตัวเอง, ส่งเข้า S3 แบบ buffer/compress โดยไม่เขียน delivery เอง, producer แยกจาก consumer",
 reasoning="1) แยกบทบาท: replayable stream (Kinesis Data Streams) กับ managed delivery pipeline (Firehose) 2) ข้อ (1) ต้องการ replay และ checkpoint ตัด Firehose ตรง (B) และ SQS (D) ที่ลบ message หลังอ่าน 3) ข้อ (2) ห้ามเขียน delivery เอง ตัด Lambda ที่ batch เข้า S3 เอง (C) 4) A ใช้ KDS เป็นแกนกลางและให้ Firehose อ่านจาก stream เพื่อส่งเข้า S3 จึงครบทั้งสามข้อ",
 refs=[("What is Amazon Data Firehose?", "https://docs.aws.amazon.com/firehose/latest/dev/what-is-this-service.html"),
       ("What is Amazon Kinesis Data Streams?", "https://docs.aws.amazon.com/streams/latest/dev/introduction.html"),
       ("Send data to Firehose from Kinesis Data Streams", "https://docs.aws.amazon.com/firehose/latest/dev/writing-with-kinesis-streams.html")])

tfix("pro-35", {
 "A": ("Replace the broker with Amazon SQS queues and use the Amazon SQS Java Messaging Library so that the application can keep calling JMS interfaces.",
       "ตกข้อ (3): library นี้ให้ JMS interface บางส่วนบน SQS แต่ไม่รองรับความสามารถของ broker เดิมทั้งหมด เช่น JMS transactions, request/reply ด้วย temporary queues และ routing semantics บางรูปแบบ การย้ายไป SQS จึงเป็น replatform ที่โจทย์ระบุให้ทำภายหลัง"),
 "B": ("Deploy Amazon MQ with a supported broker engine and suitable high-availability configuration, preserve compatible client endpoints and protocols, and plan SQS replatforming separately.",
       "ถูก: Amazon MQ for ActiveMQ รองรับ JMS ผ่าน OpenWire และ protocol มาตรฐานอื่น client เดิมจึงเปลี่ยนเพียง endpoint และ credentials การใช้ active/standby broker ข้ามสอง AZ ทำให้ทนต่อการเสีย AZ โดยเก็บข้อความใน durable storage AWS ดูแล patching และมี CloudWatch metrics ส่วนการย้ายไป SQS ทำเป็นโครงการ modernization แยกภายหลัง"),
 "C": ("Deploy a single-instance Amazon MQ for ActiveMQ broker, point the existing clients at the new broker endpoint, and rely on daily broker configuration backups for recovery.",
       "ตกข้อ (2): protocol และ client ใช้ได้ทันที แต่ single-instance broker อยู่ใน AZ เดียว เมื่อ instance หรือ AZ ล้มบริการจะหยุดจนกว่าจะกู้คืน และ configuration backup ไม่ได้ปกป้องข้อความที่ค้างอยู่ใน queue ต้องใช้ active/standby deployment"),
 "D": ("Install Apache ActiveMQ Classic on EC2 instances in an Auto Scaling group across two Availability Zones with a shared Amazon EFS file system for the message store, and patch the brokers with Systems Manager.",
       "ตกข้อ (2): ทำงานได้และคงความเข้ากันได้ของ client แต่ทีมต้องดูแลการติดตั้ง, failover, patching และ monitoring ของ broker เอง ซึ่ง operations ต้องการให้เป็น managed Amazon MQ ทำสิ่งเดียวกันนี้ให้แบบ managed"),
},
 clue="client JMS เดิมแก้ไม่ได้ใน 6 สัปดาห์, ต้องการ managed broker ที่ HA และไม่เสีย message, ห้ามบังคับ semantics เดิมเข้า SQS",
 reasoning="1) ข้อ (1)(3) ต้องคง protocol และ semantics ของ JMS broker จึงตัดการย้ายไป SQS (A) แม้มี JMS library 2) ข้อ (2) ต้องเป็น managed และ HA ตัด single-instance (C) และ self-managed บน EC2 (D) 3) B ใช้ Amazon MQ แบบ active/standby ข้าม AZ ซึ่งเข้ากันได้กับ client เดิม แล้วจึงวางแผน modernization ไป SQS แยกภายหลัง",
 refs=[("What is Amazon MQ?", "https://docs.aws.amazon.com/amazon-mq/latest/developer-guide/welcome.html"),
       ("Amazon MQ for ActiveMQ broker deployment options", "https://docs.aws.amazon.com/amazon-mq/latest/developer-guide/amazon-mq-broker-architecture.html"),
       ("Amazon SQS Java Messaging Library (JMS)", "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-java-message-service-jms-client.html")],
 edits=[("built around a commercial message broker, with JMS APIs,", "built around an Apache ActiveMQ Classic message broker, with JMS APIs over the OpenWire protocol,")],
 extra_issue="prompt: 'commercial message broker' ทำให้คำตอบ Amazon MQ ไม่แน่นอน (Amazon MQ รองรับเฉพาะ ActiveMQ และ RabbitMQ) จึงระบุว่าเป็น ActiveMQ Classic + OpenWire")
