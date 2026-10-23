# AWS VPC Peering Project Report — EWB

**Student:** Add your full name  
**Batch:** Add your batch  
**Region:** US East (N. Virginia), `us-east-1`

## Objective
Demonstrate private IPv4 connectivity between two non-overlapping VPCs using VPC peering, routes in both directions, security groups, and a bastion host.

## Resource inventory

| Resource | Address/CIDR | ID |
|---|---|---|
| VPC A | `10.10.0.0/16` | `vpc-094290dd996bdde79` |
| VPC B | `10.20.0.0/16` | `vpc-05463d53d9e3da06c` |
| VPC A public subnet | `10.10.1.0/24` | `subnet-0bca7727144ff4450` |
| VPC A private subnet | `10.10.2.0/24` | `subnet-08c38e5c7cf56cf16` |
| VPC B private subnet | `10.20.1.0/24` | `subnet-034834e10587f4b19` |
| Bastion | Private `10.10.1.10`; public `32.192.245.103` | `i-080bd656190adfe0c` |
| App-A | `10.10.2.108`; no public IPv4 observed | `i-005788d06eff77db3` |
| App-B | `10.20.1.226`; no public IPv4 observed | `i-03eb8ec8840385621` |
| VPC peering | Active when last checked | `pcx-0cf7c6b7b06ee3eeb` |

## Route tables

| Route table | Destination | Target |
|---|---|---|
| `ewb-rt-a-public` (`rtb-0bffd516469dc9220`) | `10.10.0.0/16` | local |
| | `0.0.0.0/0` | Internet Gateway |
| | `10.20.0.0/16` | `pcx-0cf7c6b7b06ee3eeb` |
| `ewb-rt-a-private` (`rtb-0df315a397a97459a`) | `10.10.0.0/16` | local |
| | `10.20.0.0/16` | `pcx-0cf7c6b7b06ee3eeb` |
| `ewb-rt-b-private` (`rtb-0e04e73e930ddf38c`) | `10.20.0.0/16` | local |
| | `10.10.0.0/16` | `pcx-0cf7c6b7b06ee3eeb` |

## Validation results observed

| Test | Observed result |
|---|---|
| Laptop SSH to bastion | Successful login to `32.192.245.103` |
| SSH to private App-B through bastion | Successful shell on `ip-10-20-1-226` using SSH ProxyCommand |
| App-A (`10.10.2.108`) → App-B (`10.20.1.226`) | 4 replies, 0% packet loss |
| App-B (`10.20.1.226`) → App-A (`10.10.2.108`) | 4 replies, 0% packet loss |
| Controlled ICMP failure | 0 received, 100% packet loss while App-B ICMP inbound rule was removed |
| Recovery | 4 replies, 0% packet loss after restoring the App-B ICMP inbound rule |

## How it works

- App-A's private route table sends `10.20.0.0/16` to the peering connection.
- App-B's route table sends `10.10.0.0/16` back to the peering connection.
- The public subnet route table includes an Internet Gateway default route and a peering route so the bastion can initiate SSH to App-B.
- The laptop uses the bastion to reach App-B's private IP; the private key remains on the laptop.

## Remaining before final submission

- Fill in student name and batch.
- Check the architecture diagram and all IDs against the live AWS console.
- Include selected evidence screenshots and label each one with the host, test and result.
- Capture cleanup evidence after AWS resources are actually deleted; cleanup is not claimed complete here.
- Keep PEM files, passwords, access tokens, and AWS credentials out of this public repository.