# AWS VPC Peering Project — EWB

A hands-on AWS networking project demonstrating private communication between two VPCs using VPC peering, custom route tables, security groups, and a bastion host.

> **Evidence note:** This README records the configuration and terminal results captured during the lab. The controlled ICMP failure/recovery test was observed in the terminal screenshots. Cleanup evidence should be added only after the resources are actually removed.

## Architecture

![AWS VPC Peering Architecture](docs/architecture.png)

**Region:** US East (N. Virginia) — `us-east-1`

## Network design

| Component | CIDR / IP | Resource ID |
|---|---|---|
| VPC A (`ewb-vpc-a`) | `10.10.0.0/16` | `vpc-094290dd996bdde79` |
| VPC B (`ewb-vpc-b`) | `10.20.0.0/16` | `vpc-05463d53d9e3da06c` |
| VPC A public subnet | `10.10.1.0/24` | `subnet-0bca7727144ff4450` |
| VPC A private subnet | `10.10.2.0/24` | `subnet-08c38e5c7cf56cf16` |
| VPC B private subnet | `10.20.1.0/24` | `subnet-034834e10587f4b19` |
| Bastion | Private `10.10.1.10`; public `32.192.245.103` | `i-080bd656190adfe0c` |
| App-A | `10.10.2.108`; no public IPv4 | `i-005788d06eff77db3` |
| App-B | `10.20.1.226`; no public IPv4 | `i-03eb8ec8840385621` |
| VPC peering | `pcx-0cf7c6b7b06ee3eeb` (observed Active) | — |

The workbook's planned host IPs differed from AWS-assigned addresses for App-A and App-B. This project uses the actual observed addresses in commands and rules.

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
| Bastion SSH | SSH login succeeded to public IPv4 `32.192.245.103` |
| SSH to App-B through bastion | Successful shell on `ip-10-20-1-226` using SSH ProxyCommand |
| App-A `10.10.2.108` → App-B `10.20.1.226` | 4 packets received, 0% packet loss |
| App-B `10.20.1.226` → App-A `10.10.2.108` | 4 packets received, 0% packet loss |
| Controlled ICMP rule removal | Ping failed with 100% packet loss |
| ICMP rule restored | A successful ping with 0% packet loss was captured after restoration |

## Evidence and report

- [Project report PDF](report/YourName_EWB_VPC_Peering.pdf)
- [Architecture diagram](docs/architecture.png)
- Screenshots are organized in `screenshots/`, with names corresponding to the step being documented.

## Key concepts demonstrated

- Non-overlapping VPC CIDR ranges
- Public and private subnet routing
- Active VPC peering and routes in both directions
- Security-group controls for SSH and ICMP
- Private SSH access through a bastion without copying the private key to an EC2 instance
- Negative testing and recovery by changing an ICMP inbound rule

## Before final submission

- Replace `YourName` in the report filename and add the student's full name and batch.
- Verify every resource ID and route association against the live console.
- Add cleanup evidence after cleaning up the lab resources.
- Keep private keys, credentials, and tokens out of this repository.
- The repository is public; upload screenshots only after reviewing them for sensitive information.