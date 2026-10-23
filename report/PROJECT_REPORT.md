# AWS VPC Peering Project Report — EWB

**Student:** VENTRAPRAGADA VENKATA SUBBARAO  
**Batch:** AWS INTERNSHIP BATCH 1.1  
**Region:** US East (N. Virginia), `us-east-1`

## 1. Objective

Create private IPv4 connectivity between two non-overlapping VPCs through VPC peering. VPC A has a public bastion and App-A in a private subnet. VPC B has App-B in a private subnet with no public IPv4 address.

## 2. Actual observed resource inventory

| Resource | CIDR / IP | ID |
|---|---|---|
| VPC A | `10.10.0.0/16` | `vpc-094290dd996bdde79` |
| VPC B | `10.20.0.0/16` | `vpc-05463d53d9e3da06c` |
| Public subnet A | `10.10.1.0/24` | `subnet-0bca7727144ff4450` |
| Private subnet A | `10.10.2.0/24` | `subnet-08c38e5c7cf56cf16` |
| Private subnet B | `10.20.1.0/24` | `subnet-034834e10587f4b19` |
| Bastion | Private `10.10.1.10`; public `32.192.245.103` | `i-080bd656190adfe0c` |
| App-A | `10.10.2.108`; no public IPv4 observed | `i-005788d06eff77db3` |
| App-B | `10.20.1.226`; no public IPv4 observed | `i-03eb8ec8840385621` |
| VPC peering | Observed Active | `pcx-0cf7c6b7b06ee3eeb` |

The actual App-A and App-B IPs differ from the sample addresses in the workbook. Actual IPs are used throughout this report.

## 3. Route tables

| Route table | Destination | Target |
|---|---|---|
| `ewb-rt-a-public` (`rtb-0bffd516469dc9220`) | `10.10.0.0/16` | local |
| | `0.0.0.0/0` | Internet Gateway |
| | `10.20.0.0/16` | `pcx-0cf7c6b7b06ee3eeb` |
| `ewb-rt-a-private` (`rtb-0df315a397a97459a`) | `10.10.0.0/16` | local |
| | `10.20.0.0/16` | `pcx-0cf7c6b7b06ee3eeb` |
| `ewb-rt-b-private` (`rtb-0e04e73e930ddf38c`) | `10.20.0.0/16` | local |
| | `10.10.0.0/16` | `pcx-0cf7c6b7b06ee3eeb` |

## 4. Validation results observed

| Test | Result |
|---|---|
| Laptop SSH to bastion | Successful |
| SSH to App-B through bastion with ProxyCommand | Successful shell on App-B |
| App-A (`10.10.2.108`) → App-B (`10.20.1.226`) | 4 replies, 0% packet loss |
| App-B (`10.20.1.226`) → App-A (`10.10.2.108`) | 4 replies, 0% packet loss |
| Controlled ICMP rule-removal | 0 received, 100% packet loss while inbound ICMP rule was removed |
| Recovery after restoring ICMP rule | 4 replies, 0% packet loss |

## 5. How the design works

Forward path: App-A's private route table sends `10.20.0.0/16` to the active peering connection. App-B's security group controls whether the incoming request is accepted.

Return path: VPC B's route table sends `10.10.0.0/16` back through the peering connection so replies can return to VPC A.

SSH: the laptop connects to the bastion public IP. ProxyCommand opens the second SSH connection to App-B's private IP. The key remains on the laptop.

## 6. Learning outcomes

- Peering requires reciprocal routes; Active status alone does not guarantee connectivity.
- Security groups allow or block instance traffic independently of route tables.
- SSH source for App-B is the bastion private IP (`10.10.1.10`).
- Use actual assigned IPs consistently when they differ from the workbook plan.

## 7. Submission and cleanup checklist

- [x] Peering status and route tables documented based on screenshots reviewed
- [x] Forward and reverse private-IP ping success observed
- [x] SSH access to App-B via bastion observed
- [x] Controlled ICMP failure and recovery observed
- [ ] Fill in student name and batch
- [ ] Verify all resource IDs and security rules in live AWS state
- [ ] Add cleanup evidence after actually deleting lab resources

After saving evidence, follow page 14 of the workbook: terminate the three lab EC2 instances; check for leftover EBS volumes, snapshots, and Elastic IPs; remove the peering connection and routes; delete lab security groups after ENIs disappear; then remove subnets, custom route tables, the Internet Gateway, and both lab VPCs. Verify the Region is clear. Do not claim cleanup is complete until it is actually done.
