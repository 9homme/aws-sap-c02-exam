from common import tfix

tfix("pro-26", {
 "A": ("Use Storage Gateway File Gateway for on-site SMB caching and S3-backed files, AWS DataSync for bulk transfer jobs, and AWS Backup for supported AWS backup plans.",
       "ถูก: S3 File Gateway ให้ SMB share ภายในโรงงานพร้อม local cache สำหรับไฟล์ที่ใช้บ่อย โดยเก็บข้อมูลจริงใน S3 DataSync ย้ายข้อมูลหลายร้อย TB พร้อม metadata, การตรวจสอบความถูกต้อง และการจำกัด bandwidth ผ่าน agent ที่ลบได้เมื่อย้ายเสร็จ ส่วน AWS Backup ใช้ backup plans, vault และ cross-account copy แทน cron scripts ต้องวางแผน ACL ของ SMB ให้สอดคล้องกับ AD"),
 "B": ("Use an S3 File Gateway for on-site SMB caching and AWS DataSync for the historical transfer. After migration, run Amazon EventBridge Scheduler rules that invoke AWS Lambda functions in each account to create snapshots and delete old ones.",
       "ตกข้อ (3): สองส่วนแรกถูกต้อง แต่การสร้าง snapshot ด้วย Lambda ตามตารางคือ hand-written cron jobs ที่ security ต้องการเลิกใช้ ต้องดูแล code ในทุกบัญชีเอง และไม่มี backup policy, vault lock หรือ cross-account recovery controls แบบรวมศูนย์ของ AWS Backup"),
 "C": ("Use AWS DataSync to move all directories to Amazon FSx for Windows File Server in AWS, point the plant controllers to the FSx share over the existing VPN, and protect FSx and other resources with AWS Backup.",
       "ตกข้อ (1): DataSync และ AWS Backup ถูกต้อง แต่ controllers ต้องการ low-latency access ภายในโรงงาน การให้ทุกการอ่านไฟล์วิ่งผ่าน VPN ไปยัง AWS ทำให้ latency สูงและขึ้นกับ WAN ตลอดเวลา โดยไม่มี local cache สำหรับเนื้อหาที่ใช้บ่อย"),
 "D": ("Deploy an S3 File Gateway, copy the several hundred terabytes of historical directories into the gateway's SMB share with Robocopy so that the gateway uploads them to Amazon S3, and use AWS Backup for the migrated AWS resources.",
       "ตกข้อ (2): File Gateway ตอบเรื่อง SMB caching และ AWS Backup ถูกต้อง แต่การใช้ gateway เป็นช่องทางย้ายข้อมูลจำนวนมากต้องผ่าน local cache ที่จำกัด อัปโหลดแบบ asynchronous และไม่มีการตรวจสอบ transfer แบบ end-to-end เหมือน DataSync งานย้ายจึงช้าและควบคุมยาก"),
},
 clue="controllers ต้องใช้ SMB พร้อม local cache, ย้ายหลายร้อย TB พร้อม metadata และ verification, backup รวมศูนย์แทน cron scripts",
 reasoning="1) แยกสามหน้าที่: hybrid file access, bulk migration และ backup governance 2) ข้อ (1) ต้องมี local cache ในโรงงาน = S3 File Gateway ไม่ใช่ให้ทุกการอ่านวิ่งไป AWS (C) 3) ข้อ (2) การย้ายข้อมูลจำนวนมากพร้อม verification = DataSync ไม่ใช่ copy ผ่าน gateway (D) 4) ข้อ (3) ต้องใช้ AWS Backup แทน Lambda/cron (B) A จึงใช้บริการที่ถูกต้องในแต่ละหน้าที่",
 refs=[("What is Amazon S3 File Gateway?", "https://docs.aws.amazon.com/filegateway/latest/files3/what-is-file-s3.html"),
       ("How AWS DataSync verifies data integrity", "https://docs.aws.amazon.com/datasync/latest/userguide/configure-data-verification-options.html"),
       ("What is AWS Backup?", "https://docs.aws.amazon.com/aws-backup/latest/devguide/whatisbackup.html")])

tfix("pro-27", {
 "A": ("Use Amazon RDS for PostgreSQL with a Multi-AZ deployment, keep automated backups for point-in-time recovery, and use AWS Backup to copy snapshots to the secondary Region every 12 hours for Regional recovery.",
       "ตกข้อ (2): Multi-AZ และ automated backups ตอบข้อ (1)(3) ได้ แต่ snapshot copy ทุก 12 ชั่วโมงไม่ใช่ data replication ที่พร้อมใช้ต่อเนื่อง RPO อาจเสียข้อมูลได้ถึงครึ่งวัน และต้อง restore ฐานข้อมูลก่อนจึงยังไม่มี secondary ที่พร้อมรับ cutover"),
 "B": ("Use Aurora PostgreSQL with Multi-AZ storage and Aurora Global Database for cross-Region read replication and planned promotion, with Route 53 application cutover and backup retention.",
       "ถูก: Aurora เก็บข้อมูลหลายชุดข้าม 3 AZ และเมื่อมี Aurora Replica ใน AZ อื่นจะ failover ได้ในระดับนาทีหรือเร็วกว่า Global Database replicate ไป secondary Region อย่างต่อเนื่องและรองรับ switchover/failover ที่ควบคุมได้ Route 53 หรือ global writer endpoint ใช้ทำ application cutover ส่วน automated backups ให้ point-in-time restore แยกจาก DR ซึ่งจำเป็นเพราะ replica จะ replicate การลบข้อมูลผิดพลาดไปด้วย"),
 "C": ("Use Aurora PostgreSQL with an Aurora Replica in a second Availability Zone and an Aurora global database secondary in another Region. Set the backup retention period to the minimum and recover from accidental data changes by promoting the secondary cluster.",
       "ตกข้อ (3): HA และ DR ข้าม Region ถูกต้อง แต่ secondary cluster ได้รับทุกการเปลี่ยนแปลงรวมถึงการลบหรือแก้ข้อมูลผิดพลาดภายในเวลาไม่ถึงวินาที การ promote จึงไม่ได้ย้อนข้อมูลกลับ point-in-time backups ต้องแยกจาก DR replica ตามที่ finance ระบุ"),
 "D": ("Run PostgreSQL on Amazon EC2 instances in three Availability Zones with Patroni for automatic failover, configure streaming replication to standby instances in the secondary Region, and take scheduled pg_basebackup backups to Amazon S3.",
       "ตกข้อ (1): ออกแบบได้ครบทั้ง HA, DR และ backup ในทางเทคนิค แต่ทีม operations ขนาดเล็กต้องดูแล streaming replication, failover tooling, patch และ backup เองบน EC2 ซึ่งโจทย์ระบุว่าไม่ต้องการ และไม่ใช่ managed multi-AZ availability"),
},
 clue="HA ภายใน Region แบบ managed ระดับนาที, DR ข้าม Region ที่ replicate ข้อมูลและมี endpoint cutover, point-in-time backup แยกจาก DR, ทีมเล็กไม่ดูแล replication เอง",
 reasoning="1) ข้อ (1) ต้องเป็น managed HA จึงตัด PostgreSQL บน EC2 (D) 2) ข้อ (2) ต้องมี replication ต่อเนื่องไป Region ที่สอง snapshot copy (A) ไม่พอ 3) ข้อ (3) DR replica ไม่ใช่ backup เพราะ replicate ความผิดพลาดไปด้วย ตัด C 4) B ใช้ Aurora (storage 3 AZ + replica) สำหรับ HA, Global Database สำหรับ DR, Route 53/global endpoint สำหรับ cutover และเก็บ automated backups แยก จึงครบทั้งสามข้อ",
 refs=[("Using Amazon Aurora Global Database", "https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-global-database.html"),
       ("High availability for Amazon Aurora", "https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Concepts.AuroraHighAvailability.html"),
       ("Backing up and restoring an Aurora DB cluster", "https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/BackupRestoreAurora.html")])

tfix("pro-28", {
 "A": ("Route all reads, including the final seat-inventory validation, through a DAX cluster to reduce DynamoDB load, and use Amazon MemoryDB for the Redis-compatible service.",
       "ตกข้อ (1): DAX และ MemoryDB ถูกเลือกถูกที่ แต่ถ้าการตรวจที่นั่งใช้ eventually consistent read ผ่าน cache อาจได้ค่าเก่าและขายที่นั่งซ้ำ การยืนยันสุดท้ายต้องใช้ conditional write หรือ transaction กับ DynamoDB โดยตรง (DAX ส่ง strongly consistent reads ผ่านไป DynamoDB โดยไม่ cache)"),
 "B": ("Use DAX for the event-metadata reads, confirm seats with DynamoDB conditional writes, and use an Amazon ElastiCache (Redis OSS) cluster with Multi-AZ and daily snapshots as the primary database for the Redis-compatible service.",
       "ตกข้อ (3): สองส่วนแรกถูกต้อง แต่ ElastiCache ใช้ asynchronous replication และ snapshot เป็นรอบ ๆ จึงอาจเสียข้อมูลที่เพิ่งเขียนเมื่อ node ล้ม เหมาะเป็น cache มากกว่า primary durable database ขณะที่ MemoryDB ใช้ Multi-AZ transaction log ที่ทนทาน"),
 "C": ("Use DAX for eventually consistent DynamoDB metadata reads, perform seat confirmation against DynamoDB with conditional writes, and use MemoryDB for the durable Redis-compatible application.",
       "ถูก: DAX cache metadata ที่ถูกอ่านซ้ำ ๆ แบบ eventually consistent โดยใช้ DynamoDB API เดิม การยืนยันที่นั่งใช้ conditional write (หรือ TransactWriteItems) กับ DynamoDB จึงขึ้นกับข้อมูลจริงไม่ใช่ cache ส่วน MemoryDB เก็บทุก write ใน distributed transaction log ข้ามหลาย AZ จึงใช้เป็น primary database ที่เข้ากันได้กับ Redis ได้"),
 "D": ("Add a cache-aside layer in Amazon ElastiCache (Redis OSS) for the event-metadata reads with application code for population and TTLs, confirm seats with DynamoDB conditional writes, and use MemoryDB for the Redis-compatible service.",
       "ตกข้อ (2) ด้าน overhead: ทำงานได้จริง แต่ต้องเขียน logic เติม cache, TTL และ invalidation เอง ขณะที่ DAX เข้ากันกับ DynamoDB API และเปลี่ยนเพียง client จึงเร่งการอ่านจาก DynamoDB ได้ด้วยงานพัฒนาและดูแลน้อยกว่า"),
},
 clue="การยืนยันที่นั่งต้องใช้ข้อมูลจริงไม่ใช่ cache, metadata อ่านซ้ำแบบ eventual ได้, อีก service ต้องการ Redis-compatible durable primary database",
 reasoning="1) แยกตาม consistency และ durability: seat allocation ต้องเขียน/ตรวจกับ DynamoDB โดยตรง ตัด A ที่ผ่าน cache 2) metadata ที่ยอม eventual consistency: DAX เร่งการอ่านด้วย API เดิม ส่วน ElastiCache cache-aside (D) ต้องเขียน code เพิ่ม 3) Redis-compatible ที่เป็น primary database ต้อง durable: MemoryDB ไม่ใช่ ElastiCache (B) 4) C จึงเลือกถูกทั้งสามส่วน",
 refs=[("In-memory acceleration with DynamoDB Accelerator (DAX)", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.html"),
       ("DynamoDB condition expressions", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.ConditionExpressions.html"),
       ("What is Amazon MemoryDB?", "https://docs.aws.amazon.com/memorydb/latest/devguide/what-is-memorydb.html")])

tfix("pro-29", {
 "A": ("Create IAM policies for each analyst that allow s3:GetObject only on approved prefixes, create a separate AWS Glue database for each department, and use S3 bucket policies to share prefixes with other accounts.",
       "ตกข้อ (1): ยังเป็นการคุมสิทธิ์ระดับ bucket/prefix ด้วย IAM ซึ่งให้สิทธิ์ทั้งไฟล์ ไม่สามารถจำกัดเฉพาะบางคอลัมน์ในตาราง และการแชร์ข้ามบัญชีด้วย bucket policy ทำให้การ grant/revoke ไม่สอดคล้องกับ catalog ต้องแก้หลายที่เมื่อสิทธิ์เปลี่ยน"),
 "B": ("Run AWS Glue ETL jobs that write a separate de-identified copy of each table with only the allowed columns for every department, and grant each department IAM access to its own copy.",
       "ตกข้อ (3): การทำสำเนาเฉพาะคอลัมน์ให้ผลลัพธ์ที่จำกัดได้จริง แต่ขัดกับข้อห้ามทำสำเนาข้อมูลต่อทีม ต้องดูแล ETL, ค่าจัดเก็บ และความสอดคล้องของข้อมูลหลายชุด และทุกครั้งที่สิทธิ์เปลี่ยนต้องสร้างหรือแก้ pipeline ใหม่"),
 "C": ("Load the curated data from Amazon S3 into Amazon Redshift, use Redshift column-level GRANT statements for analysts, and share tables with other accounts by using Redshift data sharing.",
       "ตกข้อ (2)(3): Redshift ให้ column-level permissions และ data sharing ได้จริง แต่ต้องโหลดข้อมูลเป็นอีกชุดใน warehouse และเปลี่ยนเครื่องมือ query จาก Athena ซึ่งโจทย์ต้องการคงไว้พร้อมกับให้ข้อมูลอยู่ใน S3"),
 "D": ("Register governed S3 locations with Lake Formation, apply catalog/table permissions and cross-account shares, and let Athena query permitted Glue Catalog objects.",
       "ถูก: เมื่อ register S3 location กับ Lake Formation สิทธิ์จะคุมที่ระดับ database/table/column (และ row/cell ด้วย data filters) แทนการให้ IAM อ่าน bucket ตรง Athena ได้ credentials ชั่วคราวสำหรับเฉพาะข้อมูลที่ได้รับอนุญาต การแชร์ข้ามบัญชีใช้ Lake Formation grants ผ่าน RAM ข้อมูลยังอยู่ใน S3 ชุดเดียวและ CloudTrail ยังบันทึกการเข้าถึง"),
},
 clue="สิทธิ์ระดับตาราง/คอลัมน์และข้ามบัญชีเหนือ IAM ระดับ bucket, ข้อมูลอยู่ใน S3 และใช้ Athena ต่อ, ห้ามทำสำเนาต่อทีม",
 reasoning="1) ข้อ (1) ต้องการสิทธิ์ระดับคอลัมน์ ซึ่ง IAM/bucket policy (A) ให้ได้แค่ระดับ object/prefix 2) ข้อ (3) ห้ามทำสำเนา ตัด ETL ต่อทีม (B) 3) ข้อ (2) ต้องคง S3 + Athena ตัดการโหลดเข้า Redshift (C) 4) Lake Formation วางชั้น permission เหนือ Glue Data Catalog ทั้ง column-level และ cross-account sharing โดย Athena query ผ่านสิทธิ์นั้น D จึงครบ",
 refs=[("Lake Formation permissions model", "https://docs.aws.amazon.com/lake-formation/latest/dg/managing-permissions.html"),
       ("Cross-account data sharing in Lake Formation", "https://docs.aws.amazon.com/lake-formation/latest/dg/cross-account-permissions.html"),
       ("Using Athena to query data registered with Lake Formation", "https://docs.aws.amazon.com/athena/latest/ug/security-athena-lake-formation.html")])

tfix("pro-30", {
 "A": ("Use Redshift for repeatable warehouse analytics with QuickSight dashboards, OpenSearch Service for searchable logs, and Athena for occasional S3 archive queries.",
       "ถูก: Redshift รองรับ join ขนาดใหญ่และ concurrency สูงสำหรับ BI ได้คาดเดาได้ QuickSight ให้ dashboard ที่จัดการสิทธิ์ได้ OpenSearch Service ทำ inverted index สำหรับค้นหา log ด้วย keyword แบบ latency ต่ำ ส่วน Athena เป็น serverless คิดเงินตามข้อมูลที่สแกน จึงเหมาะกับการ query Parquet ใน S3 เป็นครั้งคราวโดยไม่มี cluster ที่ต้องเปิดไว้"),
 "B": ("Use Amazon Redshift with QuickSight dashboards for the warehouse, load the application logs into Redshift tables and search them with LIKE predicates, and use Athena for the S3 archive queries.",
       "ตกข้อ (2): Redshift และ Athena ถูกต้องในส่วนของตน แต่ Redshift เป็น columnar warehouse ไม่ได้ทำ full-text index การค้นหา log กึ่งโครงสร้างด้วย LIKE ต้องสแกนข้อมูลจำนวนมาก จึงไม่ได้ latency ต่ำสำหรับการตรวจ error ล่าสุดอย่างรวดเร็ว"),
 "C": ("Use Amazon Athena with QuickSight for both the high-concurrency dashboards and the archive queries, and use OpenSearch Service for the application logs.",
       "ตกข้อ (1): Athena เหมาะกับการ query S3 เป็นครั้งคราว แต่ dashboard ที่ join ข้อมูลหลาย TB ด้วยผู้ใช้จำนวนมากพร้อมกันต้องการประสิทธิภาพที่คาดเดาได้ Athena มี query concurrency quota และ latency ขึ้นกับขนาดการสแกน warehouse อย่าง Redshift จึงเหมาะกว่า"),
 "D": ("Use Redshift with QuickSight for the dashboards and OpenSearch Service for the logs, and load the archived Parquet files into a second provisioned Redshift cluster that is reserved for audit queries.",
       "ตกข้อ (3): สองส่วนแรกถูกต้อง แต่ cluster ที่สองที่เปิดไว้สำหรับ query ไม่กี่ครั้งต่อเดือนคือการจ่ายค่า warehouse ตลอดเวลาที่ finance ไม่ยอมรับ และต้องโหลดข้อมูลซ้ำ Athena query Parquet ใน S3 ได้โดยตรงและจ่ายตามการสแกน"),
},
 clue="BI join หลาย TB ผู้ใช้พร้อมกันจำนวนมาก, ค้นหา log ด้วย keyword แบบเร็ว, query archive ใน S3 นาน ๆ ครั้งโดยไม่มี cluster เปิดตลอด",
 reasoning="1) จับคู่ access pattern กับ engine: warehouse join + concurrency = Redshift, full-text search = OpenSearch, ad hoc บน S3 นาน ๆ ครั้ง = Athena 2) B ใช้ warehouse ค้นหา text ซึ่งไม่ได้ทำ index สำหรับงานนี้ 3) C ใช้ Athena สำหรับ BI ที่ต้องการประสิทธิภาพคาดเดาได้ 4) D เปิด cluster ถาวรสำหรับงานนาน ๆ ครั้ง A จึงเป็นการแบ่งงานที่ถูกต้อง",
 refs=[("What is Amazon Redshift?", "https://docs.aws.amazon.com/redshift/latest/dg/welcome.html"),
       ("What is Amazon OpenSearch Service?", "https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html"),
       ("What is Amazon Athena?", "https://docs.aws.amazon.com/athena/latest/ug/what-is.html")])
