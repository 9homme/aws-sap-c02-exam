// App-authored teaching notes, separate from the captured question/answer record.
// Keys identify answer options, not their position in a shuffled question set.
export const courseDistractorExplanations = {
  "Attach an IAM policy to an OU and manage every account separately.": "IAM identity policies attach to identities, not OUs. Organizations policies such as SCPs attach to OUs, while centralized management avoids per-account duplication.",
  "Use public internet access instead of an organization-level control.": "Public network reachability does not implement account governance or permission boundaries. Connectivity and organization-wide authorization are separate architecture concerns.",
  "Duplicate the configuration manually in each account.": "Manual duplication creates inconsistent settings and repeated maintenance. Prefer the centrally managed or inherited mechanism identified in the recorded course answer.",
  "Use a single Availability Zone and add recovery steps later.": "A single-AZ topology is an availability tradeoff, not an answer to this course's conceptual question. It also defers resilience instead of designing recovery explicitly.",
  "Build the capability in the application without a managed AWS service.": "Custom implementation shifts scaling, maintenance, and failure handling to your team. It does not identify the framework, service, or process asked for in this course question.",
  "Choose the option that does not meet the stated availability or latency goal.": "This choice explicitly accepts a requirement violation. A solution must satisfy the business constraints before cost or convenience can make it the preferred design.",
  "Make a manual change without measuring the workload first.": "Unmeasured changes give no evidence of the bottleneck or whether the change helped. Establish a baseline and evaluate the improvement against the stated objective.",
  "Keep the existing design even when it violates the stated objective.": "Preserving a known requirement violation does not improve the workload. Use the course's review/improvement process to identify and address the gap.",
  "Use a service that does not address the identified operational gap.": "Selecting an unrelated service leaves the operational problem unsolved. Match the service's actual capability to the gap identified in the question.",
  "Rebuild the workload before collecting migration requirements.": "A rebuild commits to a strategy before dependencies, constraints, and business goals are understood. Assessment and discovery inform the appropriate migration approach.",
  "Use a tool designed for a different migration strategy.": "Migration tools differ: server replication, data transfer, schema conversion, and incremental refactoring solve different tasks. Match the tool to the strategy rather than treating them as interchangeable.",
  "Defer migration until after the stated deadline.": "Missing the deadline fails the business requirement. Choose a feasible migration wave and strategy within the allowed window instead of postponing the objective.",
};

export const answerCorrections = {
  "csv-20": {
    correctIds: ["D"],
    rationale: "A VPC attachment requires at least one selected subnet; enable each intended AZ by selecting one subnet there. Cross-account use also requires appropriate sharing and authorization. A subnet in every AZ in the Region is not mandatory.",
    studyNote: "Imported-key correction: the CSV marked A, although its rationale described selecting at least one subnet. This app now grades D as correct. The original CSV remains unchanged.",
    studyReferences: ["https://docs.aws.amazon.com/vpc/latest/tgw/tgw-vpc-attachments.html"],
  },
};

export const studyCaveats = {
  "w8-13": {
    studyNote: "Read the captured OAC wording conceptually: the bucket policy uses the cloudfront.amazonaws.com service principal, scoped with the distribution's AWS:SourceArn. An OAC ID itself is not an IAM principal, and OAC does not assign permissions to other AWS resources.",
    studyReferences: ["https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html"],
  },
  "w8-26": {
    studyNote: "Historical compliance comparison: current AWS KMS documentation describes FIPS 140-3 Level 3 validated HSMs. Do not memorize 'only CloudHSM meets Level 3' from this older question. Validate the required standard, key-custody model, availability window, and recovery timing for a real design.",
    studyReferences: ["https://docs.aws.amazon.com/kms/latest/developerguide/key-store-overview.html"],
  },
  "w8-31": {
    acceptedAnswerSets: [["B"]],
    studyNote: "The captured key is C, but S3 now supports enabling Object Lock on existing buckets. This app also accepts B as a valid single answer. Compliance mode protects retained object versions; merely enabling a default retention policy does not retroactively lock existing versions.",
    studyReferences: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock-configure.html"],
  },
  "w8-60": {
    acceptedAnswerSets: [["A"]],
    studyNote: "The captured key favors D's Organizations setup, but A also describes supported findings aggregation. This app accepts either A or D. For a real multi-Region rollout, explicitly configure cross-Region aggregation and the required member accounts/Regions.",
    studyReferences: ["https://docs.aws.amazon.com/securityhub/latest/userguide/finding-aggregation.html"],
  },
  "w8-71": {
    studyNote: "Session Manager shell sessions can log commands/output, but Session Manager cannot log the contents of SSH or port-forwarding sessions. If actual SSH command auditing is mandatory, add appropriate host-side auditing; do not assume tunnel contents appear in session logs.",
    studyReferences: ["https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html"],
  },
  "csv-13": {
    studyNote: "Historical service question: CodeGuru Reviewer stopped accepting new repository associations on November 7, 2025. The captured answer describes the older code-review capability, not a recommendation for a new pipeline today.",
    studyReferences: ["https://docs.aws.amazon.com/codeguru/latest/reviewer-ug/welcome.html"],
  },
};

export const optionExplanations = {
  "course-10": { A: "A large workload can be divided into manageable review scopes. Preserve clear boundaries, owners, and dependencies so that the combined reviews still cover the complete workload." },
  "course-11": { A: "Pillars are the high-level quality areas of the Well-Architected Framework. Questions and design principles help evaluate architecture within those areas." },
  "course-12": { A: "The course identifies Region as required workload information in the Tool. Recording deployment location helps reviewers interpret the architecture and its applicable service context." },
  "course-13": { A: "Milestones capture the workload's review state at points in time, allowing teams to compare architectural improvement as risks are addressed." },
  "course-20": { A: "Foundations is a reliability practice area: establish the account, network, and other prerequisites on which resilient workload design depends." },
  "course-51": { A: "The mainframe course records a 1-to-2-year planning estimate for its production migration context. Treat this as a course-specific estimate, not a mandatory wait for every AWS migration." },
  "course-52": { A: "The course gives 2 to 4 weeks as its Assess-phase estimate. Actual assessment length depends on portfolio size, available discovery data, and the business constraints." },
  "course-58": { A: "The recorded answer is Assess: establish the current estate, requirements, dependencies, and business case before committing to a migration plan." },
  "course-65": { A: "MGN focuses on rehosting: replicating existing server workloads into EC2 with limited application changes. It is not the database schema-conversion or application-rewrite tool." },
  "original-01": {
    B: "A VPC endpoint provides access to a supported service; it is not a backup transport from the on-premises site. 'Public VPC endpoint' also confuses public access with private endpoint connectivity.",
    C: "An internet gateway is not a site-to-site private tunnel. The on-premises application needs a configured VPN path and routing when Direct Connect fails.",
    D: "A NAT gateway translates outbound VPC traffic. Another gateway in the same AZ does not provide an independent hybrid connection or AZ failure protection.",
  },
  "original-02": {
    B: "Manual trails depend on each account administrator and do not automatically cover future accounts. Organization trails centralize configuration and member-account enforcement.",
    C: "Config snapshots describe resource configuration state, not the full API activity audit record that CloudTrail provides.",
    D: "Flow logs describe network metadata, not account API calls. They cannot replace organization-wide CloudTrail audit logging.",
  },
  "original-03": {
    B: "Tags are metadata and do not separate routes by themselves. The shared default transit route table can continue exposing both environments.",
    C: "A security group filters traffic at resources; it does not configure transit-gateway route associations/propagation or provide the requested separate routing domains.",
    D: "An internet gateway supplies public internet routing. It does not isolate production and development attachments on the transit gateway.",
  },
  "original-04": {
    B: "Publishing private service names publicly changes their exposure and does not provide the requested private hosted-zone lookup path.",
    C: "Hosts-file entries require per-server updates and rapidly become inconsistent. Conditional forwarding to managed Resolver endpoints centralizes the configuration.",
    D: "A NAT gateway translates addresses; it does not answer private hosted-zone DNS queries or establish a Resolver forwarding endpoint.",
  },
  "original-05": {
    B: "Manual inspection after an in-place update lacks controlled canary traffic and alarm-driven rollback. It exposes the deployment before the requested validation is complete.",
    C: "S3 lifecycle manages stored objects by age/tier. It does not shift live ECS traffic between application versions.",
    D: "A scheduled EC2 scaling action changes instance capacity, not application version traffic weights or deployment rollback.",
  },
  "original-06": {
    B: "Daily snapshots can lose up to roughly a day's changes and require database/server restoration. They do not provide a seconds-level replication objective.",
    C: "A monthly backup copy is far behind the requested RPO, and a single-AZ primary adds an availability weakness.",
    D: "Database exports are recovery artifacts, not continuously replicated managed PostgreSQL capacity. Their freshness depends on the export schedule.",
  },
  "original-07": {
    B: "Waiting for several minutes contradicts the immediate-response requirement and couples frontend availability to processing duration.",
    C: "Instance-store data can disappear with instance termination/failure. It is not a durable queue for accepted orders.",
    D: "One synchronous invocation waiting on downstream systems retains the long request and dependency chain. Durable queueing separates acceptance from completion.",
  },
  "original-08": {
    B: "A public bucket allows the direct S3 access that is forbidden. User ACLs do not force requests through CloudFront.",
    C: "S3 buckets are service resources, not hosts placed behind your VPC internet gateway. Use CloudFront origin authentication and the bucket policy.",
    D: "NAT performs address translation rather than viewer authentication. Private origin access and viewer authorization are separate controls.",
  },
  "original-09": {
    B: "DNS geolocation plus ALBs does not provide the requested two global static anycast IPs and is not the raw TCP accelerator design.",
    C: "CloudFront with S3 delivers HTTP content. It is not a general active-active TCP service endpoint with the requested address pair.",
    D: "A single EIP on one instance is Regional and a single point of failure. It does not supply global multi-Region active-active routing.",
  },
  "original-10": {
    B: "An RDS read replica replicates an RDS database, not a DynamoDB table. DAX is the integrated DynamoDB caching solution.",
    C: "Glacier Instant Retrieval is an S3 archival object class, not a low-latency DynamoDB key-value cache.",
    D: "More client memory can improve client compute, but does not introduce a shared cache or avoid repetitive DynamoDB reads.",
  },
  "original-11": {
    B: "Spot capacity can be interrupted, so placing the entire baseline on it risks the continuity requirement. Use it only for workloads designed to tolerate interruptions.",
    C: "Dedicated Hosts address host-level placement/licensing requirements and can cost more. No such constraint justifies them for this fleet.",
    D: "Stopping baseline capacity during business hours removes the required service. Cost optimization must preserve the stated workload demand.",
  },
  "original-12": {
    B: "Public SSH violates the no-inbound-SSH requirement and per-instance manual patching does not provide centralized fleet execution.",
    C: "A new AMI does not patch already running instances until an appropriate replacement/deployment occurs. This option explicitly leaves them unchanged.",
    D: "A bucket policy controls access to S3 objects. It cannot execute operating-system patch installation on the EC2 fleet.",
  },
  "original-13": {
    B: "A monthly spreadsheet is delayed manual detection and does not automatically remediate drift. It fails the ongoing automation requirement.",
    C: "Access keys authenticate API callers; they do not evaluate resource configuration compliance or correct violations.",
    D: "Replacing every workload with one instance changes the architecture without solving policy evaluation and remediation. It also creates a new concentration of failure.",
  },
  "original-14": {
    B: "CloudFront content delivery does not overcome insufficient upload bandwidth for this bulk offline transfer requirement.",
    C: "DNS latency routing chooses an endpoint; it does not increase the data-center uplink capacity or move archival bytes offline.",
    D: "An Elastic IP supplies a stable public address, not more network bandwidth. It cannot make the stated transfer deadline achievable.",
  },
  "original-15": {
    B: "A big-bang rewrite delays value and concentrates cutover risk. The requirement asks to replace capabilities gradually while existing clients continue working.",
    C: "S3/CloudFront can serve static objects, not execute an arbitrary server-side monolith. Copying application files does not provide incremental service routing.",
    D: "A larger instance may add capacity but leaves the monolith and routing unchanged. It does not extract capabilities into new services.",
  },
  "emerging-01": {
    B: "An S3 lifecycle rule changes object storage/retention behavior. It does not inspect model prompts or responses for disallowed content.",
    C: "A NAT gateway translates network addresses. It has no semantic understanding of prompts or generated responses.",
    D: "An EBS snapshot policy protects block-volume data. It is unrelated to real-time model content filtering.",
  },
  "emerging-02": {
    B: "A long-lived administrator key in source code exposes broad authority and prevents clear per-agent attribution. Scoped temporary role sessions reduce that risk.",
    C: "Unauthenticated public access removes the identity and authorization boundary. It does not satisfy least privilege or auditable agent access.",
    D: "AdministratorAccess grants far more than the required actions/resources. A separate identity is not least privilege unless its permissions are scoped.",
  },
  "emerging-03": {
    B: "Direct administrator access lets the model act before a person approves the refund. Enforce the approval gate outside the model's discretionary behavior.",
    C: "An ephemeral file is neither a durable approval decision nor a workflow gate. The action must remain blocked until an authenticated approval arrives.",
    D: "A CDN cache serves content; it cannot authorize an individual financial action. Approval belongs in the action workflow.",
  },
  "emerging-04": {
    B: "Public prompt/response logs expose the very sensitive content the company wants to minimize. Auditability requires controlled records, not public disclosure.",
    C: "Removing every log prevents the audit trail required by the business. Retain the minimum useful evidence with redaction, encryption, and restricted access.",
    D: "Public unencrypted records expose audit data at rest and through access permissions. Apply protection and minimize retained sensitive content.",
  },
  "emerging-05": {
    B: "An unrestricted shared retriever can return another employee's documents unless caller-specific authorization is enforced. Broad backend access is not a user access policy.",
    C: "A public bucket removes document confidentiality rather than enforcing per-employee permission boundaries.",
    D: "Client-side hiding can be bypassed through direct requests. The retrieval/data layer must enforce the requesting employee's authorization.",
  },
  "csv-32": {
    A: "Automation has implementation cost, but increased development cost is not the primary delivery benefit asked for. The key benefit is repeatable, frequent releases.",
    B: "A pipeline automates testing; it does not remove the need to test. Faster releases rely on reliable checks rather than less validation.",
    D: "Human review, approvals, and incident decisions can remain in CI/CD. Automation reduces repetitive work without eliminating all human involvement.",
  },
  "csv-33": {
    B: "Security groups filter network traffic for resources. They are not Control Tower's multi-account governance controls.",
    C: "IAM roles delegate permissions to identities/services. Control Tower's controls, historically called guardrails, express the landing-zone governance rules.",
    D: "VPC endpoints provide private service access. They are networking components rather than the named multi-account policy framework.",
  },
  "csv-34": {
    B: "SCPs do not grant permissions. A principal still needs an applicable IAM/resource-based permission within the organization guardrails.",
    C: "The policy layers are evaluated together. An applicable SCP deny can block an action even when an identity policy allows it.",
    D: "An IAM allow cannot override an applicable explicit SCP deny. Guardrails bound the permissions available to member-account principals.",
  },
  "csv-35": {
    A: "AWS APIs may represent rule-group configuration as JSON, but the question asks for the stateful inspection rule syntax: Suricata-compatible rules.",
    C: "XML is not the stateful rule language selected for Network Firewall inspection. Suricata compatibility is the relevant feature.",
    D: "Regular expressions can appear in matching logic, but they are not the complete stateful rule format. Suricata rules express protocol, direction, and matching behavior.",
  },
  "csv-36": {
    A: "You do not attach a WAF web ACL directly to an EC2 instance. Put a supported HTTP ingress resource, such as CloudFront or an ALB, in front.",
    B: "RDS speaks database protocols rather than serving as a WAF web-ACL association target. WAF protects supported web ingress resources.",
    D: "Direct Connect carries network traffic between locations. WAF application-layer inspection is associated with supported web services, not the dedicated link.",
  },
  "csv-37": {
    A: "The claim says any service in disconnected mode, which is too broad. Standard Outposts operations depend on parent-Region connectivity and only supported services run locally.",
  },
  "csv-38": {
    A: "Seven days is the minimum selectable KMS key-deletion waiting period, not the maximum.",
    C: "Ninety days exceeds the supported 7-to-30-day deletion waiting range in this question. It is not a selectable maximum.",
    D: "A year is not a KMS scheduled-deletion waiting-period setting. Use the supported maximum of 30 days and monitor deletion requests promptly.",
  },
  "csv-39": {
    B: "Fleet and instance operations belong to services such as Systems Manager and EC2. Secrets Manager stores and rotates the credentials applications need.",
    C: "Network monitoring uses flow logs and monitoring/security services. Secrets Manager does not inspect packets or traffic paths.",
    D: "Database backups protect database data. Secrets Manager protects connection secrets, not backup schedules or recovery points.",
  },
  "csv-40": {
    A: "Advanced supplies enhanced attack visibility and protection features beyond the automatic Shield Standard baseline.",
    B: "The captured answer refers to included eligible WAF/Firewall Manager usage for protected resources, subject to service terms. Do not assume all possible WAF features/usage are universally free.",
    C: "Advanced is an explicitly subscribed protection offering. It is different from the automatic Standard baseline.",
    D: "Advanced provides access to the AWS DDoS response team for eligible incident assistance, analysis, and mitigation support.",
    E: "Shield Standard is automatic; Advanced requires subscription and appropriate resource protection configuration.",
  },
  "csv-41": {
    B: "Firewall Manager's central cross-account policy management requires Organizations with all features enabled and its service prerequisites configured.",
  },
  "csv-42": {
    B: "A dedicated data-center connection is Direct Connect's purpose. Lambda@Edge executes application request/response logic at CloudFront locations.",
    C: "Route 53 manages DNS records. Lambda@Edge operates on HTTP-related CloudFront events rather than administering hosted zones.",
    D: "VPC creation is infrastructure provisioning. Lambda@Edge runs code on the edge request path, not VPC networks near every user.",
  },
  "csv-43": {
    A: "A VPC belongs to one AWS Region, though its subnets can occupy multiple AZs in that Region. Connect separate VPCs for a multi-Region network.",
  },
  "csv-44": {
    A: "A default route through a NAT gateway is the usual private-subnet outbound path. The public-subnet definition uses a direct route to an internet gateway.",
    B: "A public IP alone does not create an internet route. The subnet route table must also reach the internet gateway, and traffic controls must permit access.",
    C: "Public/private classification depends on routing, not a universal default. Custom subnets can be created with no internet route at all.",
  },
  "csv-45": {
    A: "Load balancers distribute inbound requests to targets. A NAT gateway translates outbound connections from private-addressed clients.",
    C: "Inter-VPC connectivity uses peering, transit gateway, or other appropriate network paths. NAT is not a replacement for those routes.",
    D: "A public instance's security is governed by its exposure and access controls. NAT's key function here is outbound connectivity for private clients.",
  },
  "csv-46": {
    A: "An ALB target group can register EC2 instances by instance ID and forward application traffic to their configured target port.",
    B: "A Lambda-type ALB target group can invoke a registered Lambda function for supported HTTP request handling.",
    C: "An IP-type target group can forward to supported private IP targets, including appropriate reachable workloads beyond directly registered instance IDs.",
    D: "A VPN is a network connection, not an HTTP application target registered in an ALB target group.",
    E: "An S3 bucket is not an ALB target type. CloudFront can use S3 as an origin, which is a different integration.",
    F: "An RDS database endpoint is not an HTTP ALB target. Applications connect to it using the database protocol.",
  },
  "csv-47": {
    A: "CloudFormation can declare the configuration, but the Auto Scaling group still needs a launch template specifying how new instances start.",
    C: "An AMI can contain the added application, but an Auto Scaling group selects it through its launch configuration/template. Creating the image alone does not update the group's launch settings.",
    D: "Editing an infrastructure template can implement the change, but it is not the specific launch-definition mechanism the question asks for.",
  },
  "csv-48": {
    A: "CloudFront caches web objects at distributed edge locations to reduce origin load and viewer latency.",
    B: "DAX is the purpose-built in-memory cache for supported DynamoDB read patterns.",
    C: "An ALB routes HTTP requests to targets. It is not an application response cache.",
    D: "ElastiCache provides managed in-memory caching for application/database access patterns.",
    E: "CloudTrail records API activity for auditing. It does not serve cached application responses.",
    F: "Config records/evaluates resource configuration. It is not a data or response caching layer.",
  },
  "csv-49": {
    A: "A snapshot is a recovery copy, not the immediate automatic writer-failover action. Aurora can promote an existing reader.",
    B: "Restoring a snapshot provisions a new database and is slower than promoting an available reader. It is not the native failover path being asked for.",
    D: "Aurora's cluster storage already provides its replication architecture. The failover action is promoting a reader, not first building a new synchronous replication pair.",
  },
  "csv-50": {
    A: "SNS notifications deliver events; they do not implement object-age transitions between storage classes.",
    B: "S3 Streams is not the lifecycle configuration feature described. Use supported lifecycle transition rules.",
    D: "Glacier identifies archival storage classes. A lifecycle rule defines when objects transition into them.",
  },
  "csv-51": {
    A: "Kerberos authenticates identities; it is not itself an interactive remote-terminal transport to an EC2 instance.",
    B: "RDP provides an interactive remote desktop connection to a suitably configured Windows instance.",
    C: "Session Manager provides IAM-controlled managed-node sessions without opening inbound SSH/RDP ports.",
    D: "SSH supplies an encrypted remote shell and tunneling connection to a suitably configured host.",
    E: "Qualys is a security assessment platform, not the standard direct interactive instance-access method requested.",
    F: "WorkSpaces delivers managed virtual desktops. It is not the direct administration connection method to an existing EC2 instance.",
  },
  "csv-52": {
    A: "An Aurora endpoint speaks a database protocol, not the HTTP origin protocol CloudFront expects.",
    B: "An ALB can expose the application's HTTP/HTTPS origin and distribute CloudFront's origin requests to its targets.",
    C: "A suitably reachable on-premises HTTP/HTTPS server can be a custom origin; origins are not limited to AWS-hosted servers.",
    D: "An EC2-hosted HTTP/HTTPS application can supply a custom origin when its network and origin access are configured appropriately.",
    E: "An RDS endpoint is a database connection target. CloudFront needs an HTTP/HTTPS content origin instead.",
    F: "Route 53 resolves names; it does not serve the origin content returned to CloudFront.",
  },
  "csv-53": {
    B: "This is a NOT question. EC2 can mount EFS through supported NFS connectivity, so EC2 is not the service being excluded.",
    C: "ECS tasks can use supported EFS volume integration. It is therefore not the service that cannot mount the share.",
    D: "EKS workloads can use EFS through the appropriate CSI driver and networking. DynamoDB, not EKS, lacks file-system mounting.",
  },
  "csv-54": {
    A: "Weighted DNS routing is a Route 53 feature. Because the question asks which is NOT a function, this supported feature is not the answer.",
    B: "Domain registration is a supported Route 53 function. The excluded function is executing code at the edge.",
    D: "Alias records are a Route 53 DNS feature for supported targets. They do not make Route 53 an edge-computing runtime.",
  },
  "csv-55": {
    A: "A VPN creates a network tunnel but does not itself establish the direct private S3 endpoint path in this design.",
    B: "A bucket policy authorizes requests but does not create network reachability. The private subnet still needs an appropriate endpoint path.",
    C: "An S3 gateway endpoint adds service-prefix routes in the VPC without requiring a NAT gateway or internet gateway for that S3 traffic.",
    D: "An S3 interface endpoint exposes private interface addresses using PrivateLink, with its corresponding endpoint charges and network configuration.",
    E: "Network Firewall filters traffic along a route; it does not create a private S3 service endpoint.",
  },
  "csv-56": {
    A: "Generated Glue workflows can be customized to the ingestion and transformation requirements rather than being immutable black boxes.",
    B: "Blueprints generate Glue workflow components such as jobs, crawlers, and triggers to implement an ingestion pattern.",
    C: "The recorded course includes built-in blueprint patterns, so the claim that none are supplied is false.",
    D: "Workflow execution can be arranged for an initial one-time run or recurring ingestion, depending on the data movement requirement.",
    E: "An ingestion blueprint orchestrates data movement; it does not replace the S3 storage that holds the data lake.",
  },
  "csv-57": {
    A: "Standard Outposts deployments depend on connectivity to the parent Region. They do not generally remove the connectivity requirement.",
    C: "Outposts deploys AWS equipment at the customer's site. Reducing the physical footprint is not its defining or guaranteed benefit.",
    D: "Outposts extends AWS operations on premises; it does not automatically migrate every workload into a Region.",
  },
  "csv-58": {
    A: "You can use Local Zones from the existing account after enabling the location. A separate AWS account is not the prerequisite.",
    B: "Existing VPCs do not all acquire Local Zone subnets automatically. You choose and configure the relevant network resources.",
    C: "An appropriate existing Regional VPC can be extended using a Local Zone subnet. A new VPC for each location is not universally required.",
  },
  "csv-59": {
    A: "Several pods can share an EC2 instance's bill, so per-pod cost needs allocation logic. The instance bill is not naturally a separate bill for each pod.",
    B: "Managed node groups still bill the shared EC2 worker capacity. They simplify node lifecycle rather than isolating each pod's compute charge.",
    C: "Managed Pod Groups is not the named EKS worker-capacity option in this course. Do not confuse it with managed node groups.",
  },
  "csv-60": {
    A: "Site-to-Site VPN connects networks through a customer gateway. Individual roaming users need a client-based access service.",
    B: "Direct Connect is a dedicated physical/network connection for a site, not an on-demand tunnel from a worker's personal computer.",
    D: "Transit gateway connects and routes attached networks. Client VPN provides the individual user's authenticated remote-access session.",
  },
  "csv-61": {
    B: "Resolver endpoints bridge DNS resolution paths between networks. General-purpose DNS-query load balancing is not their primary function.",
    C: "Private hosted zones are created separately. Endpoints let other networks query the appropriate AWS/private DNS or forward queries out.",
    D: "Domain registration is a separate Route 53 capability. Resolver endpoints address hybrid private-name resolution.",
  },
  "csv-01": {
    A: "Control Tower builds a governed landing zone using Organizations. The direct multi-account policy service requested is Organizations itself.",
    B: "IAM defines identities and permissions within accounts; it does not supply the organization hierarchy and centrally inherited SCPs.",
    D: "Identity Center centralizes workforce sign-in and account assignments. Organizations supplies the account-wide maximum-permission guardrails.",
  },
  "csv-02": {
    A: "Elastic Beanstalk deploys application bundles into managed environments. It does not continuously replicate existing VMware server disks for rehosting.",
    B: "EC2 Image Builder creates and maintains images. It is not the service for replicating and cutting over the current on-premises VMs.",
    C: "Outposts runs selected AWS services on premises. The question wants to move the existing workload into AWS, not extend AWS hardware to the data center.",
  },
  "csv-03": {
    A: "Local session state couples each user to a particular server. External shared state is needed if requests should move freely between instances.",
    B: "Hardcoded addresses couple clients to specific service instances. Discovery and asynchronous interfaces reduce that dependency.",
    D: "A shared database can couple services through schema and availability dependencies. A message queue explicitly separates producer and consumer execution.",
  },
  "csv-04": {
    A: "Global Accelerator improves TCP/UDP network routing but does not cache web objects. The question explicitly asks for edge content caching.",
    B: "Lambda@Edge executes request/response logic associated with CloudFront. CloudFront itself supplies the distributed content cache.",
    C: "ElastiCache accelerates application/data access within a Region. It is not the global edge content-delivery network.",
  },
  "csv-05": {
    B: "Identity Center's main benefit is centralized workforce access, not increased credential-storage capacity.",
    C: "Authentication does not change the network path or bandwidth between accounts. Connectivity uses VPC and hybrid-network services.",
    D: "Account provisioning belongs to Organizations/Control Tower workflows. Identity Center grants users access to the accounts and applications.",
  },
  "csv-06": {
    A: "These deployment/configuration tools do not provide the dedicated managed build-and-test runner plus pipeline orchestration requested.",
    C: "CodeDeploy handles deploying artifacts; EC2 supplies compute. This combination still needs a build/test execution and pipeline mechanism.",
    D: "A code repository and infrastructure templates store/provision inputs, but do not themselves compile code and execute automated tests.",
  },
  "csv-07": {
    A: "RDS manages relational databases. The direct mechanism for adjusting this application's EC2 fleet with demand is EC2 Auto Scaling.",
    C: "CloudFormation declares infrastructure. It does not continuously measure demand and resize the application fleet by itself.",
    D: "Direct Connect provides dedicated hybrid network connectivity, not elastic application instance capacity.",
  },
  "csv-08": {
    B: "Tag policies standardize resource metadata; they do not define the maximum service actions available to account principals.",
    C: "Backup policies define inherited backup behavior. They are not account permission boundaries.",
    D: "OUs group accounts so policies can be inherited. The SCP attached to an OU is the actual permission guardrail.",
  },
  "csv-09": {
    A: "Global Accelerator optimizes global application ingress. It is not a dedicated connection from the data center to AWS.",
    B: "Load balancing distributes application requests among targets. It does not provision the private hybrid transport path.",
    D: "CloudFront caches and delivers HTTP content at the edge, rather than providing dedicated data-center connectivity.",
  },
  "csv-10": {
    A: "An index improves database lookup efficiency at the database. It does not move cached content nearer geographically to users.",
    B: "Lazy loading describes when a cache entry is populated after a miss. It does not specify an edge location near the user.",
    D: "Write-through describes updating the cache when data is written. It is a cache population policy, not a geographic placement strategy.",
  },
  "csv-11": {
    A: "CloudWatch observes metrics, logs, and alarms. It does not supply the governed Account Factory/landing-zone workflow.",
    B: "Config records resource configuration and evaluates compliance. It does not create the multi-account landing zone.",
    C: "EC2 provides virtual machines. Creating organization accounts is an account-governance operation, not a compute-instance operation.",
  },
  "csv-12": {
    B: "Auto Scaling adds application capacity but does not itself detect and mitigate the attack traffic. Application scaling and DDoS protection are different controls.",
    C: "Elastic Beanstalk manages application deployment and scaling. It is not the dedicated enhanced DDoS-protection subscription.",
    D: "More EC2 instances do not replace a managed DDoS mitigation layer and can increase cost during an attack.",
  },
  "csv-13": {
    A: "Trusted Advisor checks AWS environment recommendations. It does not perform the requested source-code security review in the build pipeline.",
    B: "GuardDuty detects suspicious activity in the running environment. It is not a pre-deployment static code-analysis tool.",
    C: "Config evaluates deployed resource configurations, not application source code before production deployment.",
  },
  "csv-14": {
    A: "EFS is shared file storage for mounted clients. S3 object storage is the direct fit for a large video-object library without file-server semantics.",
    B: "RDS stores relational records and transactions. Large streaming media objects are better stored outside database rows.",
    C: "DynamoDB stores bounded-size items and metadata, not large video files. Store the objects in S3 and keep references/metadata separately if needed.",
  },
  "csv-15": {
    B: "Trusted Advisor can recommend savings, but Cost Explorer is the dedicated interactive tool for historical cost/usage trends and breakdowns.",
    C: "Pricing Calculator estimates a proposed workload's cost. It does not analyze the account's actual historical usage.",
    D: "Budgets tracks thresholds and can trigger alerts/actions. Cost Explorer supplies the exploratory cost and usage analysis requested.",
  },
  "csv-16": {
    A: "ECS is a different orchestrator from Kubernetes, and its EC2 launch type retains worker-server management.",
    C: "Managed node groups automate portions of EC2 node lifecycle, but the workload still uses a node-based data plane. Fargate removes those worker servers from the user's management scope.",
    D: "ECR stores images and Lambda runs functions. This pairing does not run the workload as Kubernetes pods.",
  },
  "csv-17": {
    A: "Secrets Manager stores credentials and secrets; it is not the S3 object-encryption key-management service.",
    B: "CloudHSM supplies dedicated HSM-backed key custody for architectures that require it. It is more complex than standard SSE-KMS and is not a direct drop-in S3 encryption setting.",
    C: "KMS integrates directly with S3 SSE-KMS and uses key policies/IAM to control cryptographic operations on the encrypted data.",
    D: "Certificate Manager manages TLS certificates for network identity/encryption. It does not manage S3 object-at-rest encryption keys.",
  },
  "csv-18": {
    B: "S3 Standard prioritizes frequent, immediate access. Its storage price is higher than archival classes for rarely accessed long-term retention.",
    C: "EBS is block storage attached to compute workloads, not the lowest-cost long-term object archive.",
    D: "EFS provides a live shared file system. It is not the lowest-cost class for rarely retrieved archival objects.",
  },
  "csv-19": {
    A: "FSx provides managed file systems. It is not the S3 feature that monitors object access and automatically changes access tiers.",
    B: "Storage Gateway supplies hybrid access interfaces. Its purpose is not automatic S3 access-tier optimization.",
    C: "Snowball moves bulk data using a device. It does not continuously classify objects by their observed access patterns.",
  },
  "csv-20": {
    A: "A transit-gateway VPC attachment needs a selected subnet in each AZ you want to enable, not every AZ in the Region. The original CSV key A contradicted its own rationale and has been corrected.",
    B: "The caller needs IAM permission to create an attachment; a VPC itself is not an IAM identity with permissions. This wording misses the concrete subnet/sharing prerequisite in D.",
    C: "IPv6 is optional; an IPv4 VPC can use transit gateway. Enabling IPv6 is not a universal attachment prerequisite.",
    D: "The attachment requires at least one selected subnet and, for cross-account use, the appropriate transit-gateway sharing/authorization. Missing those prerequisites can prevent attachment creation.",
  },
  "csv-21": {
    A: "VPC attachments are Regional, but transit gateways also support inter-Region peering attachments. The blanket single-Region statement does not describe every attachment type.",
    B: "Attachment creation does not require manually assigning an IP address to the attachment as described. Configure its subnets, routing, and supported connectivity type.",
    D: "Transit gateway connects VPCs and on-premises networks through supported attachments. It is not limited to connecting AWS services.",
  },
  "csv-22": {
    A: "A container is one process environment inside the scheduled unit. An ECS task can group one or more containers that must run together.",
    B: "A pod is Kubernetes terminology. ECS uses a task as its corresponding basic scheduled execution unit.",
    D: "An ECS service maintains the desired number of tasks. It manages a collection of execution units rather than being the atomic unit itself.",
  },
  "csv-23": {
    B: "Worker capacity depends on the chosen data plane: self-managed nodes, managed node groups, or Fargate. It is not always fully managed in the same way as the control plane.",
    C: "The application owner supplies and maintains container code/images. EKS does not automatically manage every application container's content.",
    D: "Kubernetes Service objects describe application networking. The consistently AWS-managed EKS component is the control plane.",
  },
  "csv-24": {
    A: "EKS does not expose its etcd state as a customer-managed RDS database. The managed EKS control plane owns that responsibility.",
    C: "Kubernetes uses etcd, but naming the software does not identify the operator. In EKS, AWS operates the control-plane datastore.",
    D: "Customers manage their workloads and chosen data plane; AWS manages etcd availability as part of the EKS control plane.",
  },
  "csv-25": {
    B: "Default is not the control behavior being asked for. CloudFormation hooks implement proactive checks before supported resources are provisioned.",
    C: "Detective controls evaluate deployed resources, commonly using Config rules. Hooks act earlier in the provisioning workflow.",
    D: "Preventive permission controls commonly use SCPs to restrict actions. The specific hook-based Control Tower category is proactive.",
  },
  "csv-26": {
    B: "The Cost and Usage Report supplies detailed billing data. It does not itself attach policies or stop resources when a budget threshold is breached.",
    C: "Tags classify costs and resources. They do not execute spending-control actions on their own.",
    D: "Cost Explorer analyzes spending. Budgets Actions is the mechanism for applying configured controls at spending thresholds.",
  },
  "csv-27": {
    A: "Access points create policy-controlled endpoints to the same bucket. They do not increase the bucket's storage capacity.",
    B: "Their primary purpose is access-policy separation, not faster data transfer. Transfer optimization is a different design decision.",
    C: "An access point does not create a second copy or backup of the data. Replication and backup require separate configuration.",
  },
  "csv-28": {
    A: "A monthly report is a structured reporting outcome, often served by a warehouse. It does not by itself need a raw, diverse-data lake.",
    B: "Fixed, predefined BI queries often fit a curated warehouse. A lake is especially useful when retaining raw data for varied future analysis.",
    C: "A CRM's transactional record updates typically need an operational database, rather than a data lake as the application's primary store.",
  },
  "csv-29": {
    A: "DMS moves and replicates data; it does not promise an automatic engine-version upgrade. Target engine provisioning and compatibility require planning.",
    B: "Schema-conversion tools can assist with code conversion, but not every stored procedure converts automatically. DMS replication is a separate capability.",
    D: "Continuous replication can reduce cutover downtime, but no tool eliminates downtime in every migration scenario. Application and engine constraints still matter.",
  },
  "csv-30": {
    A: "Relocate moves an existing environment/platform with minimal architectural change. The named strategy involving selective cloud optimizations is replatform.",
    B: "Repurchase replaces the application with another product, often SaaS. It is a product change rather than a small platform optimization.",
    D: "Retain keeps the workload where it is for now. It does not migrate and optimize it on AWS.",
  },
  "csv-31": {
    B: "All-at-once exposes the whole audience to the new version immediately. It has a larger initial blast radius than a small canary.",
    C: "In-place describes replacing software on existing capacity, not necessarily testing a small share of live traffic first.",
    D: "Recreate stops/replaces the old deployment and can introduce downtime. It is not progressive traffic exposure with a controlled initial cohort.",
  },
  "w8-51": {
    B: "The timed EFS/Glue polling path introduces a delay and additional integration work. S3 upload events can trigger the managed ETL path directly.",
    C: "An SNS topic is a publish/subscribe notification destination, not the requested work queue. The recorded design explicitly connects ETL-completion events to SQS.",
    D: "A cron process on EC2 retains server patching, scheduling, and failure-recovery work. Managed event-triggered transformation removes those components.",
  },
  "w8-52": {
    A: "EC2 still requires operating the application servers. The requirement explicitly asks to avoid server management, so queue-backed Lambda workers fit better.",
    C: "SQS and Lambda meet the compute requirement, but Aurora changes the Oracle database engine and reduces reuse of the company's Oracle expertise.",
    D: "A streaming platform and a new NoSQL model add unnecessary redesign for order work items. The requirement favors durable queueing while retaining managed Oracle.",
  },
  "w8-53": {
    A: "S3 cannot execute the existing server-side JavaScript UI. Converting business logic to Lambda also introduces more development than container replatforming.",
    B: "Changing MySQL to DynamoDB requires data-model and database-access redesign. EKS also adds Kubernetes concepts when ECS Fargate can run the existing containers.",
    D: "The UI is rendered on the server, so deploying it as a static S3 website does not preserve its runtime. Containerize that tier along with the application logic.",
  },
  "w8-54": {
    B: "ARC readiness checks assess recovery configuration and capacity; they are not the traffic-routing switch. Routing controls are the mechanism that drives failover decisions.",
    C: "An API endpoint can remain reachable while downstream microservices fail. A basic endpoint check does not incorporate all the supplied component metrics needed for partial failures.",
    D: "Evaluate Target Health is not an application-wide dependency assessment for these API endpoints. Alarm-driven routing controls can combine the relevant microservice health signals.",
  },
  "w8-55": {
    A: "A Regional EFS mount target does not provide the requested cross-Region S3 object access. Migrating to a different storage interface also adds unnecessary application changes.",
    B: "Copying a large dataset for only a small amount of remote access duplicates storage and adds a synchronization function. The question's traffic/storage ratio favors accessing the original through a private endpoint.",
    D: "CRR is useful for frequent local reads or a recovery copy, but duplicates this large dataset even though remote read traffic is low. Those storage and replication costs dominate here.",
  },
  "w8-56": {
    A: "Changing capacity mode does not cache the repeatedly read keys. The captured question's Savings Plans choice is not the DynamoDB capacity/caching purchase strategy in its key.",
    B: "DAX addresses repeated reads, but this option omits the explicit provisioned-capacity switch selected by the key and assumes the wrong purchasing mechanism for that historical question.",
    C: "ElastiCache can cache application data, but requires custom integration and invalidation logic. DAX supplies the purpose-built DynamoDB caching path with less application work.",
  },
  "w8-57": {
    A: "The first six months are frequently accessed, making IA retrieval charges unattractive. Moving to a new bucket is unnecessary when lifecycle can transition the existing objects.",
    C: "Using Standard-IA during frequent access adds retrieval charges, and Flexible Retrieval is a more expensive archive choice than Deep Archive when no short retrieval deadline is stated.",
    D: "Automatic tier monitoring is useful for uncertain patterns. Here the age boundary is known, so a deterministic lifecycle transition avoids unnecessary monitoring and targets the cheapest suitable archive.",
  },
  "w8-58": {
    A: "EFA may help compatible HPC software, but requires support and configuration. A cluster placement group directly improves physical network locality with the existing image and less application-specific work.",
    C: "EC2 Fleet manages capacity selection and purchasing, not the proximity of communicating instances. It does not itself provide the cluster placement needed for low-latency communication.",
    D: "ENA enables enhanced networking on supported instances, but does not place the nodes close together. The recorded solution targets the communicating cluster's placement.",
  },
  "w8-59": {
    A: "Scheduled scaling needs a known timetable. The sales spikes are unexpected, so a reactive load metric is needed.",
    C: "Predictive scaling needs a forecastable pattern and history. It is less direct for new, irregular spikes than scaling on the current ALB request load per target.",
    D: "The investigation found no useful correlation with instance metrics. CPU target tracking would therefore retain a poor demand signal; ALB requests per target better represent incoming work.",
  },
  "w8-60": {
    A: "This is a valid Security Hub aggregation design. The captured key favors D's Organizations-based onboarding; do not learn that cross-Region aggregation in A is unsupported. Current deployments should configure the required Regions explicitly.",
    B: "Audit Manager organizes compliance evidence and assessments. It is not the primary service for consolidating operational security findings from GuardDuty, Macie, and other integrations.",
    C: "Per-account/per-Region custom audit frameworks add maintenance and focus on evidence assessments rather than the requested central findings view.",
  },
  "w8-61": {
    B: "Merely naming User-Agent does not specify the logic that selects or rewrites the device-specific resource. The recorded key supplies that request-processing logic with Lambda@Edge.",
    C: "Route 53 handles DNS queries and cannot inspect an HTTP User-Agent header. DNS cannot select the device-specific ALB on that basis.",
    D: "An NLB operates at the transport layer and does not route by HTTP User-Agent. It also leaves static content on origin compute instead of offloading it to S3 and CloudFront.",
  },
  "w8-62": {
    B: "An interface endpoint exposes a service through PrivateLink; it is not a substitute for a VPC attachment on a transit gateway.",
    C: "Gateway endpoints provide supported service access from a VPC route table. They cannot be attached to a transit gateway as replacement VPC network connections.",
    D: "The VPCs and original transit gateways are in one Region. A new remote-Region transit gateway adds unnecessary complexity and cannot take those VPC attachments as described.",
  },
  "w8-63": {
    B: "Splitting reads and writes across Regional endpoints requires more application coordination for read-after-write behavior. Write forwarding offers a single Regional access path with an appropriate consistency setting.",
    C: "This retains separate read/write endpoint logic and chooses an unplanned/manual recovery procedure for routine DR tests. Planned managed transitions provide a more controlled test path.",
    D: "Write forwarding fits the access pattern, but routine DR testing should use a planned managed transition rather than manually simulating an unplanned disaster.",
  },
  "w8-64": {
    B: "Parameter Store can hold secrets, but the described synchronization requires custom password-change detection and Lambda logic. Secrets Manager supplies managed database rotation integration.",
    C: "Automatically rewriting hardcoded credentials still distributes secrets through code and deployment artifacts. Retrieve the current secret at runtime instead.",
    D: "Alternating-user rotation can reduce rotation disruption, but adds a second database user and associated permissions. The captured question chooses single-user rotation for the least development effort.",
  },
  "w8-65": {
    A: "Daily copying maintains separate on-premises and S3 datasets throughout the migration and creates synchronization lag. File Gateway presents an on-premises file interface backed by S3.",
    B: "Volume Gateway presents block storage through iSCSI; it does not expose the files as directly usable S3 objects for the refactored applications.",
    C: "A scheduled sync script retains multiple copies and requires custom monitoring/retry handling. A managed S3-backed file gateway fits the shared transitional access pattern.",
  },
  "w8-66": {
    A: "Containers, Fargate, and a NoSQL database add several unfamiliar technologies. The requirement prioritizes a familiar LAMP stack and predictable bundled pricing.",
    C: "Rewriting the application into Lambda/API Gateway functions creates the largest runtime learning and adaptation effort for this PHP developer.",
    D: "Elastic Beanstalk supports application deployment, but DynamoDB changes the familiar relational LAMP data layer and the service pricing model is less bundled than Lightsail.",
  },
  "w8-67": {
    A: "The access phases are already known, so Intelligent-Tiering monitoring is unnecessary. Re-creatable files also permit the lower-cost single-AZ IA choice during the intermediate phase.",
    C: "Deep Archive does not fit the five-hour access requirement. A cheap storage class is unsuitable when its retrieval delay misses the business deadline.",
    D: "Standard-IA keeps multi-AZ resilience that these re-creatable derivatives do not require, and Deep Archive fails the retrieval window. Flexible Retrieval is the suitable final archive here.",
  },
  "w8-68": {
    A: "Repeated Athena polling adds scheduling and query work and may detect the deletion request late. An event rule reacts when the API request occurs.",
    C: "A daily query can delay notification for almost a day and still requires custom scheduled reporting. EventBridge plus SNS directly delivers the timely alert.",
    D: "Automatic cancellation changes every deletion decision instead of notifying the administrator for review. It also adds code where the requirement only needs an event-to-SNS alert.",
  },
  "w8-69": {
    A: "A central ECS task can perform cleanup, but adds container/task management for a brief event-driven action. Lambda is the lower-overhead target for this work.",
    B: "Running a Spot worker fleet introduces queue consumers and compute management. Central event routing and an on-demand function avoid continuously managed worker capacity.",
    C: "A function in every source account duplicates deployment and bucket-access configuration. A central function can process the forwarded termination events and clean the central bucket.",
  },
  "w8-70": {
    A: "AD Connector depends on an existing directory to authenticate against. Retiring the on-premises AD would remove that dependency, so it is not the new directory host.",
    B: "Simple AD provides basic directory functions but does not meet this question's MFA requirement. Basic LDAP alone is not the complete requirement.",
    C: "IAM Identity Center supplies workforce access to AWS accounts and applications, not a general replacement LDAP/AD directory for these workloads.",
  },
  "w8-71": {
    A: "Client VPN removes public SSH exposure, but does not itself retain the commands run inside encrypted SSH sessions. Additional host-side auditing would be needed.",
    B: "Source-IP restriction reduces public attack exposure, but keeps the bastion and does not add command auditing. It meets only part of the requested change.",
    D: "Run Command executes remote commands and records output, but is not an interactive session/port-forwarding replacement. Session Manager supplies the interactive access path, with the logging caveat below.",
  },
  "w8-72": {
    A: "You cannot convert an existing standard queue in place to FIFO. Create a new FIFO queue and update the producers/consumers instead.",
    C: "A raw visible-message count does not account for the number of running workers. Backlog per instance is the proportional target-tracking signal chosen for scalable queue processing.",
    D: "This assumes an unsupported in-place queue-type conversion and uses raw queue depth rather than the workload-per-worker metric.",
  },
  "w8-73": {
    A: "A separate EBS snapshot-copy workflow duplicates orchestration already covered by the unified backup plan. Centralizing supported resource backups reduces separate schedules and monitoring.",
    B: "A separate DataSync flow adds file-copy administration alongside the backup system. AWS Backup can include EFS in the same cross-Region protection workflow.",
    D: "A database read replica is an availability/replication mechanism, not a retained backup history. It can replicate unwanted data changes and adds a separate recovery system to manage.",
  },
  "w8-74": {
    A: "Lambda and Step Functions can remove servers, but decomposing these complex existing applications into functions requires more redesign than container replatforming.",
    B: "This adds both a function-based rewrite and a relational-to-NoSQL database conversion. Those changes conflict with the limited development time.",
    C: "ECS on EC2 still leaves worker-host Linux patching and capacity administration with the company. Fargate removes that host-management layer.",
  },
  "w8-75": {
    A: "Synchronizing two independent EBS volumes is not a shared concurrent file system. It adds copy lag and does not give both application copies a single consistent working file.",
    C: "A Regional EFS file system is intended for Regional clients; a second Region adds network and recovery complexity beyond the requested multi-AZ design. The selected solution keeps both clients in the EFS Region.",
    D: "EBS Multi-Attach is restricted to supported volumes/instances within one AZ. It does not share a volume across the two Availability Zones required here.",
  },
  "w8-26": {
    A: "Disabling a KMS key schedules access to a managed key, but the captured question selects the dedicated CloudHSM design under its original compliance assumptions. Check the current-compliance caveat below before applying that historical comparison today.",
    C: "Editing access policies changes authorization rather than provisioning dedicated HSM capacity. It also creates recurring policy-management work; do not infer from this old key that current KMS lacks Level 3 validation.",
    D: "The multi-AZ CloudHSM approach matches the captured architecture, but a DynamoDB table adds storage/request cost for simple configuration metadata that fits standard Parameter Store parameters.",
  },
  "w8-27": {
    A: "S3 folders are key prefixes, not independent policy-bearing resources. Put access rules in bucket/access-point policies rather than attaching resource policies to folders.",
    C: "You do not attach IAM policies directly to individual S3 objects. Prefix-scoped access-point policies avoid per-object permission administration as the key space grows.",
    D: "Duplicating objects across multiple buckets increases storage, synchronization, and policy work. Multiple access points can expose different permitted views of the same underlying bucket.",
  },
  "w8-28": {
    A: "Replacing the root volume does not enable hibernation on instances that were not launched with it configured. Launch replacement instances with the required encrypted root and hibernation settings.",
    B: "Keeping one instance running reduces some startup delay but does not preserve the initialized memory state of the other four. Scale-out still pays their lengthy initialization cost.",
    C: "Scaling to zero saves compute cost, but every scale-out is a fresh boot. It does not solve the unacceptable cold initialization time that hibernation addresses.",
  },
  "w8-29": {
    A: "The question needs a durable primary database, not just a low-latency cache. Its recorded design uses MemoryDB's durable transaction log rather than relying on cache replication and snapshots.",
    B: "MGN rehosts servers into EC2; it does not import a Redis database into the managed MemoryDB service. Database seeding requires a supported data-import path such as an appropriate Redis snapshot.",
    C: "Self-managed Redis on EC2 leaves server maintenance and durability engineering with the company. That fails the explicit goal of avoiding database-server management.",
  },
  "w8-30": {
    A: "Latency DNS chooses an endpoint, but does not carry UDP packets over AWS's optimized global network. Global Accelerator adds that network path for the interactive gaming traffic.",
    B: "Lambda@Edge processes HTTP-related CloudFront events, not arbitrary UDP game sessions. A single Region also leaves distant players far from the game servers.",
    C: "CloudFront caches HTTP/HTTPS content; it is not a UDP session accelerator. Live multiplayer state is not a static cached website response.",
  },
  "w8-31": {
    A: "Governance retention can be bypassed by suitably authorized users. The requirement says no user may remove the protected versions, so compliance mode is the relevant retention model.",
    B: "This is a valid current AWS approach for enabling Object Lock on an existing versioned bucket. The captured answer key chooses C under an older premise; do not memorize B as technically impossible. See the current-AWS caveat below.",
    D: "Creating a new bucket does not fix governance mode's authorized-bypass capability. Compliance mode is the deciding protection, with retention applied to the relevant object versions.",
  },
  "w8-32": {
    B: "Inspector finds software vulnerabilities, not sensitive S3 content. Moving the bucket also forces application changes that in-place batch encryption avoids.",
    C: "Macie is appropriate, but moving all objects to a new bucket requires updating clients. Inventory and Batch Operations let the team process the existing bucket instead.",
    D: "The in-place encryption plan is appropriate, but Inspector is the wrong classification service. Use Macie to discover sensitive data in S3 objects.",
  },
  "w8-33": {
    A: "StackSets can distribute templates and detect drift, but detection does not by itself prevent member-account changes. The recorded key favors Config's organization-managed conformance packs with exclusions.",
    B: "Trusted access and delegated administration establish the organization-wide service authority needed for the centralized Config deployment.",
    C: "Deactivating trusted access removes the service integration needed for central administration. Independent administrators also reintroduce the inconsistency the company wants to prevent.",
    D: "An organization conformance pack deploys the common Config rules centrally and accepts excluded accounts. This supplies the policy package after the organization integration is enabled.",
    E: "A catalog product depends on product launches and subsequent drift checks. It does not provide the same direct organization-managed Config package and explicit exclusion mechanism.",
  },
  "w8-34": {
    A: "Individual VIF/VGW connectivity plus a peering mesh adds links and route administration as VPCs grow. A managed transit hub simplifies both on-premises and inter-VPC connectivity.",
    C: "One VPN per VPC and a full peering mesh scale operational work with every new network. A transit gateway centralizes the VPN and VPC attachments.",
    D: "A transit VPC requires operating the transit solution and its VPN mesh. The managed transit gateway supplies the requested hub with less infrastructure administration.",
  },
  "w8-35": {
    A: "Data-event logs show actions that actually occurred, not every principal currently authorized by a resource policy. Access analysis is needed to find potential external access even without activity.",
    B: "Management-event logs audit control-plane activity. They are not a policy analysis of who can send or receive queue messages.",
    D: "An account-level trust zone also flags other accounts in the same organization. Use the organization as the trust boundary to isolate genuinely outside principals.",
  },
  "w8-36": {
    B: "An event-driven repair runs after a noncompliant action and requires custom processing. It does not establish the standardized policy and preventive controls requested.",
    C: "Tag-policy enforcement validates supported tag values/casing, but does not universally require a missing tag to be present. Appropriate SCP conditions can enforce required tagging on supported creation actions.",
    D: "Config's required-tags rule detects missing tags; it does not itself apply them. A custom remediation workflow also adds maintenance compared with the recorded policy-and-correction approach.",
  },
  "w8-37": {
    A: "Two identity pools split the identities and complicate promotion from guest to authenticated access. One pool can support both unauthenticated and developer-authenticated flows.",
    B: "User-pool federation expects supported federation standards and is not the guest AWS-credential mechanism described. The custom provider fits developer-authenticated identity pools.",
    D: "Two user pools do not solve the unsupported custom federation or guest-credential requirements. They also make the free-to-premium identity transition harder.",
  },
  "w8-38": {
    A: "Device shipping adds lead time, while VM Import/Export lacks the ongoing server replication path chosen for minimal downtime. The stated network window makes an online migration competitive.",
    B: "MGN fits minimal-downtime VM migration, but ordering, loading, and shipping Snowball devices can exceed the given five-day online-transfer window.",
    D: "Transfer Acceleration addresses the online data path, but VM Import/Export is an image-import workflow. MGN's ongoing replication better supports a short server cutover.",
  },
  "w8-39": {
    A: "Separate logging, tooling, and audit accounts isolate security duties and protect the log archive from the operational security tooling account.",
    B: "Environment OUs apply common controls to groups of similar accounts, so new production, test, or development accounts inherit the appropriate baseline.",
    C: "An Exceptions OU separates unusual requirements from standard environment baselines. Targeted account controls can then express the special restrictions.",
    D: "Combining log archive, audit, and security tooling into one account loses the separation of duties expected by the captured multi-account design.",
    E: "An account SCP cannot override a deny inherited from its parent OU. Exceptional workloads may need a different OU policy path rather than extra policies inside the standard OU.",
    F: "One OU per workload duplicates common policies and makes governance scale with individual workloads. Group by shared control requirements instead.",
  },
  "w8-40": {
    A: "CloudFormation automates the infrastructure, but leaving software setup as a manual runbook preserves repetitive work. User data captures the bootstrap steps too.",
    C: "A console runbook documents steps but does not execute repeatable infrastructure provisioning or updates. It leaves the largest amount of manual work.",
    D: "Custom API and shell orchestration can work, but the team must maintain deployment state, dependencies, and failure handling that CloudFormation already manages.",
  },
  "w8-41": {
    A: "AD Connector is deployed as an AWS Directory Service directory in the AWS VPC, not installed on premises. It forwards authentication to the existing on-premises AD.",
    B: "Copying users and passwords to Managed Microsoft AD contradicts the condition that credentials must remain on premises. AD Connector avoids that directory duplication.",
    C: "A Managed AD trust plus an IAM federation setup introduces extra components for this direct WorkSpaces authentication requirement. The recorded design uses AD Connector as the directory gateway.",
  },
  "w8-42": {
    A: "Rekognition analyzes images and video, not the caller's spoken intent or telephone identity. Speech intent belongs to the conversational component.",
    B: "Lambda integrates the contact flow with business APIs and systems to look up or act on caller information.",
    C: "Lex supplies speech/language intent recognition for self-service conversations. It determines what the caller is asking for.",
    D: "SQS queues application messages, not live telephone calls. Connect manages the contact-center call queue and routing.",
    E: "Alexa for Business is not the managed contact-center conversational interface selected here. Lex integrates intent handling into Connect flows.",
    F: "Connect provides the telephony, contact flows, and contact-center routing foundation. Lambda and Lex supply the integration and conversational pieces.",
  },
  "w8-43": {
    A: "S3 static website hosting cannot execute server-side PHP. The existing web application needs a compute runtime such as EC2 in this least-change migration.",
    B: "Amazon MQ preserves compatible ActiveMQ broker protocols, reducing the messaging code changes required by the existing applications.",
    C: "A relational RDS model introduces schema and application changes for a document-oriented JSON workload. The captured key instead chooses a managed document-capable DynamoDB data model.",
    D: "EC2 rehosting preserves the application runtimes. Multi-AZ scaling and an ALB add availability without rewriting the PHP frontend.",
    E: "DynamoDB stores document attributes and removes database-server administration. The application still needs an API/data-model adaptation; this is not a zero-change database migration.",
    F: "SQS does not implement ActiveMQ's broker protocol. Replacing the queue with SQS requires client messaging changes instead of the lower-change MQ replatform.",
  },
  "w8-44": {
    A: "Memcached does not provide the Redis replication-group automatic-failover behavior required by the question. Cache availability is part of the requirement, not only read latency.",
    B: "Larger instances can add capacity, but do not automatically replace failed instances or scale with changing demand. Auto Scaling addresses the resilience gap.",
    C: "Adding two fixed instances adds headroom but still lacks automatic replacement and demand-responsive fleet management.",
    D: "An Auto Scaling group across AZs maintains the fleet and replaces unhealthy instances while the ALB distributes requests to healthy targets.",
    E: "Redis caching reduces repeated database reads; configure replication and Multi-AZ automatic failover to satisfy the cache fault-tolerance requirement.",
  },
  "w8-45": {
    A: "Encryption protects stored log confidentiality, but does not provide the signed digest verification needed to detect altered or missing CloudTrail log files.",
    C: "One trail can capture console and SDK API activity. S3 access logs show bucket access, not cryptographic integrity of the CloudTrail files.",
    D: "Macie classifies sensitive content; it does not validate CloudTrail signed digest chains. Splitting console and SDK events into trails is also unnecessary.",
  },
  "w8-46": {
    A: "Step scaling can react rapidly, but request count is a weak signal when requests have very different CPU costs. CPU utilization reflects this workload's actual bottleneck.",
    B: "This combines the less suitable request-count signal with simple scaling's cooldown behavior. It reacts less well to successive rapid load changes.",
    C: "CPU is the appropriate metric, but simple scaling waits through cooldown behavior. Step scaling adjusts by alarm severity and can respond to successive breaches.",
  },
  "w8-47": {
    A: "An RDS Multi-AZ standby is Regional, not a standby AZ in another Region. The option also assumes a managed-RPO setting that is not the RDS feature selected here.",
    B: "DynamoDB requires changing the relational PostgreSQL data model and application access code. That conflicts with minimum application change.",
    C: "RDS supports cross-Region read replicas, but the stated managed-RPO control belongs to the Aurora PostgreSQL global-database design in the captured answer.",
  },
  "w8-48": {
    A: "DNS geolocation cannot inspect an individual user's cookie or other HTTP attributes. It cannot implement the location-independent user exceptions.",
    B: "CloudFront behaviors select by path pattern, not by the request's hostname as described. An alternate domain alone also does not implement per-user exceptions.",
    C: "Client redirects expose a different URL and require an extra request. Direct origin selection at the edge meets the same-location and user-exception routing goal more directly.",
  },
  "w8-49": {
    B: "A custom copy Lambda adds code, retries, and synchronization maintenance. Native S3 replication handles the low-update/high-read replica with less ongoing administration.",
    C: "An interface endpoint has per-hour and processing charges, while repeated remote reads also incur cross-Region transfer. For a small, rarely changed dataset, local replicated reads are cheaper.",
    D: "Moving object data into two EFS systems and synchronizing them introduces file-system cost and management. The application already consumes S3 objects.",
  },
  "w8-50": {
    A: "Parameter Store can supply Regional AMI IDs, but an ordinary stack in one account does not itself deploy into every other account. StackSets supplies the missing multi-account orchestration.",
    C: "A Regional mapping avoids hand-editing each AMI reference, but importing and deploying the template separately in every account retains repetitive deployment work.",
    D: "Parameters centralize values by location, but copying templates and launching stacks in every account/Region remains manual. StackSets manages those instances together.",
  },
  "w8-1": {
    A: "Changing IAM in the management account affects identities in that account; it does not remove an organization-wide SCP restriction on member accounts. IAM allows cannot override an SCP deny.",
    B: "Member-account root users are also constrained by SCPs. Signing in as root and editing local IAM policies cannot remove the inherited organization restriction.",
    C: "The member-account root user does not gain authority to edit the organization's SCPs. Correct the policy through the management account with the appropriate Organizations permissions.",
  },
  "w8-2": {
    B: "This reverses the inheritance: HR would inherit Recruiting's additional restrictions. Removing and rejoining accounts also adds disruption when moving accounts between OUs is sufficient.",
    C: "The HR-parent/Recruiting-child relationship is appropriate, but taking accounts out of the organization is unnecessary. Move them directly to a newly created child OU instead.",
    D: "Making HR a child of Recruiting applies Recruiting's stricter controls to HR too. Put common controls on HR and the additional restrictions on its Recruiting child.",
  },
  "w8-3": {
    A: "Port 20641 is the client's ephemeral return port, not the server's listening port 5001. The VPC flow-log REJECT points to a VPC control, not a host-firewall change on the listener.",
    C: "Security groups are stateful: replies to permitted connections are automatically allowed. Adding a separate inbound reply-port rule addresses the wrong filtering behavior.",
    D: "Route tables select next hops; they do not contain inbound/outbound port permissions. The accepted request and rejected response identify a return-path filtering issue instead.",
  },
  "w8-4": {
    A: "For the recorded answer, the deciding detail is ordered stateless filtering: evaluate the trusted-source allow before the broad SSH deny. A stateful rule group is a different evaluation model and needs its own carefully validated ordering.",
    B: "Content auditing with remediation corrects noncompliant security groups after detection. The question's key favors centrally managed traffic enforcement that member accounts cannot modify.",
    C: "Identifying noncompliant resources is detection, not enforcement. An additional permissive security group could still broaden access unless corrective enforcement is configured.",
  },
  "w8-5": {
    A: "Latency DNS can choose a nearby ALB, but an ALB DNS name does not provide the two permanent global anycast IP addresses that customers require.",
    B: "An NLB supplies Regional addresses; DNS geolocation does not turn two Regional endpoints into a single pair of global anycast addresses. Geography also differs from measured latency.",
    D: "Failover routing is designed for primary/secondary operation. This requirement is active-active and also needs a stable global pair of IP addresses.",
  },
  "w8-6": {
    A: "Running full compute capacity in both Regions increases standby cost. Snapshot copying also gives a less current recovery database than the existing continuously replicated read replica.",
    B: "Equal-weight Regional endpoints describe active-active routing, while the backup has zero compute capacity. The design needs coordinated promotion, scale-up, and primary/secondary failover.",
    C: "Latency routing can send clients to either Region instead of holding the backup as secondary. It does not express the pilot-light failover policy the question requires.",
  },
  "w8-7": {
    A: "Rehosting Db2 on EC2 preserves the database server but leaves its administration with the company. The requirement prefers a managed database where migration is feasible.",
    D: "DataSync moves files and objects; it is not a database engine-conversion and change-data-capture service. Db2-to-MySQL migration needs schema conversion and database migration tooling.",
    E: "DataSync does not replicate a bootable Windows server, installed software, and customized OS configuration. Use server rehosting for an application whose source code is unavailable.",
    B: "Rehosting preserves the legacy Windows installation and its hardcoded OS dependencies. It avoids a source-code rewrite that the company cannot perform.",
    C: "Database migration plus schema conversion moves Db2 data toward a managed MySQL target. This addresses the managed-service objective independently of rehosting the Windows application.",
  },
  "w8-8": {
    A: "Tags describe attachments but do not automatically create tag-based packet-routing rules in a standard transit gateway route table. Isolation needs explicit route-table associations and propagation.",
    B: "Security groups have allow rules, not explicit deny rules. They also do not replace the requested separation of the transit gateway routing domains.",
    C: "The described tag-based Network Manager policy is not the standard transit-gateway mechanism for segmenting these attachments. Separate route tables directly express which VPC routes are reachable.",
  },
  "w8-9": {
    A: "OAC signs CloudFront-to-S3 requests. A bucket policy scoped to the distribution can allow that origin path while keeping direct public S3 requests blocked.",
    B: "Checking the secret origin header at the ALB rejects requests that bypass CloudFront. The enforcement must sit at the origin that an attacker could contact directly.",
    C: "A WAF rule attached only to CloudFront does not inspect requests sent directly to the ALB. It cannot close the origin-bypass path.",
    D: "CloudFront must insert the secret header on origin requests so the ALB-side rule has something to validate. This supplies the signal; the ALB-side rule enforces it.",
    E: "Adding a header at the ALB does not prove that an incoming request passed through CloudFront. The trusted upstream component must add the signal before origin validation.",
    F: "An S3 ACL cannot scope access to a particular CloudFront distribution in the way an OAC-aware bucket policy can. Use the signed origin request and policy together.",
  },
  "w8-10": {
    A: "Changing the database does not make the intake queue durable. Instance-store persistence still disappears with instance failure, and CPU is a poor scaling signal for workers mostly waiting on external calls.",
    C: "A synchronous API-to-Lambda request still waits on roughly 90 seconds of processing, while clients time out after 10 seconds. Durable asynchronous intake is the missing component.",
    D: "A Redis sidecar inside each task is not a shared durable work queue. Replacing the task can lose queued work, and scaling creates separate queues rather than one reliable backlog.",
  },
  "w8-11": {
    B: "A DNS zone apex cannot be a CNAME because it must also contain the zone's SOA and NS records. Use a Route 53 alias to the ALB at the apex.",
    C: "A private hosted zone serves associated VPCs, not the company's public internet audience. The alias type is appropriate, but the zone visibility is wrong.",
    D: "This has two mismatches: private DNS is not publicly resolvable, and a CNAME cannot be used at the zone apex. Public alias records solve both.",
  },
  "w8-12": {
    B: "ECS containers standardize container execution, not the complete approved development/test infrastructure catalog and its delegated provisioning permissions.",
    C: "Templates provide repeatable provisioning, but simply storing them in S3 does not provide the governed product portfolio and launch-role boundary described in the requirement.",
    D: "Handcrafted resource-creation IAM restrictions are harder to maintain for complete approved configurations. Service Catalog exposes vetted products without granting unrestricted underlying provisioning access.",
  },
  "w8-13": {
    A: "A distribution is not an IAM principal by itself. Private S3 delivery requires CloudFront's authenticated origin access and a correctly scoped bucket policy, not just naming the distribution as a principal.",
    B: "You cannot assign an arbitrary IAM role to a CloudFront distribution as though it were an EC2 instance profile. OAC supplies CloudFront's signed S3-origin access.",
    D: "OAC controls CloudFront's origin authentication, not other AWS resources' permissions. Grant those resources access in the first bucket's policy or their IAM policies instead.",
  },
  "w8-14": {
    A: "Changing cache engines and adding Redis replicas requires application and topology changes. It does not address the simpler issue: the client is unaware of the added Memcached endpoints.",
    C: "The application is the Memcached client; RDS does not read and write through those cache-node endpoints. Update client discovery/configuration in the application.",
    D: "Replacing Memcached with sharded Redis is a larger migration than discovering the new nodes. The question explicitly asks for the least code change.",
  },
  "w8-15": {
    A: "An actual-cost threshold fires after the spending has occurred. The CFO asks for advance warning based on a projection, even though the stop action is appropriate.",
    C: "The forecast alert is appropriate, but waiting for an operator adds response delay and execution risk. A configured Budgets action can stop the specified instances automatically.",
    D: "This waits both for actual spending to reach the threshold and for a human to respond. It misses the forecast requirement and provides the weakest response automation.",
  },
  "w8-16": {
    A: "Attaching the Region restriction at the organization root also restricts Prod, which must remain able to use any Region. Apply that restriction only to the Dev OU.",
    B: "Per-account attachment requires ongoing work for future accounts. Root and OU inheritance apply the same policy intent automatically to their descendants.",
    C: "SCP1 on Prod alone leaves Dev root users unrestricted. The root-user restriction must cover all member accounts, while only Dev receives the Region restriction.",
  },
  "w8-17": {
    B: "Fargate requires a containerized application and removes control of the underlying host OS. This tightly coupled, heavily customized workload cannot currently be modernized.",
    C: "ECS on EC2 retains host control, but containerizing and repackaging all integrated applications still adds migration work compared with rehosting their existing servers.",
    D: "Elastic Beanstalk expects a deployable application bundle in a supported environment. Packaging the customized legacy environment for it is a replatforming effort, not the least-change server migration.",
  },
  "w8-18": {
    A: "An ALB already spans the configured Availability Zones. Duplicating it does not remove the single-AZ dependency of the lone NAT gateway.",
    B: "DynamoDB is already replicated across Availability Zones within a Region. Global tables address multi-Region needs, while this design's immediate gap is AZ-local outbound connectivity.",
    D: "An internet gateway is a VPC-level component, not one deployed per subnet or AZ. The zonal component that needs redundancy is the NAT gateway.",
  },
  "w8-19": {
    B: "Fargate Spot offers interruption-tolerant savings, but Fargate does not run the company's custom EC2 AMI. The custom-image requirement forces an EC2 compute environment.",
    C: "Managed EC2 satisfies the AMI and administration requirements, but On-Demand misses the available Spot savings for this explicitly restartable batch workload.",
    D: "Fargate removes server management but cannot use a custom EC2 AMI. It also omits the Spot purchasing model suited to restartable work.",
  },
  "w8-20": {
    A: "EFA supports low-latency communication for compatible tightly coupled HPC software. The instance type and application networking stack must support it.",
    B: "Partition placement isolates failure domains for distributed systems. It is not the placement strategy aimed at the closest possible network locality for tightly coupled HPC.",
    C: "Burstable instances target intermittent CPU demand. Sustained tightly coupled computation needs predictable CPU and network performance rather than CPU-credit behavior.",
    D: "The recorded HPC tuning choice dedicates physical-core resources rather than sharing execution resources between sibling hardware threads. Benchmark this setting for the actual workload.",
    E: "Legacy PV virtualization is not a performance prerequisite for modern HPC networking. Select compatible modern instances, drivers, and images rather than PV support.",
    F: "Keeping the communicating instances in one AZ avoids cross-AZ network distance. This optimizes the stated latency goal, with the availability tradeoff assessed separately.",
  },
  "w8-21": {
    B: "StackSets can deploy plans, but an Organizations backup policy directly centralizes the inherited backup rules. The recorded question favors the organization-native policy mechanism.",
    C: "A Service Catalog product still depends on each administrator launching it. That does not reliably enforce daily backups in every existing and future account.",
    D: "Organizations backup policies integrate with AWS Backup, not with DLM as the policy execution engine. DLM manages EBS snapshot lifecycle through a different mechanism.",
  },
  "w8-22": {
    A: "The archive age is appropriate, but leaving every object in Standard for the first 180 days misses savings on objects that are already infrequently accessed during that mixed-access period.",
    B: "Deep Archive retrieval does not meet the six-hour access window. The first 180 days also remain unoptimized for varying access patterns.",
    D: "Intelligent-Tiering handles changing access patterns, but its Deep Archive Access tier has a longer retrieval window than the six-hour requirement permits.",
  },
  "w8-23": {
    A: "Trusting every user in AccountB would not enforce the requirement that only Auditor can assume the role. Restrict the trust policy's Principal to Auditor's ARN.",
    C: "Inline and managed identity policies can both grant sts:AssumeRole. Changing the policy packaging does not add the missing trust relationship in AccountA.",
    D: "A new role in AccountB does not make AccountA's existing role trust Auditor. The target role's trust policy is the missing side of cross-account authorization.",
  },
  "w8-24": {
    A: "Restoring a database from backup requires provisioning and recovery before it can serve writes. Promoting an already replicated database gives the faster recovery path requested.",
    C: "This combines a slower backup restore with weighted routing, which expresses traffic proportions rather than primary/secondary failover.",
    D: "The replica improves database recovery time, but weighted DNS alone does not express the required automatic primary/backup health-based routing behavior.",
  },
  "w8-25": {
    A: "The stable website baseline should not depend on interruptible Spot capacity, and Reserved Instances fit predictable baseline use rather than temporary peaks. Memory-optimized R instances also miss the compute-heavy analysis fit.",
    B: "The baseline/peak purchasing split is appropriate, but memory-optimized R instances are not the best match for CPU-heavy video analysis. The extra website platform migration is also unnecessary.",
    C: "Spot can interrupt peak website capacity and On-Demand misses baseline commitment savings. The recorded design reserves predictable web demand and uses Spot for restartable background analysis.",
  },
};
