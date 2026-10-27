import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { answerCorrections, courseDistractorExplanations, optionExplanations, studyCaveats } from "../content/option-explanations.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(here, "..");
const sourceRoot = path.resolve(siteRoot, "..");

const read = (name) => fs.readFileSync(path.join(sourceRoot, name), "utf8");
const clean = (value = "") =>
  value
    .replace(/\*\*/g, "")
    .replace(/`/g, "")
    .replace(/✅/g, "")
    .replace(/^>\s?/gm, "")
    .replace(/>\s*/g, " ")
    .replace(/\s+/g, " ")
    .trim();

const taskByDomain = {
  "1": "Organizational complexity",
  "2": "New solution design",
  "3": "Continuous improvement",
  "4": "Migration and modernization",
};

function inferDomain(text) {
  const value = text.toLowerCase();
  if (/(migrat|moderniz|mainframe|aws transform|application migration service|\bmgn\b|\bdms\b|schema conversion|snowball|datasync|migration hub)/.test(value)) return "4";
  if (/(organizations|service control policy|\bscp\b|control tower|multi-account|cross-account|transit gateway|aws ram|resource access manager|direct connect|site-to-site vpn|hybrid|firewall manager|iam access analyzer|identity center)/.test(value)) return "1";
  if (/(existing|improve|rightsiz|rightsiz|optimiz|cloudwatch|patch|vulnerabil|inspector|operational excellence|cost management|trusted advisor|compute optimizer|performance issue)/.test(value)) return "3";
  return "2";
}

function inferTopic(text) {
  const value = text.toLowerCase();
  const topics = [
    [/(organizations|\bscp\b|control tower|multi-account)/, "Multi-account governance"],
    [/(transit gateway|vpc|vpn|direct connect|route 53 resolver|privatelink|network)/, "Networking and hybrid connectivity"],
    [/(iam|kms|waf|shield|security hub|guardduty|macie|firewall|encrypt)/, "Security and identity"],
    [/(aurora|rds|dynamodb|database|elasticache|memorydb)/, "Databases and data"],
    [/(s3|efs|storage gateway|backup|glacier|object lock)/, "Storage and backup"],
    [/(cloudfront|global accelerator|route 53|edge)/, "Global delivery and edge"],
    [/(ecs|eks|ec2|lambda|autoscaling|batch|container)/, "Compute and scaling"],
    [/(migrat|mainframe|dms|mgn|snowball|datasync)/, "Migration and modernization"],
    [/(budget|cost|pricing|saving|reserved|spot)/, "Cost optimization"],
  ];
  return topics.find(([pattern]) => pattern.test(value))?.[1] ?? "Architecture decision-making";
}

function question({ id, sourceCategory, sourceLabel, sourceDetail, coreEligible, prompt, options, correctIds, rationale, emerging = false }) {
  const domain = inferDomain(`${prompt} ${rationale}`);
  const topic = inferTopic(`${prompt} ${rationale}`);
  return {
    id,
    sourceCategory,
    sourceLabel,
    sourceDetail,
    coreEligible,
    emerging,
    domain,
    task: taskByDomain[domain],
    topic,
    type: correctIds.length === 1 ? "multiple-choice" : "multiple-response",
    selectCount: correctIds.length,
    prompt: clean(prompt),
    options: options.map((option) => ({ id: option.id, text: clean(option.text) })),
    correctIds,
    rationale: clean(rationale),
    wrongAnswerHelp: "Start with the explicit business constraint, then eliminate choices that solve a different layer of the architecture or add unnecessary operational work.",
    references: ["https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02.html"],
  };
}

function parseWeek8() {
  const source = read("week-8-practice-exam-questions.md");
  const matches = [...source.matchAll(/^### Q(\d+) — Correct: (.*?)\n\n([\s\S]*?)(?=^### Q\d+ — Correct:|^## Appendix|(?![\s\S]))/gm)];
  const entries = matches.map((match) => {
    const [, number, correctHeader, body] = match;
    const firstOption = body.search(/^[-] (?:\*\*)?[A-F]\. /m);
    const questionBlock = firstOption >= 0 ? body.slice(0, firstOption) : body;
    const prompt = questionBlock
      .split("\n")
      .filter((line) => line.startsWith(">"))
      .join(" ");
    const options = body
      .split("\n")
      .map((line) => line.match(/^- (?:\*\*)?([A-F])\.\s+(.*)$/))
      .filter(Boolean)
      .map((option) => ({ id: option[1], text: option[2] }));
    const correctIds = [...correctHeader.matchAll(/(?:^|,\s*)([A-F])(?=,|\s|$)/g)].map((item) => item[1]);
    const rationaleMatch = body.match(/\*\*Why:\*\*\s*([^\n]+)/);
    return question({
      id: `w8-${number}`,
      sourceCategory: "captured",
      sourceLabel: "Week 8 captured practice exam",
      sourceDetail: `Official Practice Exam capture — Question ${number}`,
      coreEligible: true,
      prompt,
      options,
      correctIds,
      rationale: rationaleMatch?.[1] ?? "Review the Week 8 study notes for the recorded AWS rationale.",
    });
  });
  const invalidEntries = entries.filter((entry) => entry.options.length < 4 || entry.correctIds.length === 0);
  if (entries.length !== 75 || invalidEntries.length > 0) {
    throw new Error(`Week 8 parser validation failed: ${entries.length} records; invalid ${invalidEntries.map((entry) => `${entry.id}:${entry.options.length}/${entry.correctIds.join("")}`).join(", ")}`);
  }
  return entries;
}

function parseCsv(raw) {
  const rows = [];
  let row = [];
  let cell = "";
  let quoted = false;
  for (let index = 0; index < raw.length; index += 1) {
    const character = raw[index];
    if (character === '"') {
      if (quoted && raw[index + 1] === '"') {
        cell += '"';
        index += 1;
      } else quoted = !quoted;
    } else if (character === "," && !quoted) {
      row.push(cell);
      cell = "";
    } else if ((character === "\n" || character === "\r") && !quoted) {
      if (character === "\r" && raw[index + 1] === "\n") index += 1;
      row.push(cell);
      if (row.some((value) => value.length > 0)) rows.push(row);
      row = [];
      cell = "";
    } else cell += character;
  }
  row.push(cell);
  if (row.some((value) => value.length > 0)) rows.push(row);
  const [header, ...data] = rows;
  return data.map((values) => Object.fromEntries(header.map((key, index) => [key, values[index] ?? ""])));
}

function parseOptions(value) {
  return value
    .trim()
    .split(/\n(?=[A-F]\.\s)/)
    .map((line) => {
      const match = line.match(/^([A-F])\.\s+([\s\S]*)$/);
      return match ? { id: match[1], text: match[2] } : null;
    })
    .filter(Boolean);
}

function parseCsvBank() {
  const rows = parseCsv(read("aws_sap_c02_non_week8_quiz_bank.csv"));
  const entries = rows.map((row, index) => {
    const options = parseOptions(row.Choices);
    const correctIds = [...row.Correct_Answer.matchAll(/[A-F]/g)].map((item) => item[0]);
    const foundational = /cloud practitioner|foundations/i.test(`${row.Source} ${row.Question}`) || row.Question.split(/\s+/).length < 18;
    return question({
      id: `csv-${String(index + 1).padStart(2, "0")}`,
      sourceCategory: "csv",
      sourceLabel: "Prior assessment CSV",
      sourceDetail: row.Source,
      coreEligible: !foundational,
      prompt: row.Question,
      options,
      correctIds,
      rationale: row.Rationale,
    });
  });
  const invalidEntries = entries.filter((entry) => entry.options.length < 2 || entry.correctIds.length === 0);
  if (entries.length !== 61 || invalidEntries.length > 0) {
    throw new Error(`CSV parser validation failed: ${entries.length} records; invalid ${invalidEntries.map((entry) => `${entry.id}:${entry.options.length}/${entry.correctIds.join("")}`).join(", ")}`);
  }
  return entries;
}

function between(source, start, end) {
  const from = source.indexOf(start);
  if (from < 0) throw new Error(`Missing source heading: ${start}`);
  const after = source.slice(from + start.length);
  const to = end ? after.indexOf(end) : -1;
  return to < 0 ? after : after.slice(0, to);
}

function extractNumbered(section) {
  const matches = [...section.matchAll(/(?:^|\n)(\d+)\.\s+\*\*(.*?)\*\*\s*([\s\S]*?)(?=\n\d+\.\s+\*\*|$)/g)];
  return matches.map((match) => {
    const prompt = clean(match[2]).replace(/\(select (two|three)\)/gi, "");
    const tail = match[3];
    const answer =
      tail.match(/\*\*Correct answer:\*\*\s*([^\n]+)/i)?.[1] ??
      tail.match(/\*\*Answer:\*\*\s*([^\n]+)/i)?.[1] ??
      tail.split("\n").map(clean).find(Boolean) ??
      "Review the associated course material.";
    return { prompt, answer: clean(answer) };
  });
}

function courseDistractors(domain) {
  const options = {
    "1": [
      "Attach an IAM policy to an OU and manage every account separately.",
      "Use public internet access instead of an organization-level control.",
      "Duplicate the configuration manually in each account.",
    ],
    "2": [
      "Use a single Availability Zone and add recovery steps later.",
      "Build the capability in the application without a managed AWS service.",
      "Choose the option that does not meet the stated availability or latency goal.",
    ],
    "3": [
      "Make a manual change without measuring the workload first.",
      "Keep the existing design even when it violates the stated objective.",
      "Use a service that does not address the identified operational gap.",
    ],
    "4": [
      "Rebuild the workload before collecting migration requirements.",
      "Use a tool designed for a different migration strategy.",
      "Defer migration until after the stated deadline.",
    ],
  };
  return options[domain];
}

function parseCourseDerived() {
  const week5 = read("week-5-study-notes.md");
  const week6 = read("week-6-study-notes.md");
  const week7 = read("week-7-study-notes.md");
  const groups = [
    { label: "Week 5 Domain Practice", values: extractNumbered(between(week5, "## Captured practice questions and answers", "## Captured flashcards")), expected: 6 },
    { label: "Week 5 Well-Architected knowledge checks", values: extractNumbered(between(week5, "### Course knowledge-check questions and answers", "### Final course assessment")), expected: 24 },
    { label: "Week 5 Well-Architected assessment", values: extractNumbered(between(week5, "### Final course assessment", "## Sources")), expected: 14 },
    { label: "Week 6 Domain 3 practice", values: extractNumbered(between(week6, "### Domain 3 Practice", "### Domain 3 flashcard")), expected: 3 },
    { label: "Week 6 Domain 4 practice", values: extractNumbered(between(week6, "### Domain 4 Practice", "## Approach to Mainframe")), expected: 3 },
    { label: "Week 6 Mainframe quiz", values: extractNumbered(between(week6, "### Mainframe course quiz", "## Week 6 SimuLearn")), expected: 8 },
    { label: "Week 7 Migration Hub assessment", values: extractNumbered(between(week7, "### Final course assessment", "## Domain 2 Practice")), expected: 11 },
  ];
  const flattened = groups.flatMap((group) => {
    if (group.values.length !== group.expected) throw new Error(`${group.label}: expected ${group.expected}, got ${group.values.length}`);
    return group.values.map((item) => ({ ...item, label: group.label }));
  });
  const entries = flattened.map((item, index) => {
    const domain = inferDomain(`${item.prompt} ${item.answer}`);
    const distractors = courseDistractors(domain);
    return question({
      id: `course-${String(index + 1).padStart(2, "0")}`,
      sourceCategory: "course-derived",
      sourceLabel: "Course-derived knowledge check",
      sourceDetail: item.label,
      coreEligible: false,
      prompt: `${item.prompt} Choose the best answer based on the recorded course material.`,
      options: [
        { id: "A", text: item.answer },
        { id: "B", text: distractors[0] },
        { id: "C", text: distractors[1] },
        { id: "D", text: distractors[2] },
      ],
      correctIds: ["A"],
      rationale: `The recorded course answer is: ${item.answer}`,
    });
  });
  if (entries.length !== 69) throw new Error(`Course parser validation failed: ${entries.length} records`);
  return entries;
}

const originalSeeds = [
  {
    id: "original-01", domainHint: "1", topic: "Hybrid resilience", prompt: "A company has a critical on-premises application that accesses workloads in AWS over a single AWS Direct Connect connection. The company requires highly available private connectivity with minimal operational overhead. Which solution should the company use?", correct: "Add a Site-to-Site VPN connection as a backup path for the Direct Connect connection.", options: ["Add a Site-to-Site VPN connection as a backup path for the Direct Connect connection.", "Create a public VPC endpoint for every AWS service that the application uses.", "Use an internet gateway as the redundant path for private traffic.", "Deploy a second NAT gateway in the same Availability Zone."], rationale: "A Site-to-Site VPN provides an encrypted, independent backup path for Direct Connect and is a standard highly available hybrid design." },
  {
    id: "original-02", domainHint: "1", topic: "Centralized logging", prompt: "A company needs to retain CloudTrail logs from every current and future account in AWS Organizations in a dedicated account. Member-account administrators must not be able to stop organization-wide logging. Which solution meets these requirements?", correct: "Create an organization trail from the management or delegated administrator account and deliver logs to a bucket in the Log Archive account.", options: ["Create an organization trail from the management or delegated administrator account and deliver logs to a bucket in the Log Archive account.", "Create a trail manually in each member account and ask administrators to protect it.", "Configure AWS Config snapshots in each account and use them as API audit logs.", "Use VPC Flow Logs from a central networking account."], rationale: "An organization trail applies across accounts, including future accounts, and centralizes CloudTrail delivery without relying on member-account administrators." },
  {
    id: "original-03", domainHint: "1", topic: "Network segmentation", prompt: "A company shares a transit gateway with production and development accounts. The company must prevent any production-to-development routing while retaining connectivity inside each environment. Which configuration should the company use?", correct: "Associate and propagate production and development attachments with separate transit gateway route tables.", options: ["Associate and propagate production and development attachments with separate transit gateway route tables.", "Add production and development tags to the VPCs and rely on the default transit gateway route table.", "Use one security group in every account to control transit gateway routing.", "Create an internet gateway in each VPC."], rationale: "Transit gateway route-table association and propagation provide the network-level isolation required between attachment groups." },
  {
    id: "original-04", domainHint: "1", topic: "Hybrid DNS", prompt: "A company needs on-premises DNS clients to resolve private hosted zone records in several AWS VPCs. The company already has private connectivity to AWS. Which solution requires the least ongoing administration?", correct: "Create inbound Route 53 Resolver endpoints and forward the relevant DNS queries from on premises to those endpoints.", options: ["Create inbound Route 53 Resolver endpoints and forward the relevant DNS queries from on premises to those endpoints.", "Publish the private hosted zone records as public DNS records.", "Add a hosts-file entry to every on-premises server.", "Create a NAT gateway for DNS traffic."], rationale: "Inbound Resolver endpoints allow on-premises resolvers to query Route 53 Resolver for private hosted-zone names over private connectivity." },
  {
    id: "original-05", domainHint: "2", topic: "Deployment strategy", prompt: "A company runs a containerized application on Amazon ECS behind an Application Load Balancer. The company needs to deploy a new version, validate it with a small portion of production traffic, and automatically roll back if alarms breach. Which solution should the company use?", correct: "Use AWS CodeDeploy blue/green deployments for Amazon ECS with CloudWatch alarm-based rollback.", options: ["Use AWS CodeDeploy blue/green deployments for Amazon ECS with CloudWatch alarm-based rollback.", "Update all ECS tasks in place and manually inspect logs.", "Create an Amazon S3 lifecycle policy for the container image.", "Use an EC2 Auto Scaling scheduled action."], rationale: "CodeDeploy supports ECS blue/green traffic shifting and can automatically roll back a deployment when configured alarms fire." },
  {
    id: "original-06", domainHint: "2", topic: "Business continuity", prompt: "A company needs a multi-Region PostgreSQL database solution with low replication lag and an RPO measured in seconds. The company wants minimal application changes and managed cross-Region replication. Which solution is best?", correct: "Use an Aurora PostgreSQL global database with a secondary Region.", options: ["Use an Aurora PostgreSQL global database with a secondary Region.", "Create daily EBS snapshots of a self-managed PostgreSQL instance.", "Use a single-AZ RDS DB instance and copy backups monthly.", "Store database exports in Amazon S3 Standard-IA."], rationale: "Aurora global databases provide managed cross-Region replication designed for low-lag disaster recovery with minimal database-engine changes." },
  {
    id: "original-07", domainHint: "2", topic: "Serverless decoupling", prompt: "A company receives unpredictable order submissions. Processing can take several minutes, but the client must receive a response immediately. Which architecture is the most resilient and operationally efficient?", correct: "Accept requests with API Gateway, place messages on Amazon SQS, and process them asynchronously with scaled workers.", options: ["Accept requests with API Gateway, place messages on Amazon SQS, and process them asynchronously with scaled workers.", "Keep each request open until the processing is complete.", "Write each request to an EC2 instance store volume before processing it.", "Use a single Lambda invocation that waits for all downstream systems."], rationale: "A durable queue decouples intake from long-running work and lets the processing fleet scale independently." },
  {
    id: "original-08", domainHint: "2", topic: "Content delivery", prompt: "A company serves private documents from Amazon S3 to global users. The documents must never be reachable directly from S3 and should be delivered with low latency. Which solution meets these requirements?", correct: "Use CloudFront with an Origin Access Control and restrict the S3 bucket policy to the distribution.", options: ["Use CloudFront with an Origin Access Control and restrict the S3 bucket policy to the distribution.", "Make the bucket public and use an S3 ACL for each user.", "Put an internet gateway in front of the bucket.", "Use a NAT gateway to authenticate viewers."], rationale: "CloudFront OAC signs origin requests and allows the bucket policy to permit the distribution while blocking direct public access." },
  {
    id: "original-09", domainHint: "2", topic: "Global routing", prompt: "A company needs a global active-active TCP service in two AWS Regions. Customers require two static anycast IP addresses and the lowest practical latency. Which solution should the company use?", correct: "Use AWS Global Accelerator with regional Network Load Balancer endpoints.", options: ["Use AWS Global Accelerator with regional Network Load Balancer endpoints.", "Use Route 53 geolocation routing with Application Load Balancers.", "Use a CloudFront distribution with an S3 origin.", "Use a single Elastic IP address on an EC2 instance."], rationale: "Global Accelerator provides two static anycast IP addresses and routes TCP traffic over the AWS global network to healthy regional endpoints." },
  {
    id: "original-10", domainHint: "3", topic: "DynamoDB performance", prompt: "An existing DynamoDB workload has highly repetitive, low-latency reads for a small set of keys. The company wants to reduce read latency and DynamoDB read costs with minimal code changes. Which solution is best?", correct: "Add a DynamoDB Accelerator (DAX) cluster in front of the table.", options: ["Add a DynamoDB Accelerator (DAX) cluster in front of the table.", "Create an Amazon RDS read replica for the DynamoDB table.", "Use Amazon S3 Glacier Instant Retrieval for the keys.", "Increase the Lambda memory setting for all clients."], rationale: "DAX is an in-memory cache purpose-built for DynamoDB and is suited to repeated key-based reads." },
  {
    id: "original-11", domainHint: "3", topic: "Cost optimization", prompt: "An existing Amazon EC2 fleet has a stable baseline workload and short, unpredictable peak periods. The company wants to reduce cost without risking baseline capacity. Which purchasing strategy is most appropriate?", correct: "Cover the stable baseline with Savings Plans or Reserved Instances and use On-Demand capacity for unpredictable peaks.", options: ["Cover the stable baseline with Savings Plans or Reserved Instances and use On-Demand capacity for unpredictable peaks.", "Run all workload capacity on Spot Instances.", "Purchase Dedicated Hosts for every instance regardless of licensing needs.", "Stop the baseline fleet during business hours."], rationale: "Commitment discounts fit predictable usage, while On-Demand capacity safely handles uncertain peaks." },
  {
    id: "original-12", domainHint: "3", topic: "Patch operations", prompt: "A company must apply critical operating-system patches to a large fleet of private EC2 instances without opening inbound SSH. The company wants centralized execution and auditability. Which solution should the company use?", correct: "Use AWS Systems Manager Patch Manager and Run Command with the SSM Agent and appropriate instance roles.", options: ["Use AWS Systems Manager Patch Manager and Run Command with the SSM Agent and appropriate instance roles.", "Open port 22 from the internet and patch each instance manually.", "Create a new AMI but do not redeploy instances.", "Use an S3 bucket policy to install operating-system updates."], rationale: "Systems Manager provides agent-based, IAM-controlled fleet operations without inbound SSH access." },
  {
    id: "original-13", domainHint: "3", topic: "Governance remediation", prompt: "A company needs to detect noncompliant resource configurations across many accounts and automatically remediate supported violations. Which solution requires the least custom code?", correct: "Use AWS Config organization rules or conformance packs with Systems Manager Automation remediation.", options: ["Use AWS Config organization rules or conformance packs with Systems Manager Automation remediation.", "Run a monthly spreadsheet review in every account.", "Use only IAM access keys to identify configuration drift.", "Replace all resources with one EC2 instance."], rationale: "AWS Config evaluates configuration compliance at scale, and Systems Manager Automation can perform managed remediation workflows." },
  {
    id: "original-14", domainHint: "4", topic: "Data transfer", prompt: "A company must migrate hundreds of terabytes of archival data from on premises to Amazon S3. Available network bandwidth cannot meet the migration deadline. Which service is the most appropriate?", correct: "Use an AWS Snowball Edge device to transfer the bulk data to AWS.", options: ["Use an AWS Snowball Edge device to transfer the bulk data to AWS.", "Use an Amazon CloudFront distribution to upload the archives.", "Use a Route 53 latency record for the transfer.", "Use an Elastic IP address for the file server."], rationale: "Snowball Edge is designed for large offline data transfers when network transfer is impractical for the available window." },
  {
    id: "original-15", domainHint: "4", topic: "Incremental modernization", prompt: "A company wants to gradually extract capabilities from a monolithic application while minimizing disruption to existing clients. The company needs managed support for routing requests between the legacy application and new services. Which approach is best?", correct: "Use a strangler-fig modernization approach with AWS Migration Hub Refactor Spaces to incrementally route traffic to new services.", options: ["Use a strangler-fig modernization approach with AWS Migration Hub Refactor Spaces to incrementally route traffic to new services.", "Perform a big-bang rewrite before any migration work.", "Copy the monolith into an S3 bucket and serve it with CloudFront.", "Create a single larger EC2 instance and defer modernization."], rationale: "Refactor Spaces supports incremental modernization patterns by reducing the infrastructure work needed to route and connect refactored services." },
  {
    id: "emerging-01", domainHint: "2", emerging: true, topic: "Responsible AI", prompt: "A company is building a generative AI application that must block unsafe user input and prevent disallowed content in model responses. Which AWS capability should the company use?", correct: "Configure Amazon Bedrock Guardrails for the application.", options: ["Configure Amazon Bedrock Guardrails for the application.", "Use an Amazon S3 lifecycle rule.", "Use a NAT gateway to filter prompts.", "Use an EBS snapshot policy."], rationale: "Amazon Bedrock Guardrails provides configurable content filtering and policy controls for generative AI applications." },
  {
    id: "emerging-02", domainHint: "1", emerging: true, topic: "Agent identity", prompt: "A company needs an AI agent to access AWS resources with least privilege and auditable, scoped identities instead of sharing a long-lived access key. Which design is most appropriate?", correct: "Use a managed agent identity and IAM roles scoped to the agent's required actions and resources.", options: ["Use a managed agent identity and IAM roles scoped to the agent's required actions and resources.", "Store an administrator access key in the application source code.", "Allow unauthenticated access through a public bucket.", "Attach AdministratorAccess to every agent session."], rationale: "Scoped, auditable identities and least-privilege IAM permissions avoid shared, long-lived credentials for agentic workloads." },
  {
    id: "emerging-03", domainHint: "2", emerging: true, topic: "Human oversight", prompt: "A generative AI workflow can issue refunds, but high-value refunds require human approval before the action is taken. Which AWS design best provides this control?", correct: "Use an AWS Step Functions workflow that pauses for an explicit human approval before the refund task runs.", options: ["Use an AWS Step Functions workflow that pauses for an explicit human approval before the refund task runs.", "Let the model invoke the refund API directly with administrator permissions.", "Store the approval text in an instance-store volume.", "Use CloudFront caching to validate refunds."], rationale: "Step Functions can model durable approval workflows and prevent an automated action from continuing until an approver responds." },
  {
    id: "emerging-04", domainHint: "3", emerging: true, topic: "Responsible AI", prompt: "A company must log model requests and responses for audit while minimizing exposure of sensitive data. Which practice is best?", correct: "Apply data minimization and redaction before logging, encrypt retained audit records, and limit access with least-privilege IAM policies.", options: ["Apply data minimization and redaction before logging, encrypt retained audit records, and limit access with least-privilege IAM policies.", "Log all prompts and responses publicly for transparency.", "Disable all logs so no data can be exposed.", "Store unencrypted audit records in a public S3 bucket."], rationale: "Responsible AI auditing requires traceability while applying data-protection controls and minimizing unnecessary sensitive-data retention." },
  {
    id: "emerging-05", domainHint: "1", emerging: true, topic: "AI access controls", prompt: "A company exposes a knowledge-base assistant to employees. The assistant must retrieve only documents the requesting employee is authorized to view. Which design principle is most important?", correct: "Enforce authorization at retrieval time by propagating the caller identity and filtering documents by access permissions.", options: ["Enforce authorization at retrieval time by propagating the caller identity and filtering documents by access permissions.", "Give the assistant one unrestricted role that can read every document.", "Copy all documents into a publicly readable bucket.", "Rely only on client-side UI controls to hide documents."], rationale: "Authorization must be enforced by the retrieval and data-access layer, not only by the user interface or a broadly privileged shared identity." },
];

function parseOriginals() {
  return originalSeeds.map((seed) => {
    const entry = question({
      id: seed.id,
      sourceCategory: seed.emerging ? "emerging" : "original",
      sourceLabel: seed.emerging ? "Optional emerging-topic practice" : "Original SAP-C02-style scenario",
      sourceDetail: seed.emerging ? "Current SAP-C02 emerging-topic practice" : "Author-created from Weeks 1–4 material and AWS documentation",
      coreEligible: !seed.emerging,
      emerging: Boolean(seed.emerging),
      prompt: seed.prompt,
      options: seed.options.map((text, index) => ({ id: String.fromCharCode(65 + index), text })),
      correctIds: [String.fromCharCode(65 + seed.options.indexOf(seed.correct))],
      rationale: seed.rationale,
    });
    entry.domain = seed.domainHint;
    entry.task = taskByDomain[seed.domainHint];
    entry.topic = seed.topic;
    return entry;
  });
}

const bank = [...parseWeek8(), ...parseCsvBank(), ...parseCourseDerived(), ...parseOriginals()].map((entry) => {
  const correction = answerCorrections[entry.id];
  const updated = { ...entry, ...studyCaveats[entry.id], ...correction };
  if (correction) updated.recordedCorrectIds = entry.correctIds;
  updated.options = entry.options.map((option) => {
    const explanation = optionExplanations[entry.id]?.[option.id]
      ?? (updated.correctIds.includes(option.id) ? updated.rationale : undefined)
      ?? (entry.sourceCategory === "course-derived" ? courseDistractorExplanations[option.text] : undefined);
    if (!explanation) throw new Error(`Missing option explanation: ${entry.id}/${option.id}`);
    return { ...option, explanation };
  });
  return updated;
});
const ids = new Set(bank.map((entry) => entry.id));
const sourceCounts = bank.reduce((counts, entry) => ({ ...counts, [entry.sourceCategory]: (counts[entry.sourceCategory] ?? 0) + 1 }), {});
if (bank.length !== 225 || ids.size !== 225 || sourceCounts.captured !== 75 || sourceCounts.csv !== 61 || sourceCounts["course-derived"] !== 69 || sourceCounts.original !== 15 || sourceCounts.emerging !== 5) {
  throw new Error(`Question bank validation failed: ${bank.length} records; ${JSON.stringify(sourceCounts)}`);
}
fs.writeFileSync(path.join(siteRoot, "public", "question-bank.json"), `${JSON.stringify(bank, null, 2)}\n`);
console.log(`Generated ${bank.length} questions: ${JSON.stringify(sourceCounts)}`);
