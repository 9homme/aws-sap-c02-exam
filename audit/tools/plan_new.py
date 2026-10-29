# Plan for new AI Professional questions (pro-64 ..). Run to check coverage and render the plan table.
import json, re, collections

# (id, domain, qualifier, user-topic, scenario, deciding trade-off, key, products)
Q = "COST", "FAST", "PERF", "SECURE", "DOWNTIME"
PLAN = [
 # Topic 1: on-prem <-> AWS, no public internet, encrypted in transit
 ("pro-64", "1", "FAST", 1, "Existing Direct Connect private VIF; new rule: encrypt all traffic within 2 weeks, no internet path", "Private IP VPN over existing DX (days) vs new MACsec-capable port (weeks) vs public VIF VPN", "A", ["Direct Connect", "Site-to-Site VPN", "Transit Gateway"]),
 ("pro-65", "1", "PERF", 1, "20 Gbps encrypted replication between data center and AWS, no internet", "MACsec on 100G dedicated DX (line rate) vs ECMP of 1.25 Gbps VPN tunnels", "C", ["Direct Connect", "Site-to-Site VPN", "Amazon VPC"]),
 ("pro-66", "1", "COST", 1, "Small branch needs 100 Mbps private encrypted link to AWS", "Hosted DX connection + private IP VPN vs dedicated 1/10G port vs second DX", "B", ["Direct Connect", "Site-to-Site VPN", "Transit Gateway"]),
 ("pro-67", "2", "SECURE", 1, "Payment traffic must stay encrypted end to end from on-prem client to the EC2 backend", "TLS pass-through on NLB with ACM/backend certs vs IPsec that ends at the AWS edge vs firewall TLS decryption", "D", ["NLB", "ACM (AWS Certificate Manager)", "Direct Connect", "Network Firewall", "GWLB (Gateway Load Balancer)"]),
 ("pro-68", "3", "DOWNTIME", 1, "Hybrid link outage last month took 4 minutes to fail over", "Two DX locations + BFD + VPN backup vs single location LAG vs static routes", "A", ["Direct Connect", "Site-to-Site VPN", "CloudWatch"]),
 # Topic 2: replace Windows PCs (EC2 remote vs WorkSpaces)
 ("pro-69", "4", "COST", 2, "300 part-time call-center staff use persistent desktops ~3 h/day", "WorkSpaces Personal AutoStop (hourly) vs AlwaysOn vs one EC2 per user", "B", ["EC2", "Cost Explorer", "Amazon WorkSpaces Personal"]),
 ("pro-70", "2", "COST", 2, "2,000 seasonal students need identical apps, no persistence, files in S3", "WorkSpaces Pools / AppStream non-persistent vs Personal desktops vs EC2 RDS farm", "C", ["EC2", "S3", "Auto Scaling"]),
 ("pro-71", "4", "FAST", 2, "Retire 150 Windows PCs in 3 weeks; users keep existing apps and AD logins", "WorkSpaces Personal + AD Connector vs building EC2 RDS host farm vs refactor apps", "D", ["Site-to-Site VPN", "AWS Client VPN", "EC2", "Amazon WorkSpaces Personal", "AD Connector"]),
 ("pro-72", "4", "PERF", 2, "CAD designers need GPU desktops with large shared files", "Graphics G4dn WorkSpaces/EC2 G instances near users + FSx for Windows vs general-purpose bundles", "A", ["EC2", "FSx for Windows File Server", "Amazon WorkSpaces Personal"]),
 ("pro-73", "1", "SECURE", 2, "Contractors need desktops but must not copy data out", "WorkSpaces with clipboard/print/drive redirection off + IP access groups + trusted devices vs EC2 RDP over Client VPN", "B", ["AWS Client VPN", "IAM Identity Center", "CloudTrail", "Amazon WorkSpaces Personal"]),
 # Topic 3: Route 53 - sometimes on-prem, sometimes cloud
 ("pro-74", "1", "COST", 3, "Only on-prem servers must resolve AWS private zones (no reverse need)", "Inbound endpoint only vs inbound+outbound vs endpoints in every VPC", "C", ["Route 53 Resolver", "Route 53", "Direct Connect"]),
 ("pro-75", "1", "SECURE", 3, "Only VPCs in 50 accounts must resolve on-prem names; block DNS exfiltration", "Central outbound endpoint + RAM-shared rules + Resolver DNS Firewall vs per-VPC custom DNS EC2", "D", ["Route 53 Resolver", "AWS RAM (Resource Access Manager)", "Amazon VPC"]),
 ("pro-76", "2", "DOWNTIME", 3, "On-prem primary web app, AWS as warm standby; fail over automatically", "Route 53 failover records + health checks to on-prem IP vs Global Accelerator (no on-prem endpoints) vs manual DNS", "B", ["Route 53", "ALB (Application Load Balancer)", "Global Accelerator", "CloudWatch"]),
 # Topic 4: Active Directory on-prem / cloud
 ("pro-77", "1", "COST", 4, "New 200-user subsidiary, no existing AD, needs domain join for EC2, no trusts", "Simple AD vs AWS Managed Microsoft AD vs self-managed DCs", "C", ["EC2", "IAM", "Simple AD"]),
 ("pro-78", "1", "FAST", 4, "Employees must sign in to 120 AWS accounts with on-prem AD credentials this week", "IAM Identity Center + AD Connector vs Managed AD + trust vs ADFS on EC2", "D", ["IAM Identity Center", "AWS Organizations", "AD Connector", "Site-to-Site VPN"]),
 ("pro-79", "1", "DOWNTIME", 4, "AWS workloads must keep authenticating during a WAN outage to the data center", "Extra DCs of the existing forest on EC2 in two AZs vs Managed AD with trust (still needs on-prem DCs) vs AD Connector", "A", ["EC2", "Systems Manager", "Site-to-Site VPN", "AWS Managed Microsoft AD", "AD Connector"]),
 ("pro-80", "2", "SECURE", 4, "RDS for SQL Server must use Windows auth and keys in a customer-controlled HSM", "Kerberos via Managed AD + KMS custom key store (CloudHSM) vs SQL logins in Parameter Store vs default KMS", "B", ["RDS", "KMS (Key Management Service)", "CloudHSM", "Secrets Manager", "Parameter Store", "AWS Managed Microsoft AD"]),
 # Topic 5: API Gateway + Lambda
 ("pro-81", "3", "PERF", 5, "Java Lambda API has cold-start p99 spikes during market open", "Provisioned concurrency (scheduled via Application Auto Scaling) or SnapStart vs more memory vs EC2", "D", ["Lambda", "Auto Scaling", "CloudWatch", "API Gateway"]),
 ("pro-82", "2", "COST", 5, "Simple JWT-protected proxy API with 2 billion requests/month", "HTTP API + JWT authorizer vs REST API features not needed vs Lightsail/EC2", "A", ["Lambda", "Lightsail", "API Gateway"]),
 ("pro-83", "3", "PERF", 5, "Read-heavy catalog GET endpoints; same responses for minutes", "API/CloudFront caching in front of Lambda vs DAX behind Lambda vs more concurrency", "B", ["CloudFront", "DynamoDB", "DAX (DynamoDB Accelerator)", "API Gateway"]),
 ("pro-84", "2", "SECURE", 5, "Partner-only API must authenticate clients by certificate and resist abuse", "Regional REST API with mutual TLS + WAF + usage plans vs API keys only vs IP allow-list", "C", ["WAF (Web Application Firewall)", "ACM (AWS Certificate Manager)", "Shield", "API Gateway"]),
 ("pro-85", "3", "DOWNTIME", 5, "Frequent Lambda releases behind API Gateway broke production twice", "Aliases + CodeDeploy linear/canary + alarm rollback vs $LATEST deploys vs stage variables by hand", "D", ["Lambda", "CloudWatch", "CloudFormation", "API Gateway"]),
 ("pro-86", "2", "FAST", 5, "Report endpoint now needs 10 minutes, API times out at 29 s; ship this sprint", "API → Step Functions start + poll status vs raising timeout vs rewrite to containers", "A", ["Step Functions", "SQS (Simple Queue Service)", "S3", "API Gateway"]),
 # Topic 6: migrate apps to containers / C++ / Java / .NET
 ("pro-87", "4", "FAST", 6, ".NET Framework apps on Windows; company already uses Migration Hub/ADS data", "Rehost with MGN now, containerize later vs App2Container to Windows containers first", "B", ["Application Migration Service (MGN)", "ECS (Elastic Container Service)", "EC2", "Migration Hub", "Application Discovery Service"]),
 ("pro-88", "4", "COST", 6, "30 low-utilization Java services on EC2 to containers", "ECS on Fargate (+Fargate Spot for workers) + Compute Savings Plans vs EKS vs Beanstalk per service", "C", ["ECS (Elastic Container Service)", "Fargate", "ECR (Elastic Container Registry)", "Savings Plans", "Spot", "EKS (Elastic Kubernetes Service)", "Elastic Beanstalk"]),
 ("pro-89", "4", "PERF", 6, "Low-latency C++ trading engine in containers needs specific CPU and networking", "ECS on EC2 (compute-optimized, cluster placement group, host networking) vs Fargate", "D", ["ECS (Elastic Container Service)", "EC2", "ECR (Elastic Container Registry)", "EBS"]),
 # Topic 7: data in S3 - cheapest query vs Redshift
 ("pro-90", "3", "COST", 7, "Provisioned Redshift used a few hours a week; 90% of data is cold", "Redshift Serverless + unload cold data to S3 Parquet queried via Spectrum vs bigger RA3 vs EMR", "A", ["Redshift", "S3", "AWS Glue", "Athena", "Amazon EMR (แพลตฟอร์ม managed Spark/Hadoop)"]),
 ("pro-91", "3", "PERF", 7, "Executive dashboards need sub-second response for 500 concurrent users", "Redshift with materialized views + concurrency scaling + QuickSight SPICE vs Athena direct vs OpenSearch", "B", ["Redshift", "QuickSight", "Athena", "OpenSearch Service"]),
 ("pro-92", "3", "COST", 7, "Millions of small JSON log files make Athena slow and costly", "Firehose Parquet conversion + dynamic partitioning (or compaction) vs Redshift load vs more Athena capacity", "C", ["Kinesis Data Firehose", "Athena", "S3", "AWS Glue", "Lake Formation"]),
 # Topic 8: many accounts, central control
 ("pro-93", "1", "FAST", 8, "Acquired company with 60 accounts in its own organization must be governed now", "Invite accounts + enroll OUs in Control Tower + StackSets baseline vs recreate accounts", "D", ["AWS Organizations", "AWS Control Tower", "CloudFormation StackSets"]),
 ("pro-94", "1", "SECURE", 8, "Prevent anyone (incl. account admins) from disabling security services or leaving the org", "SCP deny + delegated admin + auto-enable vs IAM policies per account vs detective alerts only", "A", ["AWS Organizations", "GuardDuty", "Security Hub", "IAM", "AWS Config", "IAM Access Analyzer"]),
 ("pro-95", "1", "FAST", 8, "Teams need approved RDS/app stacks self-service today from existing templates", "Service Catalog portfolio shared to OUs vs custom pipeline vs admin rights", "C", ["AWS Service Catalog", "CloudFormation", "Systems Manager", "AWS RAM (Resource Access Manager)"]),
 # Coverage of remaining products + qualifiers
 ("pro-96", "3", "COST", 0, "Storage bill grew 40%: S3 cold objects, gp2 volumes, EFS rarely-read files, old backups", "Lifecycle/Intelligent-Tiering + gp3 + EFS IA + Backup cold tier vs buying RIs", "B", ["S3", "EBS", "EFS (Elastic File System)", "AWS Backup", "Compute Optimizer", "AWS Budgets", "Cost Explorer"]),
 ("pro-97", "2", "PERF", 0, "Tightly coupled MPI simulation scales poorly", "Cluster placement group + EFA + FSx for Lustre via Batch multi-node vs spread across AZs vs EFS", "C", ["EC2", "AWS Batch", "FSx for Lustre", "Auto Scaling"]),
 ("pro-98", "4", "FAST", 0, "80 TB to S3 within 7 days over a 1 Gbps link", "Data Transfer Terminal (link too slow: ~75 TB/week max) vs DataSync vs Transfer Family vs Snowball (closed)", "D", ["AWS Data Transfer Terminal", "DataSync", "Snow Family", "Storage Gateway", "Transfer Family"]),
 ("pro-99", "4", "DOWNTIME", 0, "Oracle to Aurora PostgreSQL, maximum 10-minute outage", "SCT + DMS full load + CDC + short cutover vs export/import vs native replication", "A", ["Database Migration Service (DMS)", "Schema Conversion Tool (SCT)", "Aurora", "RDS"]),
 ("pro-100", "3", "COST", 0, "NAT gateway charges dominated by EC2 traffic to S3 and DynamoDB", "Gateway VPC endpoints (no charge) vs interface endpoints vs more NAT gateways", "B", ["NAT Gateway", "Internet Gateway", "AWS PrivateLink", "S3", "DynamoDB", "VPC Flow Logs"]),
 ("pro-101", "2", "COST", 0, "Three VPCs exchange 200 TB/month; no transitive routing needed", "VPC peering (no per-GB processing) vs Transit Gateway vs VPC Lattice vs PrivateLink", "C", ["VPC Peering", "Transit Gateway", "VPC Lattice", "AWS PrivateLink"]),
 ("pro-102", "3", "FAST", 0, "Find PII across 2,000 buckets and vulnerable images before an audit next week", "Macie automated discovery + Inspector + Security Hub vs custom Glue/Lambda scanners", "D", ["Macie", "Inspector", "S3", "Security Hub"]),
 ("pro-103", "2", "DOWNTIME", 0, "Order events must not be lost when consumers or the broker are down", "EventBridge archive/replay + SQS DLQ + MQ active/standby vs single-instance broker vs SNS-only", "A", ["EventBridge", "SNS (Simple Notification Service)", "SQS (Simple Queue Service)", "Amazon MQ", "Kinesis Data Streams"]),
 ("pro-104", "3", "PERF", 0, "Real-time game leaderboard needs microsecond reads and sorted sets", "ElastiCache sorted sets vs MemoryDB (durable, slower writes) vs DAX (DynamoDB API only)", "D", ["ElastiCache", "MemoryDB", "DynamoDB", "DAX (DynamoDB Accelerator)"]),
 ("pro-105", "3", "COST", 0, "Steady RDS for 3 years, fixed engine/size, plus ElastiCache", "3-year RDS/ElastiCache Reserved Instances vs Database Savings Plans (flexibility not needed) vs Compute SP", "B", ["Reserved Instances", "Savings Plans", "RDS", "ElastiCache", "Cost Explorer"]),
 ("pro-106", "2", "DOWNTIME", 0, "Elastic Beanstalk app + RDS major upgrade with near-zero downtime", "Beanstalk blue/green CNAME swap + RDS Blue/Green Deployments vs in-place upgrade", "C", ["Elastic Beanstalk", "RDS", "Aurora", "Route 53"]),
 ("pro-107", "1", "PERF", 0, "Global users hit a single-Region TCP+HTTP API; latency 300 ms from Asia", "Global Accelerator for TCP + CloudFront for HTTP vs more instances in one Region vs Route 53 only", "A", ["Global Accelerator", "CloudFront", "NLB", "Route 53"]),
]

TOPICS = {1: "On-prem ↔ AWS private + encrypted", 2: "Replace Windows PCs (EC2 vs WorkSpaces)", 3: "Route 53 on-prem vs cloud",
          4: "Active Directory on-prem/cloud", 5: "API Gateway + Lambda", 6: "Migrate to containers (C++/Java/.NET)",
          7: "S3 query cost vs Redshift", 8: "Multi-account central control", 0: "Product/qualifier coverage"}
QNAME = {"COST": "MOST cost-effective", "FAST": "Fastest / least time", "PERF": "Best performance", "SECURE": "MOST secure", "DOWNTIME": "Least downtime / data loss"}

if __name__ == "__main__":
    ROOT = "/Users/a667282/workspace/aws-learning/sap-c02-practice"
    bible = open(f"{ROOT}/content/aws-sap-c02-thai-exam-bible.md").read()
    primer = bible.split("### Accounts, identity และ governance")[1].split("## 4. Domain")[0]
    prods = [l.split("|")[1].strip() for l in primer.split("\n") if l.startswith("| ") and not re.match(r"^\| (Product|[-: ])", l)]
    key = lambda n: re.sub(r"[^a-z0-9]+", "", re.sub(r"^(AWS|Amazon)\s+", "", re.sub(r"\s+\(.*$", "", n), flags=re.I).lower())
    used = {key(t) for row in PLAN for t in row[7]}
    missing = [p for p in prods if key(p) not in used]
    print("questions", len(PLAN), "| bible products", len(prods), "| missing:", missing or "none")
    print("qualifier", collections.Counter(r[2] for r in PLAN))
    print("domain", sorted(collections.Counter(r[1] for r in PLAN).items()))
    print("key", sorted(collections.Counter(r[6] for r in PLAN).items()))
    print("topic", sorted(collections.Counter(r[3] for r in PLAN).items()))
    with open(f"{ROOT}/audit/plan-new-questions.md", "w") as f:
        f.write("# Plan: new AI Professional questions\n\nEach question has at least two technically workable options; the qualifier decides.\n\n")
        f.write("| ID | Domain | Qualifier | Topic | Scenario | Deciding trade-off | Key | Products |\n|---|---|---|---|---|---|---|---|\n")
        for i, d, q, t, s, tr, k, p in PLAN:
            f.write(f"| {i} | {d} | {QNAME[q]} | {TOPICS[t]} | {s} | {tr} | {k} | {', '.join(p)} |\n")

# 2-3 explicit requirements per question (woven into prose in the final prompt), plus the qualifier.
REQS = {
 "pro-64": ["Encrypt all on-prem↔VPC traffic in transit within 2 weeks", "No traffic or tunnel endpoint may use the public internet", "Keep the existing transit VIF and 30 attached VPCs reachable"],
 "pro-65": ["Sustain 20 Gbps of encrypted replication", "Traffic must never traverse the public internet", "Survive the loss of one Direct Connect location"],
 "pro-66": ["Private connectivity for a 100 Mbps branch, no internet path", "Encrypt traffic in transit between branch and VPC"],
 "pro-67": ["Payload must stay encrypted from on-prem client to EC2 backend (no decryption in between)", "Clients connect to a stable private endpoint over Direct Connect", "Security team keeps control of certificate rotation"],
 "pro-68": ["Fail over to a backup path within seconds, not minutes", "Tolerate loss of a Direct Connect location", "Backup path must still be encrypted"],
 "pro-69": ["Each agent keeps a persistent personal Windows desktop", "Desktops used ~3 h/day on irregular shifts", "Keep existing corporate AD sign-in"],
 "pro-70": ["2,000 students need identical apps for 4 months", "No per-user OS state retained; files saved to S3", "Capacity must scale with class schedules"],
 "pro-71": ["Retire 150 Windows PCs within 3 weeks", "Users sign in with existing on-prem AD accounts", "No app re-packaging or rewrite"],
 "pro-72": ["GPU-accelerated CAD with low input latency", "Shared access to multi-GB project files over SMB", "Designers work from two cities"],
 "pro-73": ["Contractors must not copy, print, or download data locally", "Access only from managed contractor laptops", "Every session auditable"],
 "pro-74": ["On-prem servers resolve AWS private hosted zones", "No AWS workload needs on-prem names", "Records must stay private"],
 "pro-75": ["VPCs in 50 accounts resolve on-prem corp names", "Block DNS queries to known exfiltration domains", "Central team manages rules once for all accounts"],
 "pro-76": ["On-prem stays primary; AWS is warm standby", "Automatic failover within ~1 minute when on-prem is unhealthy", "Users keep the same hostname"],
 "pro-77": ["Domain-join 120 Windows/Linux EC2 instances for 200 users", "No existing AD and no trust requirements", "Minimal administration of directory servers"],
 "pro-78": ["Employees sign in to 120 AWS accounts with on-prem AD credentials", "Do not copy passwords or users into AWS", "Access assigned by AD group per account"],
 "pro-79": ["AWS workloads keep authenticating during a WAN outage to the data center", "Users remain in the existing on-prem forest", "Highly available across AZs"],
 "pro-80": ["RDS for SQL Server uses Windows authentication with corporate users", "Encryption keys reside in a customer-controlled single-tenant HSM", "No database passwords embedded in apps"],
 "pro-81": ["p99 latency under 200 ms at market open", "Traffic jumps 20× within seconds at a known time", "Keep the Lambda/API Gateway architecture"],
 "pro-82": ["Validate JWTs from the existing IdP", "2 billion requests/month at the lowest cost", "No need for usage plans, request validation, or caching"],
 "pro-83": ["Cut p95 latency of catalog GETs", "Reduce Lambda invocations and DynamoDB reads", "Data may be up to 5 minutes stale"],
 "pro-84": ["Authenticate partners by client certificate", "Throttle per partner and block common web exploits", "No public unauthenticated access"],
 "pro-85": ["Shift a small share of traffic first", "Roll back automatically on error alarms", "Same API endpoint for clients"],
 "pro-86": ["Report jobs run up to 10 minutes", "Clients get an immediate job ID and poll status", "Deliver within the current sprint without re-platforming"],
 "pro-87": ["Exit the data center in 8 weeks", "Apps are .NET Framework on Windows Server with no code changes", "Containerization may follow later"],
 "pro-88": ["30 stateless Java services with low, variable utilization", "Some background workers tolerate interruption", "Team has no Kubernetes expertise"],
 "pro-89": ["Microsecond-sensitive C++ engine needs specific CPU features and host networking", "Containerized deployment pipeline", "Low network latency between engine nodes"],
 "pro-90": ["Analysts query a few hours per week", "90% of 400 TB is cold history", "Keep SQL access to both hot and cold data"],
 "pro-91": ["Sub-second dashboards for 500 concurrent users", "Joins across 5 TB of structured sales data", "Governed sharing to executives"],
 "pro-92": ["Reduce Athena query cost and latency on log data", "Logs arrive continuously as small JSON files", "Keep querying with SQL in Athena"],
 "pro-93": ["Bring an acquired 60-account organization under governance quickly", "Keep existing workloads and account IDs", "Apply baseline controls and logging"],
 "pro-94": ["Nobody in member accounts can disable GuardDuty/Config/Security Hub", "Accounts cannot leave the organization", "Findings aggregated centrally"],
 "pro-95": ["Teams launch approved RDS and app stacks self-service today", "Reuse existing CloudFormation templates", "No broad IAM permissions to developers"],
 "pro-96": ["Cut storage spend across S3, EBS, EFS, and backups", "No application changes", "Keep current retention requirements"],
 "pro-97": ["Tightly coupled MPI with heavy inter-node traffic", "Shared POSIX scratch with high throughput", "Run as queued batch jobs"],
 "pro-98": ["Move 80 TB to S3 within 7 days", "Only a 1 Gbps internet link is available", "First-time customer for physical transfer options"],
 "pro-99": ["Oracle → Aurora PostgreSQL with at most 10 minutes of outage", "Stored procedures need conversion", "Data keeps changing until cutover"],
 "pro-100": ["Cut NAT gateway processing charges", "EC2 traffic is mostly to S3 and DynamoDB in-Region", "Instances stay in private subnets"],
 "pro-101": ["Three VPCs exchange 200 TB/month", "No transitive routing or new VPCs planned", "Lowest data-transfer cost"],
 "pro-102": ["Find PII across 2,000 buckets within a week", "Report vulnerable EC2 and container images", "Centralized findings for auditors"],
 "pro-103": ["No order event lost when consumers are down for hours", "Replay events after a bug fix", "Legacy JMS consumers survive broker maintenance"],
 "pro-104": ["Microsecond reads of top-N rankings", "Sorted-set operations at high write rate", "Rankings can be rebuilt from DynamoDB"],
 "pro-105": ["Fixed RDS and ElastiCache footprint for 3 years", "No engine or size change planned", "Maximum discount"],
 "pro-106": ["Upgrade app platform and database major version", "Near-zero downtime with fast rollback", "Same endpoint for users"],
 "pro-107": ["Cut latency for Asian users of a us-east-1 API with TCP and HTTP endpoints", "Static IPs for the TCP clients", "No multi-Region database rewrite"],
}

if __name__ == "__main__":
    assert set(REQS) == {r[0] for r in PLAN} and all(2 <= len(v) <= 3 for v in REQS.values())
    with open(f"{ROOT}/audit/plan-new-questions.md", "w") as f:
        f.write("# Plan: new AI Professional questions (pro-64 – pro-107)\n\n")
        f.write("Spec: prompt 1,100–1,600 chars (Week 8 median is 625); 2–3 requirements woven into the scenario plus a qualifier; "
                "options 250–450 chars, each a complete design; at least two options technically work and the qualifier decides.\n\n")
        f.write("| ID | Domain | Qualifier | Topic | Scenario | Requirements | Deciding trade-off | Key | Products |\n|---|---|---|---|---|---|---|---|---|\n")
        for i, d, q, t, s, tr, k, p in PLAN:
            f.write(f"| {i} | {d} | {QNAME[q]} | {TOPICS[t]} | {s} | {'<br>'.join(REQS[i])} | {tr} | {k} | {', '.join(p)} |\n")
    print("plan written with requirements")
