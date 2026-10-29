from common import tfix

tfix("pro-21", {
 "A": ("Build container images for the Java web application and the event consumers, and run both as Amazon ECS services on AWS Fargate behind an Application Load Balancer.",
       "ตกข้อ (1): Fargate เหมาะกับ consumers ที่เป็น container อยู่แล้ว แต่ web app ยังไม่มี container build pipeline การ containerize ก่อน launch เพิ่มงาน packaging และ pipeline ใหม่ที่โจทย์ต้องการเลี่ยง ขณะที่ Elastic Beanstalk deploy archive เดิมได้ทันที"),
 "B": ("Deploy the existing Java web package to AWS Elastic Beanstalk, and run the containerized consumers as Amazon ECS services on an EC2 Auto Scaling group capacity provider.",
       "ตกข้อ (2): ฝั่ง web ถูกต้อง แต่ ECS บน EC2 capacity provider ทำให้ทีมต้องดูแล container hosts (AMI, patch, scaling ของ instance) ซึ่งโจทย์กำหนดให้รัน consumers โดยไม่ต้องจัดการ EC2 worker nodes"),
 "C": ("Run the Java web application on an Amazon Lightsail instance behind a Lightsail load balancer and deploy new versions manually, and run the consumers as Amazon ECS services on AWS Fargate.",
       "ตกข้อ (1): Lightsail เหมาะกับงานขนาดเล็กที่ต้องการราคาคงที่และใช้ง่าย แต่ไม่มี managed environment deployment tooling เช่น rolling deployments และ managed platform updates แบบ Elastic Beanstalk ทีมต้อง deploy และ patch เองซึ่งไม่ตรงกับที่ developers ต้องการ"),
 "D": ("Deploy the existing Java web package to Elastic Beanstalk, and run the containerized background workers as ECS services using Fargate.",
       "ถูก: Elastic Beanstalk รับ WAR/JAR บน Java platform แล้วจัดการ EC2, load balancer, Auto Scaling, rolling deployments และ managed platform updates ให้ จึงย้ายได้โดยไม่ต้อง repackage ส่วน consumers ที่เป็น container อยู่แล้วรันบน ECS Fargate โดยไม่มี host ให้ดูแล บริการแต่ละตัวตรงกับรูปแบบ packaging ของ workload"),
},
 clue="web เป็น Java archive ที่ไม่มี container pipeline ต้องการ managed deployment, consumers เป็น container ที่ห้ามดูแล EC2 hosts, เลือกบริการให้ตรงกับรูปแบบ packaging",
 reasoning="1) ดูรูปแบบ packaging ก่อน: web เป็น archive ดั้งเดิม consumers เป็น container 2) web: Elastic Beanstalk ให้ managed environment และ rolling deploy โดยไม่ต้อง containerize ตัด A ที่ต้องสร้าง pipeline ใหม่ และ C ที่ Lightsail ไม่มี deployment tooling แบบนี้ 3) consumers: ห้ามดูแล EC2 hosts จึงต้องใช้ Fargate ไม่ใช่ EC2 capacity provider (B) 4) D จึงเลือกบริการที่ง่ายที่สุดสำหรับแต่ละ workload",
 refs=[("Elastic Beanstalk concepts", "https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/concepts.html"),
       ("Elastic Beanstalk managed platform updates", "https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/environment-platform-update-managed.html"),
       ("AWS Fargate for Amazon ECS", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Fargate.html")])

tfix("pro-22", {
 "A": ("Migrate the platform to Amazon ECS on AWS Fargate, convert the Helm charts and manifests into ECS task definitions, replace the admission controllers with AWS Lambda functions, and store images in private Amazon ECR repositories.",
       "ตกข้อ (1)(3): ECS และ ECR เป็นบริการ managed ที่ดี แต่ ECS ไม่ใช่ Kubernetes API การแปลง Helm charts, CRDs และ admission controllers เป็นงาน replatform ขนาดใหญ่ที่โจทย์ต้องการเลี่ยง เหมาะกับ greenfield service ที่ไม่ผูกกับ Kubernetes มากกว่า"),
 "B": ("Run the migrated platform on Amazon EKS and use private Amazon ECR repositories for images; choose compatible EC2 node groups or Fargate profiles according to workload needs.",
       "ถูก: EKS เป็น Kubernetes ที่ผ่านการรับรอง conformance จึงใช้ manifests, Helm charts, CRDs และ admission webhooks เดิมได้ AWS ดูแล control plane ให้ ECR เป็น private registry ที่คุมสิทธิ์ด้วย IAM และ repository policy รวมถึง cross-account pull ส่วน managed node groups หรือ Fargate profiles ให้เลือก compute ตาม workload โดย Fargate มีข้อจำกัด เช่น ไม่รองรับ DaemonSets"),
 "C": ("Run the platform on Amazon EKS with managed node groups, and run a self-managed Harbor container registry on Amazon EC2 instances to store the images and control pull permissions.",
       "ตกข้อ (2): EKS ตอบเรื่อง Kubernetes API แล้ว แต่ Harbor บน EC2 เป็น registry ที่บริษัทต้องดูแลเอง (patch, HA, storage, backup) และสิทธิ์ไม่ได้ผูกกับ IAM โดยตรง ขณะที่โจทย์ต้องการ managed private registry ที่ใช้ IAM/repository permissions"),
 "D": ("Run upstream Kubernetes on Amazon EC2 with kOps, operate the control plane across three Availability Zones, and store images in private Amazon ECR repositories.",
       "ตกข้อ (3): kOps รักษา Kubernetes API และ ECR ตอบข้อ (2) แต่ทีมต้องดูแล control plane, etcd, การ upgrade และ HA เอง ซึ่งเพิ่ม operational overhead โดยไม่มี requirement ที่ต้องควบคุม control plane เอง EKS ให้ความเข้ากันได้เดียวกันแบบ managed"),
},
 clue="ต้องคง Kubernetes API, manifests และ controllers เดิม, registry ต้องเป็น managed private ที่คุมด้วย IAM, replatform น้อยที่สุด",
 reasoning="1) ข้อ (1) ต้องเป็น Kubernetes จึงตัด ECS (A) ซึ่งเหมาะกับ greenfield service ในโจทย์มากกว่า 2) ระหว่าง Kubernetes แบบ managed กับ self-managed: kOps (D) ได้ API เหมือนกันแต่ต้องดูแล control plane เอง 3) registry ต้องเป็น managed และใช้ IAM ตัด Harbor บน EC2 (C) 4) B ใช้ EKS + ECR และเลือก node groups/Fargate ตาม workload จึงครบทุกข้อ",
 refs=[("What is Amazon EKS?", "https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html"),
       ("Private repository policies in Amazon ECR", "https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-policies.html"),
       ("Amazon EKS on AWS Fargate considerations", "https://docs.aws.amazon.com/eks/latest/userguide/fargate.html")])

tfix("pro-23", {
 "A": ("Use AWS Batch with a managed compute environment that can use EC2 Spot capacity, define job queues and retry strategies, and checkpoint work to durable storage.",
       "ถูก: AWS Batch รับงานเข้า job queue จัดลำดับ และสร้าง/ลด compute ใน managed compute environment ให้อัตโนมัติจนเหลือศูนย์เมื่อไม่มีงาน Spot ลดต้นทุนได้มากเพราะงาน resume จาก checkpoint ใน S3 ได้ retry strategy (เช่น evaluateOnExit สำหรับ Spot interruption) ส่งงานซ้ำให้อัตโนมัติ ควรใช้ allocation strategy SPOT_PRICE_CAPACITY_OPTIMIZED และหลาย instance types เพื่อลด interruption"),
 "B": ("Use AWS Batch with a managed compute environment that uses only On-Demand Instances, define job queues and retry strategies, and checkpoint work to Amazon S3.",
       "ตกข้อ (2): Batch ตอบเรื่อง scheduling และ retry แล้ว แต่ใช้แค่ On-Demand ทำให้ไม่ได้ประโยชน์จาก interruptible capacity ทั้งที่งานมี checkpoint และ finance ยอมรับการถูกขัดจังหวะบางส่วน ต้นทุนจึงสูงกว่าที่จำเป็นมาก"),
 "C": ("Send render requests to an Amazon SQS queue and run worker processes on an EC2 Auto Scaling group of Spot Instances that polls the queue, scale on queue depth, and implement retries in the worker code.",
       "ตกข้อ (1): Spot และ SQS ทำงานได้จริงและลดต้นทุนได้ แต่ทีมต้องสร้าง scheduler เอง ทั้งการ scale ตาม backlog, visibility timeout สำหรับงานยาว 3 ชั่วโมง, retry และการจัดการ interruption ซึ่งโจทย์ระบุว่าไม่ต้องการสร้างบน Auto Scaling group ทั่วไป"),
 "D": ("Invoke an AWS Lambda function for each video segment from Amazon S3 event notifications, and use Lambda retries and an on-failure destination to handle failed segments.",
       "ตกข้อ (1)(3): Lambda ไม่มี server ให้ดูแล แต่ invocation หนึ่งรันได้นานสุด 15 นาที งานที่ยาวถึง 3 ชั่วโมงจึงทำไม่ได้ และ asynchronous retry ของ Lambda ไม่ได้ออกแบบมาสำหรับ batch scheduling ขนาดใหญ่ที่มีกำหนดเสร็จ"),
},
 clue="งาน container ที่เข้า queue ได้ ต้องการ managed scheduling + auto compute, ใช้ Spot ได้เพราะมี checkpoint, ห้ามมี host ถาวรหรือสร้าง scheduler เอง",
 reasoning="1) งานยาว 5 นาทีถึง 3 ชั่วโมง ตัด Lambda (D) ที่จำกัด 15 นาที 2) ต้องการ managed scheduling และ retry โดยไม่สร้าง scheduler เอง ตัด SQS + ASG (C) 3) checkpoint ได้และยอมรับ interruption จึงควรใช้ Spot ตัด On-Demand-only (B) 4) A ใช้ AWS Batch กับ Spot compute environment, job queue และ retry strategy ครบทั้งสามข้อ",
 refs=[("What is AWS Batch?", "https://docs.aws.amazon.com/batch/latest/userguide/what-is-batch.html"),
       ("AWS Batch automated job retries", "https://docs.aws.amazon.com/batch/latest/userguide/job_retries.html"),
       ("Compute environment allocation strategies", "https://docs.aws.amazon.com/batch/latest/userguide/allocation-strategies.html")])

tfix("pro-24", {
 "A": ("Create an io2 Amazon EBS volume with Multi-Attach enabled, attach it to all worker instances, and copy completed outputs to Amazon S3.",
       "ตกข้อ (1): Multi-Attach ใช้ได้เฉพาะ instance ใน AZ เดียวกับ volume และต้องใช้ cluster-aware file system เพื่อป้องกันข้อมูลเสียหายเมื่อหลายเครื่องเขียนพร้อมกัน จึงไม่รองรับ workers ทั้งสาม AZ แม้ S3 จะเหมาะกับ archive"),
 "B": ("Store active and completed files in Amazon S3 and mount the bucket on each worker with Mountpoint for Amazon S3.",
       "ตกข้อ (1): S3 ทนทานและไม่ผูกกับ instance แต่ Mountpoint for Amazon S3 ไม่รองรับ POSIX semantics ครบ เช่น การแก้ไขบางส่วนของไฟล์เดิม การ rename แบบ atomic หรือ file locking จึงไม่เหมาะกับงานที่หลาย workers อ่านเขียนไฟล์เดียวกันพร้อมกัน"),
 "C": ("Use Amazon EFS for the active shared Linux filesystem and Amazon S3 for immutable archived outputs; mount EFS from each eligible worker.",
       "ถูก: EFS เป็น NFS file system ระดับ Region ที่ workers ทุก AZ mount ได้พร้อมกัน รองรับ POSIX permissions/locking และข้อมูลไม่หายเมื่อ instance ถูก terminate ส่วนผลลัพธ์ที่ไม่เปลี่ยนแล้วย้ายไป S3 ซึ่งถูกกว่าและใช้ lifecycle ไปยัง storage class ราคาต่ำได้ ต้องสร้าง mount target ในแต่ละ AZ และเลือก throughput mode ให้เหมาะ"),
 "D": ("Use Amazon EFS for both the active files and the completed outputs, and configure an EFS lifecycle policy that moves completed files to the EFS Archive storage class.",
       "ตกข้อ (3): EFS ตอบข้อ (1)(2) ได้ และ EFS Archive ลดต้นทุนไฟล์ที่ไม่ค่อยเข้าถึง แต่ผลลัพธ์ยังเป็นไฟล์ใน file system ไม่ใช่ object storage ตามที่ทีม data ต้องการ และไม่ได้ใช้ storage class ระยะยาวของ S3 ที่ถูกกว่าสำหรับการเก็บรักษานาน"),
},
 clue="workers หลาย AZ ต้องอ่านเขียน POSIX พร้อมกัน, ข้อมูลต้องไม่ผูกกับอายุ instance, ผลลัพธ์ที่เสร็จแล้วเก็บเป็น object",
 reasoning="1) แยกชนิด storage: block (EBS) ผูก AZ, file (EFS) ใช้ร่วมกันหลาย AZ, object (S3) เหมาะกับ archive 2) ข้อ (1) ตัด EBS Multi-Attach (A) ที่จำกัด AZ เดียว และ Mountpoint for S3 (B) ที่ไม่ใช่ POSIX เต็มรูปแบบ 3) ข้อ (3) ต้องเป็น object storage ตัด EFS Archive (D) 4) C ใช้ EFS สำหรับงานที่กำลังทำและ S3 สำหรับ archive จึงครบ",
 refs=[("What is Amazon EFS?", "https://docs.aws.amazon.com/efs/latest/ug/whatisefs.html"),
       ("Mountpoint for Amazon S3 file system behavior", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/mountpoint.html"),
       ("Attach a volume to multiple instances with EBS Multi-Attach", "https://docs.aws.amazon.com/ebs/latest/userguide/ebs-volumes-multi.html")])

tfix("pro-25", {
 "A": ("Create a persistent Amazon FSx for Lustre file system that runs all month, and copy input objects from Amazon S3 and results back to S3 with scheduled scripts on EC2 instances.",
       "ตกข้อ (2): FSx for Lustre ให้ประสิทธิภาพ HPC ได้ แต่การรันตลอดเดือนทั้งที่ใช้แค่ไม่กี่วันเสียค่าใช้จ่ายเกินจำเป็น และ script คัดลอกข้อมูลเองแทน data repository association ที่ import/export กับ S3 ให้อัตโนมัติ ทำให้ต้องดูแล EC2 และ script เพิ่ม"),
 "B": ("Use an Amazon EFS file system with Elastic throughput for the simulation working set, and copy results to Amazon S3 after each campaign.",
       "ตกข้อ (1): EFS เป็น managed shared file system ที่ใช้ง่าย แต่ออกแบบสำหรับงานทั่วไป ไม่ใช่ parallel file system ที่ให้ aggregate throughput สูงและ latency ต่ำระดับ sub-millisecond สำหรับหลายพัน core แบบ Lustre และไม่มีการเชื่อมกับ S3 data lake แบบ data repository"),
 "C": ("Deploy a self-managed Lustre cluster on EC2 instances with AWS ParallelCluster for each campaign, and synchronize data with Amazon S3 by using the Lustre HSM tools.",
       "ตกข้อ (3): ทำงานได้และใช้ Lustre จริง แต่ทีมต้องดูแล metadata/object storage servers, การ tune และ HSM integration เอง ซึ่งโจทย์ระบุว่าไม่ต้องการ maintain Lustre cluster เอง FSx for Lustre ให้ความสามารถเดียวกันแบบ managed"),
 "D": ("Provision Amazon FSx for Lustre integrated with S3 data repositories for active simulation data, and run compute jobs against its managed filesystem.",
       "ถูก: FSx for Lustre เป็น parallel file system แบบ managed ที่ให้ throughput สูงสำหรับ HPC data repository association กับ S3 ทำให้เห็น object เป็นไฟล์และ export ผลลัพธ์กลับไป S3 ได้ เลือก scratch deployment สำหรับข้อมูลชั่วคราวแล้วลบ file system เมื่อจบ campaign เพื่อลดต้นทุน ข้อมูลถาวรอยู่ใน S3 เสมอ"),
},
 clue="HPC หลายพัน core ต้อง parallel file system throughput สูง, input/output อยู่ใน S3, ใช้แค่ช่วง campaign และไม่ดูแล Lustre เอง",
 reasoning="1) ข้อ (1) ต้องการ parallel file system ระดับ HPC ซึ่ง EFS (B) ไม่ได้ออกแบบมาสำหรับรูปแบบ I/O นี้ 2) ข้อ (3) ห้ามดูแล Lustre เอง ตัด ParallelCluster + self-managed Lustre (C) 3) ข้อ (2) ต้องเชื่อม S3 กับ file system ชั่วคราว: data repository association ทำ import/export ให้ และสร้าง/ลบตาม campaign ได้ ส่วน A ใช้ script และรันตลอดเดือน 4) D จึงตรงทุกข้อ",
 refs=[("What is Amazon FSx for Lustre?", "https://docs.aws.amazon.com/fsx/latest/LustreGuide/what-is.html"),
       ("Linking FSx for Lustre to an S3 data repository", "https://docs.aws.amazon.com/fsx/latest/LustreGuide/create-dra-linked-data-repo.html"),
       ("FSx for Lustre deployment options", "https://docs.aws.amazon.com/fsx/latest/LustreGuide/using-fsx-lustre.html")])
