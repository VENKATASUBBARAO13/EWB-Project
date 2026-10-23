# AWS VPC Peering Project — EWB

A hands-on AWS networking project demonstrating private communication between two VPCs using VPC peering, route tables, security groups, and a bastion host.

> **Evidence note:** The successful forward/reverse pings, SSH through the bastion, and an ICMP rule-removal failure followed by recovery were observed during the lab. Cleanup evidence must be added only after resources are actually removed.

## Architecture

**Region:** US East (N. Virginia) — `us-east-1`

- **VPC A:** `10.10.0.0/16` (`vpc-094290dd996bdde79`)
  - Public subnet: `10.10.1.0/24`
  - Bastion: private `10.10.1.10`, public `32.192.245.103`
  - Private subnet: `10.10.2.0/24`
  - App-A: `10.10.2.108` (no public IPv4 observed)
- **VPC B:** `10.20.0.0/16` (`vpc-05463d53d9e3da06c`)
  - Private subnet: `10.20.1.0/24`
  - App-B: `10.20.1.226` (no public IPv4 observed)
- **Peering:** `pcx-0cf7c6b7b06ee3eeb` (observed Active)

The workbook's example host IPs differed from AWS-assigned addresses for App-A and App-B. This project documents the actual IPs observed in the EC2 details and terminal results.

## Resource inventory

| Component | CIDR / IP | Resource ID |
|---|---|---|
| VPC A | `10.10.0.0/16` | `vpc-094290dd996bdde79` |
| VPC B | `10.20.0.0/16` | `vpc-05463d53d9e3da06c` |
| VPC A public subnet | `10.10.1.0/24` | `subnet-0bca7727144ff4450` |
| VPC A private subnet | `10.10.2.0/24` | `subnet-08c38e5c7cf56cf16` |
| VPC B private subnet | `10.20.1.0/24` | `subnet-034834e10587f4b19` |
| Bastion | `10.10.1.10`; public `32.192.245.103` | `i-080bd656190adfe0c` |
| App-A | `10.10.2.108`; no public IPv4 observed | `i-005788d06eff77db3` |
| App-B | `10.20.1.226`; no public IPv4 observed | `i-03eb8ec8840385621` |

## Route tables

| Route table | Destination | Target |
|---|---|---|
| `ewb-rt-a-private` | `10.10.0.0/16` | local |
| `ewb-rt-a-private` | `10.20.0.0/16` | `pcx-0cf7c6b7b06ee3eeb` |
| `ewb-rt-b-private` | `10.20.0.0/16` | local |
| `ewb-rt-b-private` | `10.10.0.0/16` | `pcx-0cf7c6b7b06ee3eeb` |
| `ewb-rt-a-public` | `0.0.0.0/0` | Internet Gateway |
| `ewb-rt-a-public` | `10.10.0.0/16` | local |
| `ewb-rt-a-public` | `10.20.0.0/16` | `pcx-0cf7c6b7b06ee3eeb` |

## Validation

| Test | Observed result |
|---|---|
| Bastion SSH | Successful SSH login to `32.192.245.103` |
| SSH to App-B through bastion | Successful shell on `ip-10-20-1-226` through SSH ProxyCommand |
| App-A `10.10.2.108` → App-B `10.20.1.226` | 4 replies, 0% packet loss |
| App-B `10.20.1.226` → App-A `10.10.2.108` | 4 replies, 0% packet loss |
| Controlled ICMP failure | Ping failed with 100% packet loss when App-B's ICMP inbound rule was removed |
| Recovery | Ping returned to 4 replies, 0% loss after the ICMP rule was restored |

## Project report

See [report/PROJECT_REPORT.md](report/PROJECT_REPORT.md) for the report, traffic-path explanation, route tables, verification outcomes, and finalization checklist.

## Key concepts demonstrated

- Non-overlapping VPC CIDRs
- Public/private subnets and explicit route-table associations
- Active peering with forward and return routes
- Security-group controls for SSH and ICMP
- Private SSH access through a bastion without copying the private key to an EC2 instance
- Negative testing and recovery after a security-rule change

## Before final submission

- Fill in student name and batch in the report.
- Verify IDs and route associations against live AWS state.
- Add selected screenshots to this repository (after reviewing them for sensitive information).
- Add cleanup screenshots only after the lab resources are actually removed.
- Never commit PEM/private keys, passwords, AWS credentials, or tokens.

**Security reminder:** this is a public repository. Review any screenshots before uploading, and ensure the bastion SSH security group is restricted to your current public IP `/32`, not `0.0.0.0/0`.
